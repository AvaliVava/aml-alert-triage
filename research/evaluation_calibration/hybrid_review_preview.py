#!/usr/bin/env python3
"""Read-only hybrid evaluation review preview for the G02 draft packet.

Python 3.11+ standard library only. This tool verifies identity/traceability,
then ORGANIZES existing AI-authored draft judgments for human review.
It does not validate semantic truth, assign human approvals, or score models.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

REQUIRED = {
    'claim_annotations.draft.json', 'packet_manifest.draft.json',
    'evaluation_manifest.draft.json', 'source_inventory.draft.json',
    'hosted_candidate.json', 'baseline_candidate.json',
    'hosted_audit.json', 'baseline_audit.json',
    'reference_comparison.draft.json',
}
RECORD_SETS = {
    'case', 'customer', 'account', 'counterparty', 'transaction',
    'alert', 'evidence', 'verification_check',
}
DEFAULT_PACKET = (
    Path(__file__).resolve().parents[2]
    / 'outputs/evaluation/g02-paired-pilot-20261029'
)

class PacketError(ValueError):
    """Invalid/corrupted pilot packet or broken annotation binding."""


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def load_packet(path: str | Path) -> tuple[dict, dict]:
    """Read the existing local directory or an explicitly supplied immutable ZIP.

    No extraction or writes occur. A missing local packet is never reconstructed
    from the handoff archive or replaced with another source automatically.
    """
    path = Path(path)
    if path.is_dir():
        names = {entry.name for entry in path.iterdir()}
        if names != REQUIRED or any(not (path / name).is_file() for name in names):
            raise PacketError('Expected exactly nine known JSON files in packet directory')
        raw = {name: (path / name).read_bytes() for name in sorted(names)}
    else:
        with ZipFile(path) as zipped:
            names = zipped.namelist()
            if len(names) != len(set(names)):
                raise PacketError('ZIP contains duplicate entries')
            if set(names) != REQUIRED:
                raise PacketError('Expected exactly nine known JSON files; missing/extras: '
                                  f'{sorted(REQUIRED-set(names))} / {sorted(set(names)-REQUIRED)}')
            raw = {name: zipped.read(name) for name in sorted(names)}
    try:
        parsed = {name: json.loads(blob) for name, blob in raw.items()}
    except (UnicodeError, json.JSONDecodeError) as err:
        raise PacketError(f'Invalid JSON in packet: {err}') from err
    return raw, parsed


def json_pointer(obj: object, ptr: str) -> object:
    if ptr == '':
        return obj
    if not ptr.startswith('/'):
        raise PacketError(f'Invalid JSON pointer: {ptr!r}')
    try:
        for token in ptr[1:].split('/'):
            token = token.replace('~1', '/').replace('~0', '~')
            obj = obj[int(token)] if isinstance(obj, list) else obj[token]
    except (ValueError, TypeError, IndexError, KeyError) as err:
        raise PacketError(f'Unresolved JSON pointer: {ptr!r}') from err
    return obj


def verify(raw: dict, docs: dict) -> dict:
    manifest = docs['evaluation_manifest.draft.json']
    freeze = docs['packet_manifest.draft.json']
    annotations = docs['claim_annotations.draft.json']
    inventory = docs['source_inventory.draft.json']
    def assert_validation(test: bool, reason: str) -> None:
        if not test:
            raise PacketError(reason)

    assert_validation(set(raw) == set(docs) == REQUIRED, 'Packet file set mismatch')
    for name in sorted(REQUIRED):
        assert_validation(json.loads(raw[name]) == docs[name],
                          f'Parsed document differs from supplied bytes: {name}')
    assert_validation(annotations.get('human_review_status') == 'not_reviewed' and
                      annotations.get('scores') is None and
                      annotations.get('performance_ranking') is None,
                      'Draft annotations cannot claim human review, scores or rankings')
    disagreement = annotations['disagreement_log']
    assert_validation(not disagreement['human_reviews'] and
                      not disagreement['recorded_human_disagreements'] and
                      disagreement['adjudicator'] is None and
                      disagreement['adjudication_rationale'] is None,
                      'Draft packet cannot contain fabricated adjudication')

    # Check all declared artifacts, including final freeze manifest digest.
    for declared_path, hexdigest in manifest['artifacts'].items():
        name = Path(declared_path).name
        assert_validation(name in raw and digest(raw[name]) == hexdigest,
                          f'Artifact digest mismatch: {declared_path}')
    assert_validation(digest(raw['packet_manifest.draft.json']) == manifest['freeze_manifest_sha256'],
                      'Freeze manifest digest mismatch')
    assert_validation(digest(raw['source_inventory.draft.json']) == annotations['source_inventory_sha256'],
                      'Annotation source inventory digest mismatch')
    assert_validation(annotations['input_file_sha256'] == inventory['input_file_sha256'] == freeze['input_file_sha256'],
                      'Input identity mismatch')
    assert_validation(annotations['status'] == 'DRAFT_NOT_APPROVED', 'Annotations not in draft state')
    assert_validation(manifest['status'] == 'DRAFT_NOT_APPROVED', 'Manifest not in draft state')

    candidates = {k: docs[k+'_candidate.json'] for k in ('hosted', 'baseline')}
    for key in candidates:
        sha = digest(raw[key+'_candidate.json'])
        assert_validation(sha == freeze[key+'_candidate_sha256'] == annotations['candidate_hashes'][key],
                          f'Candidate identity mismatch: {key}')

    source_map = {(r['record_type'], r['record_id']): r['fields'] for r in inventory['source_records']}
    assert_validation(len(source_map) == len(inventory['source_records']), 'Duplicate source-record identifiers')

    statements = {}
    for entry in annotations['statements']:
        role, path = entry['candidate_id'], entry['json_pointer']
        assert_validation(role in candidates, f'Unknown candidate {role}')
        key = (role, path)
        assert_validation(key not in statements, f'Duplicate statement {key}')
        original = json_pointer(candidates[role], path)
        assert_validation(original == entry['exact_statement'], f'Statement text changed: {key}')
        assert_validation(path.endswith('/statement'), f'Unexpected statement pointer: {path}')
        citations = json_pointer(candidates[role], path[:-len('/statement')])['citations']
        assert_validation(citations == entry['submitted_citations'], f'Statement citations changed: {key}')
        statements[key] = entry

    seen_ids, pointer_count, used_units = set(), 0, defaultdict(list)
    for unit in annotations['units']:
        uid = unit['unit_id']
        assert_validation(uid not in seen_ids, f'Duplicate review unit {uid}')
        seen_ids.add(uid)
        role, loc = unit['candidate_id'], unit['location']
        path = loc['json_pointer']
        key = (role, path)
        assert_validation(key in statements, f'Orphan unit {uid}')
        text = statements[key]['exact_statement']
        start, end = loc['start'], loc['end']
        assert_validation(0 <= start < end <= len(text) and text[start:end] == loc['exact_text'],
                          f'Incorrect exact span {uid}')
        assert_validation(loc['exact_statement'] == text and
                          digest(text.encode('utf-8')) == loc['statement_sha256'],
                          f'Stale statement hash {uid}')
        assert_validation(unit['candidate_sha256'] == annotations['candidate_hashes'][role],
                          f'Stale candidate hash {uid}')
        assert_validation(unit['input_file_sha256'] == inventory['input_file_sha256'],
                          f'Stale input file hash {uid}')
        assert_validation(unit['submitted_citations'] == statements[key]['submitted_citations'],
                          f'Copied citations mismatch {uid}')
        assert_validation(unit['human_review_status'] == 'not_reviewed' and
                          unit['adjudication'] is None and not unit['human_reviewers'] and
                          unit['approval_status'] == 'pending_project_owner_review',
                          f'Unexpected approval/reviewer field in draft unit {uid}')
        used_units[key].append(uid)

        for field in ('supporting_input', 'context_input', 'opposing_or_alternative_reading_input'):
            for p in unit.get(field, []):
                ident = (p['record_type'], p['record_id'])
                assert_validation(p['record_type'] in RECORD_SETS and ident in source_map,
                                  f'Unknown typed source record: {uid}: {ident}')
                actual = json_pointer(source_map[ident], p['field_pointer'])
                assert_validation(actual == p['observed_value'], f'Incorrect source value {uid}: {ident}')
                pointer_count += 1

        for scope in unit.get('input_scope_evidence', []):
            assert_validation(scope['input_json_pointer'] == '/evidence',
                              f'Only frozen evidence snapshot is reviewable in this packet: {uid}')
            evidence = [r['fields'] for r in inventory['source_records'] if r['record_type']=='evidence']
            assert_validation(scope['observed_value'] == evidence, f'Scoped snapshot mismatch {uid}')

    for key, entry in statements.items():
        assert_validation(entry['unit_ids'] == used_units[key], f'Unit registry mismatch {key}')
    for role in candidates:
        audit = docs[role+'_audit.json']
        assert_validation(all(stage['status'] == 'passed' for stage in audit['stages'].values()),
                          f'Unexpected mechanical status in packet: {role}')
        assert_validation(all(stage['status'] == 'not_evaluated' for stage in audit['semantic_evaluation'].values()),
                          f'Unexpected semantic stage status: {role}')

    return {'manifest_artifact_hashes_verified':len(manifest['artifacts']),
            'source_pointers_verified':pointer_count,
            'statements_verified':len(statements), 'units_verified':len(seen_ids),
            'candidate_hashes_verified':list(candidates)}


def make_preview(docs: dict, verification: dict) -> dict:
    a = docs['claim_annotations.draft.json']
    inv = docs['source_inventory.draft.json']
    candidates = {k: docs[k+'_candidate.json'] for k in ('hosted', 'baseline')}
    by_location = defaultdict(list)
    issue_groups = defaultdict(lambda: {'roles':set(), 'statement_keys':set(), 'unit_ids':[]})
    for unit in a['units']:
        key = (unit['candidate_id'], unit['location']['json_pointer'])
        by_location[key].append(unit)
        grp = unit.get('issue_group')
        if grp:
            record = issue_groups[grp]
            record['roles'].add(key[0]);record['statement_keys'].add(key);record['unit_ids'].append(unit['unit_id'])
    statements = []
    for s in a['statements']:
        role, ptr = s['candidate_id'], s['json_pointer']
        units = by_location[(role, ptr)]
        # No whole-statement PASS/FAIL or semantic severity can be inferred from draft atomic labels.
        statements.append({
            'candidate_id':role, 'json_pointer':ptr, 'exact_statement':s['exact_statement'],
            'candidate_sha256':a['candidate_hashes'][role],
            'submitted_citations':s['submitted_citations'],
            'atomic_review':[
                {'unit_id':u['unit_id'], 'exact_span':u['location']['exact_text'],
                 'proposition':u['atomic_proposition'], 'kind':u['kind'],
                 'proposed_input_support':u['proposed_judgments']['factual_support']['category'],
                 'proposed_submitted_citation_adequacy':u['proposed_judgments']['submitted_citation_adequacy']['category'],
                 'human_review_status':'not_reviewed', 'issue_group':u.get('issue_group')}
                for u in units],
            'whole_statement_review':{
                'state':'not_reviewed', 'verdict':None,
                'meaning_and_attribution':None, 'misleading_implication':None,
                'independent_review_required':True,
                'candidate_issue_groups_for_review':sorted({u['issue_group'] for u in units if u.get('issue_group')}),
                'warning':'Atomic draft proposals do not determine whole-statement correctness.'},
        })
    issues = []
    questions = {q['id']:q['question'] for q in a.get('pending_owner_questions', [])}
    for grp, d in sorted(issue_groups.items()):
        issues.append({'group_id':grp, 'question':questions.get(grp),
                       'candidate_roles':sorted(d['roles']),
                       'affected_statement_occurrences':len(d['statement_keys']),
                       'review_unit_ids':d['unit_ids'],
                       'status':'open_for_human_review',
                       'aggregation_rule':'Grouped for triage only; repeat appearances are not independent material errors.'})
    return {
        'report_type':'HYBRID_G02_READ_ONLY_PREVIEW_V0_1', 'status':'DRAFT_NOT_APPROVED',
        'case_id':a['case_id'], 'design_approved':'Hybrid structure only (user approval in conversation)',
        'no_approved_semantic_labels':True, 'accuracy_score':None,'candidate_ranking':None,
        'checks':verification, 'candidate_actions_descriptive_only':
            {key:obj['recommended_action'] for key,obj in candidates.items()},
        'mechanical_status_descriptive_only':{key:
            {name:stage['status'] for name,stage in docs[key+'_audit.json']['stages'].items()}
            for key in candidates},
        'claim_level_and_whole_statement_review':statements,
        'recurring_issue_groups_to_review':issues,
        'case_level_review':{'status':'not_adjudicated',
            'material_inventory':[{**item, 'approved':False, 'candidate_coverage':None} for item in inv['proposed_material_inventory']],
            'omission_scores':None,'recommendation_quality':None,'citation_adequacy_rate':None},
        'review_and_approval':{'human_reviewers':[], 'adjudicator':None,
            'D-04':'Hybrid approach selected; detailed categories/rules pending',
            'D-07':'Human review procedure and responsible reviewers pending'},
        'limitations':[
            'This tool verifies bytes, spans, copied citations and source pointers, not entailment or semantic correctness.',
            'No automatic whole-statement verdict is produced from draft claim labels.',
            'G02 is an exposed synthetic development case, not independent held-out evidence.',
            'Amounts checker coverage is grammar-specific, not comparative model quality.',
            'Recurring issue grouping is not a quality metric and never double-penalizes repeat wording.',
            'Original archived candidate/reference/annotations are not modified.'
        ]
    }


def build_preview(path: str | Path) -> dict:
    raw, docs = load_packet(path)
    checks = verify(raw, docs)
    return make_preview(docs, checks)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', default=str(DEFAULT_PACKET),
                        help='Existing frozen local packet directory, or an explicit packet ZIP')
    parser.add_argument('--output', help='Optional JSON output path; refuses to overwrite an existing file')
    args = parser.parse_args()
    preview = build_preview(args.packet)
    payload = json.dumps(preview, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(payload)
        print(f'Draft hybrid preview saved to {out}')
    else:
        print(payload)

if __name__ == '__main__':
    main()
