"""Restricted field-comparison tests, independent of golden reference answers."""

import json
import unittest

from copy import deepcopy
from decimal import Decimal, localcontext
from pathlib import Path
from unittest.mock import patch

from aml_triage.contracts import InvestigationInput, InvestigationOutput
from aml_triage.transaction_amount_checks import check_transaction_amounts


INPUT = Path(__file__).resolve().parents[1] / "data" / "golden_cases" / "inputs" / "G02.json"


class TestTransactionAmountChecks(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(INPUT.read_bytes())
        self.investigation = InvestigationInput.model_validate(self.data)

    def output(self, statements, citations=None):
        if citations is None:
            citations = [{"record_type": "transaction", "record_id": "TX-G02-01"}]
        return InvestigationOutput.model_validate({
            "schema_version": "1.0",
            "case_id": self.investigation.case.case_id,
            "alert_id": self.investigation.alert.alert_id,
            "assessment_status": "recommendation_provided" if statements else "unable_to_recommend",
            "recommended_action": "investigate" if statements else None,
            "rationale": {"statement": "Independent candidate for restricted comparisons.",
                          "citations": deepcopy(citations)},
            "factual_findings": [{"statement": text, "citations": deepcopy(citations)}
                                 for text in statements],
            "interpretations": [], "unresolved_questions": [], "missing_information": [],
            "contradictions": [], "recommendation_scope": "preliminary",
            "human_review_required": True,
        })

    def check(self, statement, citations=None, investigation=None):
        report = check_transaction_amounts(
            self.investigation if investigation is None else investigation,
            self.output([statement], citations),
        )
        self.assertEqual(json.loads(json.dumps(report, allow_nan=False)), report)
        return report

    def assert_unchecked(self, statement, citations=None):
        report = self.check(statement, citations)
        self.assertEqual(report["status"], "not_evaluated")
        self.assertEqual(report["coverage"], {
            "total_findings": 1, "checked": 0, "matches_record": 0,
            "conflicts_with_record": 0, "not_checked": 1,
        })
        result = report["findings"][0]
        self.assertEqual(result["outcome"], "not_checked")
        self.assertTrue(result["reason"])
        self.assertEqual(result["comparisons"], [])
        self.assertIsNone(result["transaction_id"])
        self.assertIsNone(result["citation_path"])
        return result

    def test_correct_incoming_amount_currency_and_credit_direction(self):
        report = self.check("The incoming transaction was USD 48,500.00.")
        self.assertEqual(report["status"], "passed")
        result = report["findings"][0]
        self.assertEqual(result["outcome"], "matches_record")
        self.assertEqual(result["predicate"], "incoming_transaction_amount")
        self.assertEqual(result["transaction_id"], "TX-G02-01")
        self.assertEqual(result["citation_path"], "factual_findings[0].citations[0]")
        self.assertEqual([item["field"] for item in result["comparisons"]],
                         ["amount", "currency", "direction"])
        self.assertTrue(all(item["matches"] for item in result["comparisons"]))

    def test_false_g02_amount_conflicts_with_exact_decimal_record_value(self):
        report = self.check("The incoming transaction was USD 99,999.00.")
        self.assertEqual(report["status"], "failed")
        result = report["findings"][0]
        self.assertEqual(result["outcome"], "conflicts_with_record")
        self.assertEqual(result["comparisons"][0], {
            "field": "amount", "claimed": "99999.00", "recorded": "48500.00", "matches": False,
            "source": {"record_type": "transaction", "record_id": "TX-G02-01",
                       "field_pointer": "/amount"},
        })
        self.assertTrue(all(item["matches"] for item in result["comparisons"][1:]))

    def test_wrong_currency_is_a_separate_field_conflict(self):
        result = self.check("The incoming transaction was EUR 48,500.00.")["findings"][0]
        self.assertEqual(result["outcome"], "conflicts_with_record")
        self.assertEqual([item["field"] for item in result["comparisons"] if not item["matches"]],
                         ["currency"])

    def test_incoming_claim_conflicts_with_debit_direction(self):
        self.data["transactions"][0]["direction"] = "debit"
        investigation = InvestigationInput.model_validate(self.data)
        result = self.check("The incoming transaction was USD 48,500.00.",
                            investigation=investigation)["findings"][0]
        self.assertEqual(result["outcome"], "conflicts_with_record")
        self.assertEqual(result["comparisons"][2]["claimed"], "credit")
        self.assertEqual(result["comparisons"][2]["recorded"], "debit")
        self.assertEqual([item["field"] for item in result["comparisons"] if not item["matches"]],
                         ["direction"])

    def test_correct_amount_with_different_transaction_citation_conflicts(self):
        result = self.check("The incoming transaction was USD 48,500.00.", [
            {"record_type": "transaction", "record_id": "TX-G02-02"},
        ])["findings"][0]
        self.assertEqual(result["transaction_id"], "TX-G02-02")
        self.assertEqual(result["outcome"], "conflicts_with_record")
        self.assertEqual(result["comparisons"][0]["recorded"], "1200.00")

    def test_multiple_transaction_citations_are_not_arbitrarily_resolved(self):
        result = self.assert_unchecked("The incoming transaction was USD 48,500.00.", [
            {"record_type": "transaction", "record_id": "TX-G02-02"},
            {"record_type": "transaction", "record_id": "TX-G02-01"},
        ])
        self.assertIn("Exactly one transaction citation", result["reason"])

    def test_evidence_citation_does_not_substitute_for_transaction_citation(self):
        self.assert_unchecked("The incoming transaction was USD 48,500.00.", [
            {"record_type": "evidence", "record_id": "EV-G02-01"},
        ])

    def test_other_citation_namespaces_do_not_change_the_selected_transaction(self):
        result = self.check("The incoming transaction was USD 48,500.00.", [
            {"record_type": "evidence", "record_id": "EV-G02-01"},
            {"record_type": "transaction", "record_id": "TX-G02-01"},
        ])["findings"][0]
        self.assertEqual(result["outcome"], "matches_record")
        self.assertEqual(result["citation_path"], "factual_findings[0].citations[1]")

    def test_explicit_record_form_matches_exact_id(self):
        result = self.check("Transaction TX-G02-01 amount was USD 48,500.00.")["findings"][0]
        self.assertEqual(result["outcome"], "matches_record")
        self.assertEqual(result["predicate"], "explicit_transaction_amount")
        self.assertEqual([item["field"] for item in result["comparisons"]], ["amount", "currency"])

    def test_explicit_mentioned_and_cited_id_mismatch_is_not_checked(self):
        for mentioned in ("TX-G02-02", "tx-g02-01", "TX-G02-010"):
            with self.subTest(mentioned=mentioned):
                result = self.assert_unchecked(f"Transaction {mentioned} amount was USD 48,500.00.")
                self.assertIn(repr(mentioned), result["reason"])
                self.assertIn("'TX-G02-01'", result["reason"])

    def test_explicit_record_form_does_not_invent_incoming_direction(self):
        self.data["transactions"][0]["direction"] = "debit"
        result = self.check(
            "Transaction TX-G02-01 amount was USD 48,500.00.",
            investigation=InvestigationInput.model_validate(self.data),
        )["findings"][0]
        self.assertEqual(result["outcome"], "matches_record")
        self.assertEqual([item["field"] for item in result["comparisons"]], ["amount", "currency"])

    def test_unresolved_transaction_is_not_checked_in_standalone_use(self):
        result = self.assert_unchecked("The incoming transaction was USD 48,500.00.", [
            {"record_type": "transaction", "record_id": "NOT-SUPPLIED"},
        ])
        self.assertIn("not supplied", result["reason"])

    def test_unrecognized_compound_quoted_or_padded_text_is_not_checked(self):
        for text in (
            "A transfer of USD 48,500.00 was recorded.",
            "The incoming transaction was USD 48,500.00. This resolves the concern.",
            "The incoming transaction was USD 48,500.00 and was legitimate.",
            '"The incoming transaction was USD 48,500.00."',
            " The incoming transaction was USD 48,500.00.",
            "The incoming transaction was USD 48,500.00. ",
            "The incoming transaction was USD 48,500.00.\n",
            "the incoming transaction was USD 48,500.00.",
            "The incoming transaction was USD\u00a048,500.00.",
            "Transaction TX.G02.01 amount was USD 48,500.00.",
        ):
            with self.subTest(text=text):
                self.assert_unchecked(text)

    def test_negations_are_not_positive_assertions(self):
        for text in (
            "The incoming transaction was not USD 48,500.00.",
            "It is false that the incoming transaction was USD 48,500.00.",
            "Transaction TX-G02-01 amount was not USD 48,500.00.",
        ):
            with self.subTest(text=text):
                self.assert_unchecked(text)

    def test_customer_attributions_are_not_treated_as_transaction_facts(self):
        for text in (
            "The customer said the incoming transaction was USD 48,500.00.",
            "According to the customer, the incoming transaction was USD 48,500.00.",
            "The incoming transaction was USD 48,500.00, according to the customer.",
        ):
            with self.subTest(text=text):
                self.assert_unchecked(text)

    def test_questions_and_hypotheticals_are_not_direct_assertions(self):
        for text in (
            "Was the incoming transaction USD 48,500.00?",
            "The incoming transaction was USD 48,500.00?",
            "If the incoming transaction was USD 48,500.00.",
            "Suppose the incoming transaction was USD 48,500.00.",
            "The incoming transaction might have been USD 48,500.00.",
        ):
            with self.subTest(text=text):
                self.assert_unchecked(text)

    def test_grouped_ungrouped_and_cent_values_use_decimal_comparisons(self):
        for claimed, recorded in (
            ("48,500.00", "48500.00"), ("48500.00", "48500"),
            ("0.10", "0.10"), ("0.30", "0.30"), ("1,234,567.89", "1234567.89"),
        ):
            with self.subTest(claimed=claimed, recorded=recorded):
                self.data["transactions"][0]["amount"] = recorded
                investigation = InvestigationInput.model_validate(self.data)
                result = self.check(f"The incoming transaction was USD {claimed}.",
                                    investigation=investigation)["findings"][0]
                self.assertIsInstance(investigation.transactions[0].amount, Decimal)
                self.assertEqual(result["outcome"], "matches_record")
                self.assertIsInstance(result["comparisons"][0]["claimed"], str)

    def test_cent_conflict_beyond_binary_float_precision_is_preserved(self):
        self.data["transactions"][0]["amount"] = "9007199254740992.01"
        investigation = InvestigationInput.model_validate(self.data)
        with localcontext() as context:
            context.prec = 4
            result = self.check("The incoming transaction was USD 9,007,199,254,740,992.02.",
                                investigation=investigation)["findings"][0]
        self.assertEqual(result["outcome"], "conflicts_with_record")
        self.assertEqual(result["comparisons"][0]["claimed"], "9007199254740992.02")
        self.assertEqual(result["comparisons"][0]["recorded"], "9007199254740992.01")

    def test_malformed_or_unsupported_number_formats_are_not_checked(self):
        for number in (
            "48,50.00", "48,,500.00", "048500.00", "0,000.00", "48500", "48500.0",
            "48500.000", "48.500,00", "48 500.00", "+48500.00", "-48500.00",
            "4.85e4", "NaN", "Infinity", "48_500.00", ".50", "48500.",
            "\uff14\uff18\uff15\uff10\uff10.00",
        ):
            with self.subTest(number=number):
                self.assert_unchecked(f"The incoming transaction was USD {number}.")

    def test_recognized_zero_claim_conflicts_instead_of_being_ignored(self):
        result = self.check("The incoming transaction was USD 0.00.")["findings"][0]
        self.assertEqual(result["outcome"], "conflicts_with_record")

    def test_source_pointers_are_relative_to_exact_typed_record(self):
        result = self.check("The incoming transaction was USD 48,500.00.")["findings"][0]
        transaction = self.investigation.transactions[0]
        for item in result["comparisons"]:
            self.assertEqual(item["source"], {
                "record_type": "transaction", "record_id": transaction.transaction_id,
                "field_pointer": "/" + item["field"],
            })
            self.assertEqual(str(getattr(transaction, item["source"]["field_pointer"][1:])),
                             item["recorded"])

    def test_mixed_coverage_keeps_order_and_unchecked_findings(self):
        output = self.output([
            "The incoming transaction was USD 48,500.00.",
            "The incoming transaction was USD 99,999.00.", "Unrecognized claim.",
        ])
        report = check_transaction_amounts(self.investigation, output)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["coverage"], {
            "total_findings": 3, "checked": 2, "matches_record": 1,
            "conflicts_with_record": 1, "not_checked": 1,
        })
        self.assertEqual([item["finding_path"] for item in report["findings"]],
                         ["factual_findings[0]", "factual_findings[1]", "factual_findings[2]"])

    def test_empty_findings_do_not_imply_complete_factual_verification(self):
        report = check_transaction_amounts(self.investigation, self.output([]))
        self.assertEqual(report["status"], "not_evaluated")
        self.assertEqual(report["coverage"], {
            "total_findings": 0, "checked": 0, "matches_record": 0,
            "conflicts_with_record": 0, "not_checked": 0,
        })
        self.assertEqual(report["findings"], [])

    def test_models_text_order_and_nested_objects_are_not_mutated(self):
        output = self.output([
            "The incoming transaction was USD 99,999.00.", "  Unrecognized candidate text.\n",
        ])
        before = (self.investigation.model_dump(), output.model_dump())
        original_finding = output.factual_findings[0]
        original_citation = original_finding.citations[0]
        original_transaction = self.investigation.transactions[0]
        check_transaction_amounts(self.investigation, output)
        self.assertEqual((self.investigation.model_dump(), output.model_dump()), before)
        self.assertIs(output.factual_findings[0], original_finding)
        self.assertIs(output.factual_findings[0].citations[0], original_citation)
        self.assertIs(self.investigation.transactions[0], original_transaction)

    def test_recognized_checks_do_not_read_files_or_policy(self):
        output = self.output(["The incoming transaction was USD 48,500.00."])
        with patch("builtins.open", side_effect=AssertionError("Unexpected read")), patch.object(
            Path, "open", side_effect=AssertionError("Unexpected read")
        ):
            report = check_transaction_amounts(self.investigation, output)
        self.assertEqual(report["findings"][0]["outcome"], "matches_record")


if __name__ == "__main__":
    unittest.main()
