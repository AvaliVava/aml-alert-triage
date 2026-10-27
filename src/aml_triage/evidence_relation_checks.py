"""Evaluation-only G04 beneficiary-reference comparison with separate citation coverage.

evaluate_evidence_relationships takes three independently supplied JSON strings or
byte payloads: investigation, candidate and evaluator-authored annotations. It
does no file, policy, reference-answer or model access and never edits payloads.
The existing auditor and its report/CLI contracts are not changed or invoked.

Annotation schema 1.0: schema_version="1.0", review_status="unreviewed_development_example",
case_id, investigation_sha256, candidate_sha256, and findings (an actual list).
Each annotation requires finding_index, exact statement, asserted_relationship
("different" or "equal"), left_evidence_id="EV-004", right_evidence_id="EV-005",
and transaction_id="TX-105". An index may be annotated only once. SHA-256 binds
original bytes, or the UTF-8 encoding of strings, without JSON canonicalization.
All bundle bindings must pass before any annotation is applied.

The operator must supply annotations separately from candidate generation. Hashes
prevent stale reuse, not dishonest annotation authorship. These are unreviewed
development interpretations, not approved ground truth. No prose entailment is
inferred or verified, even when annotation text exactly matches the candidate.

Predicate 1.0 compares exact non-whitespace string values at
/facts/beneficiary_account_ref in EV-004 (supplier_invoice) and EV-005
(wire_payment_record); both must explicitly reference supplied TX-105. No value,
ID, citation or source is trimmed, normalized or inferred from a check's status.
Source dependency failures leave both dimensions not_evaluated. For eligible
sources, record consistency is independent of whether both typed evidence IDs
are cited in this particular finding. CHK-G04-02 and unrelated citations cannot
replace either source under this narrow policy; this is not a universal rule.

Report 1.0 contains artifact digests, validation stages, per-finding independent
outcomes, exact typed source/field dependencies, missing citation IDs and coverage
over all candidate factual findings. Unknown totals are null for invalid outputs.
Invalid annotation configuration is a validation failure, never a false claim.
No overall quality score or general semantic judgment is produced.
"""

from hashlib import sha256
from typing import Annotated, Literal, Self, TypeVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from aml_triage.contracts import (
    InvestigationInput,
    InvestigationOutput,
    validate_investigation_output_references,
)


_Text = Annotated[str, Field(min_length=1)]
_Digest = Annotated[str, Field(min_length=64, max_length=64, pattern=r"^[0-9a-f]+$")]
_Model = TypeVar("_Model", bound=BaseModel)


class BeneficiaryReferenceAnnotation(BaseModel):
    """Evaluator-supplied proposition; it is never extracted from candidate prose."""

    model_config = ConfigDict(extra="forbid", strict=True)

    finding_index: int = Field(ge=0)
    statement: _Text
    asserted_relationship: Literal["different", "equal"]
    left_evidence_id: Literal["EV-004"]
    right_evidence_id: Literal["EV-005"]
    transaction_id: Literal["TX-105"]


class EvidenceRelationAnnotations(BaseModel):
    """Versioned, unreviewed development bundle, separate from investigation contracts."""

    model_config = ConfigDict(extra="forbid", strict=True)

    schema_version: Literal["1.0"]
    review_status: Literal["unreviewed_development_example"]
    case_id: _Text
    investigation_sha256: _Digest
    candidate_sha256: _Digest
    findings: list[BeneficiaryReferenceAnnotation]

    @model_validator(mode="after")
    def unique_finding_indexes(self) -> Self:
        indexes = [item.finding_index for item in self.findings]
        if len(set(indexes)) != len(indexes):
            raise ValueError("Each factual finding may have only one relationship annotation")
        return self


def _stage(status: str, reason: str, diagnostics: list | None = None) -> dict:
    return {"status": status, "reason": reason,
            "diagnostics": [] if diagnostics is None else diagnostics}


def _error(error: Exception) -> dict:
    return _stage("error", "Unexpected evaluator error; no relationship judgment.", [{
        "type": type(error).__name__, "message": "Unexpected evaluator error.", "location": None,
    }])


def _parse(payload: str | bytes | None, model: type[_Model]) -> tuple[_Model | None, dict]:
    try:
        parsed = model.model_validate_json(payload)
    except ValidationError as error:
        diagnostics = [{"type": item["type"], "message": item["msg"], "location": list(item["loc"])}
                       for item in error.errors(include_input=False, include_context=False,
                                                include_url=False)]
        return None, _stage("failed", f"{model.__name__} rejected the payload.", diagnostics)
    except Exception as error:
        return None, _error(error)
    return parsed, _stage("passed", f"{model.__name__} accepted the payload.")


def _artifact(payload: str | bytes | None) -> dict:
    basis = None if payload is None else (
        "utf8_encoded_string" if isinstance(payload, str) else "supplied_bytes"
    )
    try:
        data = payload.encode("utf-8") if isinstance(payload, str) else payload
    except UnicodeEncodeError:
        data = None
    return {"sha256": None if data is None else sha256(data).hexdigest(), "digest_basis": basis}


def _binding_errors(annotations, investigation, output, artifacts) -> list[dict]:
    errors = []
    for field, expected in (
        ("case_id", investigation.case.case_id),
        ("investigation_sha256", artifacts["investigation"]["sha256"]),
        ("candidate_sha256", artifacts["candidate"]["sha256"]),
    ):
        if getattr(annotations, field) != expected:
            errors.append({"type": "annotation_binding", "location": [field],
                           "message": f"{field} does not match the supplied artifact."})
    for position, annotation in enumerate(annotations.findings):
        if annotation.finding_index >= len(output.factual_findings):
            field, message = "finding_index", "Annotated finding index is out of range."
        elif annotation.statement != output.factual_findings[annotation.finding_index].statement:
            field = "statement"
            message = "Annotation text does not exactly match the indexed finding."
        else:
            continue
        errors.append({"type": "annotation_binding", "location": ["findings", position, field],
                       "message": message})
    return errors


def _empty_finding(index: int, reason: str) -> dict:
    return {
        "finding_index": index, "finding_path": f"factual_findings[{index}]",
        "annotation_index": None, "asserted_relationship": None, "recorded_relationship": None,
        "required_evidence_ids": [], "missing_citation_ids": None, "source_dependencies": [],
        "recorded_relationship_consistency": {"outcome": "not_evaluated", "reason": reason},
        "submitted_direct_source_coverage": {"outcome": "not_evaluated", "reason": reason},
        "diagnostics": [],
    }


def _evaluate(annotation, position: int, investigation, output) -> dict:
    result = _empty_finding(annotation.finding_index, "Source dependencies are not eligible.")
    required = [annotation.left_evidence_id, annotation.right_evidence_id]
    submitted = {citation.record_id for citation in
                 output.factual_findings[annotation.finding_index].citations
                 if citation.record_type == "evidence"}
    missing = [identifier for identifier in required if identifier not in submitted]
    result.update(annotation_index=position, asserted_relationship=annotation.asserted_relationship,
                  required_evidence_ids=required, missing_citation_ids=missing)
    evidence = {record.evidence_id: record for record in investigation.evidence}
    dependencies, errors, values = [], [], []
    if not any(record.transaction_id == annotation.transaction_id
               for record in investigation.transactions):
        errors.append({
            "record_type": "transaction", "record_id": annotation.transaction_id,
            "field_pointer": "/transaction_id", "message": "Required transaction absent.",
        })
    else:
        dependencies.append({
            "record_type": "transaction", "record_id": annotation.transaction_id,
            "field_pointer": "/transaction_id", "value": annotation.transaction_id,
        })
    for identifier, expected_type in zip(required, ("supplier_invoice", "wire_payment_record")):
        record = evidence.get(identifier)
        if record is None:
            errors.append({"record_type": "evidence", "record_id": identifier,
                           "field_pointer": "/evidence_id", "message": "Required evidence absent."})
            continue
        value = record.facts.get("beneficiary_account_ref")
        for field, observed, valid in (
            ("/evidence_type", record.evidence_type, record.evidence_type == expected_type),
            ("/related_transaction_ids", record.related_transaction_ids,
             annotation.transaction_id in record.related_transaction_ids),
            ("/facts/beneficiary_account_ref", value,
             isinstance(value, str) and bool(value.strip())),
        ):
            dependency = {"record_type": "evidence", "record_id": identifier,
                          "field_pointer": field}
            if valid:
                dependencies.append({**dependency, "value": observed})
            else:
                errors.append({**dependency, "message": "Missing or ineligible source field."})
        values.append(value)
    result.update(source_dependencies=dependencies, diagnostics=errors)
    if errors:
        return result
    recorded = "equal" if values[0] == values[1] else "different"
    result["recorded_relationship"] = recorded
    result["recorded_relationship_consistency"] = {
        "outcome": "matches_supplied_records" if recorded == annotation.asserted_relationship
        else "conflicts_with_supplied_records",
        "reason": f"Exact recorded beneficiary account references are {recorded}.",
    }
    result["submitted_direct_source_coverage"] = {
        "outcome": "required_sources_missing" if missing else "required_sources_cited",
        "reason": "Both direct evidence citations are required for this predicate; "
        "verification-check and unrelated citations do not substitute.",
    }
    return result


def _coverage(findings: list[dict], total: int | None) -> dict:
    coverage = {"total_findings": total}
    for dimension, outcomes in (
        ("recorded_relationship_consistency", ("matches_supplied_records",
                                               "conflicts_with_supplied_records")),
        ("submitted_direct_source_coverage", ("required_sources_cited",
                                             "required_sources_missing")),
    ):
        counts = {outcome: sum(item[dimension]["outcome"] == outcome for item in findings)
                  for outcome in outcomes}
        checked = sum(counts.values())
        coverage[dimension] = {**counts, "checked": checked,
                               "not_evaluated": None if total is None else total - checked}
    return coverage


def evaluate_evidence_relationships(
    investigation_json: str | bytes, candidate_json: str | bytes,
    annotations_json: str | bytes | None,
) -> dict:
    """Evaluate supplied JSON with independently authored, unreviewed annotations.

    Missing, malformed or stale annotations block judgments, not candidate validity.
    No annotations are generated from candidate text or loaded from any file.
    """
    investigation, input_stage = _parse(investigation_json, InvestigationInput)
    output, output_stage = _parse(candidate_json, InvestigationOutput)
    annotations, annotation_stage = _parse(annotations_json, EvidenceRelationAnnotations)
    artifacts = {"investigation": _artifact(investigation_json),
                 "candidate": _artifact(candidate_json), "annotations": _artifact(annotations_json)}
    validation = {"input_structure": input_stage, "output_structure": output_stage,
                  "annotation_structure": annotation_stage}
    context = _stage("not_evaluated", "Both investigation and candidate structures must pass.")
    if input_stage["status"] == output_stage["status"] == "passed":
        try:
            validate_investigation_output_references(investigation, output)
        except ValueError as error:
            context = _stage("failed", "Existing contextual validator rejected the pair.", [{
                "type": type(error).__name__, "message": str(error), "location": None,
            }])
        except Exception as error:
            context = _error(error)
        else:
            context = _stage("passed", "Case/alert identities and typed citations resolve.")
    validation["contextual_references"] = context
    binding = _stage("not_evaluated", "Valid structures, references and annotations required.")
    if all(stage["status"] == "passed" for stage in validation.values()):
        errors = _binding_errors(annotations, investigation, output, artifacts)
        binding = _stage(
            "failed" if errors else "passed",
            "Annotation bindings rejected." if errors else "Exact annotation bindings match.",
            errors,
        )
    validation["annotation_binding"] = binding
    total = None if output is None else len(output.factual_findings)
    ready = all(stage["status"] == "passed" for stage in validation.values())
    findings = [] if total is None else [
        _empty_finding(index, "Finding is unannotated." if ready else
                       "Evaluator prerequisites did not pass; see validation diagnostics.")
        for index in range(total)
    ]
    if ready:
        for position, annotation in enumerate(annotations.findings):
            try:
                findings[annotation.finding_index] = _evaluate(
                    annotation, position, investigation, output,
                )
            except Exception as error:
                finding = _empty_finding(annotation.finding_index, "Unexpected evaluator error.")
                finding.update(annotation_index=position,
                               asserted_relationship=annotation.asserted_relationship,
                               diagnostics=_error(error)["diagnostics"])
                findings[annotation.finding_index] = finding
    return {
        "report_schema_version": "1.0", "evaluator_version": "0.1.0",
        "predicate": "g04_beneficiary_account_refs_v1",
        "annotation_review_status": None if annotations is None else annotations.review_status,
        "artifacts": artifacts, "validation": validation,
        "findings": findings, "coverage": _coverage(findings, total),
        "limitations": [
            "Unreviewed development annotations; authorship and prose entailment are not checked.",
            "Only the specified record relationship and finding-level citation rule are checked.",
            "No fraud, authenticity, fund tracing, policy, recommendation "
            "or verification judgment.",
        ],
    }
