"""Mechanical adapter tests; candidate text/actions are independent of references."""

import errno
import json
import subprocess
import sys
import unittest

from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from aml_triage.auditor import audit_packet, audit_packet_files
from aml_triage.contracts import InvestigationInput, InvestigationOutput


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "data" / "golden_cases" / "inputs"
SCRIPT = ROOT / "scripts" / "audit_packet.py"
SEMANTIC_DIMENSIONS = {
    "factual_input_support", "submitted_citation_adequacy", "material_finding_completeness",
    "missing_information_and_contradiction_coverage", "recommendation_quality",
    "abstention_appropriateness", "fabricated_verification_and_unsupported_certainty",
    "semantic_preliminary_scope_compliance", "leakage_and_held_out_independence",
}


def candidate_for(investigation):
    """Use supplied identities, without copying a reference action, finding or rationale."""
    citation = {
        "record_type": "transaction",
        "record_id": investigation["transactions"][0]["transaction_id"],
    }
    statement = {
        "statement": "A supplied transaction is cited for mechanical review.",
        "citations": [citation],
    }
    return {
        "schema_version": "1.0",
        "case_id": investigation["case"]["case_id"],
        "alert_id": investigation["alert"]["alert_id"],
        "assessment_status": "recommendation_provided",
        "recommended_action": "investigate",
        "rationale": deepcopy(statement),
        "factual_findings": [deepcopy(statement)],
        "interpretations": [],
        "unresolved_questions": [],
        "missing_information": [],
        "contradictions": [],
        "recommendation_scope": "preliminary",
        "human_review_required": True,
    }


class TestPacketAuditor(unittest.TestCase):
    def setUp(self):
        self.input_bytes = (INPUTS / "G02.json").read_bytes()
        self.input_data = json.loads(self.input_bytes)
        self.candidate = candidate_for(self.input_data)

    def audit(self, candidate=None, input_bytes=None):
        return audit_packet(
            self.input_bytes if input_bytes is None else input_bytes,
            json.dumps(self.candidate if candidate is None else candidate).encode("utf-8"),
        )

    def assert_stages(self, report, input_status, output_status, context_status):
        self.assertEqual(
            {name: stage["status"] for name, stage in report["stages"].items()},
            {"input_structure": input_status, "output_structure": output_status,
             "contextual_references": context_status},
        )
        self.assertEqual(json.loads(json.dumps(report, allow_nan=False)), report)
        for stage in report["stages"].values():
            self.assertEqual(set(stage), {"status", "reason", "phase", "diagnostics"})
            self.assertTrue(stage["reason"])
        self.assertEqual(set(report["semantic_evaluation"]), SEMANTIC_DIMENSIONS)
        for result in report["semantic_evaluation"].values():
            self.assertEqual(result["status"], "not_evaluated")
            self.assertIn("Not implemented", result["reason"])
        for forbidden in ("score", "overall_status", "assessment_passed", "attempts", "retries"):
            self.assertNotIn(forbidden, report)

    def test_valid_packet_report_shape_versions_and_digests(self):
        candidate_bytes = json.dumps(self.candidate).encode("utf-8")
        report = audit_packet(
            self.input_bytes, candidate_bytes,
            input_identity="supplied-investigation", candidate_identity="supplied-candidate",
        )
        self.assert_stages(report, "passed", "passed", "passed")
        self.assertEqual(set(report), {
            "report_schema_version", "auditor_version", "contracts", "artifacts", "stages",
            "semantic_evaluation", "limitations",
        })
        self.assertEqual(report["report_schema_version"], "1.0")
        self.assertEqual(report["auditor_version"], "0.1.0")
        versions = report["contracts"]
        self.assertEqual(versions["module"], "aml_triage.contracts")
        self.assertTrue(versions["package_version"])
        self.assertTrue(versions["pydantic_version"])
        self.assertIsNone(versions["source_revision"])
        self.assertTrue(versions["source_revision_reason"])
        self.assertEqual(versions["validation_entry_point"], "model_validate_json")
        for role, payload, identity in (
            ("input", self.input_bytes, "supplied-investigation"),
            ("candidate", candidate_bytes, "supplied-candidate"),
        ):
            self.assertEqual(report["artifacts"][role], {
                "identity": identity, "sha256": sha256(payload).hexdigest(),
                "digest_basis": "supplied_bytes", "validated_schema_version": "1.0",
                "digest_unavailable_reason": None,
            })

    def test_all_five_inputs_preserve_existing_incomplete_case_allowances(self):
        for case in ("G01", "G02", "G03", "G04", "G05"):
            with self.subTest(case=case):
                payload = (INPUTS / f"{case}.json").read_bytes()
                candidate = candidate_for(json.loads(payload))
                if case == "G04":
                    self.assertNotIn("TX-105", json.loads(payload)["alert"]["transaction_ids"])
                    candidate["rationale"]["citations"][0]["record_id"] = "TX-105"
                self.assert_stages(self.audit(candidate, payload), "passed", "passed", "passed")

    def test_invalid_input_still_validates_output_and_skips_context(self):
        data = deepcopy(self.input_data)
        data.pop("customer")
        with patch("aml_triage.auditor.validate_investigation_output_references") as contextual:
            report = self.audit(input_bytes=json.dumps(data).encode("utf-8"))
        contextual.assert_not_called()
        self.assert_stages(report, "failed", "passed", "not_evaluated")
        self.assertIn("input_structure", report["stages"]["contextual_references"]["reason"])
        diagnostic = report["stages"]["input_structure"]["diagnostics"][0]
        self.assertEqual(diagnostic["type"], "missing")
        self.assertEqual(diagnostic["location"], ["customer"])
        self.assertIsNone(report["artifacts"]["input"]["validated_schema_version"])

    def test_invalid_output_still_validates_input_and_skips_context(self):
        self.candidate.pop("human_review_required")
        with patch("aml_triage.auditor.validate_investigation_output_references") as contextual:
            report = self.audit()
        contextual.assert_not_called()
        self.assert_stages(report, "passed", "failed", "not_evaluated")
        self.assertIn("output_structure", report["stages"]["contextual_references"]["reason"])
        self.assertEqual(report["stages"]["output_structure"]["diagnostics"][0]["location"],
                         ["human_review_required"])

    def test_both_invalid_structures_retain_independent_diagnostics(self):
        self.candidate["recommended_action"] = None
        report = self.audit(input_bytes=b"{}")
        self.assert_stages(report, "failed", "failed", "not_evaluated")
        context_reason = report["stages"]["contextual_references"]["reason"]
        self.assertIn("input_structure", context_reason)
        self.assertIn("output_structure", context_reason)
        self.assertTrue(report["stages"]["input_structure"]["diagnostics"])
        diagnostic = report["stages"]["output_structure"]["diagnostics"][0]
        self.assertEqual(diagnostic["type"], "value_error")
        self.assertEqual(diagnostic["location"], [])
        self.assertIn("recommended_action", diagnostic["message"])

    def test_duplicate_fixture_retains_root_error_and_existing_message_path(self):
        payload = (INPUTS / "G05_invalid_duplicate.json").read_bytes()
        report = self.audit(candidate_for(json.loads(payload)), payload)
        self.assert_stages(report, "failed", "passed", "not_evaluated")
        diagnostic = report["stages"]["input_structure"]["diagnostics"][0]
        self.assertEqual(diagnostic["type"], "value_error")
        self.assertEqual(diagnostic["location"], [])
        self.assertIn("transactions[1].transaction_id", diagnostic["message"])
        self.assertIn("duplicate identifier", diagnostic["message"])

    def test_case_and_alert_identity_mismatches_use_exact_matching(self):
        for field in ("case_id", "alert_id"):
            for value in ("OTHER-ID", self.candidate[field].lower(), " " + self.candidate[field]):
                with self.subTest(field=field, value=value):
                    candidate = deepcopy(self.candidate)
                    candidate[field] = value
                    report = self.audit(candidate)
                    self.assert_stages(report, "passed", "passed", "failed")
                    diagnostic = report["stages"]["contextual_references"]["diagnostics"][0]
                    self.assertEqual(diagnostic["type"], "ValueError")
                    self.assertIsNone(diagnostic["location"])
                    self.assertTrue(diagnostic["message"].startswith(field + ":"))

    def test_unknown_wrong_namespace_and_normalized_citations_are_rejected(self):
        transaction_id = self.input_data["transactions"][0]["transaction_id"]
        for kind, identifier in (
            ("transaction", "NOT-SUPPLIED"), ("evidence", transaction_id),
            ("transaction", transaction_id.lower()), ("transaction", transaction_id + " "),
        ):
            with self.subTest(kind=kind, identifier=identifier):
                candidate = deepcopy(self.candidate)
                candidate["rationale"]["citations"] = [{
                    "record_type": kind, "record_id": identifier,
                }]
                report = self.audit(candidate)
                self.assert_stages(report, "passed", "passed", "failed")
                diagnostic = report["stages"]["contextual_references"]["diagnostics"][0]
                self.assertIn("rationale.citations[0]", diagnostic["message"])
                self.assertIn(repr(identifier), diagnostic["message"])
                self.assertIsNone(diagnostic["location"])

    def test_badly_typed_citations_are_structural_failures(self):
        for field, value in (("record_type", "supplier"), ("record_id", 123)):
            with self.subTest(field=field):
                candidate = deepcopy(self.candidate)
                candidate["rationale"]["citations"][0][field] = value
                report = self.audit(candidate)
                self.assert_stages(report, "passed", "failed", "not_evaluated")
                self.assertEqual(report["stages"]["output_structure"]["diagnostics"][0]["location"],
                                 ["rationale", "citations", 0, field])

    def test_nested_context_error_preserves_message_without_inventing_location(self):
        left = deepcopy(self.candidate["rationale"])
        right = deepcopy(left)
        right["citations"][0]["record_id"] = "MISSING-RECORD"
        self.candidate["contradictions"] = [{
            "description": "Candidate contrast for path-reporting tests.",
            "left": left, "right": right,
        }]
        report = self.audit()
        self.assert_stages(report, "passed", "passed", "failed")
        diagnostic = report["stages"]["contextual_references"]["diagnostics"][0]
        self.assertEqual(diagnostic["message"],
                         "contradictions[0].right.citations[0]: unknown transaction "
                         "identifier 'MISSING-RECORD'")
        self.assertIsNone(diagnostic["location"])

    def test_abstention_and_permitted_uncited_statements_are_mechanically_valid(self):
        self.candidate.update(
            assessment_status="unable_to_recommend", recommended_action=None,
            rationale={"statement": "This candidate cannot recommend an action.", "citations": []},
            factual_findings=[], interpretations=[],
            unresolved_questions=[{"statement": "What context is available?", "citations": []}],
            missing_information=[{"statement": "More context is requested.", "citations": []}],
        )
        self.assert_stages(self.audit(), "passed", "passed", "passed")

    def test_false_claim_with_real_citations_passes_only_mechanical_checks(self):
        self.assertGreater(float(self.input_data["transactions"][0]["amount"]), 0)
        self.candidate["factual_findings"][0]["statement"] = "The cited transaction amount is zero."
        for action in ("close", "investigate", "escalate"):
            with self.subTest(action=action):
                self.candidate["recommended_action"] = action
                report = self.audit()
                self.assert_stages(report, "passed", "passed", "passed")
                self.assertEqual(report["semantic_evaluation"]["factual_input_support"]["status"],
                                 "not_evaluated")

    def test_malformed_json_is_validation_failure_with_original_byte_digest(self):
        good_candidate = json.dumps(self.candidate).encode("utf-8")
        for malformed in (b"{", b"", b"\xff"):
            for role in ("input", "candidate"):
                with self.subTest(role=role, malformed=malformed):
                    report = audit_packet(
                        malformed if role == "input" else self.input_bytes,
                        malformed if role == "candidate" else good_candidate,
                    )
                    self.assert_stages(
                        report, "failed" if role == "input" else "passed",
                        "failed" if role == "candidate" else "passed", "not_evaluated",
                    )
                    stage_name = "input_structure" if role == "input" else "output_structure"
                    stage = report["stages"][stage_name]
                    self.assertEqual(stage["phase"], "validation")
                    self.assertEqual(stage["diagnostics"][0]["type"], "json_invalid")
                    self.assertEqual(report["artifacts"][role]["sha256"],
                                     sha256(malformed).hexdigest())

    def test_validation_diagnostics_are_json_safe_without_raw_inputs_or_context(self):
        self.candidate["unexpected"] = "PRIVATE-RAW-PAYLOAD-SENTINEL"
        self.candidate["human_review_required"] = 1
        report = self.audit()
        self.assert_stages(report, "passed", "failed", "not_evaluated")
        self.assertNotIn("PRIVATE-RAW-PAYLOAD-SENTINEL", json.dumps(report))
        diagnostics = report["stages"]["output_structure"]["diagnostics"]
        self.assertEqual(len(diagnostics), 2)
        for diagnostic in diagnostics:
            self.assertEqual(set(diagnostic), {"type", "message", "location"})
        self.assertEqual({item["type"] for item in diagnostics}, {"value_error", "extra_forbidden"})

    def test_malformed_unicode_string_reports_failure_without_digest_crash(self):
        report = audit_packet(self.input_bytes, '{"statement": "\ud800"}')
        self.assert_stages(report, "passed", "failed", "not_evaluated")
        self.assertEqual(report["stages"]["output_structure"]["diagnostics"][0]["type"],
                         "string_unicode")
        self.assertIsNone(report["artifacts"]["candidate"]["sha256"])
        self.assertEqual(report["artifacts"]["candidate"]["digest_unavailable_reason"],
                         "Supplied string cannot be encoded as UTF-8.")

    def test_unexpected_structural_errors_do_not_hide_the_other_payload(self):
        for model, role in ((InvestigationInput, "input"), (InvestigationOutput, "output")):
            with self.subTest(role=role), patch.object(
                model, "model_validate_json", side_effect=RuntimeError("PRIVATE-EXCEPTION-SENTINEL")
            ), patch("aml_triage.auditor.validate_investigation_output_references") as contextual:
                report = self.audit()
            contextual.assert_not_called()
            self.assert_stages(report, "error" if role == "input" else "passed",
                               "error" if role == "output" else "passed", "not_evaluated")
            self.assertNotIn("PRIVATE-EXCEPTION-SENTINEL", json.dumps(report))
            self.assertEqual(report["stages"][role + "_structure"]["diagnostics"][0]["type"],
                             "RuntimeError")

    def test_unexpected_reference_failure_is_error_not_rejection(self):
        with patch("aml_triage.auditor.validate_investigation_output_references",
                   side_effect=RuntimeError("PRIVATE-EXCEPTION-SENTINEL")):
            report = self.audit()
        self.assert_stages(report, "passed", "passed", "error")
        self.assertEqual(report["stages"]["contextual_references"]["diagnostics"][0]["type"],
                         "RuntimeError")
        self.assertNotIn("PRIVATE-EXCEPTION-SENTINEL", json.dumps(report))

    def test_string_payloads_use_utf8_digests_and_preserve_original_text(self):
        self.candidate["rationale"]["statement"] = "  Original café text.\n"
        input_text = self.input_bytes.decode("utf-8")
        candidate_text = json.dumps(self.candidate, ensure_ascii=False, indent=3)
        before = (input_text, candidate_text, deepcopy(self.candidate))
        report = audit_packet(input_text, candidate_text)
        self.assert_stages(report, "passed", "passed", "passed")
        self.assertEqual(report["artifacts"]["candidate"]["sha256"],
                         sha256(candidate_text.encode("utf-8")).hexdigest())
        self.assertEqual(report["artifacts"]["candidate"]["digest_basis"], "utf8_encoded_string")
        self.assertEqual((input_text, candidate_text, self.candidate), before)

    def write_packet(self, directory):
        input_path = Path(directory) / "investigation.json"
        candidate_path = Path(directory) / "candidate.json"
        input_path.write_bytes(self.input_bytes)
        candidate_path.write_text(json.dumps(self.candidate), encoding="utf-8")
        return input_path, candidate_path

    def test_file_artifacts_are_unchanged_on_success_and_failure(self):
        with TemporaryDirectory() as directory:
            paths = self.write_packet(directory)
            for matches in (True, False):
                self.candidate["case_id"] = (
                    self.input_data["case"]["case_id"] if matches else "OTHER"
                )
                candidate_bytes = (
                    " \n" + json.dumps(self.candidate, indent=3) + "\n"
                ).encode("utf-8")
                paths[1].write_bytes(candidate_bytes)
                before = [path.read_bytes() for path in paths]
                report = audit_packet_files(*paths)
                self.assert_stages(report, "passed", "passed", "passed" if matches else "failed")
                self.assertEqual([path.read_bytes() for path in paths], before)
                for role, path, payload in zip(("input", "candidate"), paths, before):
                    self.assertEqual(report["artifacts"][role]["identity"], str(path))
                    self.assertEqual(report["artifacts"][role]["sha256"],
                                     sha256(payload).hexdigest())
                    self.assertEqual(report["artifacts"][role]["digest_basis"], "file_bytes")

    def test_each_missing_file_still_allows_other_structure_validation(self):
        for role in ("input", "candidate"):
            with self.subTest(role=role), TemporaryDirectory() as directory:
                input_path, candidate_path = self.write_packet(directory)
                missing = Path(directory) / "not-present.json"
                report = audit_packet_files(missing if role == "input" else input_path,
                                            missing if role == "candidate" else candidate_path)
                self.assert_stages(report, "error" if role == "input" else "passed",
                                   "error" if role == "candidate" else "passed", "not_evaluated")
                stage_name = "input_structure" if role == "input" else "output_structure"
                stage = report["stages"][stage_name]
                self.assertEqual(stage["phase"], "ingestion")
                self.assertEqual(stage["diagnostics"][0]["type"], "FileNotFoundError")
                self.assertIsNone(report["artifacts"][role]["sha256"])
                self.assertEqual(report["artifacts"][role]["identity"], str(missing))

    def test_permission_error_is_ingestion_error_and_other_file_is_checked(self):
        with TemporaryDirectory() as directory:
            input_path, candidate_path = self.write_packet(directory)
            read_bytes = Path.read_bytes

            def read(path):
                if path == input_path:
                    raise PermissionError(errno.EACCES, "Permission denied")
                return read_bytes(path)

            with patch.object(Path, "read_bytes", read):
                report = audit_packet_files(input_path, candidate_path)
            self.assert_stages(report, "error", "passed", "not_evaluated")
            self.assertEqual(report["stages"]["input_structure"]["diagnostics"][0]["type"],
                             "PermissionError")

    def test_both_missing_files_report_both_errors(self):
        with TemporaryDirectory() as directory:
            report = audit_packet_files(
                Path(directory) / "missing-input", Path(directory) / "missing-output",
            )
        self.assert_stages(report, "error", "error", "not_evaluated")
        self.assertIn("input_structure", report["stages"]["contextual_references"]["reason"])
        self.assertIn("output_structure", report["stages"]["contextual_references"]["reason"])

    def test_unexpected_reader_error_still_attempts_the_other_file(self):
        with TemporaryDirectory() as directory:
            paths = self.write_packet(directory)
            read_bytes = Path.read_bytes

            def read(path):
                if path == paths[0]:
                    raise RuntimeError("PRIVATE-EXCEPTION-SENTINEL")
                return read_bytes(path)

            with patch.object(Path, "read_bytes", read):
                report = audit_packet_files(*paths)
            self.assert_stages(report, "error", "passed", "not_evaluated")
            self.assertEqual(report["stages"]["input_structure"]["phase"], "ingestion")
            self.assertEqual(report["stages"]["input_structure"]["diagnostics"][0]["type"],
                             "RuntimeError")
            self.assertNotIn("PRIVATE-EXCEPTION-SENTINEL", json.dumps(report))

    def test_raw_audit_reads_no_files_policy_references_or_annotations(self):
        with patch("builtins.open", side_effect=AssertionError("forbidden read")), patch.object(
            Path, "open", side_effect=AssertionError("forbidden read")
        ), patch.object(
            Path, "read_bytes", side_effect=AssertionError("forbidden read")
        ), patch.object(
            Path, "read_text", side_effect=AssertionError("forbidden read")
        ):
            report = self.audit()
        self.assert_stages(report, "passed", "passed", "passed")

    def test_file_audit_reads_only_the_two_explicit_files(self):
        with TemporaryDirectory() as directory:
            paths = self.write_packet(directory)
            original_open = Path.open
            reads = []

            def allowed_open(path, *args, **kwargs):
                self.assertIn(path, paths)
                self.assertEqual(args[0] if args else kwargs.get("mode"), "rb")
                reads.append(path)
                return original_open(path, *args, **kwargs)

            with patch.object(Path, "open", allowed_open), patch(
                "builtins.open", side_effect=AssertionError("forbidden read")
            ):
                report = audit_packet_files(*paths)
            self.assertEqual(reads, list(paths))
            self.assert_stages(report, "passed", "passed", "passed")

    def run_cli(self, paths, cwd):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(paths[0]), "--candidate", str(paths[1])],
            cwd=cwd, capture_output=True, text=True, check=False, timeout=30,
        )
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_cli_success_is_json_and_exit_zero(self):
        with TemporaryDirectory() as directory:
            paths = self.write_packet(directory)
            code, report = self.run_cli(paths, directory)
        self.assertEqual(code, 0)
        self.assert_stages(report, "passed", "passed", "passed")

    def test_cli_validation_and_context_failures_are_json_and_exit_one(self):
        for failure in ("input", "output", "context"):
            with self.subTest(failure=failure), TemporaryDirectory() as directory:
                paths = self.write_packet(directory)
                if failure == "input":
                    paths[0].write_bytes(b"{")
                elif failure == "output":
                    paths[1].write_bytes(b"{}")
                else:
                    self.candidate["alert_id"] = "WRONG-ALERT"
                    paths[1].write_text(json.dumps(self.candidate), encoding="utf-8")
                code, report = self.run_cli(paths, directory)
                self.assertEqual(code, 1)
                self.assert_stages(report, "failed" if failure == "input" else "passed",
                                   "failed" if failure == "output" else "passed",
                                   "failed" if failure == "context" else "not_evaluated")

    def test_cli_missing_files_are_json_and_exit_two(self):
        for role in (0, 1):
            with self.subTest(role=role), TemporaryDirectory() as directory:
                paths = list(self.write_packet(directory))
                paths[role] = Path(directory) / "absent.json"
                code, report = self.run_cli(paths, directory)
                self.assertEqual(code, 2)
                self.assert_stages(report, "error" if role == 0 else "passed",
                                   "error" if role == 1 else "passed", "not_evaluated")

    def test_cli_errors_take_exit_code_precedence_over_validation_failure(self):
        with TemporaryDirectory() as directory:
            paths = list(self.write_packet(directory))
            paths[0] = Path(directory) / "absent.json"
            paths[1].write_bytes(b"{}")
            code, report = self.run_cli(paths, directory)
        self.assertEqual(code, 2)
        self.assert_stages(report, "error", "failed", "not_evaluated")


if __name__ == "__main__":
    unittest.main()
