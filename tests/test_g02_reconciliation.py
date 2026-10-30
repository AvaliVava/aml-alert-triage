"""Frozen G02 binding, recorded adjudication and non-scoring regression tests."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'research/evaluation_calibration'))
from g02_reconciliation import (
    DEFAULT_CATALOG, DEFAULT_INPUT, DEFAULT_PACKET, DEFAULT_REGISTER, REGISTER_KEYS,
    ReconciliationError, build_reconciliation, load_register, validate_register,
)
from hybrid_calibration import CalibrationError
from hybrid_review_preview import PacketError, load_packet, verify


class G02ReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DEFAULT_PACKET.exists():
            raise unittest.SkipTest('Frozen ignored G02 packet is unavailable locally')
        cls.raw, cls.docs = load_packet(DEFAULT_PACKET)
        cls.register = load_register()
        cls.input_bytes = DEFAULT_INPUT.read_bytes()
        cls.report = build_reconciliation()

    def setUp(self):
        self.data = deepcopy(self.register)

    def validate(self):
        return validate_register(self.data, self.raw, self.docs, self.input_bytes)

    def unit(self, uid):
        return next(u for u in self.data['unit_adjudications'] if u['unit_id'] == uid)

    def report_unit(self, uid):
        return next(u for u in self.report['reconciled_units'] if u['unit_id'] == uid)

    def test_valid_register_loading_and_reconciliation(self):
        checks = self.validate()
        self.assertEqual(checks['status'], 'passed')
        self.assertEqual(checks['frozen_checks']['units_verified'], 75)
        self.assertEqual(checks['frozen_checks']['statements_verified'], 21)
        self.assertEqual(checks['frozen_checks']['source_pointers_verified'], 203)
        self.assertEqual(len(self.report['reconciled_units']), 75)

    def test_missing_duplicate_and_unknown_unit_ids(self):
        for kind in ('missing', 'duplicate', 'unknown'):
            with self.subTest(kind=kind):
                self.data = deepcopy(self.register)
                units = self.data['unit_adjudications']
                if kind == 'missing':
                    units.pop()
                else:
                    units[0]['unit_id'] = units[1]['unit_id'] if kind == 'duplicate' else 'UNKNOWN'
                with self.assertRaises(ReconciliationError):
                    self.validate()

    def test_unit_text_span_pointer_and_offset_binding(self):
        edits = {
            'original_span': 'Changed text', 'statement_pointer': '/missing/statement',
            'original_span_offsets': {'start': 0, 'end': 1},
            'draft_atomic_proposition': 'Rewritten proposition', 'candidate': 'hosted',
        }
        for field, value in edits.items():
            with self.subTest(field=field):
                self.data = deepcopy(self.register)
                self.unit('B005')[field] = value
                with self.assertRaises(ReconciliationError):
                    self.validate()

    def test_whole_statement_text_membership_identity_and_population(self):
        for field, value in (
            ('statement_text', 'Changed text'), ('statement_pointer', '/unknown/statement'),
            ('unit_ids', ['B008']), ('candidate', 'unknown'),
        ):
            with self.subTest(field=field):
                self.data = deepcopy(self.register)
                self.data['whole_statement_adjudications'][0][field] = value
                with self.assertRaises(ReconciliationError):
                    self.validate()
        for duplicate in (False, True):
            self.data = deepcopy(self.register)
            whole = self.data['whole_statement_adjudications']
            if duplicate:
                whole[0] = deepcopy(whole[1])
            else:
                whole.pop()
            with self.assertRaises(ReconciliationError):
                self.validate()

    def test_citation_namespace_identifier_and_order_are_exact(self):
        for change in ('namespace', 'identifier', 'order'):
            with self.subTest(change=change):
                self.data = deepcopy(self.register)
                cites = self.unit('B001')['original_submitted_citations']
                if change == 'namespace':
                    cites[0]['record_type'] = 'evidence'
                elif change == 'identifier':
                    cites[0]['record_id'] = 'TX-G02-02'
                else:
                    cites.reverse()
                with self.assertRaises(ReconciliationError):
                    self.validate()

    def test_copied_evidence_pointer_and_value_must_match(self):
        for field, value in [('field_pointer', '/unknown'), ('observed_value', '99999.00')]:
            with self.subTest(field=field):
                self.data = deepcopy(self.register)
                p = self.unit('B005')['original_draft_evidence_pointer_candidates']['supporting_input'][0]
                p[field] = value
                with self.assertRaises(ReconciliationError):
                    self.validate()

    def test_input_inventory_candidate_and_revision_hash_bindings(self):
        for field in ('input_file_sha256', 'source_inventory_sha256', 'checkout_revision'):
            with self.subTest(field=field):
                self.data = deepcopy(self.register)
                self.data['source_packet'][field] = '0' * 64
                with self.assertRaises(ReconciliationError):
                    self.validate()
        self.data = deepcopy(self.register)
        self.data['source_packet']['candidate_sha256']['hosted'] = '0' * 64
        with self.assertRaises(ReconciliationError):
            self.validate()

    def test_raw_and_canonical_hashes_are_separate(self):
        identities = self.report['artifact_integrity']
        self.assertEqual(identities['input']['original_file_sha256'], sha256(self.input_bytes).hexdigest())
        self.assertEqual(identities['input']['canonical_validated_json_sha256'],
                         self.docs['packet_manifest.draft.json']['canonical_input_sha256'])
        self.assertNotEqual(identities['input']['original_file_sha256'],
                            identities['input']['canonical_validated_json_sha256'])
        self.assertFalse(identities['packet']['zip_bytes_verified'])
        self.data['source_packet']['input_file_sha256'] = identities['input']['canonical_validated_json_sha256']
        with self.assertRaises(ReconciliationError):
            self.validate()
        with self.assertRaises(ReconciliationError):
            validate_register(self.register, self.raw, self.docs, self.input_bytes + b'\n')

    def test_artifact_bytes_changed_in_temporary_copy_are_rejected(self):
        with TemporaryDirectory() as directory:
            for name, blob in self.raw.items():
                if name == 'hosted_candidate.json':
                    blob += b'\n'
                (Path(directory) / name).write_bytes(blob)
            with self.assertRaises((ReconciliationError, PacketError, CalibrationError)):
                build_reconciliation(packet_path=directory)

    def test_batch_partition_and_declared_population_counts(self):
        key = next(iter(self.data['approved_review_bundles']))
        self.data['approved_review_bundles'][key].append('B005')
        with self.assertRaises(ReconciliationError):
            self.validate()
        for field, value in [('frozen_unit_count', 0), ('frozen_original_statement_count', 20),
                             ('all_75_units_covered_once_by_six_approved_batches', False)]:
            self.data = deepcopy(self.register)
            self.data['validation'][field] = value
            with self.assertRaises(ReconciliationError):
                self.validate()
        self.data = deepcopy(self.register)
        self.data['validation']['unit_factual_dispositions_counts']['unassessable'] = True
        with self.assertRaises(ReconciliationError):
            self.validate()

    def test_missing_required_and_unknown_scoring_fields(self):
        for key in ('pending', 'policy_decisions', 'source_packet'):
            self.data = deepcopy(self.register)
            del self.data[key]
            with self.assertRaises(ReconciliationError):
                self.validate()
        for key, value in [('scores', {'accuracy': 1}), ('approved_scoring', True),
                           ('performance_percentage', 100)]:
            self.data = deepcopy(self.register)
            self.data[key] = value
            with self.assertRaises(ReconciliationError):
                self.validate()
        self.data = deepcopy(self.register)
        self.unit('B005')['approved_factual_support']['score'] = 1
        with self.assertRaises(ReconciliationError):
            self.validate()

    def test_invalid_field_types_and_categories(self):
        for value in (None, [], 'invalid', True):
            self.data = deepcopy(self.register)
            self.unit('B005')['approved_factual_support']['category'] = value
            with self.assertRaises(ReconciliationError):
                self.validate()

    def test_fidelity_withheld_units_never_become_candidate_error_scores(self):
        self.assertEqual(self.report['exclusions']['fidelity_withheld'], ['H004', 'H034'])
        for uid in ('H004', 'H034'):
            row = self.report_unit(uid)
            decision = row['recorded_owner_adjudication']
            self.assertEqual(decision['approved_factual_support']['category'], 'not_established')
            self.assertEqual(decision['score_eligibility'], 'withheld_pending_original_fidelity')
            self.assertEqual(row['original_frozen_annotation']['human_review_status'], 'not_reviewed')
        self.unit('H004')['score_eligibility'] = 'eligible'
        with self.assertRaises(ReconciliationError):
            self.validate()

    def test_corrected_absence_citation_judgments_are_preserved(self):
        for uid in ('H044', 'H045', 'B017', 'B018', 'B019', 'B023', 'B024', 'B025'):
            decision = self.report_unit(uid)['recorded_owner_adjudication']
            self.assertEqual(decision['approved_factual_support']['category'], 'supported')
            self.assertEqual(decision['approved_submitted_citation_treatment']['category'], 'inadequate')
        h046 = self.report_unit('H046')['recorded_owner_adjudication']
        self.assertEqual(h046['approved_submitted_citation_treatment']['category'], 'partial')
        self.unit('H044')['approved_submitted_citation_treatment']['category'] = 'adequate'
        with self.assertRaises(ReconciliationError):
            self.validate()

    def test_h047_narrow_support_and_h049_ambiguity_do_not_clear_whole_statements(self):
        for uid, status in [('H047', 'supported'), ('H049', 'unassessable')]:
            row = self.report_unit(uid)
            decision = row['recorded_owner_adjudication']
            self.assertEqual(decision['approved_factual_support']['category'], status)
            self.assertIn('corroboration', decision['interpretation_or_limit'])
            statement = next(s for s in self.report['whole_statement_reconciliation']['statements']
                             if s['candidate'] == decision['candidate']
                             and s['statement_pointer'] == decision['statement_pointer'])
            self.assertEqual(statement['approved_whole_statement_status'],
                             'reviewed_not_cleared_unconditional_pass')

    def test_process_authorities_are_separate_from_case_record_support(self):
        observations = self.report['process_evidence_observations']
        self.assertEqual({u['unit_id'] for u in observations['units']},
                         {'B003', 'B009', 'B010', 'B011', 'B012', 'B013', 'B014'})
        self.assertFalse(observations['independent_runtime_certification'])
        for unit in observations['units']:
            self.assertEqual(unit['approved_factual_support']['applicability'], 'not_applicable')
            self.assertEqual(unit['approved_submitted_citation_treatment']['handling'],
                             'separate_process_authority_dimension')
        self.assertEqual(self.report['preliminary_action_adjudication']['human_review'],
                         'required_not_completed')

    def test_repeated_baseline_m02_has_two_occurrences_one_coverage_item(self):
        coverage = self.report['material_coverage']
        repeat = next(r for r in coverage['repeated_statement_occurrences']
                      if r['candidate_id'] == 'baseline')
        self.assertEqual(repeat['occurrences'], 2)
        self.assertEqual(coverage['M02_coverage_items_per_candidate'], 1)
        self.assertEqual(coverage['mandatory_items']['M02']['baseline'], 'covered')
        self.assertEqual(self.report['submitted_citation_review']['category_and_routing_counts']['inadequate'], 10)

    def test_material_applicability_and_exact_matrix(self):
        coverage = self.report['material_coverage']
        self.assertEqual(set(coverage['mandatory_items']), {'M01', 'M02', 'M03'})
        self.assertEqual(coverage['category_counts']['hosted'], {'covered': 3})
        self.assertEqual(coverage['category_counts']['baseline'],
                         {'covered': 1, 'partly_covered': 1, 'omitted': 1})
        self.assertEqual(set(coverage['contextual_items']), {'M04', 'M05'})
        self.data['case_level_materiality_and_coverage']['M04']['applicability'] = 'mandatory'
        with self.assertRaises(ReconciliationError):
            self.validate()

    def test_whole_statement_totals_are_not_binary_accuracy(self):
        whole = self.report['whole_statement_reconciliation']
        self.assertEqual(whole['population'], 21)
        self.assertEqual(whole['status_counts'], {'qualified_factual_pass': 10,
                         'qualified_investigative_question': 3,
                         'reviewed_not_cleared_unconditional_pass': 8})
        self.data['whole_statement_adjudications'][0]['approved_whole_statement_status'] = 'qualified_investigative_question'
        with self.assertRaises(ReconciliationError):
            self.validate()

    def test_action_and_alternatives_use_register_not_provisional_reference(self):
        action = self.report['preliminary_action_adjudication']
        self.assertEqual(action['action'], 'investigate')
        self.assertEqual(action['approved_alternatives'], [])
        self.assertEqual(action['reference_file_label_status'], 'provisional_frozen_unchanged')
        self.assertTrue(all(r['matches_registered_action'] for r in action['candidate_comparisons'].values()))
        self.data['policy_decisions']['g02_action']['approved_alternatives'] = ['close']
        with self.assertRaises(ReconciliationError):
            self.validate()

    def test_approved_records_and_original_annotations_are_carried_without_rewriting(self):
        originals = {u['unit_id']: u for u in self.docs['claim_annotations.draft.json']['units']}
        for row, decision in zip(self.report['reconciled_units'], self.register['unit_adjudications']):
            self.assertEqual(row['recorded_owner_adjudication'], decision)
            self.assertEqual(row['original_frozen_annotation'], originals[decision['unit_id']])
        self.assertEqual(self.report['whole_statement_reconciliation']['statements'],
                         self.register['whole_statement_adjudications'])
        self.assertEqual(self.report['provenance']['recorded_corrections'],
                         self.register['approved_corrections'])

    def test_missing_review_metadata_and_release_gates_are_explicit(self):
        self.assertTrue(all(row['review_state'] is None and row['reviewer_id'] is None
                            for row in self.report['reconciled_units']))
        self.assertIsNone(self.report['preliminary_action_adjudication']['rubric_version'])
        self.assertIsNone(self.report['provenance']['dated_approval_event_history'])
        self.assertEqual(self.report['unresolved_decisions'], self.register['pending'])
        self.assertEqual(self.report['exclusions']['publication_gate_counts'],
                         {'not_yet_approved_for_published_scoring': 73,
                          'withheld_pending_original_fidelity': 2})

    def test_scoring_is_disabled_and_requests_are_rejected(self):
        self.assertIsNone(self.report['scoring']['rates'])
        self.assertFalse(self.report['scoring']['authorized'])
        for value in (True, 1, 0, 'yes'):
            with self.assertRaisesRegex(ReconciliationError, 'scoring'):
                build_reconciliation(scoring=value)

    def test_existing_frozen_draft_guards_remain_active(self):
        docs = deepcopy(self.docs)
        docs['claim_annotations.draft.json']['units'][0]['human_review_status'] = 'approved'
        with self.assertRaises(PacketError):
            verify(self.raw, docs)
        for audit in self.report['mechanical_validation'].values():
            self.assertTrue(all(s['status'] == 'passed' for s in audit['stages'].values()))
            self.assertTrue(all(s['status'] == 'not_evaluated'
                                for s in audit['semantic_evaluation'].values()))

    def test_deterministic_json_and_no_mutation(self):
        before = deepcopy(self.register), deepcopy(self.docs), dict(self.raw)
        file_before = {p: p.read_bytes() for p in
                       [DEFAULT_REGISTER, DEFAULT_INPUT, *DEFAULT_PACKET.iterdir()] if p.is_file()}
        report = build_reconciliation()
        self.assertEqual(report, self.report)
        self.assertEqual(json.loads(json.dumps(report, allow_nan=False)), report)
        self.assertEqual((self.register, self.docs, self.raw), before)
        self.assertTrue(all(p.read_bytes() == blob for p, blob in file_before.items()))

    def test_only_explicit_sources_are_read_and_no_network_is_used(self):
        allowed = {p.resolve() for p in DEFAULT_PACKET.iterdir()}
        allowed.update(p.resolve() for p in (DEFAULT_REGISTER, DEFAULT_CATALOG, DEFAULT_INPUT))
        original = Path.open

        def guarded(path, *args, **kwargs):
            self.assertIn(path.resolve(), allowed)
            return original(path, *args, **kwargs)

        with patch.object(Path, 'open', guarded), \
                patch('socket.socket', side_effect=AssertionError('Network access forbidden')):
            self.assertEqual(build_reconciliation()['status'], 'reconciled_non_scoring')

    def run_cli(self, *args):
        script = ROOT / 'research/evaluation_calibration/g02_reconciliation.py'
        return subprocess.run([sys.executable, '-B', str(script), *map(str, args)],
                              capture_output=True, text=True, check=False)

    def test_cli_publishes_new_report_and_refuses_overwrite(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / 'report.json'
            first = self.run_cli('--output', output)
            self.assertEqual(first.returncode, 0, first.stderr)
            blob = output.read_bytes()
            self.assertEqual(json.loads(blob)['status'], 'reconciled_non_scoring')
            second = self.run_cli('--output', output)
            self.assertEqual(second.returncode, 2)
            self.assertEqual(json.loads(second.stdout)['reconciliation_validation']['status'], 'error')
            self.assertEqual(output.read_bytes(), blob)

    def test_cli_stdout_is_complete_json_without_progress_messages(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), self.report)

    def test_cli_reports_expected_failures_as_json_without_publishing(self):
        with TemporaryDirectory() as directory:
            registry = Path(directory) / 'register.json'
            output = Path(directory) / 'report.json'
            self.data['validation']['frozen_unit_count'] = 0
            registry.write_text(json.dumps(self.data), encoding='utf-8')
            result = self.run_cli('--register', registry, '--output', output)
            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertEqual(report['reconciliation_validation']['status'], 'failed')
            self.assertIsNone(report['scoring']['rates'])
            self.assertFalse(output.exists())

    def test_cli_missing_artifact_and_frozen_output_destination(self):
        with TemporaryDirectory() as directory:
            result = self.run_cli('--register', Path(directory) / 'missing.json')
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['reconciliation_validation']['status'], 'error')
        target = DEFAULT_PACKET / 'must-not-publish.json'
        self.assertFalse(target.exists())
        result = self.run_cli('--output', target)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(target.exists())


class RegisterParsingTests(unittest.TestCase):
    def load_text(self, text):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'register.json'
            path.write_text(text, encoding='utf-8')
            return load_register(path)

    def test_malformed_json_is_rejected(self):
        with self.assertRaisesRegex(ReconciliationError, 'invalid JSON'):
            self.load_text('{')

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaisesRegex(ReconciliationError, 'duplicate JSON'):
            self.load_text('{"case_id":"A","case_id":"B"}')

    def test_nonfinite_json_is_rejected(self):
        with self.assertRaisesRegex(ReconciliationError, 'non-finite'):
            self.load_text('{"value":NaN}')

    def test_missing_required_fields_are_rejected(self):
        with self.assertRaises(ReconciliationError):
            self.load_text('{}')

    def test_unknown_scoring_field_is_rejected(self):
        data = dict.fromkeys(REGISTER_KEYS)
        data['scores'] = {'accuracy': 100}
        with self.assertRaises(ReconciliationError):
            self.load_text(json.dumps(data))


if __name__ == '__main__':
    unittest.main()
