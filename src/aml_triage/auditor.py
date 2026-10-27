"""Mechanical audits of explicitly supplied investigation/candidate JSON pairs.

Report schema 1.0 (a JSON-serializable dictionary):
* report_schema_version, auditor_version: versions of this report and adapter.
* contracts: module, package/Pydantic versions and unavailable source revision.
* artifacts: input/candidate identity, SHA-256, digest basis, digest-unavailability
  reason and validated schema version (null when unavailable). File digests cover
  original bytes; string payload digests cover UTF-8. No Git or policy lookup occurs.
* stages: input_structure, output_structure, contextual_references. Each has
  status, reason, phase and diagnostics. Status is passed/failed/not_evaluated/error.
* semantic_evaluation: named, unimplemented dimensions, always not_evaluated.
* limitations: scope and diagnostic limitations, never an overall quality score.

Diagnostics contain type, message and location. Pydantic locations become JSON
arrays; contextual ValueError paths remain in the original message with a null
location. Validation inputs, exception context and tracebacks are not embedded.
Unexpected exception messages are omitted because they may contain payload data.
Only schema versions from successfully validated structures are reported.
"""

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError, __version__ as pydantic_version

from aml_triage import __version__ as package_version
from aml_triage.contracts import (
    InvestigationInput,
    InvestigationOutput,
    validate_investigation_output_references,
)


REPORT_SCHEMA_VERSION = "1.0"
AUDITOR_VERSION = "0.1.0"

_SEMANTIC_REASONS = {
    "factual_input_support": "Not implemented: cited records are not checked for claim support.",
    "submitted_citation_adequacy": (
        "Not implemented: citation existence does not establish adequacy."
    ),
    "material_finding_completeness": (
        "Not implemented: no material-finding annotations are applied."
    ),
    "missing_information_and_contradiction_coverage": (
        "Not implemented: uncertainty and source-conflict coverage require semantic review."
    ),
    "recommendation_quality": "Not implemented: no policy or provisional-label scoring occurs.",
    "abstention_appropriateness": (
        "Not implemented: structural abstention is not eligibility review."
    ),
    "fabricated_verification_and_unsupported_certainty": (
        "Not implemented: assertions and verification claims are not substantively reviewed."
    ),
    "semantic_preliminary_scope_compliance": (
        "Not implemented: prose is not reviewed; required literal fields do not prove human review."
    ),
    "leakage_and_held_out_independence": (
        "Not implemented: candidate context and exposure history are not audited."
    ),
}

_Model = TypeVar("_Model", bound=BaseModel)


def _stage(status: str, reason: str, phase: str, diagnostics: list | None = None) -> dict:
    return {
        "status": status,
        "reason": reason,
        "phase": phase,
        "diagnostics": [] if diagnostics is None else diagnostics,
    }


def _unexpected_error(error: Exception, phase: str) -> dict:
    return _stage("error", "Unexpected evaluator failure.", phase, [{
        "type": type(error).__name__,
        "message": "Unexpected evaluator failure; exception details are not included.",
        "location": None,
    }])


@dataclass
class _Artifact:
    identity: str | None
    payload: str | bytes | None
    digest_basis: str
    read_error: dict | None = None


def _read_artifact(path: str | Path) -> _Artifact:
    path = Path(path)
    try:
        return _Artifact(str(path), path.read_bytes(), "file_bytes")
    except OSError as error:
        result = _stage("error", "Could not read supplied artifact.", "ingestion", [{
            "type": type(error).__name__,
            "message": error.strerror or "Could not read supplied artifact.",
            "location": None,
        }])
    except Exception as error:
        result = _unexpected_error(error, "ingestion")
    return _Artifact(str(path), None, "file_bytes", result)


def _validate(artifact: _Artifact, model: type[_Model]) -> tuple[_Model | None, dict]:
    if artifact.read_error is not None:
        return None, artifact.read_error
    try:
        parsed = model.model_validate_json(artifact.payload)
    except ValidationError as error:
        diagnostics = [{
            "type": item["type"],
            "message": item["msg"],
            "location": list(item["loc"]),
        } for item in error.errors(include_input=False, include_context=False, include_url=False)]
        return None, _stage(
            "failed", "Existing contract rejected the JSON payload.", "validation", diagnostics,
        )
    except Exception as error:
        return None, _unexpected_error(error, "validation")
    return parsed, _stage("passed", "Existing contract accepted the JSON payload.", "validation")


def _artifact_metadata(artifact: _Artifact, model: BaseModel | None) -> dict:
    payload = artifact.payload
    unavailable_reason = "Artifact was not read." if payload is None else None
    if isinstance(payload, str):
        try:
            payload = payload.encode("utf-8")
        except UnicodeEncodeError:
            payload = None
            unavailable_reason = "Supplied string cannot be encoded as UTF-8."
    return {
        "identity": artifact.identity,
        "sha256": None if payload is None else sha256(payload).hexdigest(),
        "digest_basis": artifact.digest_basis,
        "digest_unavailable_reason": unavailable_reason,
        "validated_schema_version": None if model is None else model.schema_version,
    }


def _audit(investigation: _Artifact, candidate: _Artifact) -> dict[str, Any]:
    parsed_input, input_stage = _validate(investigation, InvestigationInput)
    parsed_output, output_stage = _validate(candidate, InvestigationOutput)
    blockers = [
        name for name, result in (
            ("input_structure", input_stage), ("output_structure", output_stage),
        ) if result["status"] != "passed"
    ]
    if blockers:
        context_stage = _stage(
            "not_evaluated", "Prerequisites did not pass: " + ", ".join(blockers) + ".",
            "prerequisites",
        )
    else:
        try:
            validate_investigation_output_references(parsed_input, parsed_output)
        except ValueError as error:
            context_stage = _stage(
                "failed", "Existing reference validator rejected the pair.", "references", [{
                    "type": type(error).__name__,
                    "message": str(error),
                    "location": None,
                }],
            )
        except Exception as error:
            context_stage = _unexpected_error(error, "references")
        else:
            context_stage = _stage(
                "passed", "Case/alert identities and typed citations resolve.", "references",
            )

    return {
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "auditor_version": AUDITOR_VERSION,
        "contracts": {
            "module": "aml_triage.contracts",
            "package_version": package_version,
            "pydantic_version": pydantic_version,
            "source_revision": None,
            "source_revision_reason": "Not discovered; no Git metadata lookup is performed.",
            "validation_entry_point": "model_validate_json",
        },
        "artifacts": {
            "input": _artifact_metadata(investigation, parsed_input),
            "candidate": _artifact_metadata(candidate, parsed_output),
        },
        "stages": {
            "input_structure": input_stage,
            "output_structure": output_stage,
            "contextual_references": context_stage,
        },
        "semantic_evaluation": {
            name: _stage("not_evaluated", reason, "semantic")
            for name, reason in _SEMANTIC_REASONS.items()
        },
        "limitations": [
            "Mechanical structure and identity checks only; no semantic quality judgment.",
            "Existing relationship/reference validators may stop at the first mismatch; "
            "diagnostics are not exhaustive.",
            "No reference answers, adjudication annotations or fictional policy are loaded.",
        ],
    }


def audit_packet(
    investigation_json: str | bytes, candidate_json: str | bytes,
    *, input_identity: str | None = None, candidate_identity: str | None = None,
) -> dict[str, Any]:
    """Audit original JSON payloads without file access, repairs or semantic scoring.

    Optional identities are caller-supplied labels, not inferred case identifiers.
    Strings are hashed as UTF-8; bytes are hashed exactly as supplied.
    """
    return _audit(
        _Artifact(
            input_identity, investigation_json,
            "utf8_encoded_string" if isinstance(investigation_json, str) else "supplied_bytes",
        ),
        _Artifact(
            candidate_identity, candidate_json,
            "utf8_encoded_string" if isinstance(candidate_json, str) else "supplied_bytes",
        ),
    )


def audit_packet_files(input_file: str | Path, candidate_file: str | Path) -> dict[str, Any]:
    """Read only the two explicit files, independently, and audit their original bytes."""
    investigation = _read_artifact(input_file)
    candidate = _read_artifact(candidate_file)
    return _audit(investigation, candidate)
