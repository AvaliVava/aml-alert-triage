"""Deterministic safeguards; do not assert that G02 semantic judgments are correct."""
import copy
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research/evaluation_calibration'))
from hybrid_review_preview import DEFAULT_PACKET, load_packet
from hybrid_calibration import (
    CalibrationError, build_blank_review_worksheet, build_calibration,
    compare_amounts_without_policy, contains_exact_citation_set,
    grouped_identical_statements, load_catalog, validate_catalog,
)
from build_calibration_review_ui import build_html

PACKET=DEFAULT_PACKET
CATALOG=ROOT/'research/evaluation_calibration/calibration_cases.draft.json'

class CalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not PACKET.exists():
            raise unittest.SkipTest('Frozen ignored G02 pilot packet is not available locally')
        cls.raw,cls.docs=load_packet(PACKET)
        cls.catalog=load_catalog(CATALOG)
        cls.inv=cls.docs['source_inventory.draft.json']['source_records']

    def test_read_only_source_verification(self):
        x=validate_catalog(self.catalog,self.raw,self.docs,PACKET)
        self.assertEqual((x['selected_bundles'],x['selected_review_units']),(7,38))
        self.assertFalse(x['semantic_judgments_verified'])
        self.assertEqual(x['source_packet_integrity']['source_pointers_verified'],203)

    def test_no_accuracy_ranking_or_adjudication(self):
        report=build_calibration(PACKET,CATALOG)
        for k in ('factual_accuracy','citation_adequacy_rate','model_ranking','approved_g02_material_omissions','approved_semantic_categories'):
            self.assertIsNone(report[k])
        self.assertEqual(report['status'],'AI_DRAFT_UNADJUDICATED')
        self.assertTrue(all(e['whole_statement_verdict'] is None for e in report['selected_units']))

    def test_no_fabricated_human_review_in_worksheet(self):
        w=build_blank_review_worksheet(self.catalog)
        self.assertIsNone(w['reviewer_id'])
        self.assertIsNone(w['adjudicator_id'])
        self.assertEqual(w['rule_approvals'],[])
        self.assertTrue(all(b['review_state']=='not_reviewed' and b['whole_statement_judgment'] is None for b in w['bundles']))

    def test_catalog_contains_fidelity_problem_in_exact_source_span(self):
        a=self.catalog['calibration_bundles'][0]
        h047=next(u for u in a['source_units'] if u['unit_id']=='H047')
        self.assertIn('notes their absence',h047['exact_span'])
        self.assertIn('no such corroboration',h047['atomic_proposition_as_proposed'])
        self.assertIsNone(a['meaning_preservation_review'])
        self.assertEqual(a['status'],'not_reviewed')

    def test_attribution_qualifier_not_erased_from_frozen_span(self):
        b=self.catalog['calibration_bundles'][1]
        h032=next(u for u in b['source_units'] if u['unit_id']=='H032')
        self.assertIn("customer's stated",h032['exact_span'])
        self.assertNotIn("customer's stated",h032['atomic_proposition_as_proposed'])
        self.assertIn('H-00',b['rule_ids'])

    def test_question_premise_and_question_are_separately_registered(self):
        b=self.catalog['calibration_bundles'][3]
        self.assertEqual({u['unit_id'] for u in b['source_units']},{'H040','H041'})
        h040=next(u for u in b['source_units'] if u['unit_id']=='H040')
        self.assertEqual(h040['submitted_citations'],[])
        self.assertIn('H-04',b['rule_ids'])

    def test_process_assertions_require_different_authorities(self):
        b=self.catalog['calibration_bundles'][4]
        self.assertIn('source_code_and_execution_context',b['authority'])
        self.assertIn('output_contract',b['authority'])
        self.assertIn('B014',{u['unit_id'] for u in b['source_units']})

    def test_baseline_repeat_preserved_at_two_locations(self):
        stmts=self.docs['claim_annotations.draft.json']['statements']
        duplicates=grouped_identical_statements(stmts)
        b=next(x for x in duplicates if x['candidate_id']=='baseline')
        self.assertEqual(b['occurrences'],2)
        self.assertEqual(set(b['locations']),{'/unresolved_questions/0/statement','/missing_information/0/statement'})
        self.assertIsNone(b['distinct_material_items_assumed'])

    def test_baseline_invoice_type_mapping_is_flagged_not_assumed(self):
        b=self.catalog['calibration_bundles'][5]
        b017=next(u for u in b['source_units'] if u['unit_id']=='B017')
        self.assertIn('No linked invoice',b017['exact_span'])
        self.assertIn('supplier_invoice',b017['atomic_proposition_as_proposed'])

    def test_absent_baseline_assertion_not_invented_as_an_annotation(self):
        b=self.catalog['calibration_bundles'][6]
        self.assertTrue(all(u['candidate_id']=='hosted' for u in b['source_units']))
        self.assertEqual(self.catalog['selected_case_level_items'][0]['item_id'],'M03')
        self.assertTrue(self.catalog['selected_case_level_items'][0]['no_baseline_unit_for_omission'])
        self.assertEqual(self.catalog['selected_case_level_items'][0]['status'],'proposed_not_adjudicated')

    def test_numeric_comparison_does_not_claim_materiality(self):
        result=compare_amounts_without_policy(self.inv,'TX-G02-01','CUST-G02')
        self.assertTrue(result['comparable'])
        self.assertTrue(result['transaction_above_recorded_maximum'])
        self.assertIn('not an adjudicated single-payment limit',result['reason'])

    def test_currency_mismatch_refuses_comparison(self):
        records=copy.deepcopy(self.inv)
        tx=next(x for x in records if x['record_id']=='TX-G02-01')
        tx['fields']['currency']='EUR'
        result=compare_amounts_without_policy(records,'TX-G02-01','CUST-G02')
        self.assertFalse(result['comparable'])
        self.assertIsNone(result['transaction_above_recorded_maximum'])

    def test_invalid_amount_does_not_fabricate_result(self):
        records=copy.deepcopy(self.inv)
        tx=next(x for x in records if x['record_id']=='TX-G02-01')
        tx['fields']['amount']='not-a-number'
        self.assertFalse(compare_amounts_without_policy(records,'TX-G02-01','CUST-G02')['comparable'])

    def test_missing_customer_citation_changes_membership_not_input_truth(self):
        b=self.catalog['calibration_bundles'][1]
        u=next(x for x in b['source_units'] if x['unit_id']=='H032')
        citations=u['submitted_citations']
        req=[{'record_type':'transaction','record_id':'TX-G02-01'},
             {'record_type':'customer','record_id':'CUST-G02'}]
        self.assertTrue(contains_exact_citation_set(citations,req))
        self.assertFalse(contains_exact_citation_set([c for c in citations if c['record_type']!='customer'],req))

    def test_approval_and_semantic_scores_cannot_be_injected_into_draft_catalog(self):
        for change in ({'approved_scoring':True},{'approved_semantic_rules':['H-00']},{'review_status':'HUMAN_APPROVED'}):
            a=copy.deepcopy(self.catalog);a.update(change)
            with self.assertRaises(CalibrationError): validate_catalog(a,self.raw,self.docs,PACKET)

    def test_changed_text_anchor_cannot_pass_validation(self):
        bad=copy.deepcopy(self.catalog)
        bad['calibration_bundles'][0]['source_units'][0]['exact_span']='No contract is supplied'
        with self.assertRaises(CalibrationError):validate_catalog(bad,self.raw,self.docs,PACKET)

    def test_unreviewed_semantic_hypotheses_are_not_replaced_with_true_false(self):
        report=build_calibration(PACKET,CATALOG)
        self.assertFalse(report['checks']['semantic_judgments_verified'])
        self.assertTrue(all(b['candidate_comparison_outcome'] is None for b in self.catalog['calibration_bundles']))

    def test_catalog_contains_counterfactuals_for_all_seven_bundles(self):
        for bundle in self.catalog['calibration_bundles']:
            self.assertTrue(bundle['tests'])
            for scenario in bundle['tests']:
                self.assertIn('change',scenario)
                self.assertIn('fixed',scenario)
                self.assertIn('expected',scenario)
                self.assertIn('method',scenario)

    def test_directory_identity_does_not_claim_zip_bytes_verified(self):
        report=build_calibration(PACKET,CATALOG)
        identity=report['packet_identity']
        self.assertEqual(identity['source_kind'],'directory')
        self.assertFalse(identity['zip_bytes_verified'])
        self.assertEqual(identity['artifact_sha256'],self.catalog['packet_artifact_sha256'])
        self.assertEqual(identity['historical_zip_sha256'],self.catalog['frozen_packet_sha256'])

    def test_changed_catalog_artifact_digest_is_rejected(self):
        catalog=copy.deepcopy(self.catalog)
        catalog['packet_artifact_sha256']['hosted_candidate.json']='0'*64
        with self.assertRaisesRegex(CalibrationError,'artifact bytes mismatch'):
            validate_catalog(catalog,self.raw,self.docs,PACKET)

    def test_case_materiality_cannot_be_promoted_by_catalog(self):
        catalog=copy.deepcopy(self.catalog)
        catalog['selected_case_level_items'][0]['status']='approved'
        with self.assertRaisesRegex(CalibrationError,'remain proposals'):
            validate_catalog(catalog,self.raw,self.docs,PACKET)

    def test_nonfinite_float_and_missing_amount_fields_are_not_compared(self):
        for value in ('NaN','Infinity','-Infinity',48500.0,True,None):
            with self.subTest(value=value):
                records=copy.deepcopy(self.inv)
                next(r for r in records if r['record_id']=='TX-G02-01')['fields']['amount']=value
                result=compare_amounts_without_policy(records,'TX-G02-01','CUST-G02')
                self.assertFalse(result['comparable'])
                self.assertIsNone(result['transaction_above_recorded_maximum'])
        self.assertFalse(compare_amounts_without_policy([], 'missing','missing')['comparable'])

    def test_inspection_and_ui_read_only_explicit_packet_and_catalog(self):
        allowed={path.resolve() for path in PACKET.iterdir()} | {CATALOG.resolve()}
        original_path_open=Path.open
        original_open=open

        def path_open(path,*args,**kwargs):
            self.assertIn(path.resolve(),allowed)
            return original_path_open(path,*args,**kwargs)

        def plain_open(path,*args,**kwargs):
            self.assertIn(Path(path).resolve(),allowed)
            return original_open(path,*args,**kwargs)

        with patch.object(Path,'open',path_open), patch('builtins.open',plain_open), \
                patch('socket.socket',side_effect=AssertionError('Network access forbidden')):
            build_calibration(PACKET,CATALOG)
            html=build_html(PACKET,CATALOG)
        self.assertIn('Proposed source links, exact field values',html)
        self.assertEqual(load_packet(PACKET)[0],self.raw)
        self.assertEqual(load_catalog(CATALOG),self.catalog)

    def test_ui_embeds_verified_sources_and_unreviewed_export(self):
        html=build_html(PACKET,CATALOG)
        data=json.loads(html.split('const DATA=',1)[1].split(';\nconst notes=',1)[0])
        self.assertEqual(data['checks'],{'verified_bundles':7,'selected_units':38})
        self.assertEqual(data['source_records'],self.inv)
        source=data['unit_evidence_for_review']['H047']['supporting_input'][0]
        self.assertEqual(source['record_id'],'CHK-G02-01')
        self.assertEqual(source['field_pointer'],'/findings/0')
        self.assertIn('corroborates',source['observed_value'])
        self.assertIn("status:'UNREVIEWED_NOTES_ONLY'",html)
        self.assertIn('approved_rules:[],scores:null',html)
        self.assertNotIn('fetch(',html)
        self.assertNotIn('<script src=',html)

    def test_ui_escapes_catalog_text_in_embedded_script(self):
        catalog=copy.deepcopy(self.catalog)
        catalog['calibration_bundles'][0]['name']='</script><script>test()</script>'
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'catalog.json'
            path.write_text(json.dumps(catalog),encoding='utf-8')
            html=build_html(PACKET,path)
        self.assertNotIn('</script><script>test()',html)
        self.assertIn('\\u003c/script\\u003e',html)

    def test_blank_worksheet_binds_exact_artifact_identities(self):
        worksheet=build_blank_review_worksheet(self.catalog)
        self.assertEqual(worksheet['candidate_source_hashes'],self.catalog['candidate_source_hashes'])
        self.assertEqual(worksheet['input_file_sha256'],self.catalog['input_file_sha256'])
        self.assertEqual(worksheet['packet_artifact_sha256'],self.catalog['packet_artifact_sha256'])

    def test_cli_generates_report_worksheet_and_html_offline(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            script=ROOT/'research/evaluation_calibration/hybrid_calibration.py'
            result=subprocess.run(
                [sys.executable,'-B',str(script),'--output',str(root/'report.json'),
                 '--blank-review',str(root/'worksheet.json')],
                cwd=root,capture_output=True,text=True,check=False,
            )
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIsNone(json.loads((root/'report.json').read_bytes())['factual_accuracy'])
            self.assertIsNone(json.loads((root/'worksheet.json').read_bytes())['reviewer_id'])
            script=ROOT/'research/evaluation_calibration/build_calibration_review_ui.py'
            result=subprocess.run(
                [sys.executable,'-B',str(script),'--output',str(root/'review.html')],
                cwd=root,capture_output=True,text=True,check=False,
            )
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('G02 Hybrid Calibration Lab',(root/'review.html').read_text(encoding='utf-8'))

    def test_cli_refuses_existing_report_and_ui_destinations(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'existing'
            target.write_bytes(b'keep these bytes')
            for name in ('hybrid_calibration.py','build_calibration_review_ui.py'):
                script=ROOT/'research/evaluation_calibration'/name
                result=subprocess.run(
                    [sys.executable,'-B',str(script),'--output',str(target)],
                    cwd=directory,capture_output=True,text=True,check=False,
                )
                self.assertNotEqual(result.returncode,0)
                self.assertEqual(target.read_bytes(),b'keep these bytes')

if __name__=='__main__':unittest.main(verbosity=2)
