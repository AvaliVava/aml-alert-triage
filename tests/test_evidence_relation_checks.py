"""Unreviewed development examples, independently authored; no golden answers used."""

import json
import unittest

from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

from aml_triage.auditor import audit_packet
from aml_triage.evidence_relation_checks import evaluate_evidence_relationships


INPUT = Path(__file__).resolve().parents[1] / "data" / "golden_cases" / "inputs" / "G04.json"
DIFFERENT = "The invoice's account reference and the wire record's account reference differ."
EQUAL = "The invoice's account reference and the wire record's account reference are equal."


def json_bytes(value):
    return json.dumps(value, ensure_ascii=False).encode("utf-8")


def development_annotations(input_bytes, candidate_bytes, relationship="different"):
    """Evaluator-side test authoring helper; no candidate infers or generates annotations."""
    candidate = json.loads(candidate_bytes)
    return {
        "schema_version": "1.0", "review_status": "unreviewed_development_example",
        "case_id": json.loads(input_bytes)["case"]["case_id"],
        "investigation_sha256": sha256(input_bytes).hexdigest(),
        "candidate_sha256": sha256(candidate_bytes).hexdigest(),
        "findings": [{
            "finding_index": 0, "statement": candidate["factual_findings"][0]["statement"],
            "asserted_relationship": relationship,
            "left_evidence_id": "EV-004", "right_evidence_id": "EV-005",
            "transaction_id": "TX-105",
        }],
    }


class TestEvidenceRelationChecks(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(INPUT.read_bytes())
        statement = {"statement": DIFFERENT, "citations": [
            {"record_type": "evidence", "record_id": "EV-004"},
            {"record_type": "evidence", "record_id": "EV-005"},
        ]}
        self.candidate = {
            "schema_version": "1.0", "case_id": "CASE-G04", "alert_id": "ALT-G04",
            "assessment_status": "recommendation_provided", "recommended_action": "investigate",
            "rationale": {"statement": "Independent candidate for relationship evaluation.",
                          "citations": [{"record_type": "transaction", "record_id": "TX-105"}]},
            "factual_findings": [statement], "interpretations": [], "unresolved_questions": [],
            "missing_information": [], "contradictions": [],
            "recommendation_scope": "preliminary", "human_review_required": True,
        }

    def packet(self, relationship="different"):
        investigation, candidate = json_bytes(self.data), json_bytes(self.candidate)
        annotations = development_annotations(investigation, candidate, relationship)
        return investigation, candidate, annotations

    def evaluate(self, relationship="different"):
        investigation, candidate, annotations = self.packet(relationship)
        return evaluate_evidence_relationships(investigation, candidate, json_bytes(annotations))

    def cite(self, identifiers, kind="evidence"):
        self.candidate["factual_findings"][0]["citations"] = [
            {"record_type": kind, "record_id": identifier} for identifier in identifiers
        ]

    def assert_outcomes(self, report, relationship, coverage):
        self.assertEqual(json.loads(json.dumps(report, allow_nan=False)), report)
        finding = report["findings"][0]
        self.assertEqual(finding["recorded_relationship_consistency"]["outcome"], relationship)
        self.assertEqual(finding["submitted_direct_source_coverage"]["outcome"], coverage)
        for dimension in ("recorded_relationship_consistency", "submitted_direct_source_coverage"):
            self.assertTrue(finding[dimension]["reason"])
            counts = report["coverage"][dimension]
            self.assertEqual(counts["checked"] + counts["not_evaluated"],
                             report["coverage"]["total_findings"])
        for key in ("score", "overall_status", "quality_passed", "recommended_action"):
            self.assertNotIn(key, report)
        return finding

    def test_true_difference_and_both_direct_sources_are_separate_matches(self):
        report = self.evaluate()
        finding = self.assert_outcomes(report, "matches_supplied_records", "required_sources_cited")
        self.assertEqual(report["report_schema_version"], "1.0")
        self.assertEqual(report["evaluator_version"], "0.1.0")
        self.assertEqual(report["annotation_review_status"], "unreviewed_development_example")
        self.assertTrue(all(stage["status"] == "passed" for stage in report["validation"].values()))
        self.assertEqual(finding["required_evidence_ids"], ["EV-004", "EV-005"])
        self.assertEqual(finding["missing_citation_ids"], [])
        self.assertEqual(finding["recorded_relationship"], "different")

    def test_true_difference_with_only_invoice_cited_is_consistent_but_insufficient(self):
        self.cite(["EV-004"])
        finding = self.assert_outcomes(self.evaluate(), "matches_supplied_records",
                                       "required_sources_missing")
        self.assertEqual(finding["missing_citation_ids"], ["EV-005"])

    def test_true_difference_with_only_wire_cited_is_consistent_but_insufficient(self):
        self.cite(["EV-005"])
        finding = self.assert_outcomes(self.evaluate(), "matches_supplied_records",
                                       "required_sources_missing")
        self.assertEqual(finding["missing_citation_ids"], ["EV-004"])

    def test_unrelated_evidence_is_insufficient_even_when_it_exists(self):
        self.cite(["EV-003", "EV-006"])
        finding = self.assert_outcomes(self.evaluate(), "matches_supplied_records",
                                       "required_sources_missing")
        self.assertEqual(finding["missing_citation_ids"], ["EV-004", "EV-005"])

    def test_check_conclusion_cannot_replace_the_direct_sources(self):
        self.cite(["CHK-G04-02"], "verification_check")
        finding = self.assert_outcomes(self.evaluate(), "matches_supplied_records",
                                       "required_sources_missing")
        self.assertEqual(finding["missing_citation_ids"], ["EV-004", "EV-005"])

    def test_false_equality_conflicts_despite_complete_direct_source_coverage(self):
        self.candidate["factual_findings"][0]["statement"] = EQUAL
        self.assert_outcomes(self.evaluate("equal"), "conflicts_with_supplied_records",
                             "required_sources_cited")

    def test_changing_underlying_reference_changes_result_after_explicit_rebinding(self):
        self.assert_outcomes(self.evaluate(), "matches_supplied_records", "required_sources_cited")
        self.data["evidence"][4]["facts"]["beneficiary_account_ref"] = "SUPPLIER-ACC-A"
        finding = self.assert_outcomes(self.evaluate(), "conflicts_with_supplied_records",
                                       "required_sources_cited")
        self.assertEqual(finding["recorded_relationship"], "equal")
        self.candidate["factual_findings"][0]["statement"] = EQUAL
        self.assert_outcomes(self.evaluate("equal"), "matches_supplied_records",
                             "required_sources_cited")
        self.assertEqual(self.data["verification_checks"][1]["status"], "contradicted")

    def test_source_values_are_compared_exactly_without_normalization(self):
        self.data["evidence"][4]["facts"]["beneficiary_account_ref"] = " supplier-acc-a "
        self.assert_outcomes(self.evaluate(), "matches_supplied_records", "required_sources_cited")

    def test_both_sources_must_explicitly_reference_the_required_transaction(self):
        for indexes in ((3,), (4,), (3, 4)):
            with self.subTest(indexes=indexes):
                data = deepcopy(self.data)
                for index in indexes:
                    self.data["evidence"][index]["related_transaction_ids"] = ["TX-101"]
                report = self.evaluate()
                finding = self.assert_outcomes(report, "not_evaluated", "not_evaluated")
                self.assertEqual(report["validation"]["input_structure"]["status"], "passed")
                self.assertTrue(any(error["field_pointer"] == "/related_transaction_ids"
                                    for error in finding["diagnostics"]))
                self.data = data

    def test_wrong_evidence_types_are_ineligible_not_false_claims(self):
        for index in (3, 4):
            with self.subTest(index=index):
                original = self.data["evidence"][index]["evidence_type"]
                self.data["evidence"][index]["evidence_type"] = "unrelated_record"
                finding = self.assert_outcomes(self.evaluate(), "not_evaluated", "not_evaluated")
                self.assertTrue(any(error["field_pointer"] == "/evidence_type"
                                    for error in finding["diagnostics"]))
                self.data["evidence"][index]["evidence_type"] = original

    def test_missing_or_malformed_account_fields_cannot_match(self):
        for index in (3, 4):
            for value in (None, "", " \t", 12, True, [], {"value": "SUPPLIER-ACC-A"}):
                with self.subTest(index=index, value=value):
                    original = self.data["evidence"][index]["facts"]["beneficiary_account_ref"]
                    self.data["evidence"][index]["facts"]["beneficiary_account_ref"] = value
                    report = self.evaluate()
                    finding = self.assert_outcomes(report, "not_evaluated", "not_evaluated")
                    self.assertEqual(report["validation"]["input_structure"]["status"], "passed")
                    self.assertIsNone(finding["recorded_relationship"])
                    self.assertTrue(any(error["field_pointer"] == "/facts/beneficiary_account_ref"
                                        for error in finding["diagnostics"]))
                    self.data["evidence"][index]["facts"]["beneficiary_account_ref"] = original
            original = self.data["evidence"][index]["facts"].pop("beneficiary_account_ref")
            self.assert_outcomes(self.evaluate(), "not_evaluated", "not_evaluated")
            self.data["evidence"][index]["facts"]["beneficiary_account_ref"] = original

    def test_unannotated_findings_remain_unevaluated_with_explicit_coverage(self):
        self.candidate["factual_findings"].append({
            "statement": "A second, unannotated development statement.",
            "citations": [{"record_type": "evidence", "record_id": "EV-001"}],
        })
        report = self.evaluate()
        self.assert_outcomes(report, "matches_supplied_records", "required_sources_cited")
        self.assertEqual(report["findings"][1]["recorded_relationship_consistency"]["outcome"],
                         "not_evaluated")
        self.assertEqual(report["findings"][1]["submitted_direct_source_coverage"]["outcome"],
                         "not_evaluated")
        for dimension in ("recorded_relationship_consistency", "submitted_direct_source_coverage"):
            self.assertEqual(report["coverage"][dimension]["checked"], 1)
            self.assertEqual(report["coverage"][dimension]["not_evaluated"], 1)

    def test_stale_text_case_index_and_artifact_hashes_reject_the_bundle(self):
        for field, value in (
            ("case_id", "OTHER-CASE"), ("investigation_sha256", "0" * 64),
            ("candidate_sha256", "0" * 64), ("statement", DIFFERENT + " "), ("finding_index", 99),
        ):
            with self.subTest(field=field):
                investigation, candidate, annotations = self.packet()
                target = (
                    annotations["findings"][0]
                    if field in ("statement", "finding_index") else annotations
                )
                target[field] = value
                report = evaluate_evidence_relationships(
                    investigation, candidate, json_bytes(annotations),
                )
                self.assert_outcomes(report, "not_evaluated", "not_evaluated")
                self.assertEqual(report["validation"]["annotation_binding"]["status"], "failed")
                self.assertTrue(report["validation"]["annotation_binding"]["diagnostics"])

    def test_artifact_binding_rejects_reformatting_or_changed_citations(self):
        investigation, candidate, annotations = self.packet()
        reformatted = json.dumps(self.data, indent=2).encode("utf-8")
        self.assertNotEqual(investigation, reformatted)
        report = evaluate_evidence_relationships(reformatted, candidate, json_bytes(annotations))
        self.assertEqual(report["validation"]["annotation_binding"]["status"], "failed")
        self.cite(["EV-004"])
        report = evaluate_evidence_relationships(investigation, json_bytes(self.candidate),
                                                 json_bytes(annotations))
        self.assert_outcomes(report, "not_evaluated", "not_evaluated")

    def test_missing_malformed_and_incomplete_annotations_are_configuration_failures(self):
        investigation, candidate, annotations = self.packet()
        for payload in (None, b"", b"{", b"{}", b"[]", json_bytes({"schema_version": "1.0"})):
            with self.subTest(payload=payload):
                report = evaluate_evidence_relationships(investigation, candidate, payload)
                self.assert_outcomes(report, "not_evaluated", "not_evaluated")
                self.assertEqual(report["validation"]["annotation_structure"]["status"], "failed")
                self.assertEqual(report["validation"]["output_structure"]["status"], "passed")

    def test_annotation_fields_are_required_strict_and_versioned(self):
        investigation, candidate, original = self.packet()
        for field, value in (
            ("schema_version", "2.0"), ("schema_version", 1), ("review_status", "approved"),
            ("finding_index", True), ("finding_index", "0"), ("finding_index", -1),
            ("asserted_relationship", "fraud"), ("left_evidence_id", "EV-001"),
            ("right_evidence_id", "EV-004"), ("transaction_id", "TX-101"),
            ("candidate_sha256", "invalid"), ("statement", 7),
        ):
            with self.subTest(field=field, value=value):
                annotations = deepcopy(original)
                target = annotations if field in annotations else annotations["findings"][0]
                target[field] = value
                report = evaluate_evidence_relationships(
                    investigation, candidate, json_bytes(annotations),
                )
                self.assert_outcomes(report, "not_evaluated", "not_evaluated")
                self.assertEqual(report["validation"]["annotation_structure"]["status"], "failed")
        for nested in (False, True):
            source = original["findings"][0] if nested else original
            for field in source:
                with self.subTest(nested=nested, missing=field):
                    annotations = deepcopy(original)
                    (annotations["findings"][0] if nested else annotations).pop(field)
                    report = evaluate_evidence_relationships(investigation, candidate,
                                                             json_bytes(annotations))
                    self.assertEqual(report["validation"]["annotation_structure"]["status"],
                                     "failed")

    def test_extra_annotation_fields_and_duplicate_indexes_are_rejected(self):
        investigation, candidate, original = self.packet()
        for nested in (False, True):
            annotations = deepcopy(original)
            target = annotations["findings"][0] if nested else annotations
            target["unexpected"] = "PRIVATE-SENTINEL"
            report = evaluate_evidence_relationships(
                investigation, candidate, json_bytes(annotations),
            )
            self.assert_outcomes(report, "not_evaluated", "not_evaluated")
            self.assertNotIn("PRIVATE-SENTINEL", json.dumps(report))
        annotations = deepcopy(original)
        annotations["findings"].append(deepcopy(annotations["findings"][0]))
        report = evaluate_evidence_relationships(investigation, candidate, json_bytes(annotations))
        self.assertEqual(report["validation"]["annotation_structure"]["status"], "failed")

    def test_structural_and_contextual_failures_block_relationships(self):
        for failure in ("input_structure", "output_structure", "contextual_references"):
            with self.subTest(failure=failure):
                investigation, candidate, annotations = self.packet()
                if failure == "input_structure":
                    investigation = b"{}"
                elif failure == "output_structure":
                    candidate = b"{}"
                else:
                    changed = deepcopy(self.candidate)
                    changed["factual_findings"][0]["citations"][0]["record_id"] = "MISSING"
                    candidate = json_bytes(changed)
                    annotations = development_annotations(investigation, candidate)
                with patch("aml_triage.evidence_relation_checks._evaluate") as compare:
                    report = evaluate_evidence_relationships(
                        investigation, candidate, json_bytes(annotations),
                    )
                compare.assert_not_called()
                self.assertEqual(report["validation"][failure]["status"], "failed")
                if failure == "output_structure":
                    self.assertEqual(report["findings"], [])
                    self.assertIsNone(report["coverage"]["total_findings"])
                else:
                    self.assert_outcomes(report, "not_evaluated", "not_evaluated")

    def test_bindings_apply_atomically_not_partially(self):
        self.candidate["factual_findings"].append(deepcopy(self.candidate["factual_findings"][0]))
        investigation, candidate, annotations = self.packet()
        invalid = deepcopy(annotations["findings"][0])
        invalid.update(finding_index=1, statement="Stale annotation text")
        annotations["findings"].append(invalid)
        report = evaluate_evidence_relationships(investigation, candidate, json_bytes(annotations))
        self.assert_outcomes(report, "not_evaluated", "not_evaluated")
        self.assertEqual(report["coverage"]["recorded_relationship_consistency"]["checked"], 0)

    def test_proposition_is_supplied_explicitly_not_inferred_from_prose(self):
        self.candidate["factual_findings"][0]["statement"] = "Opaque development statement A."
        self.assert_outcomes(self.evaluate("equal"), "conflicts_with_supplied_records",
                             "required_sources_cited")

    def test_candidates_cannot_embed_evaluation_annotations(self):
        investigation, candidate, annotations = self.packet()
        self.candidate["evaluation_annotations"] = annotations
        report = evaluate_evidence_relationships(investigation, json_bytes(self.candidate),
                                                 json_bytes(annotations))
        self.assertEqual(report["validation"]["output_structure"]["status"], "failed")

    def test_citations_elsewhere_in_candidate_do_not_count_for_this_finding(self):
        complete = deepcopy(self.candidate["factual_findings"][0])
        self.cite(["EV-004"])
        self.candidate["rationale"] = complete
        self.candidate["factual_findings"].append(complete)
        finding = self.assert_outcomes(self.evaluate(), "matches_supplied_records",
                                       "required_sources_missing")
        self.assertEqual(finding["missing_citation_ids"], ["EV-005"])

    def test_dependencies_explain_fields_types_links_and_exact_values(self):
        finding = self.evaluate()["findings"][0]
        dependencies = {
            (item["record_type"], item["record_id"], item["field_pointer"]): item["value"]
            for item in finding["source_dependencies"]
        }
        self.assertEqual(len(dependencies), 7)
        self.assertEqual(dependencies[("transaction", "TX-105", "/transaction_id")], "TX-105")
        for identifier, expected_type, value in (
            ("EV-004", "supplier_invoice", "SUPPLIER-ACC-A"),
            ("EV-005", "wire_payment_record", "BENEFICIARY-ACC-B"),
        ):
            self.assertEqual(dependencies[("evidence", identifier, "/evidence_type")],
                             expected_type)
            self.assertEqual(dependencies[("evidence", identifier, "/related_transaction_ids")],
                             ["TX-105"])
            self.assertEqual(
                dependencies[("evidence", identifier, "/facts/beneficiary_account_ref")], value,
            )

    def test_no_policy_reference_llm_or_file_access_occurs(self):
        investigation, candidate, annotations = self.packet()
        with patch("builtins.open", side_effect=AssertionError("Unexpected read")), patch.object(
            Path, "open", side_effect=AssertionError("Unexpected file read")
        ):
            report = evaluate_evidence_relationships(
                investigation, candidate, json_bytes(annotations),
            )
        self.assert_outcomes(report, "matches_supplied_records", "required_sources_cited")

    def test_payloads_models_findings_citations_and_golden_input_are_not_mutated(self):
        original_file = INPUT.read_bytes()
        original_data, original_candidate = deepcopy(self.data), deepcopy(self.candidate)
        self.candidate["factual_findings"][0]["citations"].reverse()
        self.candidate["factual_findings"][0]["statement"] = "  Independently annotated text.\n"
        investigation, candidate, annotations = self.packet()
        before = (investigation, candidate, deepcopy(annotations))
        report = evaluate_evidence_relationships(investigation, candidate, json_bytes(annotations))
        self.assert_outcomes(report, "matches_supplied_records", "required_sources_cited")
        self.assertEqual((investigation, candidate, annotations), before)
        self.assertEqual(self.data, original_data)
        self.assertEqual(INPUT.read_bytes(), original_file)
        self.assertEqual(json.loads(candidate)["factual_findings"][0]["citations"],
                         list(reversed(original_candidate["factual_findings"][0]["citations"])))

    def test_existing_auditor_report_and_broad_semantic_dimensions_remain_unchanged(self):
        investigation, candidate, annotations = self.packet()
        before = audit_packet(investigation, candidate)
        evaluate_evidence_relationships(investigation, candidate, json_bytes(annotations))
        self.assertEqual(audit_packet(investigation, candidate), before)
        self.assertEqual(len(before["semantic_evaluation"]), 9)
        self.assertTrue(all(item["status"] == "not_evaluated"
                            for item in before["semantic_evaluation"].values()))
        self.assertEqual(before["report_schema_version"], "1.1")

    def test_unexpected_errors_are_not_reported_as_factual_conflicts(self):
        with patch("aml_triage.evidence_relation_checks._evaluate",
                   side_effect=RuntimeError("PRIVATE-SENTINEL")):
            report = self.evaluate()
        finding = self.assert_outcomes(report, "not_evaluated", "not_evaluated")
        self.assertEqual(finding["diagnostics"][0]["type"], "RuntimeError")
        self.assertNotIn("PRIVATE-SENTINEL", json.dumps(report))

    def test_empty_annotation_list_is_not_a_factual_verification(self):
        investigation, candidate, annotations = self.packet()
        annotations["findings"] = []
        report = evaluate_evidence_relationships(investigation, candidate, json_bytes(annotations))
        self.assert_outcomes(report, "not_evaluated", "not_evaluated")
        self.assertEqual(report["validation"]["annotation_binding"]["status"], "passed")

    def test_json_string_payloads_bind_to_their_exact_utf8_bytes(self):
        investigation, candidate, annotations = self.packet()
        report = evaluate_evidence_relationships(investigation.decode("utf-8"),
                                                 candidate.decode("utf-8"),
                                                 json_bytes(annotations).decode("utf-8"))
        self.assert_outcomes(report, "matches_supplied_records", "required_sources_cited")
        self.assertEqual(report["artifacts"]["candidate"]["sha256"], sha256(candidate).hexdigest())

    def test_missing_direct_source_cannot_be_an_eligible_pair(self):
        self.data["evidence"] = [record for record in self.data["evidence"]
                                 if record["evidence_id"] != "EV-005"]
        self.data["verification_checks"] = []
        self.cite(["EV-004"])
        report = self.evaluate()
        finding = self.assert_outcomes(report, "not_evaluated", "not_evaluated")
        self.assertEqual(report["validation"]["contextual_references"]["status"], "passed")
        self.assertTrue(any(error["record_id"] == "EV-005"
                            and error["field_pointer"] == "/evidence_id"
                            for error in finding["diagnostics"]))

    def test_required_transaction_must_exist_as_well_as_be_linked(self):
        self.data["transactions"] = [record for record in self.data["transactions"]
                                     if record["transaction_id"] != "TX-105"]
        for record in self.data["evidence"]:
            record["related_transaction_ids"] = [identifier for identifier in
                                                  record["related_transaction_ids"]
                                                  if identifier != "TX-105"]
        self.candidate["rationale"]["citations"][0]["record_id"] = "TX-101"
        report = self.evaluate()
        finding = self.assert_outcomes(report, "not_evaluated", "not_evaluated")
        self.assertEqual(report["validation"]["input_structure"]["status"], "passed")
        self.assertTrue(any(error["record_type"] == "transaction"
                            and error["record_id"] == "TX-105"
                            for error in finding["diagnostics"]))

    def test_same_textual_id_in_another_namespace_is_not_a_direct_evidence_citation(self):
        transaction = deepcopy(self.data["transactions"][-1])
        transaction["transaction_id"] = "EV-004"
        self.data["transactions"].append(transaction)
        self.cite(["EV-004"], "transaction")
        report = self.evaluate()
        finding = self.assert_outcomes(report, "matches_supplied_records",
                                       "required_sources_missing")
        self.assertEqual(report["validation"]["contextual_references"]["status"], "passed")
        self.assertEqual(finding["missing_citation_ids"], ["EV-004", "EV-005"])

    def test_empty_abstention_has_zero_checked_and_unchecked_findings(self):
        investigation, candidate, annotations = self.packet()
        self.candidate.update(assessment_status="unable_to_recommend", recommended_action=None,
                              factual_findings=[], rationale={"statement": "No recommendation.",
                                                            "citations": []})
        candidate = json_bytes(self.candidate)
        annotations.update(candidate_sha256=sha256(candidate).hexdigest(), findings=[])
        report = evaluate_evidence_relationships(investigation, candidate, json_bytes(annotations))
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["coverage"]["total_findings"], 0)
        for dimension in ("recorded_relationship_consistency", "submitted_direct_source_coverage"):
            self.assertEqual(report["coverage"][dimension]["checked"], 0)
            self.assertEqual(report["coverage"][dimension]["not_evaluated"], 0)


if __name__ == "__main__":
    unittest.main()
