"""Read-only calibration planner for seven G02 hybrid-evaluation design bundles.

This module checks artifact identity/traceability, not semantic truth. It never
loads reference answers for scoring, does not run any model, and never approves
annotations or changes source records. Python 3.11+; standard library only.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
from pathlib import Path

from hybrid_review_preview import DEFAULT_PACKET, REQUIRED, PacketError, load_packet, verify

HERE = Path(__file__).resolve().parent
DEFAULT_CATALOG = HERE / 'calibration_cases.draft.json'


class CalibrationError(ValueError):
    """Invalid frozen packet, catalog identity or unsupported approval claim."""


def load_catalog(path: str | Path = DEFAULT_CATALOG) -> dict:
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def validate_catalog(catalog: dict, raw: dict, docs: dict, packet_path: str | Path) -> dict:
    """Verify *identities*, text semantics deliberately require human review."""
    check = verify(raw, docs)  # Prior prototype's complete byte/span/typed-pointer checker
    a = docs['claim_annotations.draft.json']
    if catalog.get('approved_semantic_rules') != [] or catalog.get('approved_scoring') is not False:
        raise CalibrationError('Draft catalog cannot claim approved rules or approved scoring')
    if catalog.get('review_status') != 'AI_PREPARED_NOT_HUMAN_REVIEWED':
        raise CalibrationError('Calibration draft review status changed without adjudication')
    artifact_hashes = {name: sha256(raw[name]).hexdigest() for name in sorted(REQUIRED)}
    if artifact_hashes != catalog.get('packet_artifact_sha256'):
        raise CalibrationError('Frozen packet artifact bytes mismatch')
    packet_path = Path(packet_path)
    zip_verified = not packet_path.is_dir()
    if zip_verified and sha256(packet_path.read_bytes()).hexdigest() != catalog['frozen_packet_sha256']:
        raise CalibrationError('Frozen packet ZIP bytes mismatch')
    if catalog['input_file_sha256'] != a['input_file_sha256']:
        raise CalibrationError('Catalog input digest mismatch')
    if catalog['source_inventory_sha256'] != a['source_inventory_sha256']:
        raise CalibrationError('Catalog source-inventory digest mismatch')
    if catalog['candidate_source_hashes'] != a['candidate_hashes']:
        raise CalibrationError('Catalog candidate identities mismatch')
    inventory_items = {item['id']: item for item in
                       docs['source_inventory.draft.json']['proposed_material_inventory']}
    for item in catalog['selected_case_level_items']:
        if (item['item_id'] not in inventory_items or
                item.get('status') != 'proposed_not_adjudicated' or
                item.get('no_baseline_unit_for_omission') is not True):
            raise CalibrationError('Case-level items remain proposals, not omission verdicts')
    refs = {u['unit_id']: u for u in a['units']}
    if len(catalog['calibration_bundles']) != 7:
        raise CalibrationError('Expected exactly seven proposed calibration bundles')
    all_ids = []
    seen_bundle_ids=set()
    for b in catalog['calibration_bundles']:
        if b['id'] in seen_bundle_ids:
            raise CalibrationError('Duplicate calibration bundle id')
        seen_bundle_ids.add(b['id'])
        if b.get('status') != 'not_reviewed' or b.get('human_review') is not None or b.get('rule_decisions') is not None:
            raise CalibrationError('Human review / rule approval cannot be prefilled')
        if b.get('meaning_preservation_review') is not None or b.get('candidate_comparison_outcome') is not None:
            raise CalibrationError('Meaning or comparison verdict cannot be prefilled')
        if not b.get('tests') or not b.get('rule_ids') or not b.get('authority'):
            raise CalibrationError('Calibration bundle needs rule, authority and counterfactual proposals')
        for item in b['source_units']:
            uid = item['unit_id']; all_ids.append(uid)
            u = refs.get(uid)
            if u is None:
                raise CalibrationError(f'Unknown source unit: {uid}')
            loc = u['location']
            keys = {'candidate_id': u['candidate_id'], 'json_pointer':loc['json_pointer'],
                    'statement_sha256':loc['statement_sha256'], 'exact_statement':loc['exact_statement'],
                    'span_start':loc['start'], 'span_end':loc['end'], 'exact_span':loc['exact_text'],
                    'atomic_proposition_as_proposed':u['atomic_proposition'],
                    'candidate_sha256':u['candidate_sha256'],
                    'submitted_citations':u['submitted_citations'],
                    'proposed_support_category_not_approved':u['proposed_judgments']['factual_support']['category'],
                    'proposed_citation_category_not_approved':u['proposed_judgments']['submitted_citation_adequacy']['category']}
            for name, expected in keys.items():
                if item.get(name) != expected:
                    raise CalibrationError(f'Unit {uid} drift: {name}')
            if loc['exact_statement'][loc['start']:loc['end']] != loc['exact_text']:
                raise CalibrationError(f'Invalid anchor span: {uid}')
    if len(all_ids) != len(set(all_ids)):
        raise CalibrationError('Duplicate unit reference across calibration bundles; use explicit cross-links instead')
    return {'packet_artifacts_verified':True,
            'packet_identity': {'source_kind':'zip' if zip_verified else 'directory',
                                'artifact_sha256':artifact_hashes,
                                'historical_zip_sha256':catalog['frozen_packet_sha256'],
                                'zip_bytes_verified':zip_verified},
            'selected_bundles':len(catalog['calibration_bundles']),
            'selected_review_units':len(all_ids), 'source_packet_integrity':check,
            'semantic_judgments_verified':False, 'semantic_scores':None}


def compare_amounts_without_policy(input_records: list[dict], transaction_id: str, customer_id: str) -> dict:
    """Exact-currency numeric comparison; no materiality or monthly-limit conclusion."""
    try:
        idx={(r['record_type'],r['record_id']):r['fields'] for r in input_records}
        tx=idx[('transaction',transaction_id)]
        profile=idx[('customer',customer_id)]['expected_monthly_activity']
        if tx['currency'] != profile['currency']:
            return {'comparable':False, 'transaction_above_recorded_maximum':None,
                    'reason':'Currency mismatch; no FX conversion permitted'}
        amounts = (tx['amount'], profile['maximum'])
        if any(type(value) not in (str, int, Decimal) for value in amounts):
            raise ValueError('Expected decimal text or an exact numeric representation')
        amount, maximum = map(Decimal, amounts)
        if not amount.is_finite() or not maximum.is_finite():
            raise ValueError('Non-finite comparison')
        above=amount > maximum
    except (InvalidOperation, KeyError, TypeError, ValueError) as e:
        return {'comparable':False, 'transaction_above_recorded_maximum':None,
                'reason':f'Numeric input not usable: {type(e).__name__}'}
    return {'comparable':True, 'transaction_above_recorded_maximum':above,
            'reason':'Recorded numerical comparison only; profile is monthly and not an adjudicated single-payment limit'}


def contains_exact_citation_set(submitted: list[dict], required: list[dict]) -> bool:
    """Mechanical citation membership, NOT semantic citation sufficiency."""
    actual={(d['record_type'],d['record_id']) for d in submitted}
    return all((r['record_type'],r['record_id']) in actual for r in required)


def grouped_identical_statements(statements: list[dict]) -> list[dict]:
    grouped=defaultdict(list)
    for s in statements:
        grouped[(s['candidate_id'], s['exact_statement'])].append(s['json_pointer'])
    return [dict(candidate_id=key[0], exact_statement=key[1], locations=locs,
                 occurrences=len(locs), distinct_material_items_assumed=None)
            for key,locs in grouped.items() if len(locs)>1]


def build_calibration(packet_path: str|Path=DEFAULT_PACKET, catalog_path: str|Path=DEFAULT_CATALOG) -> dict:
    raw,docs=load_packet(packet_path)
    catalog=load_catalog(catalog_path)
    checks=validate_catalog(catalog,raw,docs,packet_path)
    inv=docs['source_inventory.draft.json']
    original=docs['claim_annotations.draft.json']
    comparison=compare_amounts_without_policy(inv['source_records'],'TX-G02-01','CUST-G02')
    required=[{'record_type':'transaction','record_id':'TX-G02-01'},
              {'record_type':'customer','record_id':'CUST-G02'}]
    interpretation=next(s for s in original['statements'] if s['candidate_id']=='hosted'
                        and s['json_pointer']=='/interpretations/0/statement')
    return {
      'report_type':'G02_HYBRID_CALIBRATION_DESIGN_INSPECTION_V0_1',
      'status':'AI_DRAFT_UNADJUDICATED',
      'frozen_packet_sha256':catalog['frozen_packet_sha256'],
      'packet_identity':checks['packet_identity'],
      'checks':checks,
      'proposed_review_order':[b['id'] for b in sorted(catalog['calibration_bundles'], key=lambda x:x['rank'])],
      'selected_units':[{ 'id':b['id'], 'name':b['name'], 'unit_ids':[u['unit_id'] for u in b['source_units']],
           'rule_ids':b['rule_ids'],'human_review_status':b['status'],
           'whole_statement_verdict':None, 'case_quality_verdict':None,
           'counterfactuals':[t['id'] for t in b['tests']]} for b in catalog['calibration_bundles']],
      'deterministic_sanity_checks_only':{
          'recorded_numeric_comparison':comparison,
          'hosted_interpretation_contains_both_amount_sources':contains_exact_citation_set(interpretation['submitted_citations'],required),
          'removing_customer_citation_changes_required_set_membership':not contains_exact_citation_set(
              [c for c in interpretation['submitted_citations'] if c['record_type']!='customer'],required),
          'identical_statement_occurrences':grouped_identical_statements(original['statements'])},
      'pending_rules': ['H-00','H-01','H-02','H-03','H-04','H-05','H-06','H-07'],
      'approved_semantic_categories':None, 'factual_accuracy':None,'citation_adequacy_rate':None,
      'model_ranking':None,'approved_g02_material_omissions':None,
      'review_authority':{'status':'pending_D-07','ai_assistance':'proposals_only',
                          'qualified_AML_expert_review':'not_obtained'},
      'limitations':['Mechanical checks and exact text bindings are not entailment.',
         'The 38 selected review units are not 38 independent factual claims.',
         'All semantic conclusions and proposed case inventory M03 require human adjudication.',
         'G01-G05 are exposed synthetic development examples; G02 is not a held-out benchmark.',
         'Hosted and baseline candidates have unequal policy access; comparative causal claims are prohibited.']}


def build_blank_review_worksheet(catalog: dict) -> dict:
    """Emit an unfilled, evidence-linked template; never impersonate a human reviewer."""
    return {'status':'DRAFT_WORKSHEET_NOT_ADJUDICATED',
      'input_file_sha256':catalog['input_file_sha256'],
      'candidate_source_hashes':catalog['candidate_source_hashes'],
      'packet_artifact_sha256':catalog['packet_artifact_sha256'],
      'reviewer_id':None,
      'reviewer_qualification':None, 'adjudicator_id':None,
      'rule_approvals':[], 'scores':None,
      'bundles':[{'bundle_id':b['id'],'evidence_review_notes':'','annotation_fidelity_notes':'',
          'source_sufficiency_notes':'','ambiguity_and_scope_notes':'',
          'possible_meaning_loss_unit_ids':[], 'counterexample_results':[],
          'whole_statement_judgment':None,'atomic_claim_judgments':None,
          'case_level_judgment':None,'disagreement_notes':'',
          'review_state':'not_reviewed'} for b in catalog['calibration_bundles']]}


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',default=str(DEFAULT_PACKET))
    p.add_argument('--catalog',default=str(DEFAULT_CATALOG))
    p.add_argument('--output',help='New JSON report path, refuses to overwrite')
    p.add_argument('--blank-review',help='New review worksheet JSON path, refuses to overwrite')
    args=p.parse_args()
    cat=load_catalog(args.catalog)
    report=build_calibration(args.packet,args.catalog)
    print(f"Verified {report['checks']['selected_bundles']} bundles / {report['checks']['selected_review_units']} draft review units; semantic judgments NOT approved")
    for name,obj in [('output',report),('blank_review',build_blank_review_worksheet(cat))]:
        target=getattr(args, 'output' if name=='output' else 'blank_review')
        if target:
            out=Path(target);out.parent.mkdir(parents=True,exist_ok=True)
            with out.open('x',encoding='utf-8') as f:
                f.write(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
            print(f'Created {name}: {out}')

if __name__=='__main__':main()
