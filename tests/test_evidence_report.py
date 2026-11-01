"""First-slice composer tests only; no producer orchestration, publication or API."""

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
import os
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from pydantic import ValidationError

from aml_triage.auditor import audit_packet
from aml_triage.contracts import InvestigationInput
from aml_triage.evidence_report import compose_evidence_report, serialize_evidence_report
from aml_triage.openai_prompt import build_assessment_prompt


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "data/golden_cases/inputs"
DEVELOPMENT = ROOT / "data/generated/development"


def payload(data):
    return json.dumps(data, ensure_ascii=False, allow_nan=False).encode("utf-8")


def candidate(data):
    """Construct a mechanical candidate from supplied fields, never reference answers."""
    tx = data["transactions"][0]
    statement = {
        "statement": f"Transaction {tx['transaction_id']} amount was "
                     f"{tx['currency']} {Decimal(tx['amount']):,.2f}.",
        "citations": [{"record_type": "transaction", "record_id": tx["transaction_id"]}],
    }
    return {
        "schema_version": "1.0", "case_id": data["case"]["case_id"],
        "alert_id": data["alert"]["alert_id"], "assessment_status": "recommendation_provided",
        "recommended_action": "investigate", "rationale": deepcopy(statement),
        "factual_findings": [deepcopy(statement)], "interpretations": [],
        "unresolved_questions": [], "missing_information": [], "contradictions": [],
        "recommendation_scope": "preliminary", "human_review_required": True,
    }


def pointer(value, location):
    for part in location.split("/")[1:]:
        key = part.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


class TestEvidenceReport(unittest.TestCase):
    def setUp(self):
        self.raw = (GOLDEN / "G02.json").read_bytes()
        self.input = json.loads(self.raw)
        self.output = candidate(self.input)
        guard = patch.object(socket.socket, "connect", side_effect=AssertionError("no network"))
        guard.start()
        self.addCleanup(guard.stop)

    def compose(self, data=None, output=None, **kwargs):
        return compose_evidence_report(
            self.raw if data is None else payload(data),
            payload(self.output if output is None else output), **kwargs,
        )

    def assert_qualified(self, report):
        self.assertEqual(report["report_state"], "qualified_companion", report["validation"])
        self.assertEqual(report["semantic_evaluation"],
                         {"status": "not_evaluated", "scoring_authorized": False})
        audit = report["validation"]["audit"]
        self.assertTrue(all(s["status"] == "passed" for s in audit["stages"].values()))
        self.assertEqual(len(audit["semantic_evaluation"]), 9)
        self.assertTrue(all(s["status"] == "not_evaluated"
                            for s in audit["semantic_evaluation"].values()))
        self.assertEqual(json.loads(serialize_evidence_report(report)), report)

    def assert_rejected(self, report, code=None):
        self.assertEqual(report["report_state"], "rejected")
        self.assertIsNone(report["candidate_content"])
        for field in ("source_records", "source_observations", "candidate_occurrences",
                      "source_conditions", "narrative_units", "qualification_reasons"):
            self.assertEqual(report[field], [])
        if code is not None:
            self.assertIn(code, [row["code"] for row in report["validation"]["diagnostics"]])
        serialize_evidence_report(report)

    def test_valid_companion_has_exact_versioned_schema(self):
        report = self.compose()
        self.assert_qualified(report)
        self.assertEqual(set(report), {
            "report_schema_version", "composer_version", "template_version", "report_state",
            "case_identity", "artifacts", "provenance", "component_versions", "source_records",
            "source_observations", "source_conditions", "candidate_content", "candidate_occurrences",
            "restricted_checks", "validation", "qualification_reasons", "narrative_units",
            "semantic_evaluation", "limitations",
        })
        self.assertEqual(report["report_schema_version"], "1.0")
        self.assertEqual(report["composer_version"], "0.1.0")
        self.assertEqual(report["candidate_content"], self.output)

    def test_tracked_golden_and_development_inputs_need_no_ignored_packet(self):
        paths = [GOLDEN / f"G{i:02d}.json" for i in range(1, 6)]
        paths += sorted(DEVELOPMENT.glob("CASE-*.json"))
        self.assertEqual(len(paths), 55)
        for path in paths:
            with self.subTest(path=path.name):
                raw = path.read_bytes()
                report = compose_evidence_report(raw, payload(candidate(json.loads(raw))))
                self.assert_qualified(report)

    def test_every_binding_resolves_to_exact_original_source_value(self):
        report = self.compose()
        raw = json.loads(self.raw, parse_float=Decimal)
        bindings = [b for unit in report["source_observations"] + report["narrative_units"]
                    for b in unit["bindings"]]
        bindings += [row["binding"] for row in report["source_conditions"]]
        self.assertTrue(bindings)
        for binding in bindings:
            self.assertEqual(binding["input_sha256"], sha256(self.raw).hexdigest())
            self.assertEqual(binding["input_pointer"],
                             binding["record_pointer"] + binding["field_pointer"])
            observed = pointer(raw, binding["input_pointer"])
            self.assertEqual(json.loads(binding["value_json"], parse_float=Decimal), observed)
            if binding["missing_member"] is not None:
                self.assertNotIn(binding["missing_member"], observed)

    def test_contextual_evidence_unflagged_transactions_and_namespace_reuse_survive(self):
        self.input["accounts"][0]["account_id"] = self.input["customer"]["customer_id"]
        for tx in self.input["transactions"]:
            tx["account_id"] = self.input["accounts"][0]["account_id"]
        self.input["evidence"][0]["related_transaction_ids"] = []
        report = self.compose(self.input)
        self.assert_qualified(report)
        records = report["source_records"]
        kinds = {r["record_type"] for r in records}
        self.assertEqual(kinds, {"case", "customer", "account", "counterparty", "transaction",
                                 "alert", "evidence", "verification_check"})
        same_id = [r for r in records if r["record_id"] == self.input["customer"]["customer_id"]]
        self.assertEqual({r["record_type"] for r in same_id}, {"customer", "account"})
        self.assertTrue(any(r["record_id"] == "TX-G02-02" for r in records))

    def test_source_record_snapshots_preserve_fractional_json_numbers_losslessly(self):
        self.input["evidence"][0]["facts"]["precise_number"] = "NUMERIC_TOKEN"
        raw = payload(self.input).replace(b'"precise_number": "NUMERIC_TOKEN"',
            b'"precise_number": 0.12345678901234567890123456789')
        report = compose_evidence_report(raw, payload(self.output))
        self.assert_qualified(report)
        record = next(r for r in report["source_records"] if r["record_type"] == "evidence")
        restored = json.loads(record["record_json"], parse_float=Decimal)
        self.assertEqual(restored["facts"]["precise_number"],
                         Decimal("0.12345678901234567890123456789"))

    def test_e01_ids_and_alert_scope_have_direct_source_bindings(self):
        report = self.compose()
        rows = [r for r in report["source_observations"] if r["rule_id"] == "E01"]
        self.assertEqual(len(rows), 2)
        self.assertEqual({b["input_pointer"] for r in rows for b in r["bindings"]}, {
            "/case/case_id", "/case/primary_alert_id", "/alert/alert_id", "/alert/transaction_ids",
        })

    def test_e02_retains_large_decimal_precision_and_original_offset_timestamp(self):
        self.input["transactions"][0]["amount"] = "999999999999999999999999.99"
        self.input["transactions"][0]["occurred_at"] = "2026-10-13T14:00:00+03:00"
        self.output = candidate(self.input)
        report = self.compose(self.input)
        self.assert_qualified(report)
        observation = next(r for r in report["source_observations"] if r["rule_id"] == "E02")
        self.assertIn("999999999999999999999999.99", observation["text"])
        self.assertIn("2026-10-13T14:00:00+03:00", observation["text"])
        amount = next(b for b in observation["bindings"] if b["field_pointer"] == "/amount")
        self.assertEqual(json.loads(amount["value_json"]), self.input["transactions"][0]["amount"])

    def test_null_counterparty_is_not_invented_as_a_missing_payment_recipient(self):
        self.input["transactions"][0]["counterparty_id"] = None
        report = self.compose(self.input)
        self.assert_qualified(report)
        observation = next(r for r in report["source_observations"] if r["rule_id"] == "E02")
        self.assertIn("counterparty reference null", observation["text"])
        self.assertNotIn("missing beneficiary", observation["text"])

    def test_rounded_existing_contract_number_cannot_become_a_source_observation(self):
        data = deepcopy(self.input)
        data["transactions"][0]["amount"] = "EXACT_NUMBER_TOKEN"
        raw = payload(data).replace(b'"EXACT_NUMBER_TOKEN"', b'999999999999999999999999.99')
        report = compose_evidence_report(raw, payload(self.output))
        self.assert_rejected(report, "source_numeric_normalization")
        diagnostic = next(d for d in report["validation"]["diagnostics"]
                          if d["code"] == "source_numeric_normalization")
        self.assertEqual(diagnostic["location"], "/transactions/0/amount")
        self.assertEqual(report["artifacts"]["input"]["sha256"], sha256(raw).hexdigest())

    def test_e03_keeps_monthly_daily_scope_without_a_new_profile_comparison(self):
        profile = self.input["customer"]["expected_monthly_activity"]
        profile.update(typical_daily_cash_deposit_min="100.00",
                       typical_daily_cash_deposit_max="200.00")
        report = self.compose(self.input)
        rows = [r for r in report["source_observations"] if r["rule_id"] == "E03"]
        self.assertEqual(len(rows), 2)
        self.assertIn("expected monthly", rows[0]["text"])
        self.assertIn("no hard individual-payment limit or personal authorship is inferred", rows[0]["text"])
        self.assertIn("typical daily", rows[1]["text"])
        self.assertNotIn("materially", " ".join(r["text"] for r in rows))
        self.assertNotIn("customer personally stated", " ".join(r["text"] for r in rows))

    def test_e04_attributes_customer_claims_and_recorded_checks(self):
        report = self.compose()
        text = " ".join(r["text"] for r in report["source_observations"] if r["rule_id"] == "E04")
        self.assertIn("recorded customer claim", text)
        self.assertIn("did not independently execute", text)
        self.assertIn("not verification performed by this composer", text)

    def test_unallowlisted_fact_shapes_are_snapshots_not_generated_prose(self):
        self.input["evidence"][1]["facts"]["claim"] = {"hidden_claim": "UNSUPPORTED_MARKER"}
        report = self.compose(self.input)
        self.assert_qualified(report)
        self.assertNotIn("UNSUPPORTED_MARKER", " ".join(r["text"] for r in report["source_observations"]))
        self.assertIn("UNSUPPORTED_MARKER", " ".join(r["record_json"] for r in report["source_records"]))

    def test_e05_distinguishes_missing_null_unusable_and_available(self):
        for value, state in (("ABSENT", "missing"), (None, "explicit_null"),
                             (" ", "unsupported_or_unusable"), ({}, "unsupported_or_unusable"),
                             ("Recorded explanation", "available")):
            with self.subTest(state=state, value=value):
                data = deepcopy(self.input)
                facts = data["evidence"][1]["facts"]
                if value == "ABSENT":
                    facts.pop("claim")
                else:
                    facts["claim"] = value
                report = self.compose(data)
                self.assert_qualified(report)
                row = next(r for r in report["source_conditions"]
                           if r["queried_field_pointer"] == "/facts/claim")
                self.assertEqual(row["state"], state)
                if state == "missing":
                    self.assertEqual(row["binding"]["input_pointer"], "/evidence/1/facts")
                    self.assertEqual(row["binding"]["missing_member"], "claim")

    def test_model_default_for_omitted_daily_bound_is_not_a_supplied_null(self):
        profile = self.input["customer"]["expected_monthly_activity"]
        profile.pop("typical_daily_cash_deposit_min", None)
        profile.pop("typical_daily_cash_deposit_max", None)
        report = self.compose(self.input)
        daily = [r for r in report["source_conditions"] if "typical_daily" in r["queried_field_pointer"]]
        self.assertEqual([r["state"] for r in daily], ["missing", "missing"])

    def test_differing_or_null_beneficiary_excerpts_do_not_gain_a_new_verdict(self):
        for left in (None, "ACCOUNT-A"):
            with self.subTest(left=left):
                data = deepcopy(self.input)
                for index, (kind, account) in enumerate((
                    ("supplier_invoice", left), ("wire_payment_record", "ACCOUNT-B"),
                )):
                    data["evidence"].append({
                        "evidence_id": f"EV-COMPARISON-{index}", "evidence_type": kind,
                        "source": "synthetic", "verification_status": "supplied",
                        "related_transaction_ids": ["TX-G02-01"],
                        "facts": {"beneficiary_account_ref": account},
                    })
                report = self.compose(data)
                self.assert_qualified(report)
                text = " ".join(r["text"] for r in report["source_observations"])
                self.assertIn("ACCOUNT-B", text)
                self.assertNotIn("mismatch", text)
                self.assertNotIn("fraud", text)
                self.assertEqual({r["rule_id"] for r in report["source_observations"]},
                                 {"E01", "E02", "E03", "E04", "E05"})

    def test_e06_reuses_exact_existing_audit_and_matched_field_coverage(self):
        raw_candidate = payload(self.output)
        report = self.compose()
        original = audit_packet(self.raw, raw_candidate)
        self.assertEqual(report["validation"]["audit"], original)
        self.assertEqual(report["restricted_checks"], original["deterministic_fact_checks"])
        self.assertEqual(report["restricted_checks"]["coverage"]["matches_record"], 1)

    def test_recognized_conflict_is_qualified_conspicuous_and_never_promoted(self):
        wrong = "The incoming transaction was USD 99,999.00."
        self.output["factual_findings"][0]["statement"] = wrong
        report = self.compose()
        self.assert_qualified(report)
        self.assertIn("restricted_conflict", report["qualification_reasons"])
        diagnostic = next(r for r in report["validation"]["diagnostics"]
                          if r["code"] == "restricted_conflict")
        self.assertEqual(diagnostic["location"], "/factual_findings/0/statement")
        unit = next(r for r in report["narrative_units"] if r["diagnostic_code"] == "restricted_conflict")
        self.assertEqual(unit["check_outcome"], "conflicts_with_record")
        self.assertIn("RESTRICTED FIELD CONFLICT", unit["text"])
        self.assertIn(wrong, unit["text"])
        self.assertIn("48500.00", unit["text"])
        self.assertTrue(unit["bindings"])
        self.assertEqual(pointer(report, unit["check_pointer"])["outcome"], "conflicts_with_record")
        occurrence = next(r for r in report["candidate_occurrences"]
                          if r["occurrence_id"] == unit["candidate_occurrence_id"])
        self.assertEqual(occurrence["text"], wrong)
        self.assertEqual(occurrence["submitted_citations"], self.output["factual_findings"][0]["citations"])
        self.assertFalse(any(wrong in r["text"] for r in report["source_observations"]))

    def test_wrong_currency_and_incoming_direction_keep_existing_outcomes(self):
        for text, data in (("The incoming transaction was EUR 48,500.00.", self.input),
                           ("The incoming transaction was USD 48,500.00.",
                            {**self.input, "transactions": [
                                {**self.input["transactions"][0], "direction": "debit"},
                                self.input["transactions"][1]]})):
            with self.subTest(text=text):
                output = deepcopy(self.output)
                output["factual_findings"][0]["statement"] = text
                report = self.compose(data, output)
                self.assert_qualified(report)
                self.assertEqual(report["restricted_checks"]["coverage"]["conflicts_with_record"], 1)

    def test_every_recognized_conflict_has_its_own_preserved_occurrence_and_warning(self):
        second = deepcopy(self.output["factual_findings"][0])
        self.output["factual_findings"][0]["statement"] = "The incoming transaction was USD 99,999.00."
        second["statement"] = "The incoming transaction was EUR 48,500.00."
        self.output["factual_findings"].append(second)
        report = self.compose()
        self.assert_qualified(report)
        diagnostics = [d for d in report["validation"]["diagnostics"] if d["code"] == "restricted_conflict"]
        units = [u for u in report["narrative_units"] if u["diagnostic_code"] == "restricted_conflict"]
        self.assertEqual(len(diagnostics), 2)
        self.assertEqual(len(units), 2)
        self.assertEqual(len({u["candidate_occurrence_id"] for u in units}), 2)
        self.assertEqual(report["restricted_checks"]["coverage"]["conflicts_with_record"], 2)

    def test_unrecognized_unsupported_assertion_stays_unchecked_candidate_text(self):
        text = "This software authenticated every document."
        self.output["factual_findings"][0]["statement"] = text
        report = self.compose(provenance={"producer": "constructed test producer"})
        self.assert_qualified(report)
        self.assertEqual(report["restricted_checks"]["coverage"]["checked"], 0)
        self.assertIn("restricted_coverage_incomplete", report["qualification_reasons"])
        self.assertFalse(any(text in r["text"] for r in report["source_observations"]))
        quote = next(r for r in report["narrative_units"] if r["origin"] == "candidate_quote"
                     and text in r["text"])
        self.assertIn("recorded producer", quote["text"])
        self.assertIn("Semantic support is not evaluated", quote["text"])

    def test_complete_occurrences_include_every_field_and_contradiction_description(self):
        item = deepcopy(self.output["rationale"])
        item["statement"] = "Repeated exact text with preserved spacing.  "
        self.output["interpretations"] = [deepcopy(item), deepcopy(item)]
        self.output["unresolved_questions"] = [{"statement": "What remains unknown?", "citations": []}]
        self.output["missing_information"] = [{"statement": "Scoped missing material.", "citations": []}]
        self.output["contradictions"] = [{"description": "Candidate-described difference.",
                                          "left": deepcopy(item), "right": deepcopy(item)}]
        report = self.compose()
        self.assert_qualified(report)
        occurrences = report["candidate_occurrences"]
        self.assertEqual(len(occurrences), 9)
        self.assertEqual(len({r["occurrence_id"] for r in occurrences}), 9)
        for row in occurrences:
            self.assertEqual(row["text"], pointer(self.output, row["json_pointer"]))
            self.assertEqual(row["statement_sha256"], sha256(row["text"].encode()).hexdigest())
            if row["citation_pointer"] is not None:
                self.assertEqual(row["submitted_citations"], pointer(self.output, row["citation_pointer"]))
            else:
                self.assertEqual(row["kind"], "contradiction_description")
                self.assertIsNone(row["submitted_citations"])
        quotes = [r for r in report["narrative_units"] if r["candidate_occurrence_id"] is not None
                  and r["origin"] == "candidate_quote"]
        self.assertEqual(len(quotes), 9)
        self.assertEqual(report["candidate_content"], self.output)

    def test_candidate_original_string_and_byte_hash_bases_are_explicit(self):
        raw = " \n" + json.dumps(self.output, indent=3) + "\n "
        for supplied, basis in ((raw, "utf8_encoded_candidate_text"),
                                (raw.encode(), "supplied_bytes")):
            with self.subTest(basis=basis):
                report = compose_evidence_report(self.raw, supplied)
                self.assert_qualified(report)
                self.assertEqual(report["artifacts"]["candidate"]["sha256"], sha256(raw.encode()).hexdigest())
                self.assertEqual(report["artifacts"]["candidate"]["digest_basis"], basis)
                self.assertEqual(report["candidate_content"], self.output)

    def test_correct_expected_identities_bind_raw_canonical_and_case_values(self):
        canonical = build_assessment_prompt(InvestigationInput.model_validate_json(self.raw))
        report = self.compose(expected_identities={
            "input_sha256": sha256(self.raw).hexdigest(),
            "candidate_sha256": sha256(payload(self.output)).hexdigest(),
            "canonical_input_sha256": canonical.input_sha256,
            "case_id": self.output["case_id"], "alert_id": self.output["alert_id"],
        })
        self.assert_qualified(report)
        self.assertNotEqual(report["artifacts"]["input"]["sha256"], canonical.input_sha256)
        checks = report["validation"]["expected_identity_checks"]
        self.assertEqual(len(checks), 5)
        self.assertEqual([c["name"] for c in checks], sorted(c["name"] for c in checks))
        self.assertTrue(all(c["outcome"] == "matched" and c["actual"] == c["expected"]
                            for c in checks))

    def test_each_mismatching_expected_identity_is_a_hard_rejection(self):
        for key in ("input_sha256", "candidate_sha256", "canonical_input_sha256", "case_id", "alert_id"):
            with self.subTest(key=key):
                value = "0" * 64 if key.endswith("sha256") else "WRONG"
                report = self.compose(expected_identities={key: value})
                self.assert_rejected(report, "expected_identity_mismatch")
                check = report["validation"]["expected_identity_checks"][0]
                self.assertEqual(check["expected"], value)
                self.assertEqual(check["outcome"], "mismatch")
                self.assertNotEqual(check["actual"], check["expected"])

    def test_line_endings_and_whitespace_are_not_normalized_to_match_expected_bytes(self):
        altered = self.raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n") + b" "
        original = self.compose()
        report = compose_evidence_report(altered, payload(self.output))
        self.assert_qualified(report)
        self.assertNotEqual(report["artifacts"]["input"]["sha256"], original["artifacts"]["input"]["sha256"])
        self.assertEqual(report["artifacts"]["canonical_validated_input"],
                         original["artifacts"]["canonical_validated_input"])
        self.assert_rejected(compose_evidence_report(altered, payload(self.output),
            expected_identities={"input_sha256": sha256(self.raw).hexdigest()}),
            "expected_identity_mismatch")

    def test_optional_metadata_is_unknown_or_recorded_never_guessed_verified(self):
        report = self.compose()
        self.assertTrue(all(v["value"] is None for v in report["provenance"].values()))
        self.assertTrue(all(v["evidence_state"] == "not_supplied_or_unavailable"
                            for v in report["provenance"].values()))
        report = self.compose(provenance={"model": "synthetic-model", "request_id": None},
                              generation_status="completed")
        self.assertEqual(report["provenance"]["model"]["evidence_state"],
                         "recorded_not_independently_verified")
        self.assertIsNone(report["provenance"]["request_id"]["value"])

    def test_invalid_argument_types_and_secret_metadata_keys_are_rejected_safely(self):
        for settings in ({"provenance": {"api_key": "SECRET_MARKER"}},
                         {"provenance": {"model": 5}}, {"generation_status": "running"},
                         {"expected_identities": {"unknown": "x"}},
                         {"expected_identities": {"input_sha256": "invalid"}}):
            with self.subTest(settings=list(settings)):
                report = self.compose(**settings)
                self.assert_rejected(report, "invalid_arguments")
                self.assertNotIn("SECRET_MARKER", serialize_evidence_report(report).decode())
        self.assert_rejected(compose_evidence_report(self.input, payload(self.output)), "invalid_arguments")
        self.assert_rejected(compose_evidence_report(self.raw, self.output), "invalid_arguments")

    def test_invalid_input_json_duplicate_ids_and_cross_record_references_reject(self):
        self.assert_rejected(compose_evidence_report(b"{", payload(self.output)), "invalid_investigation")
        for kind in ("duplicate", "reference"):
            with self.subTest(kind=kind):
                data = deepcopy(self.input)
                if kind == "duplicate":
                    data["transactions"].append(deepcopy(data["transactions"][0]))
                else:
                    data["alert"]["transaction_ids"] = ["NOT-SUPPLIED"]
                self.assert_rejected(self.compose(data), "invalid_investigation")

    def test_invalid_candidate_structure_is_not_repaired(self):
        for field, value in (("recommended_action", "approve"), ("factual_findings", []),
                             ("assessment_status", "unable_to_recommend")):
            with self.subTest(field=field):
                output = deepcopy(self.output)
                output[field] = value
                self.assert_rejected(self.compose(output=output), "mechanical_validation_failed")
        self.assert_rejected(compose_evidence_report(self.raw, b"{"), "mechanical_validation_failed")

    def test_unknown_or_wrong_namespace_citations_reject_without_substitution(self):
        for kind, identifier in (("transaction", "NOT-SUPPLIED"), ("evidence", "TX-G02-01")):
            with self.subTest(kind=kind):
                output = deepcopy(self.output)
                output["rationale"]["citations"] = [{"record_type": kind, "record_id": identifier}]
                self.assert_rejected(self.compose(output=output), "mechanical_validation_failed")

    def test_wrong_case_or_alert_identity_rejects(self):
        for field in ("case_id", "alert_id"):
            with self.subTest(field=field):
                output = deepcopy(self.output)
                output[field] = "WRONG"
                self.assert_rejected(self.compose(output=output), "mechanical_validation_failed")

    def test_missing_required_citations_and_duplicate_citations_reject(self):
        for cites in ([], self.output["rationale"]["citations"] * 2):
            with self.subTest(citations=cites):
                output = deepcopy(self.output)
                output["factual_findings"][0]["citations"] = cites
                self.assert_rejected(self.compose(output=output), "mechanical_validation_failed")

    def test_valid_abstention_stays_null_with_permitted_uncited_text(self):
        self.output.update(assessment_status="unable_to_recommend", recommended_action=None,
                           factual_findings=[], rationale={"statement": "No supported decision.", "citations": []})
        report = self.compose()
        self.assert_qualified(report)
        self.assertIsNone(report["candidate_content"]["recommended_action"])
        self.assertEqual(report["candidate_occurrences"][0]["submitted_citations"], [])
        self.assertEqual(report["restricted_checks"]["coverage"]["checked"], 0)

    def test_failed_refused_incomplete_supplied_outcomes_never_become_assessments(self):
        for status in ("failed", "refused", "incomplete"):
            for supplied in (payload(self.output), None, b'{"fragment":'):
                with self.subTest(status=status, present=supplied is not None):
                    self.assert_rejected(compose_evidence_report(self.raw, supplied,
                        generation_status=status), "generation_not_completed")

    def test_absent_candidate_is_not_fabricated_abstention(self):
        self.assert_rejected(compose_evidence_report(self.raw, None), "candidate_unavailable")

    def test_preliminary_and_exact_human_review_contract_remain_required(self):
        for field, value in (("recommendation_scope", "final"), ("human_review_required", False),
                             ("human_review_required", 1)):
            with self.subTest(field=field, value=value):
                output = deepcopy(self.output)
                output[field] = value
                self.assert_rejected(self.compose(output=output), "mechanical_validation_failed")
        report = self.compose()
        self.assertIn("not certified completed", report["narrative_units"][0]["text"])

    def test_no_file_network_git_environment_or_credential_discovery(self):
        with patch("builtins.open", side_effect=AssertionError("no files")), \
             patch.object(Path, "open", side_effect=AssertionError("no paths")), \
             patch("subprocess.run", side_effect=AssertionError("no commands")), \
             patch("subprocess.check_output", side_effect=AssertionError("no commands")), \
             patch("os.getenv", side_effect=AssertionError("no environment")), \
             patch.object(type(os.environ), "__getitem__", side_effect=AssertionError("no environment")), \
             patch("socket.getaddrinfo", side_effect=AssertionError("no DNS")), \
             patch("socket.create_connection", side_effect=AssertionError("no network")):
            report = self.compose()
            self.assert_qualified(report)

    def test_reproducible_serialization_has_no_clock_or_machine_path_dependency(self):
        first = self.compose()
        second = self.compose()
        self.assertEqual(serialize_evidence_report(first), serialize_evidence_report(second))
        blob = serialize_evidence_report(first)
        self.assertTrue(blob.endswith(b"\n"))
        self.assertFalse(blob.endswith(b"\n\n"))
        self.assertNotIn(b"\r\n", blob)
        self.assertNotIn(str(ROOT).encode(), blob)
        self.assertNotIn("started_at", first)

    def test_input_candidate_and_provenance_remain_unchanged_and_unaliased(self):
        provenance = {"producer": "constructed"}
        expected = {"input_sha256": sha256(self.raw).hexdigest()}
        before = deepcopy((self.input, self.output, provenance, expected))
        report = self.compose(provenance=provenance, expected_identities=expected)
        report["candidate_content"]["rationale"]["statement"] = "Changed returned object"
        self.assertEqual((self.input, self.output, provenance, expected), before)
        self.assertNotEqual(self.compose()["candidate_content"]["rationale"]["statement"],
                            "Changed returned object")

    def test_existing_source_fixtures_remain_byte_identical_on_success_and_failure(self):
        paths = list(GOLDEN.glob("*.json")) + list(DEVELOPMENT.glob("*.json"))
        before = {p: sha256(p.read_bytes()).hexdigest() for p in paths}
        self.compose()
        self.compose(expected_identities={"candidate_sha256": "0" * 64})
        self.assertEqual(before, {p: sha256(p.read_bytes()).hexdigest() for p in paths})

    def test_invalid_mandatory_binding_rejects_instead_of_publishing_observations(self):
        from aml_triage import evidence_report
        original = evidence_report._bind
        def stale(*args, **kwargs):
            binding = original(*args, **kwargs)
            binding["value_json"] = '"WRONG"'
            return binding
        with patch.object(evidence_report, "_bind", side_effect=stale):
            self.assert_rejected(self.compose(), "source_binding_invalid")

    def test_audit_representation_mismatch_is_not_silently_rebound(self):
        for artifact in ("input", "candidate"):
            for field, value in (("digest_basis", "canonical_substitute"), ("sha256", "0" * 64)):
                with self.subTest(artifact=artifact, field=field):
                    original = audit_packet(self.raw, payload(self.output))
                    original["artifacts"][artifact][field] = value
                    with patch("aml_triage.evidence_report.audit_packet", return_value=original):
                        self.assert_rejected(self.compose(), "source_binding_invalid")

    def test_unexpected_errors_are_rejected_without_raw_exception_details(self):
        for boundary in ("audit_packet", "_source_observations"):
            with self.subTest(boundary=boundary), patch("aml_triage.evidence_report." + boundary,
                    side_effect=RuntimeError("SECRET_TRACE_MARKER")):
                report = self.compose()
                self.assert_rejected(report, "unexpected_error")
                self.assertNotIn("SECRET_TRACE_MARKER", serialize_evidence_report(report).decode())

    def test_restricted_checker_error_is_not_an_unchecked_success(self):
        audit = audit_packet(self.raw, payload(self.output))
        audit["deterministic_fact_checks"]["status"] = "error"
        with patch("aml_triage.evidence_report.audit_packet", return_value=audit):
            self.assert_rejected(self.compose(), "restricted_check_error")

    def test_serializer_rejects_schema_mutations_and_unauthorized_scoring(self):
        for mutate in (lambda r: r.update(score=100),
                       lambda r: r["semantic_evaluation"].update(scoring_authorized=True),
                       lambda r: r["semantic_evaluation"].update(scoring_authorized=0),
                       lambda r: r.update(report_state="factual_pass"),
                       lambda r: r["case_identity"].update(unexpected="value"),
                       lambda r: r["artifacts"]["input"].update(sha256="invalid"),
                       lambda r: r["validation"]["audit"].update(stages={}),
                       lambda r: r["source_observations"][0].update(unknown=True)):
            report = self.compose()
            mutate(report)
            with self.assertRaises(ValidationError):
                serialize_evidence_report(report)


if __name__ == "__main__":
    unittest.main()
