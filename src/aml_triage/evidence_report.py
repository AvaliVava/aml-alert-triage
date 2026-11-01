"""Offline, bounded source observations and attributed assessment text; no producer/I/O.

See docs/week-6/EVIDENCE_REPORT_IMPLEMENTATION_CONTRACT_v0.1.md. An eligible
companion is always qualified, including when restricted amount checks conflict.
Neither source lookup nor this report certifies general factual support.
"""

from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
from hashlib import sha256
import json
import re
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from aml_triage.auditor import AUDITOR_VERSION, audit_packet
from aml_triage.contracts import InvestigationInput, RecordCitation
from aml_triage.openai_prompt import build_assessment_prompt
from aml_triage.transaction_amount_checks import CHECK_VERSION


REPORT_SCHEMA_VERSION = "1.0"
COMPOSER_VERSION = "0.1.0"
TEMPLATE_VERSION = "1.0"
_METADATA = ("producer", "model", "sdk_version", "prompt_version", "prompt_sha256", "request_id")
_EXPECTED = {"input_sha256", "candidate_sha256", "canonical_input_sha256", "case_id", "alert_id"}
_STAGES = {"input_structure", "output_structure", "contextual_references"}
_Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
_RecordType = RecordCitation.model_fields["record_type"].annotation
_SETS = (
    ("case", "case", "case_id"), ("customer", "customer", "customer_id"),
    ("account", "accounts", "account_id"), ("counterparty", "counterparties", "counterparty_id"),
    ("transaction", "transactions", "transaction_id"), ("alert", "alert", "alert_id"),
    ("evidence", "evidence", "evidence_id"),
    ("verification_check", "verification_checks", "check_id"),
)
_LIMITATIONS = [
    "Supplied synthetic records only; no evidence authenticity or independent verification.",
    "Citation existence and field matches do not establish whole-statement factual support.",
    "Unchecked assertions, questions and interpretations remain candidate-attributed.",
    "No general absence, contradiction, materiality, policy or recommendation evaluator.",
    "Preliminary decision support; required human review is not completed human review.",
    "All nine existing audit semantic dimensions remain not_evaluated; scoring is disabled.",
    "P01/P02 remain approved; P03 is open and P04/P05 remain separately controlled.",
    "Optional run metadata is recorded, not authenticated; no hidden discovery occurs.",
]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class _Artifact(_Strict):
    sha256: _Digest | None
    bytes: Annotated[int, Field(ge=0)] | None
    digest_basis: Literal["supplied_bytes", "utf8_encoded_candidate_text",
                          "validated_input_canonical_json_utf8"]
    unavailable_reason: str | None


class _Metadata(_Strict):
    value: str | None
    evidence_state: Literal["recorded_not_independently_verified", "not_supplied_or_unavailable"]
    reason: str


class _Binding(_Strict):
    input_sha256: _Digest
    record_type: _RecordType
    record_id: str
    record_pointer: str
    field_pointer: str
    input_pointer: str
    value_json: str
    missing_member: str | None
    evidence_state: Literal["verified_against_supplied_evidence"]


class _RecordSnapshot(_Strict):
    input_sha256: _Digest
    record_type: _RecordType
    record_id: str
    record_pointer: str
    record_json: str


class _Condition(_Strict):
    record_type: _RecordType
    record_id: str
    queried_field_pointer: str
    state: Literal["missing", "explicit_null", "unsupported_or_unusable", "available"]
    binding: _Binding


class _Occurrence(_Strict):
    occurrence_id: _Digest
    candidate_sha256: _Digest
    json_pointer: str
    statement_sha256: _Digest
    text: str
    section: str
    kind: Literal["statement", "contradiction_description"]
    citation_pointer: str | None
    submitted_citations: list[RecordCitation] | None
    semantic_review: Literal["not_evaluated"]


class _Unit(_Strict):
    unit_id: _Digest
    origin: Literal["source_template", "restricted_check", "candidate_quote", "diagnostic"]
    rule_id: str | None
    text: str
    bindings: list[_Binding]
    candidate_occurrence_id: _Digest | None
    check_pointer: str | None
    check_outcome: str | None
    diagnostic_code: str | None


class _Diagnostic(_Strict):
    severity: Literal["rejection", "qualification"]
    code: str
    location: str | None
    message: str


class _IdentityCheck(_Strict):
    name: Literal["input_sha256", "candidate_sha256", "canonical_input_sha256", "case_id", "alert_id"]
    expected: str
    actual: str | None
    outcome: Literal["not_evaluated", "matched", "mismatch", "unavailable"]


class _Validation(_Strict):
    audit: dict[str, Any] | None
    diagnostics: list[_Diagnostic]
    expected_identity_checks: list[_IdentityCheck]


class _Semantic(_Strict):
    status: Literal["not_evaluated"]
    scoring_authorized: Literal[False]


class _CaseIdentity(_Strict):
    case_id: str
    alert_id: str


class _Report(_Strict):
    report_schema_version: Literal["1.0"]
    composer_version: Literal["0.1.0"]
    template_version: Literal["1.0"]
    report_state: Literal["qualified_companion", "rejected"]
    case_identity: _CaseIdentity | None
    artifacts: dict[str, _Artifact]
    provenance: dict[str, _Metadata]
    component_versions: dict[str, str]
    source_records: list[_RecordSnapshot]
    source_observations: list[_Unit]
    source_conditions: list[_Condition]
    candidate_content: dict[str, Any] | None
    candidate_occurrences: list[_Occurrence]
    restricted_checks: dict[str, Any] | None
    validation: _Validation
    qualification_reasons: list[str]
    narrative_units: list[_Unit]
    semantic_evaluation: _Semantic
    limitations: list[str]

    @model_validator(mode="before")
    @classmethod
    def require_disabled_scoring(cls, value):
        if (isinstance(value, dict)
                and value.get("semantic_evaluation", {}).get("scoring_authorized") is not False):
            raise ValueError("semantic scoring is disabled")
        return value

    @model_validator(mode="after")
    def require_eligible_shape(self):
        if set(self.artifacts) != {"input", "candidate", "canonical_validated_input"}:
            raise ValueError("artifact set differs from schema")
        if set(self.provenance) != set(_METADATA) | {"generation_status"}:
            raise ValueError("provenance set differs from schema")
        if self.report_state == "qualified_companion":
            audit = self.validation.audit
            if (self.case_identity is None or self.candidate_content is None or audit is None
                    or set(audit["stages"]) != _STAGES
                    or not all(s["status"] == "passed" for s in audit["stages"].values())
                    or any(c.outcome != "matched" for c in self.validation.expected_identity_checks)
                    or any(d.severity == "rejection" for d in self.validation.diagnostics)):
                raise ValueError("qualified companion prerequisites did not pass")
        return self


class _BindingError(ValueError):
    pass


class _NumericSourceError(_BindingError):
    """An existing typed normalization cannot stand in for the supplied amount."""


@dataclass(frozen=True)
class _Source:
    kind: str
    identifier: str
    pointer: str
    data: dict


def _json(value) -> str:
    """Lossless decoded-source JSON: Decimal numbers never pass through float."""
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("non-finite source value")
        text = str(value)
    elif isinstance(value, dict):
        text = "{" + ",".join(_json(key) + ":" + _json(value[key])
                              for key in sorted(value)) + "}"
    elif isinstance(value, list):
        text = "[" + ",".join(_json(item) for item in value) + "]"
    else:
        text = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    text.encode("utf-8")
    return text


def _pointer(value, pointer: str):
    if pointer and not pointer.startswith("/"):
        raise _BindingError("invalid pointer")
    for part in pointer.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def _artifact(payload, basis: str) -> dict:
    if payload is None or type(payload) not in (str, bytes):
        return {"sha256": None, "bytes": None, "digest_basis": basis,
                "unavailable_reason": "No supported payload supplied."}
    try:
        raw = payload.encode("utf-8") if isinstance(payload, str) else payload
    except UnicodeEncodeError:
        return {"sha256": None, "bytes": None, "digest_basis": basis,
                "unavailable_reason": "Supplied text is not encodable as UTF-8."}
    return {"sha256": sha256(raw).hexdigest(), "bytes": len(raw), "digest_basis": basis,
            "unavailable_reason": None}


def _metadata(value: str | None) -> dict:
    return {"value": value,
            "evidence_state": ("not_supplied_or_unavailable" if value is None
                               else "recorded_not_independently_verified"),
            "reason": ("Not supplied or unavailable." if value is None else
                       "Recorded caller metadata; not independently verified.")}


def _unit(origin, key, text, *, rule=None, bindings=None, occurrence=None,
          check_pointer=None, outcome=None, diagnostic=None):
    return {"unit_id": sha256((origin + ":" + key).encode("utf-8")).hexdigest(),
            "origin": origin, "rule_id": rule, "text": text,
            "bindings": [] if bindings is None else bindings,
            "candidate_occurrence_id": occurrence, "check_pointer": check_pointer,
            "check_outcome": outcome, "diagnostic_code": diagnostic}


def _diagnostic(report, code, location, message, severity="rejection"):
    report["validation"]["diagnostics"].append({
        "severity": severity, "code": code, "location": location, "message": message,
    })


def _reject(report, code, location, message):
    _diagnostic(report, code, location, message)
    report["report_state"] = "rejected"
    for field in ("source_records", "source_observations", "source_conditions",
                  "candidate_occurrences", "qualification_reasons", "narrative_units"):
        report[field] = []
    report["candidate_content"] = None
    return _Report.model_validate(report).model_dump(mode="json")


def _sources(document) -> list[_Source]:
    records = []
    for kind, collection, identifier in _SETS:
        values = document[collection]
        if isinstance(values, list):
            records.extend(_Source(kind, row[identifier], f"/{collection}/{index}", row)
                           for index, row in enumerate(values))
        else:
            records.append(_Source(kind, values[identifier], f"/{collection}", values))
    return records


def _bind(source: _Source, field: str, input_digest: str, missing=None) -> dict:
    value = _pointer(source.data, field)
    if missing is not None and (not isinstance(value, dict) or missing in value):
        raise _BindingError("missing-member binding is not absent")
    return {"input_sha256": input_digest, "record_type": source.kind,
            "record_id": source.identifier, "record_pointer": source.pointer,
            "field_pointer": field, "input_pointer": source.pointer + field,
            "value_json": _json(value), "missing_member": missing,
            "evidence_state": "verified_against_supplied_evidence"}


def _inspect(report, source, field, accepted_types):
    digest = report["artifacts"]["input"]["sha256"]
    parent_pointer, key = field.rsplit("/", 1)
    parent = _pointer(source.data, parent_pointer)
    if key not in parent:
        state, binding = "missing", _bind(source, parent_pointer, digest, missing=key)
    else:
        value = parent[key]
        state = ("explicit_null" if value is None else "available"
                 if type(value) in accepted_types and not (
                     isinstance(value, str) and not value.strip()) else "unsupported_or_unusable")
        binding = _bind(source, field, digest)
    report["source_conditions"].append({
        "record_type": source.kind, "record_id": source.identifier,
        "queried_field_pointer": field, "state": state, "binding": binding,
    })
    if state != "available":
        text = (f"In supplied {source.kind} {_json(source.identifier)}, field {_json(field)} "
                f"is {state}; no wider absence is inferred.")
        report["source_observations"].append(_unit(
            "source_template", digest + ":E05:" + source.pointer + field, text,
            rule="E05", bindings=[binding],
        ))
    return state, binding


def _observe(report, source, rule, key, text, bindings):
    report["source_observations"].append(_unit(
        "source_template", report["artifacts"]["input"]["sha256"] + ":" + rule + ":"
        + source.pointer + key, text, rule=rule, bindings=bindings,
    ))


def _source_observations(report, records, investigation):
    typed_tx = {row.transaction_id: row for row in investigation.transactions}
    for source in records:
        row = source.data
        if source.kind in ("case", "alert"):
            fields = (("case_id", "primary_alert_id") if source.kind == "case" else
                      ("alert_id", "transaction_ids"))
            bindings = [_inspect(report, source, "/" + field,
                                 (list,) if field == "transaction_ids" else (str,))[1]
                        for field in fields]
            _observe(report, source, "E01", "identity", "Supplied " + source.kind + " records "
                     + "; ".join(field + "=" + _json(row[field]) for field in fields)
                     + ". Alert membership does not establish suspiciousness.", bindings)
        elif source.kind == "transaction":
            fields = ("transaction_id", "amount", "currency", "direction", "transaction_type",
                      "occurred_at", "account_id", "counterparty_id")
            bindings = [_inspect(report, source, "/" + field,
                                 (str, int, Decimal) if field == "amount" else (str,))[1]
                        for field in fields]
            transaction = typed_tx[source.identifier]
            # JSON number parsing in the existing contract can round very large
            # fractional numbers. Never present that normalized value as supplied.
            if (type(row["amount"]) not in (str, int, Decimal)
                    or Decimal(row["amount"]) != transaction.amount):
                raise _NumericSourceError(source.pointer + "/amount")
            text = (f"Supplied transaction {_json(source.identifier)} records {transaction.currency} "
                    f"{transaction.amount:f} as {_json(row['direction'])} "
                    f"({_json(row['transaction_type'])}) at {_json(row['occurred_at'])}; "
                    f"account reference {_json(row['account_id'])}, counterparty reference "
                    f"{_json(row['counterparty_id'])}. No payment purpose or legitimacy is inferred.")
            _observe(report, source, "E02", "transaction", text, bindings)
        elif source.kind == "customer":
            prefix = "/expected_monthly_activity/"
            fields = ("minimum", "maximum", "currency", "typical_daily_cash_deposit_min",
                      "typical_daily_cash_deposit_max")
            inspected = {field: _inspect(report, source, prefix + field,
                                        (str,) if field == "currency" else (str, int, Decimal))
                         for field in fields}
            profile = row["expected_monthly_activity"]
            _observe(report, source, "E03", "monthly", "The supplied profile records expected "
                     f"monthly activity minimum {_json(profile['minimum'])}, maximum "
                     f"{_json(profile['maximum'])}, currency {_json(profile['currency'])}; "
                     "no hard individual-payment limit or personal authorship is inferred.",
                     [inspected[field][1] for field in fields[:3]])
            daily = fields[3:]
            if all(inspected[field][0] == "available" for field in daily):
                _observe(report, source, "E03", "daily", "The supplied profile records typical "
                         f"daily cash-deposit bounds {_json(profile[daily[0]])} to "
                         f"{_json(profile[daily[1]])}, currency {_json(profile['currency'])}; "
                         "no transaction-limit or materiality conclusion is inferred.",
                         [inspected[field][1] for field in (*daily, "currency")])
        elif source.kind == "evidence":
            fields = ("source", "evidence_type", "verification_status")
            bindings = [_inspect(report, source, "/" + field, (str,))[1] for field in fields]
            _observe(report, source, "E04", "metadata", "Supplied evidence "
                     + _json(source.identifier) + " records "
                     + "; ".join(field + "=" + _json(row[field]) for field in fields)
                     + ". A supplied status is not verification performed by this composer.", bindings)
            fact = ("claim" if row["evidence_type"] == "customer_explanation" else
                    "beneficiary_account_ref" if row["evidence_type"] in
                    ("supplier_invoice", "wire_payment_record") else None)
            if fact is not None:
                state, binding = _inspect(report, source, "/facts/" + fact, (str,))
                if state == "available":
                    suffix = (" This remains a recorded customer claim." if fact == "claim" else
                              " This is a recorded reference, not proof of recipient legitimacy.")
                    _observe(report, source, "E04", fact, "Supplied evidence "
                             + _json(source.identifier) + f" records {fact}="
                             + _json(row["facts"][fact]) + "." + suffix, [binding, *bindings])
        elif source.kind == "verification_check":
            fields = ("check_type", "status", "findings", "subject_evidence_ids")
            bindings = [_inspect(report, source, "/" + field,
                                 (list,) if field in ("findings", "subject_evidence_ids")
                                 else (str,))[1] for field in fields]
            _observe(report, source, "E04", "check", "Supplied verification-check record "
                     + _json(source.identifier) + " records "
                     + "; ".join(field + "=" + _json(row[field]) for field in fields)
                     + ". This composer did not independently execute that verification.", bindings)


def _occurrences(candidate, digest):
    result = []

    def add(text, pointer, section, citations, citation_pointer, kind="statement"):
        result.append({"occurrence_id": sha256((digest + pointer).encode("utf-8")).hexdigest(),
                       "candidate_sha256": digest, "json_pointer": pointer,
                       "statement_sha256": sha256(text.encode("utf-8")).hexdigest(),
                       "text": text, "section": section, "kind": kind,
                       "citation_pointer": citation_pointer, "submitted_citations": citations,
                       "semantic_review": "not_evaluated"})

    for field in ("rationale", "factual_findings", "interpretations", "unresolved_questions",
                  "missing_information"):
        rows = [("/rationale", candidate[field])] if field == "rationale" else [
            (f"/{field}/{index}", row) for index, row in enumerate(candidate[field])]
        for pointer, row in rows:
            add(row["statement"], pointer + "/statement", field,
                deepcopy(row["citations"]), pointer + "/citations")
    for index, row in enumerate(candidate["contradictions"]):
        pointer = f"/contradictions/{index}"
        add(row["description"], pointer + "/description", "contradictions", None, None,
            "contradiction_description")
        for side in ("left", "right"):
            add(row[side]["statement"], pointer + f"/{side}/statement", "contradictions",
                deepcopy(row[side]["citations"]), pointer + f"/{side}/citations")
    return result


def _comparison_units(report, sources):
    occurrences = {row["json_pointer"]: row for row in report["candidate_occurrences"]}
    units = []
    checks = report["restricted_checks"]
    for index, finding in enumerate(checks["findings"]):
        pointer = f"/factual_findings/{index}/statement"
        occurrence = occurrences[pointer]
        bindings = []
        for comparison in finding["comparisons"]:
            ref = comparison["source"]
            bindings.append(_bind(sources[(ref["record_type"], ref["record_id"])],
                                  ref["field_pointer"], report["artifacts"]["input"]["sha256"]))
        conflict = finding["outcome"] == "conflicts_with_record"
        text = ("RESTRICTED FIELD CONFLICT" if conflict else "Restricted amount check")
        text += ": " + finding["outcome"] + "; candidate " + _json(occurrence["text"])
        text += "; compared fields=" + _json(finding["comparisons"])
        text += ". " + finding["reason"] + " No whole-statement semantic approval."
        if conflict:
            _diagnostic(report, "restricted_conflict", pointer,
                        "Restricted fields conflict; inspect the original claim and source values.",
                        "qualification")
        units.append(_unit(
            "restricted_check", occurrence["occurrence_id"], text,
            rule=f"E06:{checks['check']}:{checks['check_version']}:{finding['predicate']}",
            bindings=bindings, occurrence=occurrence["occurrence_id"],
            check_pointer=f"/validation/audit/deterministic_fact_checks/findings/{index}",
            outcome=finding["outcome"], diagnostic="restricted_conflict" if conflict else None,
        ))
    return units


def _verify_bindings(report, document):
    digest = report["artifacts"]["input"]["sha256"]
    sources = {(source.kind, source.identifier): source for source in _sources(document)}
    for row in report["source_records"]:
        source = sources[(row["record_type"], row["record_id"])]
        if (row["input_sha256"] != digest or row["record_pointer"] != source.pointer
                or row["record_json"] != _json(source.data)):
            raise _BindingError("invalid record binding")
    bindings = [row["binding"] for row in report["source_conditions"]]
    bindings += [binding for unit in report["source_observations"] + report["narrative_units"]
                 for binding in unit["bindings"]]
    for binding in bindings:
        source = sources[(binding["record_type"], binding["record_id"])]
        pointer = source.pointer + binding["field_pointer"]
        if (binding["input_sha256"] != digest or binding["record_pointer"] != source.pointer
                or binding["input_pointer"] != pointer
                or binding["value_json"] != _json(_pointer(document, pointer))
                or binding["evidence_state"] != "verified_against_supplied_evidence"):
            raise _BindingError("invalid field binding")
        missing = binding["missing_member"]
        if missing is not None:
            parent = _pointer(document, pointer)
            if not isinstance(parent, dict) or missing in parent:
                raise _BindingError("invalid missing-member binding")


def compose_evidence_report(
    investigation_json: bytes, candidate_json: bytes | str | None, *,
    expected_identities: dict[str, str] | None = None,
    provenance: dict[str, str | None] | None = None,
    generation_status: str | None = None,
) -> dict:
    """Compose in memory from exact supplied payloads; return qualification or rejection.

    Unknown optional metadata stays unknown. Expected identities are checked, never
    discovered. No source observation is derived from candidate prose. Errors do not
    repair candidates or leak unexpected exception messages. No I/O or generation.
    """
    report = {
        "report_schema_version": REPORT_SCHEMA_VERSION, "composer_version": COMPOSER_VERSION,
        "template_version": TEMPLATE_VERSION, "report_state": "rejected", "case_identity": None,
        "artifacts": {"input": _artifact(investigation_json, "supplied_bytes"),
                      "candidate": _artifact(candidate_json, "utf8_encoded_candidate_text"
                                             if isinstance(candidate_json, str) else "supplied_bytes"),
                      "canonical_validated_input": _artifact(
                          None, "validated_input_canonical_json_utf8")},
        "provenance": {key: _metadata(None) for key in (*_METADATA, "generation_status")},
        "component_versions": {"composer": COMPOSER_VERSION, "template": TEMPLATE_VERSION,
                               "auditor": AUDITOR_VERSION, "amount_check": CHECK_VERSION},
        "source_records": [], "source_observations": [], "source_conditions": [],
        "candidate_content": None, "candidate_occurrences": [], "restricted_checks": None,
        "validation": {"audit": None, "diagnostics": [], "expected_identity_checks": []},
        "qualification_reasons": [],
        "narrative_units": [],
        "semantic_evaluation": {"status": "not_evaluated", "scoring_authorized": False},
        "limitations": list(_LIMITATIONS),
    }
    try:
        if (type(investigation_json) is not bytes
                or type(candidate_json) not in (bytes, str, type(None))
                or generation_status not in (None, "completed", "failed", "refused", "incomplete")
                or (provenance is not None and (type(provenance) is not dict
                    or set(provenance) - set(_METADATA)
                    or any(value is not None and (type(value) is not str or not value.strip())
                           for value in provenance.values())))
                or (expected_identities is not None and (type(expected_identities) is not dict
                    or set(expected_identities) - _EXPECTED
                    or any(type(value) is not str or (key.endswith("sha256") and
                               re.fullmatch(r"[0-9a-f]{64}", value) is None)
                           for key, value in expected_identities.items())))):
            return _reject(report, "invalid_arguments", None,
                           "Unsupported payload type, metadata or expected-identity configuration.")
        for key in _METADATA:
            report["provenance"][key] = _metadata((provenance or {}).get(key))
        report["provenance"]["generation_status"] = _metadata(generation_status)
        report["validation"]["expected_identity_checks"] = [
            {"name": key, "expected": value, "actual": None, "outcome": "not_evaluated"}
            for key, value in sorted((expected_identities or {}).items())
        ]
        if candidate_json is not None:
            audit = audit_packet(investigation_json, candidate_json)
            report["validation"]["audit"] = audit
            report["restricted_checks"] = deepcopy(audit["deterministic_fact_checks"])
            for key in ("package_version", "pydantic_version"):
                report["component_versions"][key] = audit["contracts"][key]
        else:
            audit = None
        try:
            investigation = InvestigationInput.model_validate_json(investigation_json)
        except ValidationError:
            return _reject(report, "invalid_investigation", None,
                           "Investigation contract rejected the supplied payload; see available audit.")
        report["case_identity"] = {"case_id": investigation.case.case_id,
                                   "alert_id": investigation.alert.alert_id}
        canonical = build_assessment_prompt(investigation)
        report["artifacts"]["canonical_validated_input"] = _artifact(
            canonical.input_json, "validated_input_canonical_json_utf8")
        actual = {"input_sha256": report["artifacts"]["input"]["sha256"],
                  "candidate_sha256": report["artifacts"]["candidate"]["sha256"],
                  "canonical_input_sha256": canonical.input_sha256, **report["case_identity"]}
        for check in report["validation"]["expected_identity_checks"]:
            check["actual"] = actual[check["name"]]
            check["outcome"] = ("unavailable" if check["actual"] is None else
                                "matched" if check["actual"] == check["expected"] else "mismatch")
        bad_checks = [c for c in report["validation"]["expected_identity_checks"]
                      if c["outcome"] != "matched"]
        if bad_checks:
            return _reject(report, "expected_identity_mismatch", "/" + bad_checks[0]["name"],
                           "A supplied expected identity does not match an available actual identity.")
        if generation_status in ("failed", "refused", "incomplete"):
            return _reject(report, "generation_not_completed", None,
                           "Supplied generation outcome is not a completed assessment.")
        if candidate_json is None:
            return _reject(report, "candidate_unavailable", None,
                           "No candidate supplied; this is not an assessment abstention.")
        if (set(audit["stages"]) != _STAGES
                or not all(stage["status"] == "passed" for stage in audit["stages"].values())):
            return _reject(report, "mechanical_validation_failed", "/validation/audit/stages",
                           "All three existing mechanical stages must pass; see original diagnostics.")
        for key, basis in (("input", "supplied_bytes"), ("candidate", "utf8_encoded_string"
                           if isinstance(candidate_json, str) else "supplied_bytes")):
            if (audit["artifacts"][key]["sha256"] != report["artifacts"][key]["sha256"]
                    or audit["artifacts"][key]["digest_basis"] != basis):
                raise _BindingError("audit representation mismatch")
        if audit["deterministic_fact_checks"]["status"] == "error":
            return _reject(report, "restricted_check_error", None,
                           "Existing restricted checker errored; no trustworthy comparison report.")
        document = json.loads(investigation_json, parse_float=Decimal)
        candidate = json.loads(candidate_json)
        records = _sources(document)
        digest = actual["input_sha256"]
        report["source_records"] = [{"input_sha256": digest, "record_type": source.kind,
                                     "record_id": source.identifier,
                                     "record_pointer": source.pointer,
                                     "record_json": _json(source.data)} for source in records]
        report["candidate_content"] = candidate
        report["candidate_occurrences"] = _occurrences(candidate, actual["candidate_sha256"])
        _source_observations(report, records, investigation)
        comparisons = _comparison_units(report, {(s.kind, s.identifier): s for s in records})
        report["report_state"] = "qualified_companion"
        reasons = ["bounded_scope", "unchecked_candidate_content"]
        if any(row["state"] != "available" for row in report["source_conditions"]):
            reasons.append("source_field_gaps")
        coverage = report["restricted_checks"]["coverage"]
        if coverage["conflicts_with_record"]:
            reasons.append("restricted_conflict")
        if coverage["not_checked"] or coverage["checked"] == 0:
            reasons.append("restricted_coverage_incomplete")
        if generation_status is None:
            reasons.append("generation_status_unavailable")
        report["qualification_reasons"] = reasons
        scope = _unit("diagnostic", "scope", "Preliminary synthetic decision support; human review "
                      "is required, not certified completed. This is not an overall factual or "
                      "semantic pass.", diagnostic="bounded_scope")
        producer = report["provenance"]["producer"]["value"]
        attribution = ("The supplied candidate" if producer is None else
                       "The supplied candidate (recorded producer " + _json(producer) + ")")
        scalar = _unit("candidate_quote", actual["candidate_sha256"] + ":assessment",
                       attribution + " records assessment_status=" + _json(candidate["assessment_status"])
                       + ", recommended_action=" + _json(candidate["recommended_action"])
                       + ", recommendation_scope=" + _json(candidate["recommendation_scope"])
                       + ", human_review_required=" + _json(candidate["human_review_required"]) + ".")
        quoted = [_unit("candidate_quote", row["occurrence_id"], attribution + " states "
                        + _json(row["text"]) + ". Semantic support is not evaluated.",
                        occurrence=row["occurrence_id"]) for row in report["candidate_occurrences"]]
        report["narrative_units"] = [scope, *deepcopy(report["source_observations"]),
                                     *comparisons, scalar, *quoted]
        _verify_bindings(report, document)
        return _Report.model_validate(report).model_dump(mode="json")
    except _NumericSourceError as error:
        return _reject(report, "source_numeric_normalization", str(error),
                       "Typed amount differs from the exact supplied value; no rounded "
                       "source observation or accepted companion is produced.")
    except _BindingError:
        return _reject(report, "source_binding_invalid", None,
                       "Mandatory source or audit representation binding did not validate.")
    except Exception:
        return _reject(report, "unexpected_error", None,
                       "Unexpected composition/audit error; details omitted, no accepted companion.")


def serialize_evidence_report(report: dict) -> bytes:
    """Validate report structure and encode deterministically; no source re-adjudication/I/O."""
    validated = _Report.model_validate(report).model_dump(mode="json")
    return (json.dumps(validated, sort_keys=True, indent=2, ensure_ascii=False,
                       allow_nan=False) + "\n").encode("utf-8")
