"""Fixed-rule development regressions, not accuracy against provisional labels."""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from decimal import Decimal, localcontext
import io
import json
from pathlib import Path
import runpy
import socket
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from aml_triage.auditor import audit_packet
from aml_triage.contracts import (
    InvestigationInput, InvestigationOutput, validate_investigation_output_references,
)
from aml_triage.deterministic_baseline import assess_investigation


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "data" / "golden_cases" / "inputs"
DEVELOPMENT = ROOT / "data" / "generated" / "development"
SCRIPT = ROOT / "scripts" / "run_baseline.py"


def read_case(tag="G03"):
    return json.loads((GOLDEN / f"{tag}.json").read_bytes())


def generated(index):
    return json.loads((DEVELOPMENT / f"CASE-DEV-S20261027-{index:04d}.json").read_bytes())


def assess(data):
    return assess_investigation(InvestigationInput.model_validate(data))


def facts(output):
    return "\n".join(item.statement for item in output.factual_findings)


def questions(output):
    return "\n".join(item.statement for item in output.unresolved_questions)


class TestDeterministicBaseline(unittest.TestCase):
    def test_all_existing_development_inputs_produce_valid_resolved_outputs(self):
        paths = [GOLDEN / f"G{index:02d}.json" for index in range(1, 6)]
        paths += sorted(DEVELOPMENT.glob("CASE-*.json"))
        self.assertEqual(len(paths), 55)
        for path in paths:
            with self.subTest(path=path.name):
                model = InvestigationInput.model_validate_json(path.read_bytes())
                output = assess_investigation(model)
                parsed = InvestigationOutput.model_validate_json(output.model_dump_json())
                self.assertEqual(parsed, output)
                self.assertIs(validate_investigation_output_references(model, output), output)
                self.assertEqual(output.recommendation_scope, "preliminary")
                self.assertIs(output.human_review_required, True)
                self.assertNotEqual(output.recommended_action, "close")

    def test_identical_input_is_deterministic_and_never_mutated(self):
        model = InvestigationInput.model_validate(read_case())
        before = deepcopy(model.model_dump())
        first = assess_investigation(model)
        self.assertEqual(first.model_dump_json(), assess_investigation(model).model_dump_json())
        self.assertEqual(model.model_dump(), before)

    def test_public_interface_requires_a_validated_input(self):
        with self.assertRaises(TypeError):
            assess_investigation(read_case())

    def test_contextual_validator_is_called_before_return(self):
        model = InvestigationInput.model_validate(read_case())
        with patch("aml_triage.deterministic_baseline.validate_investigation_output_references",
                   wraps=validate_investigation_output_references) as validator:
            output = assess_investigation(model)
        validator.assert_called_once_with(model, output)

    def test_explicit_missing_beneficiary_and_purpose_are_material_scoped_gaps(self):
        output = assess(generated(9))
        self.assertEqual(output.recommended_action, "investigate")
        self.assertIn("beneficiary account", questions(output))
        self.assertIn("commercial-purpose", questions(output))
        self.assertTrue(output.missing_information)
        self.assertTrue(all(item.citations for item in output.unresolved_questions))
        self.assertIn("supplied review scope", questions(output))

    def test_null_counterparty_alone_is_not_treated_as_a_missing_payee_account(self):
        data = read_case()
        for record in data["transactions"]:
            record["counterparty_id"] = None
        output = assess(data)
        self.assertEqual(output.recommended_action, "escalate")
        self.assertNotIn("[MI-01]", questions(output))

    def test_missing_customer_support_is_scoped_to_linked_documents(self):
        data = read_case("G02")
        data["evidence"].append({
            "evidence_id": "OTHER-INVOICE", "evidence_type": "supplier_invoice",
            "source": "customer_supplied", "verification_status": "recorded",
            "related_transaction_ids": [data["transactions"][1]["transaction_id"]],
            "facts": {"invoice_total": "1200.00", "currency": "USD"},
        })
        output = assess(data)
        self.assertEqual(output.recommended_action, "investigate")
        self.assertIn("[MI-02]", questions(output))
        self.assertIn("records the claim", facts(output))

    def test_linked_invoice_does_not_automatically_prove_purpose_or_allow_closure(self):
        output = assess(generated(1))
        self.assertEqual(output.assessment_status, "unable_to_recommend")
        self.assertIsNone(output.recommended_action)
        self.assertIn("claimed", questions(assess(read_case("G02"))))

    def test_beneficiary_difference_has_both_direct_sources_and_no_fraud_inference(self):
        data = generated(15)
        output = assess(data)
        self.assertEqual(output.recommended_action, "investigate")
        finding = next(item for item in output.factual_findings if "[BEN-01]" in item.statement)
        ids = {citation.record_id for citation in finding.citations
               if citation.record_type == "evidence"}
        self.assertEqual(ids, {data["evidence"][1]["evidence_id"],
                               data["evidence"][2]["evidence_id"]})
        self.assertEqual(len(output.contradictions), 1)
        self.assertIn("neither fraud nor an unauthorized payment", questions(output))

    def test_equal_beneficiary_references_abstain_without_commercial_certification(self):
        data = generated(15)
        reference = data["evidence"][1]["facts"]["beneficiary_account_ref"]
        data["evidence"][2]["facts"]["beneficiary_account_ref"] = reference
        output = assess(data)
        self.assertIn("are equal", facts(output))
        self.assertEqual(output.contradictions, [])
        self.assertIsNone(output.recommended_action)

    def test_missing_or_malformed_beneficiary_is_unknown_not_a_proven_conflict(self):
        for value in (None, "", "  ", 7, {"account": "A"}):
            with self.subTest(value=value):
                data = generated(15)
                data["evidence"][1]["facts"]["beneficiary_account_ref"] = value
                output = assess(data)
                self.assertEqual(output.recommended_action, "investigate")
                self.assertIn("[BEN-02]", questions(output))
                self.assertEqual(output.contradictions, [])

    def test_unrelated_invoice_is_not_paired_with_a_wire(self):
        data = generated(15)
        data["evidence"][1]["related_transaction_ids"] = []
        output = assess(data)
        self.assertNotIn("[BEN-01]", facts(output))
        self.assertEqual(output.contradictions, [])

    def test_supplied_transactions_outside_alert_subset_are_analyzed(self):
        output = assess(read_case("G04"))
        finding = next(item for item in output.factual_findings if "[BEN-01]" in item.statement)
        self.assertTrue(any(item.record_id == "TX-105" for item in finding.citations))
        self.assertEqual(output.recommended_action, "investigate")

    def test_original_cash_sum_and_individual_range_findings_cite_profile(self):
        output = assess(read_case("G01"))
        self.assertIn("sum to 34,150.00", facts(output))
        comparisons = [item for item in output.factual_findings if "[CASH-02]" in item.statement]
        self.assertEqual(len(comparisons), 4)
        for item in comparisons:
            self.assertIn("is above", item.statement)
            self.assertIn("customer", {citation.record_type for citation in item.citations})
        self.assertIsNone(output.recommended_action)
        self.assertIn("closure corroboration remains under review", output.rationale.statement)

    def test_multi_day_total_is_not_compared_to_a_daily_bound(self):
        data = read_case("G01")
        for record in data["transactions"]:
            record["amount"] = "2000.00"
        data["evidence"][1]["facts"].update(daily_sales=["2000.00"] * 4, summary_total="8000.00")
        data["evidence"][2]["facts"]["reconciled_deposits"] = "8000.00"
        output = assess(data)
        self.assertIn("sum to 8,000.00", facts(output))
        comparisons = [item.statement for item in output.factual_findings
                       if "[CASH-02]" in item.statement]
        self.assertTrue(all("is within" in statement for statement in comparisons))
        self.assertIsNone(output.recommended_action)

    def test_cash_groups_currencies_and_skips_incomparable_daily_ranges(self):
        data = read_case("G01")
        data["transactions"][0]["currency"] = "EUR"
        output = assess(data)
        self.assertIn("deposits in EUR sum to 8,150.00", facts(output))
        self.assertIn("deposits in USD sum to 26,000.00", facts(output))
        comparisons = [item.statement for item in output.factual_findings
                       if "[CASH-02]" in item.statement]
        self.assertTrue(all("EUR" not in statement for statement in comparisons))

    def test_absent_daily_range_does_not_create_a_threshold(self):
        data = read_case("G01")
        data["customer"]["expected_monthly_activity"].pop("typical_daily_cash_deposit_min")
        data["customer"]["expected_monthly_activity"].pop("typical_daily_cash_deposit_max")
        self.assertNotIn("[CASH-02]", facts(assess(data)))

    def test_unflagged_context_transactions_do_not_create_universal_document_requirements(self):
        data = generated(8)
        for kind in ("cash_deposit", "domestic_transfer"):
            record = deepcopy(data["transactions"][0])
            record.update(transaction_id=f"CONTEXT-{kind}", transaction_type=kind,
                          direction="credit" if kind == "cash_deposit" else "debit",
                          counterparty_id=None, amount="100.00")
            data["transactions"].append(record)
        output = assess(data)
        self.assertIsNone(output.recommended_action)
        self.assertNotIn("[CASH-03]", questions(output))

    def test_partial_sales_and_explicit_unmatched_amount_require_investigation(self):
        output = assess(generated(7))
        self.assertEqual(output.recommended_action, "investigate")
        self.assertIn("unmatched_amount", facts(output))
        self.assertIn("remaining cash deposits", questions(output))

    def test_missing_reconciliation_is_not_treated_as_zero_unmatched(self):
        data = read_case("G01")
        data["evidence"] = [record for record in data["evidence"]
                            if record["evidence_type"] != "deposit_reconciliation"]
        data["verification_checks"] = []
        output = assess(data)
        self.assertEqual(output.recommended_action, "investigate")
        self.assertIn("No complete, currency-comparable numeric reconciliation", questions(output))
        self.assertNotIn("unmatched_amount USD 0.00", facts(output))

    def test_invalid_reconciliation_and_conflicting_pos_totals_do_not_resolve_gaps(self):
        for value in (None, "NaN", "invalid", "0.001", True, -1):
            with self.subTest(value=value):
                data = read_case("G01")
                data["evidence"][2]["facts"]["unmatched_amount"] = value
                self.assertEqual(assess(data).recommended_action, "investigate")
        data = read_case("G01")
        data["evidence"][1]["facts"]["summary_total"] = "1.00"
        self.assertIn("POS numeric summary", questions(assess(data)))

    def test_decimal_arithmetic_survives_changed_ambient_precision(self):
        model = InvestigationInput.model_validate(read_case("G01"))
        with localcontext() as context:
            context.prec = 2
            output = assess_investigation(model)
        self.assertIn("sum to 34,150.00", facts(output))

    def test_referral_original_and_generated_positive_depend_on_underlying_records(self):
        for data in (read_case(), generated(3)):
            with self.subTest(case=data["case"]["case_id"]):
                data["verification_checks"] = []
                output = assess(data)
                self.assertEqual(output.recommended_action, "escalate")
                self.assertIn("[REF-01]", output.rationale.statement)
                self.assertTrue(any("registers list" in item.statement
                                    for item in output.factual_findings))

    def test_referral_does_not_follow_recorded_status_or_findings(self):
        data = read_case()
        before = assess(data)
        for check in data["verification_checks"]:
            check.update(status="close", findings=["This text is not decision evidence."])
        self.assertEqual(assess(data), before)

    def test_insufficient_same_account_transfers_do_not_establish_referral(self):
        data = read_case()
        data["transactions"][1]["occurred_at"] = "2026-10-11T09:00:00Z"
        output = assess(data)
        self.assertNotEqual(output.recommended_action, "escalate")
        self.assertIn("Fewer than two", " ".join(item.statement for item in output.interpretations))

    def test_single_supplied_transfer_does_not_establish_referral(self):
        data = read_case()
        removed = data["transactions"].pop()["transaction_id"]
        data["alert"]["transaction_ids"].remove(removed)
        for record in data["evidence"]:
            record["related_transaction_ids"].remove(removed)
        data["evidence"][2]["facts"]["total_amount"] = data["transactions"][0]["amount"]
        self.assertIsNone(assess(data).recommended_action)

    def test_all_pre_instruction_payments_do_not_establish_referral(self):
        data = read_case()
        data["evidence"][1]["facts"]["issued_at"] = "2026-10-15T14:00:00Z"
        self.assertIsNone(assess(data).recommended_action)

    def test_equal_instruction_time_is_not_after_and_offsets_are_compared_as_instants(self):
        data = read_case()
        data["evidence"][1]["facts"]["issued_at"] = "2026-10-13T05:00:00-04:00"
        self.assertNotEqual(assess(data).recommended_action, "escalate")

    def test_same_supplier_different_payee_accounts_do_not_establish_referral(self):
        data = generated(3)
        data["evidence"][3]["facts"]["payments"][1]["payee_account_ref"] = "DIFFERENT-ACCOUNT"
        self.assertIsNone(assess(data).recommended_action)

    def test_authorized_change_prevents_referral_without_universal_fallback(self):
        output = assess(generated(8))
        self.assertIsNone(output.recommended_action)
        self.assertEqual(output.assessment_status, "unable_to_recommend")
        self.assertIn("authorized_change_recorded=True", facts(output))

    def test_missing_register_instruction_or_ledger_blocks_referral_with_question(self):
        for kind in ("supplier_authorization_register", "supplier_instruction_notice",
                     "payment_record"):
            with self.subTest(kind=kind):
                data = read_case()
                data["evidence"] = [record for record in data["evidence"]
                                    if record["evidence_type"] != kind]
                data["verification_checks"] = []
                output = assess(data)
                self.assertNotEqual(output.recommended_action, "escalate")
                self.assertIn("[REF-01]", questions(output))

    def test_naive_or_malformed_instruction_timestamp_blocks_referral(self):
        for value in (None, "not-a-date", "2026-10-12T14:00:00"):
            with self.subTest(value=value):
                data = read_case()
                data["evidence"][1]["facts"]["issued_at"] = value
                self.assertNotEqual(assess(data).recommended_action, "escalate")

    def test_instruction_account_and_exact_review_requirement_are_required(self):
        for changes in ({"instruction": "Consider looking at payments"},
                        {"review_required_account_ref": "OTHER-ACCOUNT"}):
            with self.subTest(changes=changes):
                data = read_case()
                data["evidence"][1]["facts"].update(changes)
                self.assertNotEqual(assess(data).recommended_action, "escalate")

    def test_unrecognized_register_provenance_and_unknown_change_status_block_referral(self):
        for field, value in (("source", "customer_supplied"), ("authorized_change_recorded", None)):
            with self.subTest(field=field):
                data = read_case()
                target = data["evidence"][0] if field == "source" else data["evidence"][0]["facts"]
                target[field] = value
                self.assertNotEqual(assess(data).recommended_action, "escalate")

    def test_senior_review_entry_is_not_an_added_exception_or_bypass_allegation(self):
        data = read_case()
        data["evidence"].append({
            "evidence_id": "REVIEW-ENTRY", "evidence_type": "senior_review_entry",
            "source": "synthetic_internal_case_log", "verification_status": "recorded",
            "related_transaction_ids": data["alert"]["transaction_ids"].copy(),
            "facts": {"recorded_at": "2026-10-12T15:00:00Z",
                      "reviewed_account_ref": "ACCT-G03-UNAPPROVED"},
        })
        output = assess(data)
        self.assertEqual(output.recommended_action, "escalate")
        self.assertIn("bypass and independent authenticity have not been established",
                      output.rationale.statement)

    def test_conflicting_ledger_mapping_and_register_approval_block_certainty(self):
        for kind in ("ledger", "register"):
            with self.subTest(kind=kind):
                data = read_case()
                extra = deepcopy(data["evidence"][2 if kind == "ledger" else 0])
                extra["evidence_id"] = "CONFLICTING-RECORD"
                if kind == "ledger":
                    extra["facts"]["payee_account_ref"] = "OTHER-ACCOUNT"
                else:
                    extra["facts"]["approved_payee_account_ref"] = "ACCT-G03-UNAPPROVED"
                data["evidence"].append(extra)
                self.assertNotEqual(assess(data).recommended_action, "escalate")

    def test_mixed_legacy_and_row_or_register_formats_cannot_hide_conflicts(self):
        data = generated(3)
        data["evidence"][3]["facts"]["payee_account_ref"] = "CONFLICTING-AGGREGATE"
        self.assertNotEqual(assess(data).recommended_action, "escalate")
        data = read_case()
        data["evidence"][0]["facts"]["approved_payee_account_refs"] = ["DIFFERENT-ACCOUNT"]
        output = assess(data)
        self.assertNotEqual(output.recommended_action, "escalate")
        self.assertIn("[REF-01]", questions(output))

    def test_conflicting_registers_preserve_a_material_question(self):
        data = read_case()
        extra = deepcopy(data["evidence"][0])
        extra["evidence_id"] = "OTHER-REGISTER"
        extra["facts"]["approved_payee_account_ref"] = "ACCT-G03-UNAPPROVED"
        data["evidence"].append(extra)
        output = assess(data)
        self.assertEqual(output.recommended_action, "investigate")
        self.assertIn("differing supplied register", questions(output))

    def test_payment_row_amount_currency_time_and_duplicate_rows_are_checked(self):
        for field, value in (("amount", "1.00"), ("currency", "EUR"),
                             ("occurred_at", "2020-01-01T00:00:00Z"), ("duplicate", None)):
            with self.subTest(field=field):
                data = generated(3)
                rows = data["evidence"][3]["facts"]["payments"]
                if field == "currency":
                    value = "USD" if rows[0]["currency"] != "USD" else "EUR"
                if field == "duplicate":
                    rows.append(deepcopy(rows[0]))
                else:
                    rows[0][field] = value
                self.assertNotEqual(assess(data).recommended_action, "escalate")

    def test_unknown_policy_abstains_even_with_a_supported_record_pattern(self):
        data = read_case()
        data["case"]["policy_id"] = "UNSUPPORTED-POLICY"
        self.assertIsNone(assess(data).recommended_action)

    def test_record_renaming_and_irrelevant_alert_rule_do_not_choose_the_action(self):
        data = read_case()
        collections = (
            ("accounts", "account_id"), ("transactions", "transaction_id"),
            ("evidence", "evidence_id"), ("verification_checks", "check_id"),
            ("counterparties", "counterparty_id"),
        )
        names = {record[key]: f"RENAMED-{position}-{index}"
                 for position, (collection, key) in enumerate(collections)
                 for index, record in enumerate(data[collection])}
        names.update({data["case"]["case_id"]: "ANOTHER-CASE",
                      data["alert"]["alert_id"]: "ANOTHER-ALERT",
                      data["customer"]["customer_id"]: "ANOTHER-CUSTOMER"})
        def rename(value):
            if isinstance(value, dict):
                return {key: rename(nested) for key, nested in value.items()}
            if isinstance(value, list):
                return [rename(nested) for nested in value]
            return names.get(value, value) if isinstance(value, str) else value
        data = rename(data)
        data["alert"]["rule_id"] = "ARBITRARY-ALERT-NAME"
        self.assertEqual(assess(data).recommended_action, "escalate")

    def test_assessment_has_no_file_network_manifest_reference_or_policy_access(self):
        model = InvestigationInput.model_validate(read_case())
        with patch("builtins.open", side_effect=AssertionError("File read")), patch.object(
            Path, "open", side_effect=AssertionError("Path read")
        ), patch.object(socket, "socket", side_effect=AssertionError("Network")):
            self.assertEqual(assess_investigation(model).recommended_action, "escalate")

    def test_output_is_a_candidate_for_existing_auditor_without_changing_evaluator_scope(self):
        raw = (GOLDEN / "G03.json").read_bytes()
        output = assess_investigation(InvestigationInput.model_validate_json(raw))
        report = audit_packet(raw, output.model_dump_json().encode())
        self.assertTrue(all(stage["status"] == "passed" for stage in report["stages"].values()))
        self.assertTrue(all(stage["status"] == "not_evaluated"
                            for stage in report["semantic_evaluation"].values()))


class TestReferralWireReconciliation(unittest.TestCase):
    """Direct bank-side counterfactuals; wire records cannot establish a mapping."""

    def with_wire(self, data, account=None, source="synthetic_bank_ledger"):
        ledger = next(record for record in data["evidence"]
                      if record["evidence_type"] == "payment_record")
        account = account if account is not None else (
            ledger["facts"].get("payee_account_ref")
            or ledger["facts"]["payments"][0]["payee_account_ref"]
        )
        transaction = data["transactions"][0]
        wire = {
            "evidence_id": "COUNTERFACTUAL-WIRE", "evidence_type": "wire_payment_record",
            "source": source, "verification_status": "recorded",
            "related_transaction_ids": [transaction["transaction_id"]],
            "facts": {"beneficiary_account_ref": account, "wire_amount": transaction["amount"],
                      "currency": transaction["currency"]},
        }
        data["evidence"].append(wire)
        return wire, ledger

    def validated_assessment(self, data):
        model = InvestigationInput.model_validate_json(json.dumps(data))
        output = assess_investigation(model)
        self.assertEqual(InvestigationOutput.model_validate_json(output.model_dump_json()), output)
        self.assertIs(validate_investigation_output_references(model, output), output)
        self.assertEqual(output.recommendation_scope, "preliminary")
        self.assertIs(output.human_review_required, True)
        return output

    def test_original_aggregate_and_row_ledgers_still_escalate(self):
        for data in (read_case(), generated(3)):
            with self.subTest(case=data["case"]["case_id"]):
                self.assertEqual(self.validated_assessment(data).recommended_action, "escalate")

    def test_compatible_bank_wire_preserves_supported_referral(self):
        for data in (read_case(), generated(3)):
            with self.subTest(case=data["case"]["case_id"]):
                self.with_wire(data)
                self.assertEqual(self.validated_assessment(data).recommended_action, "escalate")

    def test_conflicting_bank_wire_blocks_referral_and_cites_direct_records(self):
        for data in (read_case(), generated(3)):
            with self.subTest(case=data["case"]["case_id"]):
                wire, ledger = self.with_wire(data, "DIFFERENT-RECORDED-RECIPIENT")
                before = deepcopy(data)
                output = self.validated_assessment(data)
                self.assertEqual(output.recommended_action, "investigate")
                question = next(item for item in output.unresolved_questions
                                if "[REF-01]" in item.statement
                                and "conflict" in item.statement.lower())
                citations = {(item.record_type, item.record_id) for item in question.citations}
                self.assertTrue({("evidence", wire["evidence_id"]),
                                 ("evidence", ledger["evidence_id"]),
                                 ("transaction", data["transactions"][0]["transaction_id"])}
                                <= citations)
                self.assertEqual(data, before)

    def test_unrelated_or_contextual_wire_does_not_block_supported_referral(self):
        for contextual in (False, True):
            with self.subTest(contextual=contextual):
                data = read_case()
                wire, _ = self.with_wire(data, "DIFFERENT-RECORDED-RECIPIENT")
                if contextual:
                    wire["related_transaction_ids"] = []
                else:
                    transaction = deepcopy(data["transactions"][0])
                    transaction.update(transaction_id="UNRELATED-TRANSFER", amount="100.00")
                    data["transactions"].append(transaction)
                    wire["related_transaction_ids"] = [transaction["transaction_id"]]
                    wire["facts"]["wire_amount"] = transaction["amount"]
                    ledger = deepcopy(data["evidence"][2])
                    ledger.update(evidence_id="UNRELATED-LEDGER",
                                  related_transaction_ids=[transaction["transaction_id"]])
                    ledger["facts"].update(payee_account_ref="OTHER-RECORDED-ACCOUNT",
                                           total_amount=transaction["amount"])
                    data["evidence"].append(ledger)
                self.assertEqual(self.validated_assessment(data).recommended_action, "escalate")

    def test_wire_records_alone_cannot_establish_referral_mappings(self):
        data = read_case()
        wire, _ = self.with_wire(data)
        second = deepcopy(wire)
        second.update(evidence_id="SECOND-WIRE",
                      related_transaction_ids=[data["transactions"][1]["transaction_id"]])
        second["facts"]["wire_amount"] = data["transactions"][1]["amount"]
        data["evidence"].append(second)
        data["evidence"] = [record for record in data["evidence"]
                            if record["evidence_type"] != "payment_record"]
        data["verification_checks"] = []
        output = self.validated_assessment(data)
        self.assertNotEqual(output.recommended_action, "escalate")
        self.assertIn("linked payment ledger is absent", questions(output))

    def test_invoice_reference_does_not_override_recorded_payment_recipient(self):
        data = read_case()
        wire, _ = self.with_wire(data)
        invoice = deepcopy(wire)
        invoice.update(evidence_id="INTENDED-BENEFICIARY", evidence_type="supplier_invoice",
                       source="customer_supplied")
        invoice["facts"]["beneficiary_account_ref"] = "DIFFERENT-INVOICE-INSTRUCTION"
        data["evidence"].append(invoice)
        output = self.validated_assessment(data)
        self.assertEqual(output.recommended_action, "escalate")
        self.assertIn("[BEN-01]", questions(output))

    def test_nonbank_wire_does_not_become_supported_bank_mapping_evidence(self):
        data = read_case()
        self.with_wire(data, "CUSTOMER-STATED-ACCOUNT", source="customer_supplied")
        self.assertEqual(self.validated_assessment(data).recommended_action, "escalate")

    def test_explicit_wire_account_is_compared_exactly_without_normalization(self):
        for account in ("ACCT-G03-UNAPPROVED ", "acct-g03-unapproved"):
            with self.subTest(account=account):
                data = read_case()
                self.with_wire(data, account)
                self.assertEqual(self.validated_assessment(data).recommended_action, "investigate")


class TestBaselineCLI(unittest.TestCase):
    def command(self, source, target):
        return [sys.executable, str(SCRIPT), "--input", str(source), "--output", str(target)]

    def test_cli_publishes_valid_output_and_refuses_overwrite(self):
        with TemporaryDirectory() as temp:
            target = Path(temp) / "new" / "assessment.json"
            source = GOLDEN / "G03.json"
            before = source.read_bytes()
            result = subprocess.run(self.command(source, target), cwd=ROOT,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["recommended_action"], "escalate")
            output = InvestigationOutput.model_validate_json(target.read_bytes())
            validate_investigation_output_references(
                InvestigationInput.model_validate_json(before), output,
            )
            written = target.read_bytes()
            result = subprocess.run(self.command(source, target), cwd=ROOT,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("already exists", result.stderr)
            self.assertEqual(target.read_bytes(), written)
            self.assertEqual(source.read_bytes(), before)

    def test_bad_or_missing_input_creates_no_partial_output(self):
        with TemporaryDirectory() as temp:
            source, target = Path(temp) / "invalid.json", Path(temp) / "new" / "output.json"
            for raw in (None, b"{", b"{}"):
                with self.subTest(raw=raw):
                    if raw is not None:
                        source.write_bytes(raw)
                    result = subprocess.run(self.command(source, target), cwd=ROOT,
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2)
                    self.assertFalse(target.parent.exists())

    def test_output_destination_is_required(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--input", str(GOLDEN / "G03.json")],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--output", result.stderr)

    def test_failed_atomic_publication_leaves_no_partial_output_or_temporary_files(self):
        namespace = runpy.run_path(str(SCRIPT))
        with TemporaryDirectory() as temp:
            target = Path(temp) / "assessment.json"
            with patch.object(sys, "argv", self.command(GOLDEN / "G03.json", target)[1:]), patch(
                "os.link", side_effect=OSError("Simulated publication failure")
            ), redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    namespace["main"]()
            self.assertEqual(error.exception.code, 2)
            self.assertEqual(list(Path(temp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
