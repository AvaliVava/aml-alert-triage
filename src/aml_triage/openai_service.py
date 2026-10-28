"""One-shot Responses assessment adapter; importing it never creates an API client.

Live execution is disabled by default. Tests explicitly enable the same guard with
injected mock clients/transports. Request allowance counts SDK parse invocations,
not billed requests: local failures can occur before sending, and timeouts can occur
after processing. No automatic application or SDK retries are allowed.

Execution record 1.0 keeps structure, references, mechanics and unevaluated semantics
separate. Error messages are fixed allowlisted descriptions, never provider bodies,
request headers or exception strings. Original candidate text/audits are separate
synthetic artifacts, not redacted execution diagnostics. No prices are assumed.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from importlib.metadata import version
import json
import math
import os
from pathlib import Path
import re
import tempfile
from threading import Lock
from time import perf_counter
from typing import Any

from openai import (
    APIConnectionError, APIStatusError, APITimeoutError, AuthenticationError,
    BadRequestError, InternalServerError, OpenAI, OpenAIError, PermissionDeniedError,
    RateLimitError,
)
from pydantic import ValidationError

from aml_triage.auditor import audit_packet
from aml_triage.contracts import (
    InvestigationInput, InvestigationOutput, validate_investigation_output_references,
)
from aml_triage.openai_prompt import build_assessment_prompt


SERVICE_VERSION = "0.1.0"
_ERROR_MESSAGES = {
    "request_limit": "The one-request allowance is unavailable or already consumed.",
    "authentication": "Authentication failed; check credentials outside the execution log.",
    "permission": "The configured request is not permitted.",
    "invalid_schema": "The API rejected the structured-output schema.",
    "invalid_request": "The API rejected the request configuration.",
    "exhausted_credit": "The API reported unavailable quota or credit; no retry was made.",
    "rate_limit": "The API rate-limited the request; no retry was made.",
    "timeout": "The request timed out; server processing and billing may have occurred.",
    "connection": "The connection failed; server processing cannot be ruled out.",
    "server": "The API returned a server error; no retry was made.",
    "api_error": "The API operation failed; provider details are not logged.",
    "credentials_unavailable": "The API client could not obtain its configuration.",
    "sdk_parsing": "SDK parsing rejected the response; original candidate text is unavailable.",
    "output_validation": "The original candidate JSON failed the output contract.",
    "citation_validation": "Candidate identities or citations do not resolve.",
    "missing_output": "No parsed final assessment with original JSON text was available.",
    "ambiguous_output": "More than one final text part was returned; none was selected.",
    "response_mismatch": "Parsed SDK output differs from the original candidate JSON.",
    "refusal": "The model refused; refusal text is not copied to the execution log.",
    "incomplete": "The response was incomplete; no assessment was accepted.",
    "response_failed": "The response did not complete successfully.",
    "auditor_error": "Mechanical auditing did not complete successfully.",
    "unexpected_error": "Unexpected service failure; exception details are not logged.",
}


@dataclass(frozen=True)
class AssessmentConfig:
    model: str | None = None
    timeout_seconds: float = 60.0
    max_output_tokens: int | None = None
    reasoning_effort: str | None = None
    request_allowance: int = 0
    live_enabled: bool = False
    sdk_max_retries: int = 0
    application_max_retries: int = 0

    def __post_init__(self) -> None:
        if type(self.live_enabled) is not bool:
            raise ValueError("live_enabled must be boolean")
        if self.model is not None and (
            not isinstance(self.model, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}", self.model)
        ):
            raise ValueError("model must be an explicit identifier")
        if (type(self.timeout_seconds) not in (int, float)
                or not math.isfinite(self.timeout_seconds) or self.timeout_seconds <= 0):
            raise ValueError("timeout_seconds must be positive and finite")
        if self.max_output_tokens is not None and (
            type(self.max_output_tokens) is not int or self.max_output_tokens <= 0
        ):
            raise ValueError("max_output_tokens must be a positive integer")
        if type(self.request_allowance) is not int or self.request_allowance not in (0, 1):
            raise ValueError("request_allowance must be 0 or 1")
        for retries in (self.sdk_max_retries, self.application_max_retries):
            if type(retries) is not int or retries != 0:
                raise ValueError("automatic retries must be zero")
        if self.reasoning_effort is not None and self.reasoning_effort not in (
            "none", "minimal", "low", "medium", "high", "xhigh", "max",
        ):
            raise ValueError("unsupported reasoning_effort configuration")
        if self.live_enabled and (
            self.model is None or self.max_output_tokens is None or self.request_allowance != 1
        ):
            raise ValueError("live execution requires model, token ceiling and allowance 1")


@dataclass
class AssessmentRun:
    record: dict[str, Any]
    assessment: InvestigationOutput | None = None
    candidate_json: str | None = None
    audit: dict | None = None

    def artifact(self) -> dict:
        return {
            "execution": self.record,
            "assessment": (None if self.assessment is None
                           else self.assessment.model_dump(mode="json")),
            "candidate_json": self.candidate_json,
            "audit": self.audit,
        }


def _check(status: str, reason: str) -> dict:
    return {"status": status, "reason": reason}


def _request_id(value: Any) -> str | None:
    if isinstance(value, str) and re.fullmatch(r"req_[A-Za-z0-9_-]{1,128}", value):
        return value
    return None


def _api_category(error: Exception) -> str:
    code = getattr(error, "code", None)
    if any(value in ("insufficient_quota", "billing_hard_limit_reached", "credit_balance_exhausted")
           for value in (code, getattr(error, "type", None))):
        return "exhausted_credit"
    for cls, category in (
        (AuthenticationError, "authentication"), (PermissionDeniedError, "permission"),
        (APITimeoutError, "timeout"), (APIConnectionError, "connection"),
        (RateLimitError, "rate_limit"), (InternalServerError, "server"),
    ):
        if isinstance(error, cls):
            return category
    if isinstance(error, BadRequestError):
        schema_error = code in ("invalid_json_schema", "invalid_schema") or getattr(
            error, "param", None
        ) == "text.format.schema"
        return "invalid_schema" if schema_error else "invalid_request"
    return "api_error"


def _fail(run: AssessmentRun, category: str) -> AssessmentRun:
    run.record["status"] = "failed"
    run.record["error"] = {
        "category": category, "message": _ERROR_MESSAGES[category],
        "transient": category in ("rate_limit", "timeout", "connection", "server"),
        "retry_performed": False,
    }
    return run


class OpenAIAssessmentService:
    """One invocation allowance per instance, including concurrent callers/failures.

    A supplied client must implement OpenAI.with_options and responses.parse. The
    service forces zero retries and the configured timeout on its client copy.
    Injection alone never bypasses live_enabled or the one-request guard.
    """

    def __init__(self, config: AssessmentConfig | None = None, *, client: Any = None):
        self.config = config if config is not None else AssessmentConfig()
        self._client = client
        self._requests_used = 0
        self._lock = Lock()

    def assess(self, investigation: InvestigationInput) -> AssessmentRun:
        prompt = build_assessment_prompt(investigation)
        # Resolve against the submitted snapshot even if the caller later mutates its model.
        investigation = InvestigationInput.model_validate_json(prompt.input_json)
        config = self.config
        run = AssessmentRun({
            "record_schema_version": "1.0", "service_version": SERVICE_VERSION,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "case_id": investigation.case.case_id,
            "input_sha256": prompt.input_sha256,
            "input_digest_basis": "validated_input_canonical_json_utf8",
            "prompt_version": prompt.version, "prompt_sha256": prompt.instructions_sha256,
            "model": config.model, "sdk_version": version("openai"),
            "settings": {
                "timeout_seconds": config.timeout_seconds,
                "max_output_tokens": config.max_output_tokens,
                "reasoning_effort": config.reasoning_effort, "store": False,
                "request_allowance": config.request_allowance, "live_enabled": config.live_enabled,
                "sdk_max_retries": 0, "application_max_retries": 0,
            },
            "request_attempts": 0, "requests_used": self._requests_used,
            "request_id": None, "latency_ms": None,
            "usage": {"input_tokens": None, "output_tokens": None, "total_tokens": None},
            "candidate_sha256": None, "status": "dry_run", "error": None,
            "validation": {name: _check("not_evaluated", "No completed candidate validation.")
                           for name in ("valid_structure", "valid_citations", "mechanical_checks")},
            "semantic_evaluation": _check(
                "not_evaluated", "General semantic support and recommendation quality "
                "are unevaluated."
            ),
        })
        if not config.live_enabled:
            return run
        with self._lock:
            if self._requests_used >= config.request_allowance:
                run.record["requests_used"] = self._requests_used
                return _fail(run, "request_limit")
            # Reserve before creating/copying a client: concurrent calls cannot both proceed.
            self._requests_used += 1
            run.record["requests_used"] = self._requests_used
        owned_client = None
        started = perf_counter()
        try:
            if self._client is None:
                owned_client = OpenAI(base_url="https://api.openai.com/v1", max_retries=0,
                                      timeout=config.timeout_seconds)
                client = owned_client
            else:
                client = self._client.with_options(max_retries=0, timeout=config.timeout_seconds)
            request = {
                "model": config.model, "input": prompt.messages(),
                "text_format": InvestigationOutput, "max_output_tokens": config.max_output_tokens,
                "store": False,
            }
            if config.reasoning_effort is not None:
                request["reasoning"] = {"effort": config.reasoning_effort}
            run.record["request_attempts"] = 1
            response = client.responses.parse(**request)
        except ValidationError as error:
            run.record["validation"]["valid_structure"] = _check(
                "failed", "SDK Pydantic rejection."
            )
            run.record["validation_error_types"] = sorted({item["type"] for item in error.errors(
                include_input=False, include_context=False, include_url=False,
            )})
            return _fail(run, "sdk_parsing")
        except (APIStatusError, APIConnectionError) as error:
            run.record["request_id"] = _request_id(getattr(error, "request_id", None))
            return _fail(run, _api_category(error))
        except OpenAIError:
            category = ("credentials_unavailable"
                        if run.record["request_attempts"] == 0 else "api_error")
            return _fail(run, category)
        except Exception:
            return _fail(run, "unexpected_error")
        finally:
            run.record["latency_ms"] = round((perf_counter() - started) * 1000, 3)
            if owned_client is not None:
                try:
                    owned_client.close()
                except Exception:
                    run.record["client_cleanup_error"] = True
        try:
            run.record["request_id"] = _request_id(getattr(response, "_request_id", None))
            usage = getattr(response, "usage", None)
            for field in run.record["usage"]:
                value = getattr(usage, field, None)
                if type(value) is int and value >= 0:
                    run.record["usage"][field] = value
            messages = [item for item in (getattr(response, "output", None) or [])
                        if item.type == "message"]
            parts = [part for item in messages
                     if getattr(item, "phase", None) in (None, "final_answer")
                     for part in (getattr(item, "content", None) or [])
                     if part.type == "output_text"]
            if len(parts) == 1 and isinstance(parts[0].text, str):
                run.candidate_json = parts[0].text
                run.record["candidate_sha256"] = sha256(
                    run.candidate_json.encode("utf-8")
                ).hexdigest()
            if any(part.type == "refusal" for item in messages
                   for part in (getattr(item, "content", None) or [])):
                return _fail(run, "refusal")
            if response.status == "incomplete":
                return _fail(run, "incomplete")
            if response.status != "completed":
                return _fail(run, "response_failed")
            if len(parts) > 1:
                return _fail(run, "ambiguous_output")
            if run.candidate_json is None:
                return _fail(run, "missing_output")
            return self._validate(
                run, prompt.input_json, investigation, getattr(parts[0], "parsed", None)
            )
        except Exception:
            return _fail(run, "unexpected_error")

    @staticmethod
    def _validate(run: AssessmentRun, input_json: str, investigation: InvestigationInput,
                  sdk_parsed: Any) -> AssessmentRun:
        try:
            run.audit = audit_packet(input_json, run.candidate_json)
        except Exception:
            run.record["validation"]["mechanical_checks"] = _check(
                "error", "Auditor raised unexpectedly."
            )
            return _fail(run, "auditor_error")
        stages = run.audit["stages"]
        for result, source in (("valid_structure", "output_structure"),
                               ("valid_citations", "contextual_references")):
            run.record["validation"][result] = _check(
                stages[source]["status"], stages[source]["reason"]
            )
        mechanical = "passed" if all(s["status"] == "passed" for s in stages.values()) else "failed"
        if any(s["status"] == "error" for s in stages.values()):
            mechanical = "error"
        run.record["validation"]["mechanical_checks"] = _check(
            mechanical, "Existing auditor stages only."
        )
        try:
            output = InvestigationOutput.model_validate_json(run.candidate_json)
        except ValidationError:
            return _fail(run, "output_validation")
        try:
            validate_investigation_output_references(investigation, output)
        except ValueError:
            return _fail(run, "citation_validation")
        if not isinstance(sdk_parsed, InvestigationOutput):
            return _fail(run, "missing_output")
        if sdk_parsed.model_dump() != output.model_dump():
            return _fail(run, "response_mismatch")
        if mechanical != "passed":
            return _fail(run, "auditor_error")
        run.assessment = output
        run.record["status"] = "validated"
        return run


def publish_run(run: AssessmentRun, output: str | Path) -> Path:
    """Atomically hard-link a complete JSON bundle; never overwrite a destination.

    candidate_json retains the original Unicode text; its SHA covers UTF-8 text,
    not the API HTTP envelope. The CLI confines runs to ignored outputs/.
    """
    target = Path(output).absolute()
    if target.suffix != ".json" or ".." in Path(output).parts:
        raise ValueError("output must be a new .json file without parent traversal")
    if target.exists() or target.is_symlink():
        raise FileExistsError("output already exists")
    payload = (json.dumps(run.artifact(), indent=2, ensure_ascii=False,
                          allow_nan=False) + "\n").encode("utf-8")
    with tempfile.TemporaryDirectory(prefix=".openai-run-", dir=target.parent) as folder:
        staged = Path(folder) / "run.json"
        staged.write_bytes(payload)
        if staged.read_bytes() != payload:
            raise OSError("staged run differs from serialized bytes")
        os.link(staged, target)
    return target
