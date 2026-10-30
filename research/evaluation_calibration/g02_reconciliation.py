"""Reconcile the frozen G02 packet with recorded owner decisions, without scoring.

The original draft verifier and catalog guards remain authoritative for frozen
artifacts. This separate layer validates the supplied 0.1 register, carries its
decisions verbatim, and reports counts. It does not adjudicate prose or certify
human approval, evidence sufficiency, runtime execution or AML correctness.

Python interface: build_reconciliation(register_path=..., packet_path=...,
input_path=..., catalog_path=...). The CLI emits JSON or writes a new file after
validation. Exit codes: 0 = reconciled within this scope, 1 = expected rejection,
2 = I/O/configuration or unexpected execution error. No import-time execution.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from pydantic import ValidationError

from aml_triage.auditor import audit_packet
from aml_triage.contracts import InvestigationInput, InvestigationOutput
from hybrid_calibration import (
    DEFAULT_CATALOG, CalibrationError, grouped_identical_statements, validate_catalog,
)
from hybrid_review_preview import DEFAULT_PACKET, PacketError, json_pointer, load_packet, verify


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTER = ROOT / 'data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json'
DEFAULT_INPUT = ROOT / 'data/golden_cases/inputs/G02.json'
REPORT_VERSION = '0.1.0'
REGISTER_KEYS = {
    'schema_id', 'schema_version', 'created_on', 'case_id', 'status', 'decision_authority',
    'independent_aml_expert_review', 'source_packet', 'policy_decisions',
    'approved_review_bundles', 'approved_corrections', 'unit_adjudications',
    'whole_statement_adjudications', 'case_level_materiality_and_coverage',
    'evidence_authority_rules', 'pending', 'validation',
}
SUPPORT = {'supported', 'partly_supported', 'contradicted', 'not_established', 'unassessable'}
CITATIONS = {'adequate', 'partial', 'inadequate', 'unassessable'}
ROUTES = {
    'separate_nonfactual_dimension', 'separate_process_authority_dimension',
    'separate_action_dimension', 'separate_materiality_dimension', 'separate_reasoning_dimension',
}
PROCESS_UNITS = {'B003', 'B009', 'B010', 'B011', 'B012', 'B013', 'B014'}
WITHHELD = {'H004', 'H034'}


class ReconciliationError(ValueError):
    """Expected register, binding or release-gate rejection; messages include paths."""


def _require(condition, path, reason):
    if not condition:
        raise ReconciliationError(f'{path}: {reason}')


def _object(value, keys, path):
    _require(type(value) is dict, path, 'expected an object')
    _require(set(value) == set(keys), path,
             f'expected fields {sorted(keys)}; unknown or missing fields are not accepted')


def _text(value, path):
    _require(type(value) is str and bool(value.strip()), path, 'expected non-whitespace text')


def _texts(value, path):
    _require(type(value) is list and bool(value), path, 'expected a nonempty list')
    for index, item in enumerate(value):
        _text(item, f'{path}[{index}]')


def _equal(actual, expected, path):
    _require(actual == expected and type(actual) is type(expected), path,
             'does not match the required value or frozen binding')
    if isinstance(expected, dict):
        for key in expected:
            _equal(actual[key], expected[key], path + '.' + str(key))
    elif isinstance(expected, (list, tuple)):
        for index, value in enumerate(expected):
            _equal(actual[index], value, f'{path}[{index}]')


def _counts(values):
    return dict(sorted(Counter(values).items()))


def _canonical(model):
    """Match the existing validated-input serialization; never rewrite file bytes."""
    return json.dumps(model.model_dump(mode='json'), sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def _parse(payload):
    def pairs(items):
        result = {}
        for key, value in items:
            _require(key not in result, 'register', 'duplicate JSON object key')
            result[key] = value
        return result

    def constant(_):
        raise ReconciliationError('register: non-finite JSON number')

    try:
        return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ReconciliationError('register: invalid JSON') from error


def load_register(path=DEFAULT_REGISTER):
    """Load a register without mutation; contextual validation is a separate step."""
    register = _parse(Path(path).read_bytes())
    _object(register, REGISTER_KEYS, 'register')
    return register


def validate_register(register, raw, docs, input_json):
    """Validate this G02 register against already supplied frozen artifacts.

    Existing verification checks all original source pointers. Copied register
    pointers must match those proposals, without certifying semantic sufficiency.
    Returns JSON-serializable validation facts, never new semantic judgments.
    """
    _object(register, REGISTER_KEYS, 'register')
    frozen_checks = verify(raw, docs)
    r = register
    for key, value in (
        ('schema_id', 'g02_conversation_adjudication_register'),
        ('schema_version', '0.1.0-draft'), ('case_id', 'CASE-G02'),
        ('status', 'CONSOLIDATED_DRAFT_NOT_REPOSITORY_RELEASE'),
        ('independent_aml_expert_review', 'not_performed'),
    ):
        _equal(r[key], value, f'register.{key}')
    for key in ('created_on', 'decision_authority'):
        _text(r[key], f'register.{key}')

    annotations = docs['claim_annotations.draft.json']
    freeze = docs['packet_manifest.draft.json']
    source = r['source_packet']
    _object(source, {'filename', 'zip_sha256', 'input_file_sha256', 'source_inventory_sha256',
                     'checkout_revision', 'candidate_sha256', 'source_inventory_exposure'},
            'register.source_packet')
    for key in ('filename', 'zip_sha256', 'source_inventory_exposure'):
        _text(source[key], f'register.source_packet.{key}')
    _equal(source['input_file_sha256'], sha256(input_json).hexdigest(),
           'register.source_packet.input_file_sha256')
    _equal(source['input_file_sha256'], annotations['input_file_sha256'],
           'register.source_packet.input_file_sha256')
    _equal(source['source_inventory_sha256'], sha256(raw['source_inventory.draft.json']).hexdigest(),
           'register.source_packet.source_inventory_sha256')
    _equal(source['checkout_revision'], freeze['checkout_revision'],
           'register.source_packet.checkout_revision')
    _object(source['candidate_sha256'], {'hosted', 'baseline'},
            'register.source_packet.candidate_sha256')
    for role in ('hosted', 'baseline'):
        _equal(source['candidate_sha256'][role], sha256(raw[f'{role}_candidate.json']).hexdigest(),
               f'register.source_packet.candidate_sha256.{role}')
    try:
        investigation = InvestigationInput.model_validate_json(input_json)
    except ValidationError as error:
        raise ReconciliationError('input_structure: existing input contract rejected input') from error
    _equal(investigation.case.case_id, r['case_id'], 'register.case_id')
    canonical_hash = sha256(_canonical(investigation)).hexdigest()
    _equal(canonical_hash, freeze['canonical_input_sha256'], 'input.canonical_sha256')

    decisions = r['policy_decisions']
    _object(decisions, {'methodology_approved', 'review_roles', 'g02_action'},
            'register.policy_decisions')
    _texts(decisions['methodology_approved'], 'register.policy_decisions.methodology_approved')
    _text(decisions['review_roles'], 'register.policy_decisions.review_roles')
    action = decisions['g02_action']
    _object(action, {'action', 'approved_alternatives', 'alternatives_explicitly_reviewed',
                     'scope', 'reference_file_label_status', 'policy_ref_01', 'human_review'},
            'register.policy_decisions.g02_action')
    for key, value in (
        ('action', 'investigate'), ('approved_alternatives', []),
        ('alternatives_explicitly_reviewed', True),
        ('reference_file_label_status', 'provisional_frozen_unchanged'),
        ('policy_ref_01', 'not_established_in_supplied_g02_records'),
        ('human_review', 'required_not_completed'),
    ):
        _equal(action[key], value, f'register.policy_decisions.g02_action.{key}')
    _text(action['scope'], 'register.policy_decisions.g02_action.scope')

    original = {u['unit_id']: u for u in annotations['units']}
    units = r['unit_adjudications']
    _require(type(units) is list and len(units) == 75, 'register.unit_adjudications',
             'expected all 75 units')
    seen = set()
    unit_keys = {
        'unit_id', 'candidate', 'statement_pointer', 'original_span', 'draft_atomic_proposition',
        'original_span_offsets', 'source_sufficient_for_evaluation', 'original_submitted_citations',
        'approved_factual_support', 'approved_submitted_citation_treatment', 'score_eligibility',
        'approval_provenance', 'interpretation_or_limit', 'original_draft_evidence_pointer_candidates',
        'pointer_provenance_note',
    }
    for index, unit in enumerate(units):
        path = f'register.unit_adjudications[{index}]'
        _object(unit, unit_keys, path)
        uid = unit['unit_id']
        _text(uid, path + '.unit_id')
        _require(uid in original and uid not in seen, path + '.unit_id', 'unknown or duplicate unit')
        seen.add(uid)
        old = original[uid]
        location = old['location']
        for key, value in (
            ('candidate', old['candidate_id']), ('statement_pointer', location['json_pointer']),
            ('original_span', location['exact_text']),
            ('draft_atomic_proposition', old['atomic_proposition']),
            ('original_submitted_citations', old['submitted_citations']),
            ('original_span_offsets', {'start': location['start'], 'end': location['end']}),
        ):
            _equal(unit[key], value, path + '.' + key)
        offsets = unit['original_span_offsets']
        _require(all(type(offsets[key]) is int for key in ('start', 'end')),
                 path + '.original_span_offsets', 'expected integer offsets')
        candidates = docs[unit['candidate'] + '_candidate.json']
        text = json_pointer(candidates, unit['statement_pointer'])
        _equal(text[offsets['start']:offsets['end']], unit['original_span'], path + '.original_span')
        copied = unit['original_draft_evidence_pointer_candidates']
        _object(copied, {'supporting_input', 'opposing_or_alternative_reading_input',
                         'input_scope_evidence', 'source_conflict'}, path + '.evidence_pointers')
        for key, value in copied.items():
            _equal(value, old[key], path + '.evidence_pointers.' + key)
        _texts(unit['source_sufficient_for_evaluation'], path + '.source_sufficient_for_evaluation')
        for key in ('interpretation_or_limit', 'pointer_provenance_note'):
            _text(unit[key], path + '.' + key)
        provenance = unit['approval_provenance']
        _object(provenance, {'source', 'independent_domain_expert_validation',
                             'frozen_file_mutated'}, path + '.approval_provenance')
        _text(provenance['source'], path + '.approval_provenance.source')
        for key in ('independent_domain_expert_validation', 'frozen_file_mutated'):
            _equal(provenance[key], False, path + '.approval_provenance.' + key)
        factual = unit['approved_factual_support']
        _object(factual, {'applicability', 'category', 'proposition_scope'}, path + '.factual_support')
        _require(factual['applicability'] in ('applicable', 'not_applicable'), path,
                 'invalid factual applicability')
        if factual['applicability'] == 'applicable':
            _text(factual['category'], path + '.factual_support.category')
        _require((factual['category'] in SUPPORT if factual['applicability'] == 'applicable'
                  else factual['category'] is None), path, 'invalid factual category')
        expected_scope = ('draft_atomic_only_original_fidelity_pending' if uid in WITHHELD
                          else 'scoped_atomic')
        _equal(factual['proposition_scope'], expected_scope, path + '.proposition_scope')
        treatment = unit['approved_submitted_citation_treatment']
        _object(treatment, {'applicability', 'category', 'handling'}, path + '.citation_treatment')
        applicability = treatment['applicability']
        _require(applicability in ('applicable', 'not_applicable', 'other_dimension'), path,
                 'invalid citation applicability')
        if applicability == 'applicable':
            _text(treatment['category'], path + '.citation_treatment.category')
            _require(treatment['category'] in CITATIONS and treatment['handling'] is None,
                     path, 'invalid citation category or handling')
        else:
            _text(treatment['handling'], path + '.citation_treatment.handling')
            _require(treatment['category'] is None and
                     (treatment['handling'] in ROUTES if applicability == 'other_dimension'
                      else treatment['handling'] == 'not_applicable'),
                     path, 'invalid non-applicable citation treatment')
        eligibility = ('withheld_pending_original_fidelity' if uid in WITHHELD
                       else 'not_yet_approved_for_published_scoring')
        _equal(unit['score_eligibility'], eligibility, path + '.score_eligibility')
        corrected = {'H004', 'H034', 'H044', 'H045', 'B017', 'B018', 'B019',
                     'B023', 'B024', 'B025'}
        if uid in corrected:
            _equal(treatment['category'], 'inadequate', path + '.citation_treatment.category')
        if uid == 'H046':
            _equal(treatment['category'], 'partial', path + '.citation_treatment.category')
        if uid in WITHHELD:
            _equal(factual['category'], 'not_established', path + '.factual_support.category')
        if uid == 'H047':
            _equal(factual['category'], 'supported', path + '.factual_support.category')
            _equal(treatment['category'], 'adequate', path + '.citation_treatment.category')
        if uid == 'H049':
            _equal(factual['category'], 'unassessable', path + '.factual_support.category')
        if uid in PROCESS_UNITS:
            _equal(factual['applicability'], 'not_applicable', path + '.factual_support.applicability')
            _equal(treatment['handling'], 'separate_process_authority_dimension',
                   path + '.citation_treatment.handling')
    _equal(seen, set(original), 'register.unit_adjudications')

    batches = r['approved_review_bundles']
    _require(type(batches) is dict and len(batches) == 6, 'register.approved_review_bundles',
             'expected six unit batches')
    grouped = []
    for key, value in batches.items():
        _texts(value, 'register.approved_review_bundles.' + key)
        grouped.extend(value)
    _equal(Counter(grouped), Counter(original.keys()), 'register.approved_review_bundles')

    whole = r['whole_statement_adjudications']
    _require(type(whole) is list and len(whole) == 21, 'register.whole_statement_adjudications',
             'expected all 21 original statement occurrences')
    originals = {(s['candidate_id'], s['json_pointer']): s for s in annotations['statements']}
    statement_keys = set()
    for index, statement in enumerate(whole):
        path = f'register.whole_statement_adjudications[{index}]'
        _object(statement, {'candidate', 'statement_pointer', 'statement_text', 'unit_ids',
                            'original_submitted_citations', 'approved_whole_statement_status',
                            'limitations', 'approval_provenance'}, path)
        for field in ('candidate', 'statement_pointer'):
            _text(statement[field], path + '.' + field)
        key = (statement['candidate'], statement['statement_pointer'])
        _require(key in originals and key not in statement_keys, path,
                 'unknown or duplicate statement identity')
        statement_keys.add(key)
        old = originals[key]
        for field, value in (
            ('statement_text', old['exact_statement']), ('unit_ids', old['unit_ids']),
            ('original_submitted_citations', old['submitted_citations']),
        ):
            _equal(statement[field], value, path + '.' + field)
        _texts(statement['limitations'], path + '.limitations')
        _text(statement['approval_provenance'], path + '.approval_provenance')
        role, pointer = key
        factual_pass = pointer.startswith('/factual_findings/') or (
            role == 'hosted' and pointer == '/interpretations/1/statement')
        question = role == 'hosted' and pointer.startswith('/unresolved_questions/')
        expected = ('qualified_factual_pass' if factual_pass else
                    'qualified_investigative_question' if question else
                    'reviewed_not_cleared_unconditional_pass')
        _equal(statement['approved_whole_statement_status'], expected, path + '.status')
    _equal(statement_keys, set(originals), 'register.whole_statement_adjudications')

    coverage = r['case_level_materiality_and_coverage']
    _object(coverage, {'M01', 'M02', 'M03', 'M04', 'M05'}, 'register.material_coverage')
    expected_coverage = {
        'M01': ('mandatory', 'covered', 'partly_covered'),
        'M02': ('mandatory', 'covered', 'covered'),
        'M03': ('mandatory', 'covered', 'omitted'),
        'M04': ('contextual_independent_materiality_pending', 'discussed_contextually', 'not_discussed'),
        'M05': ('contextual_nonmandatory', 'described', 'amount_described'),
    }
    for key, item in coverage.items():
        _object(item, {'requirement', 'applicability', 'hosted', 'baseline', 'reason'},
                'register.material_coverage.' + key)
        for field in ('requirement', 'reason'):
            _text(item[field], 'register.material_coverage.' + key + '.' + field)
        _equal(tuple(item[field] for field in ('applicability', 'hosted', 'baseline')),
               expected_coverage[key], 'register.material_coverage.' + key)
    _require(type(r['approved_corrections']) is list and bool(r['approved_corrections']),
             'register.approved_corrections', 'expected recorded corrections')
    for index, correction in enumerate(r['approved_corrections']):
        _object(correction, {'issue', 'previous', 'revised'}, f'register.approved_corrections[{index}]')
        for key in correction:
            _text(correction[key], f'register.approved_corrections[{index}].{key}')
    _object(r['evidence_authority_rules'], {
        'case_record', 'customer_explanation', 'verification_check', 'complete_input_inventory',
        'code', 'output_contract', 'frozen_output', 'packet_manifest', 'owner_review',
    }, 'register.evidence_authority_rules')
    for key, value in r['evidence_authority_rules'].items():
        _text(value, 'register.evidence_authority_rules.' + key)
    _require(type(r['pending']) is list and len(r['pending']) == 5, 'register.pending',
             'expected the five recorded release/interpretation gates')
    for index, item in enumerate(r['pending']):
        _object(item, {'id', 'item', 'blocking'}, f'register.pending[{index}]')
        _equal(item['id'], f'P0{index + 1}', f'register.pending[{index}].id')
        for key in ('item', 'blocking'):
            _text(item[key], f'register.pending[{index}].{key}')

    factual_counts = _counts(u['approved_factual_support']['category']
                             if u['approved_factual_support']['applicability'] == 'applicable'
                             else 'not_applicable' for u in units)
    citation_counts = _counts(u['approved_submitted_citation_treatment']['category']
                              if u['approved_submitted_citation_treatment']['applicability'] == 'applicable'
                              else u['approved_submitted_citation_treatment']['handling'] for u in units)
    whole_counts = _counts(s['approved_whole_statement_status'] for s in whole)
    declared = r['validation']
    _require(type(declared) is dict, 'register.validation', 'expected an object')
    snapshots = {}
    _object(declared.get('snapshot_candidate_sha256_match_manifest'), {'hosted', 'baseline'},
            'register.validation.snapshot_candidate_sha256_match_manifest')
    for role in ('hosted', 'baseline'):
        row = declared.get('snapshot_candidate_sha256_match_manifest', {}).get(role)
        _object(row, {'expected', 'actual_file_bytes', 'match', 'note'},
                'register.validation.snapshot.' + role)
        for field in ('expected', 'actual_file_bytes'):
            _equal(row[field], source['candidate_sha256'][role], 'register.validation.snapshot.' + field)
        _equal(row['match'], True, 'register.validation.snapshot.match')
        _text(row['note'], 'register.validation.snapshot.note')
        snapshots[role] = row
    expected_validation = {
        'frozen_unit_count': 75, 'frozen_original_statement_count': 21,
        'all_75_units_covered_once_by_six_approved_batches': True,
        'atomic_spans_match_frozen_candidate_text': True,
        'statement_text_matches_frozen_candidates': True,
        'unit_to_statement_membership_matches': True,
        'submitted_citation_lists_match_frozen_candidate': True,
        'snapshot_candidate_sha256_match_manifest': snapshots,
        'packet_zip_sha256': source['zip_sha256'],
        'unit_factual_dispositions_counts': factual_counts,
        'unit_submitted_citation_treatments_counts': citation_counts,
        'whole_statement_status_counts': whole_counts,
        'asserted_requirement_counts': {'mandatory': 3, 'contextual': 2},
        'baseline_M02_covered_is_separate_from_citation_inadequacies': True,
        'all_statement_sha256_match_frozen_draft': True,
        'source_inventory_bytes_sha256_match_approved_manifest': True,
    }
    _object(declared, expected_validation, 'register.validation')
    for key, value in expected_validation.items():
        _equal(declared[key], value, 'register.validation.' + key)
    _equal(whole_counts, {'qualified_factual_pass': 10, 'qualified_investigative_question': 3,
                          'reviewed_not_cleared_unconditional_pass': 8}, 'register.whole_totals')
    return {
        'status': 'passed', 'reason': 'Recorded register identities and populations reconcile.',
        'frozen_checks': frozen_checks, 'factual_counts': factual_counts,
        'citation_counts': citation_counts, 'whole_counts': whole_counts,
        'input_original_file_sha256': source['input_file_sha256'],
        'input_canonical_sha256': canonical_hash, 'policy_id': investigation.case.policy_id,
    }


def build_reconciliation(register_path=DEFAULT_REGISTER, packet_path=DEFAULT_PACKET,
                         input_path=DEFAULT_INPUT, catalog_path=DEFAULT_CATALOG, *, scoring=False):
    """Read explicit artifacts and return a deterministic, JSON-serializable report.

    ``scoring`` exists only as a rejection guard: only boolean False is accepted.
    Recorded decisions are not signed approvals; register identity/provenance and
    absent metadata are reported rather than invented. No sources are modified.
    """
    _require(scoring is False, 'scoring', 'numerical scoring is not authorized')
    register_bytes = Path(register_path).read_bytes()
    register = _parse(register_bytes)
    raw, docs = load_packet(packet_path)
    catalog = _parse(Path(catalog_path).read_bytes())
    integrity = validate_catalog(catalog, raw, docs, packet_path)
    input_bytes = Path(input_path).read_bytes()
    checks = validate_register(register, raw, docs, input_bytes)
    _equal(register['source_packet']['zip_sha256'], catalog['frozen_packet_sha256'],
           'register.source_packet.zip_sha256')
    audits, candidate_identities = {}, {}
    for role in ('hosted', 'baseline'):
        blob = raw[role + '_candidate.json']
        audit = audit_packet(input_bytes, blob, input_identity=str(input_path),
                             candidate_identity=role + '_candidate.json')
        _require(all(stage['status'] == 'passed' for stage in audit['stages'].values()),
                 'mechanical_validation.' + role, 'existing mechanical prerequisites did not pass')
        audits[role] = audit
        parsed = InvestigationOutput.model_validate_json(blob)
        candidate_identities[role] = {
            'original_file_sha256': sha256(blob).hexdigest(),
            'canonical_validated_json_sha256': sha256(_canonical(parsed)).hexdigest(),
            'binding_basis': 'original_file_bytes',
        }

    original = {u['unit_id']: u for u in docs['claim_annotations.draft.json']['units']}
    units = register['unit_adjudications']
    whole = register['whole_statement_adjudications']
    records = []
    for unit in units:
        old = original[unit['unit_id']]
        records.append({
            'unit_id': unit['unit_id'], 'candidate': unit['candidate'],
            'case_id': register['case_id'],
            'input_original_file_sha256': checks['input_original_file_sha256'],
            'candidate_original_file_sha256': old['candidate_sha256'],
            'original_frozen_annotation': deepcopy(old),
            'recorded_owner_adjudication': deepcopy(unit),
            'review_state': None, 'reviewer_id': None, 'approval_event_id': None,
            'metadata_limit': 'No structured per-unit review_state, reviewer/event ID or dated '
                              'revision history supplied; approval provenance is carried verbatim.',
        })

    factual_by_candidate, citations_by_candidate, whole_by_candidate = {}, {}, {}
    for role in ('hosted', 'baseline'):
        selected = [u for u in units if u['candidate'] == role]
        factual_by_candidate[role] = _counts(
            u['approved_factual_support']['category']
            if u['approved_factual_support']['applicability'] == 'applicable'
            else 'not_applicable' for u in selected)
        citations_by_candidate[role] = _counts(
            u['approved_submitted_citation_treatment']['category']
            if u['approved_submitted_citation_treatment']['applicability'] == 'applicable'
            else u['approved_submitted_citation_treatment']['handling'] for u in selected)
        whole_by_candidate[role] = _counts(s['approved_whole_statement_status'] for s in whole
                                         if s['candidate'] == role)
    coverage = register['case_level_materiality_and_coverage']
    mandatory = {key: deepcopy(value) for key, value in coverage.items()
                 if value['applicability'] == 'mandatory'}
    coverage_counts = {role: _counts(item[role] for item in mandatory.values())
                       for role in ('hosted', 'baseline')}
    repeated = grouped_identical_statements(docs['claim_annotations.draft.json']['statements'])
    action = deepcopy(register['policy_decisions']['g02_action'])
    action['candidate_comparisons'] = {}
    for role in ('hosted', 'baseline'):
        candidate = docs[role + '_candidate.json']
        rationale = next(s for s in whole if s['candidate'] == role
                         and s['statement_pointer'] == '/rationale/statement')
        action['candidate_comparisons'][role] = {
            'submitted_action': candidate['recommended_action'],
            'matches_registered_action': candidate['recommended_action'] == action['action'],
            'rationale_whole_statement_status': rationale['approved_whole_statement_status'],
            'recommendation_scope': candidate['recommendation_scope'],
            'human_review_required': candidate['human_review_required'],
        }
    action.update(policy_id=checks['policy_id'], rubric_version=None,
                  rubric_version_reason='No structured rubric version is supplied by the register; '
                                        'no policy/reference lookup is performed.')
    return {
        'report_schema_version': REPORT_VERSION, 'status': 'reconciled_non_scoring',
        'case_id': register['case_id'],
        'implementation': {
            'module': 'research/evaluation_calibration/g02_reconciliation.py',
            'version': REPORT_VERSION, 'source_revision': None,
            'reason': 'Runtime Git revision is not discovered; recorded frozen revision is separate.',
        },
        'artifact_integrity': {
            'status': 'passed', 'reason': 'Frozen bytes and declared register bindings agree.',
            'packet': integrity['packet_identity'],
            'register': {'identity': str(register_path), 'sha256': sha256(register_bytes).hexdigest(),
                         'digest_basis': 'original_file_bytes'},
            'input': {'identity': str(input_path),
                      'original_file_sha256': checks['input_original_file_sha256'],
                      'canonical_validated_json_sha256': checks['input_canonical_sha256'],
                      'binding_basis': 'original_file_bytes'},
            'candidates': candidate_identities,
            'canonical_serialization': 'Validated model_dump(mode=json); UTF-8; sorted keys; '
                                       'compact separators; ensure_ascii=False; allow_nan=False.',
            'zip_limitation': 'Directory verification does not verify container bytes; '
                              'historical ZIP identity is checked against the catalog declaration.',
        },
        'mechanical_validation': audits,
        'reconciliation_validation': checks,
        'reconciled_units': records,
        'atomic_factual_support': {
            'population': len(units), 'category_counts': checks['factual_counts'],
            'by_candidate': factual_by_candidate,
            'meaning': 'Counts of recorded dispositions, including explicit non-applicability; '
                       'not a correctness rate or independent semantic validation.',
        },
        'submitted_citation_review': {
            'category_and_routing_counts': checks['citation_counts'],
            'by_candidate': citations_by_candidate,
            'meaning': 'Recorded adequacy is separate from identifier existence and input support; '
                       'uncited permitted statements and other authority domains remain separate.',
        },
        'whole_statement_reconciliation': {
            'population': len(whole), 'status_counts': checks['whole_counts'],
            'by_candidate': whole_by_candidate, 'statements': deepcopy(whole),
            'meaning': 'Qualified passes, questions and not-cleared occurrences are separate; '
                       'atomic labels never generate whole-statement judgments.',
        },
        'process_evidence_observations': {
            'units': [deepcopy(u) for u in units if u['unit_id'] in PROCESS_UNITS],
            'output_navigation_units': [deepcopy(u) for u in units if u['unit_id'] == 'B002'],
            'authority_rules': deepcopy(register['evidence_authority_rules']),
            'independent_runtime_certification': False,
            'meaning': 'Recorded code/contract/output assessments; case citations do not establish '
                       'software execution, and required review does not establish completed review.',
        },
        'material_coverage': {
            'scope': 'Owner-adjudicated exposed G02 development case only',
            'mandatory_items': mandatory, 'mandatory_item_count_per_candidate': len(mandatory),
            'category_counts': coverage_counts,
            'contextual_items': {k: deepcopy(v) for k, v in coverage.items() if k not in mandatory},
            'repeated_statement_occurrences': repeated,
            'M02_coverage_items_per_candidate': 1,
            'meaning': 'Coverage uses each mandatory item once; citation inadequacy does not '
                       'erase registered M02 coverage. M04/M05 receive no mandatory credit.',
        },
        'preliminary_action_adjudication': action,
        'provenance': {
            'register_schema': register['schema_id'], 'register_version': register['schema_version'],
            'register_status': register['status'], 'register_created_on': register['created_on'],
            'decision_authority': register['decision_authority'],
            'review_roles_as_recorded': register['policy_decisions']['review_roles'],
            'methodology_approvals_as_recorded': deepcopy(register['policy_decisions']['methodology_approved']),
            'independent_aml_expert_review': register['independent_aml_expert_review'],
            'frozen_annotation_status': docs['claim_annotations.draft.json']['status'],
            'recorded_frozen_checkout_revision': register['source_packet']['checkout_revision'],
            'source_inventory_exposure': register['source_packet']['source_inventory_exposure'],
            'recorded_corrections': deepcopy(register['approved_corrections']),
            'dated_approval_event_history': None,
            'approval_authentication': 'Declared provenance only; no signature or conversation '
                                       'approval trace is independently authenticated.',
        },
        'exclusions': {
            'fidelity_withheld': sorted(WITHHELD),
            'factual_not_applicable': [u['unit_id'] for u in units
                                       if u['approved_factual_support']['applicability'] == 'not_applicable'],
            'factual_unassessable': [u['unit_id'] for u in units
                                     if u['approved_factual_support']['category'] == 'unassessable'],
            'citation_not_applicable': [u['unit_id'] for u in units
                                        if u['approved_submitted_citation_treatment']['applicability'] == 'not_applicable'],
            'citation_other_dimension': [u['unit_id'] for u in units
                                         if u['approved_submitted_citation_treatment']['applicability'] == 'other_dimension'],
            'publication_gate_counts': _counts(u['score_eligibility'] for u in units),
            'contextual_not_mandatory': ['M04', 'M05'],
        },
        'unresolved_decisions': deepcopy(register['pending']),
        'scoring': {'status': 'not_evaluated', 'authorized': False, 'rates': None,
                    'reason': 'Non-scoring implementation only. Eligibility/report release remains '
                              'pending; no percentages, composite, thresholds or ranking are produced.'},
        'limitations': [
            'Consumes recorded judgments for frozen G02 only; no semantic claims are newly adjudicated.',
            'G02 is synthetic exposed development data, N=1; no held-out or generalization claim.',
            'Original references remain provisional and are not loaded or modified.',
            'The mechanical auditor retains all nine broad semantic dimensions as not_evaluated.',
            'Exact pointer/value checks do not establish approved source sufficiency. Register '
            'source descriptions remain prose; copied pointers remain original AI proposals.',
            'Original context pointers and qualifications remain available in the frozen annotation '
            'alongside, not overwritten by, the owner decision.',
            'Missing structured review_state, reviewer IDs, approval-event history and rubric '
            'version are not invented. Semantic dimension judgments absent from the register '
            'are not synthesized from explanatory prose.',
            'H004/H034 remain fidelity-withheld; H047 support is narrow and its whole statement '
            'is not cleared; H049 readings remain in the recorded qualification.',
            'Process observations do not certify runtime execution or completed human AML review.',
            'Generation attempts, retries, missing attempts and independent runtime trace are '
            'not reconstructed from this paired candidate packet.',
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--register', default=str(DEFAULT_REGISTER))
    parser.add_argument('--packet', default=str(DEFAULT_PACKET))
    parser.add_argument('--input', default=str(DEFAULT_INPUT))
    parser.add_argument('--catalog', default=str(DEFAULT_CATALOG))
    parser.add_argument('--output', help='New report path; refuses existing files and frozen packet paths')
    args = parser.parse_args(argv)
    try:
        report = build_reconciliation(args.register, args.packet, args.input, args.catalog)
        payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n'
        if args.output:
            output = Path(args.output)
            packet = Path(args.packet)
            _require(not packet.is_dir() or not output.resolve().is_relative_to(packet.resolve()),
                     'output', 'cannot publish inside the frozen packet directory')
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(payload)
        else:
            # ASCII escapes preserve Unicode text through Windows console encodings.
            print(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2,
                             allow_nan=False))
        return 0
    except (ReconciliationError, PacketError, CalibrationError) as error:
        status, reason, code = 'failed', str(error), 1
    except OSError:
        status, reason, code = 'error', 'Artifact read/write failed; no report publication confirmed.', 2
    except Exception:
        status, reason, code = 'error', 'Unexpected reconciliation error; details omitted.', 2
    print(json.dumps({
        'report_schema_version': REPORT_VERSION,
        'reconciliation_validation': {'status': status, 'reason': reason},
        'scoring': {'status': 'not_evaluated', 'authorized': False, 'rates': None},
    }, sort_keys=True))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
