"""Bounded library integration/examples, not a runtime runner or semantic evaluator.

Only tracked inputs and constructed responses are used. Reports stay in memory.
The explicit SDK client has a synthetic key, MockTransport and a non-provider URL.
"""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import httpx2
from openai import OpenAI
from pydantic import ValidationError

from aml_triage.auditor import audit_packet
from aml_triage.contracts import InvestigationInput, InvestigationOutput
from aml_triage.deterministic_baseline import BASELINE_VERSION, assess_investigation
from aml_triage.evidence_report import compose_evidence_report, serialize_evidence_report
from aml_triage.openai_prompt import build_assessment_prompt
from aml_triage.openai_service import AssessmentConfig, AssessmentRun, OpenAIAssessmentService


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "data/golden_cases/inputs"
ABSTENTION_INPUT = ROOT / "data/generated/development/CASE-DEV-S20261027-0002.json"
SOURCES = [GOLDEN / f"G{i:02d}.json" for i in (2, 3, 4, 5)] + [ABSTENTION_INPUT]


def baseline_bytes(value):
    """Same JSON convention as scripts/run_baseline.py; call once per assessment."""
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False,
                       allow_nan=False) + "\n").encode("utf-8")


def constructed_candidate(investigation, *, statement=None, action="investigate"):
    """Mechanical test response, constructed without reference answers or annotations."""
    tx = investigation.transactions[0]
    finding = {
        "statement": statement if statement is not None else (
            f"Transaction {tx.transaction_id} amount was {tx.currency} {tx.amount:,.2f}."
        ),
        "citations": [{"record_type": "transaction", "record_id": tx.transaction_id}],
    }
    value = {
        "schema_version": "1.0", "case_id": investigation.case.case_id,
        "alert_id": investigation.alert.alert_id,
        "assessment_status": "recommendation_provided", "recommended_action": action,
        "rationale": deepcopy(finding), "factual_findings": [deepcopy(finding)],
        "interpretations": [], "unresolved_questions": [], "missing_information": [],
        "contradictions": [], "recommendation_scope": "preliminary", "human_review_required": True,
    }
    if action is None:
        value.update(assessment_status="unable_to_recommend", factual_findings=[],
                     rationale={"statement": "No recommendation is supplied in this test response.",
                                "citations": []})
    return value


def candidate_text(value):
    # Deliberate outer whitespace demonstrates that hosted text is never replaced by a model dump.
    return " \n" + json.dumps(value, indent=3, ensure_ascii=False, allow_nan=False) + "\n "


def at_pointer(value, pointer):
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def baseline_pipeline(raw):
    """Test-local composition of existing interfaces; no publication or fallback."""
    assessment = assess_investigation(InvestigationInput.model_validate_json(raw))
    candidate = baseline_bytes(assessment.model_dump(mode="json"))
    report = compose_evidence_report(
        raw, candidate, generation_status="completed",
        expected_identities={"input_sha256": sha256(raw).hexdigest(),
                             "candidate_sha256": sha256(candidate).hexdigest()},
        provenance={"producer": f"deterministic_baseline:{BASELINE_VERSION}"},
    )
    return assessment, candidate, report


def companion_for_run(raw, run):
    """Explicit handoff used only by these tests, not a new application interface.

    Unknown/dry-run states are deliberately diagnostic-only. A validated label with
    no accepted assessment/text is also insufficient for a completed handoff.
    """
    status = run.record.get("status")
    if status == "validated" and run.assessment is not None and run.candidate_json is not None:
        outcome = "completed"
    elif status == "failed":
        outcome = {"refusal": "refused", "incomplete": "incomplete"}.get(
            (run.record.get("error") or {}).get("category"), "failed",
        )
    else:
        outcome = "failed"
    expected = {"input_sha256": sha256(raw).hexdigest()}
    for field, key in (("input_sha256", "canonical_input_sha256"),
                       ("candidate_sha256", "candidate_sha256"), ("case_id", "case_id")):
        if run.record.get(field) is not None:
            expected[key] = run.record[field]
    return compose_evidence_report(
        raw, run.candidate_json, generation_status=outcome, expected_identities=expected,
        provenance={"producer": "OpenAIAssessmentService", **{
            key: run.record.get(key) for key in
            ("model", "sdk_version", "prompt_version", "prompt_sha256", "request_id")
        }},
    )


class TestWeek6PipelineIntegration(unittest.TestCase):
    def setUp(self):
        self.fixture_hashes = {p: sha256(p.read_bytes()).hexdigest() for p in SOURCES}
        self.raw = (GOLDEN / "G02.json").read_bytes()
        self.input = InvestigationInput.model_validate_json(self.raw)
        self.guards = []
        for target in ("socket.socket.connect", "socket.create_connection", "socket.getaddrinfo",
                       "aml_triage.openai_service.OpenAI", "aml_triage.openai_service.publish_run",
                       "pathlib.Path.write_bytes", "pathlib.Path.write_text"):
            guard = patch(target, side_effect=AssertionError("forbidden integration boundary"))
            self.guards.append(guard.start())
            self.addCleanup(guard.stop)
        # Do not consult real environment values (including optional SDK configuration).
        for target in ("os.environ.get", "os.getenv"):
            guard = patch(target, return_value=None)
            guard.start()
            self.addCleanup(guard.stop)

    def tearDown(self):
        self.assertEqual(self.fixture_hashes,
                         {p: sha256(p.read_bytes()).hexdigest() for p in SOURCES})
        for guard in self.guards:
            guard.assert_not_called()

    def hosted_run(self, raw=None, data=None, *, response_status="completed", refusal=False,
                   empty=False, http_status=200, raw_text=None, enabled=True):
        raw = self.raw if raw is None else raw
        investigation = InvestigationInput.model_validate_json(raw)
        data = constructed_candidate(investigation) if data is None else data
        text = candidate_text(data) if raw_text is None else raw_text
        calls = []

        def respond(request):
            calls.append(request)
            if http_status != 200:
                return httpx2.Response(http_status, json={"error": {
                    "message": "Synthetic server failure", "type": "server_error",
                }}, headers={"x-request-id": "req_integration_error"})
            content = ([{"type": "refusal", "refusal": "Synthetic refusal"}] if refusal else
                       [{"type": "output_text", "text": text, "annotations": []}])
            body = {
                "id": "resp_integration", "object": "response", "created_at": 1,
                "model": "synthetic-test-model", "status": response_status,
                "output": [] if empty else [{
                    "id": "msg_integration", "type": "message", "role": "assistant",
                    "status": response_status, "phase": "final_answer", "content": content,
                }],
                "usage": {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
            }
            if response_status == "incomplete":
                body["incomplete_details"] = {"reason": "max_output_tokens"}
            return httpx2.Response(200, json=body, headers={"x-request-id": "req_integration"})

        http = httpx2.Client(transport=httpx2.MockTransport(respond), trust_env=False)
        client = OpenAI(api_key="synthetic-not-a-real-key", http_client=http,
                        base_url="https://mock.invalid/v1", max_retries=0)
        self.addCleanup(client.close)
        config = AssessmentConfig(model="synthetic-test-model", max_output_tokens=1200,
                                  reasoning_effort="none", live_enabled=enabled,
                                  request_allowance=1 if enabled else 0)
        run = OpenAIAssessmentService(config, client=client).assess(investigation)
        self.assertIsInstance(run, AssessmentRun)
        self.assertEqual(len(calls), 1 if enabled else 0)
        if enabled:
            self.assertEqual(run.record["request_attempts"], 1)
            self.assertEqual(run.record["requests_used"], 1)
            request = json.loads(calls[0].content)
            self.assertEqual(request["input"], build_assessment_prompt(investigation).messages())
            self.assertFalse(request["store"])
            self.assertEqual(request["max_output_tokens"], 1200)
            self.assertEqual(request["reasoning"], {"effort": "none"})
            self.assertTrue(request["text"]["format"]["strict"])
            self.assertEqual(request["text"]["format"]["schema"],
                             InvestigationOutput.model_json_schema())
            self.assertEqual(run.record["settings"]["sdk_max_retries"], 0)
            self.assertEqual(run.record["settings"]["application_max_retries"], 0)
        return run, calls

    def handoff(self, raw, run):
        before = deepcopy(run.artifact())
        report = companion_for_run(raw, run)
        self.assertEqual(before, run.artifact())
        self.assertEqual(report["semantic_evaluation"],
                         {"status": "not_evaluated", "scoring_authorized": False})
        self.assertEqual(json.loads(serialize_evidence_report(report)), report)
        for audit in (run.audit, report["validation"]["audit"]):
            if audit is not None:
                self.assertEqual(len(audit["semantic_evaluation"]), 9)
                self.assertTrue(all(v["status"] == "not_evaluated"
                                    for v in audit["semantic_evaluation"].values()))
        return report

    def assert_qualified(self, report, candidate):
        self.assertEqual(report["report_state"], "qualified_companion", report["validation"])
        self.assertEqual(report["candidate_content"], json.loads(candidate))
        self.assertEqual(report["candidate_content"]["recommendation_scope"], "preliminary")
        self.assertIs(report["candidate_content"]["human_review_required"], True)
        self.assertTrue(all(s["status"] == "passed"
                            for s in report["validation"]["audit"]["stages"].values()))
        self.assertTrue(all(c["outcome"] == "matched"
                            for c in report["validation"]["expected_identity_checks"]))
        semantics = report["validation"]["audit"]["semantic_evaluation"]
        self.assertEqual(len(semantics), 9)
        self.assertTrue(all(v["status"] == "not_evaluated" for v in semantics.values()))
        original = json.loads(candidate)
        for row in report["candidate_occurrences"]:
            self.assertEqual(at_pointer(original, row["json_pointer"]), row["text"])
            if row["citation_pointer"] is not None:
                self.assertEqual(at_pointer(original, row["citation_pointer"]),
                                 row["submitted_citations"])
        self.assertEqual(report["semantic_evaluation"],
                         {"status": "not_evaluated", "scoring_authorized": False})

    def assert_diagnostic(self, report):
        self.assertEqual(report["report_state"], "rejected")
        self.assertIsNone(report["candidate_content"])
        self.assertEqual(report["narrative_units"], [])
        self.assertTrue(report["validation"]["diagnostics"])

    def test_real_baseline_pipeline_preserves_once_serialized_candidate_and_audit(self):
        for path, action in ((GOLDEN / "G03.json", "escalate"),
                             (GOLDEN / "G05.json", "investigate"), (ABSTENTION_INPUT, None)):
            with self.subTest(path=path.name):
                raw = path.read_bytes()
                assessment, candidate, report = baseline_pipeline(raw)
                self.assert_qualified(report, candidate)
                self.assertEqual(assessment.recommended_action, action)  # Fixed behavior, not truth.
                self.assertEqual(report["candidate_content"]["recommended_action"], action)
                self.assertEqual(report["artifacts"]["candidate"]["sha256"],
                                 sha256(candidate).hexdigest())
                self.assertEqual(report["artifacts"]["candidate"]["digest_basis"], "supplied_bytes")
                self.assertEqual(report["validation"]["audit"], audit_packet(raw, candidate))
                self.assertEqual(report["artifacts"]["input"]["sha256"], sha256(raw).hexdigest())
                self.assertEqual(serialize_evidence_report(report),
                                 serialize_evidence_report(baseline_pipeline(raw)[2]))
                if action is None:
                    self.assertEqual(report["candidate_content"]["assessment_status"],
                                     "unable_to_recommend")

    def test_example_a_sdk_pipeline_preserves_text_and_separate_audit_representations(self):
        run, calls = self.hosted_run()
        self.assertEqual(run.record["status"], "validated")
        original = run.candidate_json
        report = self.handoff(self.raw, run)
        self.assert_qualified(report, original)
        self.assertTrue(original.startswith(" \n"))
        digest = sha256(original.encode("utf-8")).hexdigest()
        self.assertEqual(digest, run.record["candidate_sha256"])
        self.assertEqual(digest, report["artifacts"]["candidate"]["sha256"])
        self.assertEqual(report["artifacts"]["candidate"]["digest_basis"],
                         "utf8_encoded_candidate_text")
        self.assertEqual(report["artifacts"]["canonical_validated_input"]["sha256"],
                         run.record["input_sha256"])
        self.assertEqual(run.audit["artifacts"]["input"]["sha256"], run.record["input_sha256"])
        raw_audit = report["validation"]["audit"]
        self.assertEqual(run.audit["artifacts"]["input"]["digest_basis"], "utf8_encoded_string")
        self.assertEqual(raw_audit["artifacts"]["input"]["digest_basis"], "supplied_bytes")
        self.assertNotEqual(run.audit["artifacts"]["input"]["sha256"],
                            raw_audit["artifacts"]["input"]["sha256"])
        self.assertEqual(run.audit["stages"], raw_audit["stages"])
        self.assertEqual(run.audit["deterministic_fact_checks"], report["restricted_checks"])
        observation = next(u for u in report["source_observations"] if u["rule_id"] == "E02")
        binding = next(b for b in observation["bindings"] if b["field_pointer"] == "/amount")
        self.assertEqual(binding["input_sha256"], sha256(self.raw).hexdigest())
        self.assertEqual(binding["input_pointer"], "/transactions/0/amount")
        self.assertEqual(json.loads(binding["value_json"]), "48500.00")
        self.assertEqual(serialize_evidence_report(report),
                         serialize_evidence_report(self.handoff(self.raw, run)))
        self.assertEqual(len(calls), 1)  # Handoff/replay never repeats generation.

    def test_example_b_service_validated_amount_conflict_stays_conspicuously_qualified(self):
        text = "The incoming transaction was USD 99,999.00."
        run, _ = self.hosted_run(data=constructed_candidate(self.input, statement=text))
        self.assertEqual(run.record["status"], "validated")
        report = self.handoff(self.raw, run)
        self.assert_qualified(report, run.candidate_json)
        self.assertEqual(report["restricted_checks"]["coverage"]["conflicts_with_record"], 1)
        self.assertIn("restricted_conflict", report["qualification_reasons"])
        warning = next(u for u in report["narrative_units"]
                       if u["diagnostic_code"] == "restricted_conflict")
        self.assertIn("RESTRICTED FIELD CONFLICT", warning["text"])
        self.assertIn(text, warning["text"])
        self.assertEqual(warning["check_outcome"], "conflicts_with_record")
        amount = next(c for c in report["restricted_checks"]["findings"][0]["comparisons"]
                      if c["field"] == "amount")
        self.assertEqual((amount["claimed"], amount["recorded"]), ("99999.00", "48500.00"))
        self.assertTrue(any(b["input_pointer"] == "/transactions/0/amount"
                            for b in warning["bindings"]))
        self.assertTrue(any(d["code"] == "restricted_conflict"
                            for d in report["validation"]["diagnostics"]))
        self.assertFalse(any(text in u["text"] for u in report["source_observations"]))

    def test_example_c_unchecked_authentication_assertion_remains_candidate_attributed(self):
        text = "This software authenticated all supplier documents."
        run, _ = self.hosted_run(data=constructed_candidate(self.input, statement=text))
        self.assertEqual(run.record["status"], "validated")
        report = self.handoff(self.raw, run)
        self.assert_qualified(report, run.candidate_json)
        self.assertEqual(report["restricted_checks"]["coverage"]["checked"], 0)
        self.assertEqual(report["restricted_checks"]["coverage"]["not_checked"], 1)
        self.assertEqual(report["restricted_checks"]["status"], "not_evaluated")
        occurrence = next(o for o in report["candidate_occurrences"]
                          if o["json_pointer"] == "/factual_findings/0/statement")
        self.assertEqual(occurrence["semantic_review"], "not_evaluated")
        quoted = next(u for u in report["narrative_units"] if u["origin"] == "candidate_quote"
                      and u["candidate_occurrence_id"] == occurrence["occurrence_id"])
        self.assertIn("recorded producer", quoted["text"])
        self.assertIn(text, quoted["text"])
        self.assertFalse(any(text in u["text"] for u in report["source_observations"]))

    def test_example_d_differing_excerpts_and_missing_null_variants_preserve_scope(self):
        original = (GOLDEN / "G04.json").read_bytes()
        for state in ("available", "missing", "explicit_null"):
            with self.subTest(state=state):
                document = json.loads(original)
                facts = document["evidence"][3]["facts"]
                if state == "missing":
                    facts.pop("beneficiary_account_ref")
                elif state == "explicit_null":
                    facts["beneficiary_account_ref"] = None
                raw = original if state == "available" else baseline_bytes(document)
                run, _ = self.hosted_run(raw)
                self.assertEqual(run.record["status"], "validated")
                report = self.handoff(raw, run)
                self.assert_qualified(report, run.candidate_json)
                field = next(c for c in report["source_conditions"] if c["record_id"] == "EV-004"
                             and c["queried_field_pointer"] == "/facts/beneficiary_account_ref")
                self.assertEqual(field["state"], state)
                self.assertEqual(field["binding"]["input_pointer"], "/evidence/3/facts"
                                 + ("" if state == "missing" else "/beneficiary_account_ref"))
                self.assertEqual(field["binding"]["missing_member"],
                                 "beneficiary_account_ref" if state == "missing" else None)
                excerpts = [u for u in report["source_observations"]
                            if any(b["field_pointer"] == "/facts/beneficiary_account_ref"
                                   for b in u["bindings"]) and u["rule_id"] == "E04"]
                self.assertTrue(any("BENEFICIARY-ACC-B" in u["text"] for u in excerpts))
                self.assertEqual(any("SUPPLIER-ACC-A" in u["text"] for u in excerpts),
                                 state == "available")
                self.assertFalse(any("mismatch" in u["text"] or "fraud" in u["text"]
                                     for u in excerpts))
                self.assertEqual(report["restricted_checks"]["check"], "transaction_amount")

    def test_example_e_sdk_abstention_remains_null_and_preliminary(self):
        run, _ = self.hosted_run(data=constructed_candidate(self.input, action=None))
        self.assertEqual(run.record["status"], "validated")
        report = self.handoff(self.raw, run)
        self.assert_qualified(report, run.candidate_json)
        self.assertEqual(report["candidate_content"]["assessment_status"], "unable_to_recommend")
        self.assertIsNone(report["candidate_content"]["recommended_action"])
        self.assertEqual(report["candidate_content"]["rationale"]["citations"], [])

    def test_example_f_parseable_incomplete_response_is_diagnostic_only(self):
        run, calls = self.hosted_run(response_status="incomplete")
        self.assertEqual(run.record["status"], "failed")
        self.assertEqual(run.record["error"]["category"], "incomplete")
        InvestigationOutput.model_validate_json(run.candidate_json)  # A valid fragment is possible.
        self.assertIsNone(run.assessment)
        report = self.handoff(self.raw, run)
        self.assert_diagnostic(report)
        self.assertEqual(report["provenance"]["generation_status"]["value"], "incomplete")
        self.assertEqual(report["artifacts"]["candidate"]["sha256"],
                         run.record["candidate_sha256"])
        self.assertEqual(len(calls), 1)

    def test_valid_text_without_sdk_parsed_output_cannot_become_completed(self):
        # Fault injection only: transport and SDK parse path are real, but the SDK's
        # text-parser result is made unavailable to exercise the producer handoff.
        with patch("openai.lib._parsing._responses.parse_text", return_value=None):
            run, calls = self.hosted_run()
        self.assertEqual(run.record["status"], "failed")
        self.assertEqual(run.record["error"]["category"], "missing_output")
        InvestigationOutput.model_validate_json(run.candidate_json)
        self.assertIsNone(run.assessment)
        report = self.handoff(self.raw, run)
        self.assert_diagnostic(report)
        self.assertEqual(report["provenance"]["generation_status"]["value"], "failed")
        self.assertEqual(len(calls), 1)

    def test_refusal_empty_output_and_server_failure_remain_failed_without_retry(self):
        for settings, category, outcome in (({"refusal": True}, "refusal", "refused"),
                                            ({"empty": True}, "missing_output", "failed"),
                                            ({"http_status": 500}, "server", "failed")):
            with self.subTest(category=category):
                run, calls = self.hosted_run(**settings)
                self.assertEqual(run.record["status"], "failed")
                self.assertEqual(run.record["error"]["category"], category)
                self.assertIsNone(run.assessment)
                report = self.handoff(self.raw, run)
                self.assert_diagnostic(report)
                self.assertEqual(report["provenance"]["generation_status"]["value"], outcome)
                self.assertEqual(len(calls), 1)

    def test_real_sdk_malformed_or_contract_invalid_text_has_no_successful_substitute(self):
        invalid = constructed_candidate(self.input)
        invalid["human_review_required"] = False
        for text in ("{", candidate_text(invalid)):
            with self.subTest(text=text[:20]):
                run, _ = self.hosted_run(raw_text=text)
                self.assertEqual(run.record["error"]["category"], "sdk_parsing")
                self.assertIsNone(run.candidate_json)  # Existing SDK limitation, not fabricated bytes.
                self.assertIsNone(run.assessment)
                self.assert_diagnostic(self.handoff(self.raw, run))

    def test_wrong_identities_and_typed_citations_propagate_service_rejection(self):
        for field in ("case_id", "alert_id", "unknown_id", "wrong_namespace"):
            with self.subTest(field=field):
                data = constructed_candidate(self.input)
                if field in ("case_id", "alert_id"):
                    data[field] = "NOT-THIS-INVESTIGATION"
                else:
                    data["factual_findings"][0]["citations"] = [{
                        "record_type": "evidence" if field == "wrong_namespace" else "transaction",
                        "record_id": "TX-G02-01" if field == "wrong_namespace" else "NOT-SUPPLIED",
                    }]
                run, _ = self.hosted_run(data=data)
                self.assertEqual(run.record["error"]["category"], "citation_validation")
                report = self.handoff(self.raw, run)
                self.assert_diagnostic(report)
                self.assertEqual(report["validation"]["audit"]["stages"]
                                 ["contextual_references"]["status"], "failed")

    def test_dry_run_and_unknown_status_with_parseable_text_never_accept(self):
        dry, calls = self.hosted_run(enabled=False)
        self.assertEqual(dry.record["status"], "dry_run")
        self.assertEqual(dry.record["request_attempts"], 0)
        self.assertEqual(calls, [])
        self.assert_diagnostic(self.handoff(self.raw, dry))
        run, calls = self.hosted_run()
        for status in ("dry_run", "unknown", None):
            with self.subTest(status=status):
                altered = deepcopy(run)
                altered.record["status"] = status  # Constructed invalid handoff, not a service observation.
                self.assert_diagnostic(self.handoff(self.raw, altered))
        altered = deepcopy(run)
        altered.assessment = None
        self.assert_diagnostic(self.handoff(self.raw, altered))
        self.assertEqual(len(calls), 1)

    def test_handoff_preserves_all_sections_citations_and_contradiction_occurrences(self):
        data = constructed_candidate(self.input)
        statement = deepcopy(data["factual_findings"][0])
        data["interpretations"] = [deepcopy(statement)]
        data["missing_information"] = [{"statement": "Constructed unresolved information.",
                                        "citations": []}]
        data["unresolved_questions"] = [{"statement": "What additional records exist?", "citations": []}]
        data["contradictions"] = [{"description": "Constructed candidate contradiction description.",
                                   "left": deepcopy(statement), "right": deepcopy(statement)}]
        run, _ = self.hosted_run(data=data)
        self.assertEqual(run.record["status"], "validated")
        report = self.handoff(self.raw, run)
        self.assert_qualified(report, run.candidate_json)
        paths = {o["json_pointer"] for o in report["candidate_occurrences"]}
        self.assertTrue({"/interpretations/0/statement", "/missing_information/0/statement",
                         "/unresolved_questions/0/statement", "/contradictions/0/description",
                         "/contradictions/0/left/statement", "/contradictions/0/right/statement"}
                        <= paths)

    def test_changed_source_after_assessment_is_rejected_by_canonical_identity(self):
        run, calls = self.hosted_run()
        changed = json.loads(self.raw)
        changed["transactions"][0]["amount"] = "48501.00"
        report = self.handoff(baseline_bytes(changed), run)
        self.assert_diagnostic(report)
        check = next(c for c in report["validation"]["expected_identity_checks"]
                     if c["name"] == "canonical_input_sha256")
        self.assertEqual(check["outcome"], "mismatch")
        self.assertEqual(len(calls), 1)

    def test_composition_failure_preserves_validated_run_without_fallback_generation(self):
        run, calls = self.hosted_run()
        with patch("aml_triage.evidence_report._source_observations",
                   side_effect=RuntimeError("synthetic diagnostic marker")):
            report = self.handoff(self.raw, run)
        self.assert_diagnostic(report)
        self.assertEqual(run.record["status"], "validated")
        self.assertEqual(len(calls), 1)
        self.assertNotIn("synthetic diagnostic marker", serialize_evidence_report(report).decode())

    def test_invalid_input_stops_before_either_producer(self):
        with patch(__name__ + ".assess_investigation") as baseline, \
             patch.object(OpenAIAssessmentService, "assess") as hosted:
            with self.assertRaises(ValidationError):
                baseline_pipeline(b"{")
            with self.assertRaises(ValidationError):
                self.hosted_run(raw=b"{")
            baseline.assert_not_called()
            hosted.assert_not_called()


if __name__ == "__main__":
    unittest.main()
