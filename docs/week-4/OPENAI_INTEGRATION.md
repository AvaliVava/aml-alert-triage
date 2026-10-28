# Week 4, Checkpoint 2 — OpenAI assessment service

**Local implementation, verified with mocks only. No hosted requests or credentials used.**

Preflight confirmed a clean `feature/week-4-openai-integration` branch at `4e95484`, the PR #10 merge. The existing contracts, baseline, policy and datasets are unchanged. This implements an API adapter, not evidence authentication, adjudicated AML policy or a measured classifier.

## Modules and Python interface

- [openai_prompt.py](../../src/aml_triage/openai_prompt.py): fixed developer instructions and separate canonical investigation JSON. No file access, policy lookup, reference answers, manifest, tools or conversation history are added to the request.
- [openai_service.py](../../src/aml_triage/openai_service.py): configuration, one-request guard, lazy SDK construction, response handling, validation, execution records and atomic bundle publication.
- [run_openai_assessment.py](../../scripts/run_openai_assessment.py): one-input CLI, default dry run, explicit live opt-in and output confinement to ignored `outputs/`.
- [test_openai_service.py](../../tests/test_openai_service.py): injected clients and the installed SDK parser on `httpx2.MockTransport`; API tests block socket connections. CLI live-path tests inject a mock service.

```python
from aml_triage.openai_service import AssessmentConfig, OpenAIAssessmentService

# Safe configuration inspection: no client or credential is created/read.
run = OpenAIAssessmentService(AssessmentConfig()).assess(validated_investigation)
assert run.record["status"] == "dry_run"
```

`assess` requires an `InvestigationInput`. It snapshots and revalidates its serialized data before any request, protecting citation resolution from subsequent caller mutation. Wrong input types, invalidated input instances and invalid configuration raise before execution. API/response/validation failures return an `AssessmentRun` with no accepted assessment, a structured error category and execution metadata. Its `assessment` is an `InvestigationOutput` only when structure, references and auditor stages pass. `candidate_json` and `audit` are separate attributes; `artifact()` returns the JSON-serializable bundle.

## Dependency and compatibility evidence

Pinned **`openai==3.40.0`** in [pyproject.toml](../../pyproject.toml), the published version verified from PyPI during this checkpoint. The dependency-review correction adds [constraints.txt](../../constraints.txt), containing the exact 14-package application dependency closure used by the tested service. It was derived by traversing the SDK and Pydantic requirements, not by freezing the whole developer environment. Pydantic remains **2.14.1**, with its existing `>=2.14.1,<3` project requirement unchanged. No existing runtime package was upgraded.

The SDK declares Python `>=3.10` and Pydantic `>=1.10.13,<3` with exclusions for early V2 versions. Its new dependencies include anyio, httpx2/httpcore2, jiter and sniffio; the installed HTTP stack requires Python `>=3.11`, consistent with this project's unchanged Python 3.11–3.13 range. Existing typing-extensions satisfies the SDK requirement. Optional SDK extras were not installed.

Installed versions include SDK 3.40.0, Pydantic 2.14.1/pydantic-core 2.50.1, httpx2/httpcore2 2.16.0, jiter 0.18.0 and anyio 4.15.1. A requirement-graph audit evaluated environment markers and `Requires-Python` for Python 3.11, 3.12 and 3.13 on Windows and Linux: every active dependency is present, satisfies its constraints and is pinned; no unrelated package is included. Published Windows amd64 and Linux x86_64 wheels exist for both binary dependencies on all three versions.

Verification performed during the dependency-review correction, using pip 24.0:

| Target | Actually executed | Limits |
| --- | --- | --- |
| Windows amd64, CPython 3.11.9 | Fresh temporary virtual environment; constrained editable install; smoke check; `pip check`; all **358 tests passed**. Existing environment also passed 358 tests and `pip check`. | Only locally installed supported interpreter. |
| CPython 3.11, Windows amd64 and Linux x86_64 | Targeted pip resolution/download of all **14 wheels** succeeded for both targets. | Linux wheels were downloaded on Windows, not executed on Linux. |
| CPython 3.12 and 3.13, Windows amd64 and Linux x86_64 | Requirement/marker closure and `Requires-Python` checks passed; published binary-wheel availability checked. | Four targeted pip resolution/download probes timed out after 150 seconds each; a Windows 3.12 retry outside the sandbox also timed out. No completed install or runtime test on these interpreters. |

These bounded timeouts do not demonstrate a dependency conflict or a successful cross-version installation. The 3.12 retry reached the pydantic-core wheel download, but did not finish. Earlier unpinned probes also timed out; these results supersede their verification status without claiming remote CI passed. **GitHub Actions remains unverified.** The configured 3.11/3.12/3.13 matrix is the next source of actual Linux runtime evidence.

Development setup and the [CI matrix](../../.github/workflows/foundation-tests.yml) now install with `python -m pip install -c constraints.txt -e .`, followed by dependency checks and the full tests. Constraints restrict dependency versions while [project metadata](../../pyproject.toml) still determines what to install; they do not install unrelated packages on their own. A plain `pip install -e .` bypasses these pins. The Windows and Unix commands in [README.md](../../README.md) and [START_HERE.md](../../START_HERE.md) consume the same file. See pip's official [constraints documentation](https://pip.pypa.io/en/stable/user_guide/#constraints-files) and [repeatable-install guidance](https://pip.pypa.io/en/stable/topics/repeatable-installs/).

This is a **runtime version constraints mechanism**, not a hash-verified artifact lock or byte-identical environment specification. It excludes pip, isolated build tools, interpreter patch releases and optional SDK extras. Different supported platforms install different wheels at the same versions. Index availability and trust remain necessary; macOS, ARM and free-threaded Python were not verified. No new dependency manager or build-tool upgrade is needed for this correction.

For a deliberate dependency update, use a fresh supported virtual environment, review the declared root requirements and their complete transitive closure, then update only the affected exact pins. Recheck markers/`Requires-Python` for every supported target, resolve/download wheels for Windows amd64 and Linux x86_64 on 3.11/3.12/3.13, and rerun fresh installation, `pip check` and the complete suite. Do not regenerate this file from an unrelated personal environment. Review the constraints diff with the implementation change; the existing CI matrix provides the actual Linux runtime checks when run remotely. Broader artifact-hash/build-tool locking would be a separate change if required.

The prior [compatibility report](OPENAI_SCHEMA_COMPATIBILITY.md) remains historical; no schema adapter or duplicate transport contract was added. Official [Python SDK documentation](https://developers.openai.com/api/reference/python) and the [Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses) informed this implementation.

## Prompt and request

Prompt version: **`aml-preliminary-1.0`**. SHA-256 of the exact UTF-8 developer instructions: `f6472c5d27337626e113cfa982297b0c6b317282eefc4a600f049fa025bb6c83`. Instruction edits must receive a new version; hashes record actual content independently of the version name.

The developer message constrains the task to supplied synthetic records. It treats record contents as data, separates observations and interpretations, requires typed citations, preserves missing/conflicting information, prohibits invented verification/documents/authorizations, allows explicit abstention and requires preliminary scope plus human review. It does not invent closure criteria or supply an adjudicated rubric. A `policy_id` is not treated as policy text. Recorded check statuses are not new work performed by the software. This instruction boundary is not a proof of prompt-injection resistance.

The user message contains only `InvestigationInput.model_dump(mode="json")`, serialized deterministically with sorted keys, compact separators and UTF-8 Unicode. Its hash covers canonical validated-model JSON, not original file formatting. The CLI additionally records the original input file's SHA-256. No golden reference labels or evaluation annotations are loaded.

Requests use `client.responses.parse(..., text_format=InvestigationOutput)`, `store=False`, the configured model and output-token ceiling. Reasoning effort is omitted unless explicitly configured; model-specific support is left to the API's validation. The service does not infer capabilities from model names or route requests to other providers. The default client uses the OpenAI API endpoint; injected clients are explicit caller-owned boundaries.

## Execution guards and configuration

| Setting | Behavior |
| --- | --- |
| `live_enabled` | Default `False`; even an injected client cannot bypass it. |
| `model` | No default; explicit nonempty identifier required for live execution. |
| `max_output_tokens` | No default ceiling; positive integer required for live execution. |
| `request_allowance` | Default 0; only 0 or 1 permitted; live execution requires 1. |
| `timeout_seconds` | Default 60; positive finite SDK timeout, not a guaranteed overall billing deadline. |
| `reasoning_effort` | Optional SDK vocabulary; omit for unsupported models. No model-support guarantee. |
| SDK/application retries | Must both be zero. Supplied clients are copied with `with_options(max_retries=0, timeout=...)`. |

A lock reserves the single allowance before client creation, including concurrent callers. Setup failures consume the reservation conservatively, even if no SDK request was attempted. `request_attempts` counts `responses.parse` invocations; it is not a count of billable server executions. Reusing a service after success, error or timeout cannot initiate a second attempt. A new process/service instance has a new local allowance; this is not a global spending-control system.

No application retry, batch execution or monetary estimate is implemented. Usage is recorded only when supplied by the API. A timeout/connection error may occur after server processing; local guards and `store=False` are not guaranteed billing caps or claims about provider data retention. Review failures deliberately before authorizing a separate invocation.

## Validation and response handling

1. Accept only a completed response with exactly one final (or legacy unphased) output-text part. Refusals, incomplete/failed responses, missing parsed output and ambiguous final parts are failures. Commentary is not concatenated into candidate JSON.
2. Preserve that part's original Unicode text and SHA-256 of its UTF-8 encoding. No trimming, repair, field insertion or silent deduplication occurs.
3. Run the existing `audit_packet` against the submitted input snapshot and original candidate. Preserve its full report separately.
4. Revalidate the original text with `InvestigationOutput.model_validate_json`, explicitly run `validate_investigation_output_references`, and confirm consistency with the SDK-parsed object. A reserialized SDK object never substitutes for the original candidate.
5. Return the typed assessment only when the three mechanical stages pass. A restricted amount conflict can still accompany structurally/citation-valid output; it remains visible in the audit. General semantic support, citation adequacy, completeness, recommendation quality and abstention appropriateness remain unevaluated.

The SDK already runs Pydantic during parsing. **If it raises `ValidationError` before returning, original candidate text, response status, request ID and usage may be unavailable to this adapter.** The record uses `sdk_parsing`, failed structure and safe Pydantic error types; no raw response or metadata is fabricated. This can also mask an underlying incomplete response whose partial JSON fails parsing. No raw-HTTP interception or alternative parsing architecture was added. Exact server/schema behavior still needs an authorized live test.

## Error categories and execution records

Expected categories include `authentication`, `permission`, `invalid_schema`, `invalid_request`, `exhausted_credit`, `rate_limit`, `timeout`, `connection`, `server`, `api_error`, `credentials_unavailable`, `sdk_parsing`, `output_validation`, `citation_validation`, `refusal`, `incomplete`, `response_failed`, `missing_output`, `ambiguous_output`, `response_mismatch`, `auditor_error` and `request_limit`. Unexpected exceptions become `unexpected_error` without their messages or tracebacks. API schema/credit classification uses recognized error codes (and a schema parameter), not copied provider prose. Unrecognized API errors stay generic.

Execution record **1.0**, service **0.1.0**, contains case/input identity, prompt version/hash, model/SDK, request settings, UTC start, allowance/attempt counts, available request ID, measured local SDK-operation latency, optional input/output/total tokens, candidate hash, final status and error category. Request IDs are allowlisted. Provider error bodies, authorization headers, keys, payment details and exception messages are excluded. Missing usage is null, never fabricated as zero. No cost or accuracy estimate is produced.

`validation.valid_structure`, `validation.valid_citations` and `validation.mechanical_checks` have separate status/reason entries; `semantic_evaluation` always states `not_evaluated`. Top-level `validated` means only structure/citation/mechanical acceptance. The audit preserves its nine broad unevaluated dimensions and restricted factual-check section. Auditor crashes are distinguished from candidate rejection.

`publish_run` writes one JSON bundle with `execution`, validated `assessment` or null, original `candidate_json` or null, and the separate `audit` or null. Raw candidate/audit artifacts deliberately preserve synthetic text; they are not a general-purpose secret-redaction service. The API key is never part of the prompt. Inspect artifacts before sharing.

Publication stages complete serialized bytes on the same filesystem, checks them, then uses an atomic no-overwrite hard link. Existing files/symlinks are refused; unsupported hard links fail without a partial destination. The library helper requires an existing parent and an explicit new JSON path; callers must keep artifacts in appropriate ignored/local storage. The CLI confines output to this repository's ignored `outputs/`, rejects parent traversal and resolved escapes, and validates input/destination before any request. A later publication failure is reported with execution metadata and never triggers a retry; the complete bundle may be unavailable. Abrupt process interruption can leave temporary staging content.

## CLI and future credentials workflow

Install the reviewed project environment normally:

```powershell
.\.venv\Scripts\python.exe -m pip install -c constraints.txt -e .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts\run_openai_assessment.py --help
.\.venv\Scripts\python.exe scripts\run_openai_assessment.py --input data\golden_cases\inputs\G02.json
```

The last command is a **dry run**, with zero request attempts, no client construction and no credential access. An optional `--output outputs/openai/new-inspection.json` saves the dry-run bundle. Importing modules and checking help do not call a model.

Only after separate human authorization and an agreed model/token/cost limit, configure `OPENAI_API_KEY` in the process environment or approved external secret store. Do not paste a key into command history or commit it. For a future PowerShell session, an interactive secure prompt can populate the environment:

```powershell
# FUTURE AUTHORIZED SESSION ONLY — not executed in this checkpoint.
$key = Read-Host 'OpenAI API key' -AsSecureString
$env:OPENAI_API_KEY = [System.Net.NetworkCredential]::new('', $key).Password
```

The SDK reads its process environment only when the live client is constructed. No `.env` loader or new secret-management dependency was added; existing ignore rules do not make committing secrets acceptable.

Illustrative **future** one-request command, not run here (replace the model and agree the token ceiling first):

```powershell
.\.venv\Scripts\python.exe scripts\run_openai_assessment.py `
  --input data\golden_cases\inputs\G02.json `
  --live --model 'REPLACE_WITH_APPROVED_MODEL' `
  --max-output-tokens 1200 --request-allowance 1 --timeout 60 `
  --output outputs\openai\new-approved-run.json
```

After the authorized invocation, clear the process environment value:

```powershell
Remove-Item Env:\OPENAI_API_KEY
```

Exit codes: **0** dry run or mechanically validated assessment; **1** recorded service failure; **2** configuration/input/publication failure. CLI stdout is JSON except normal help/argparse usage; error messages avoid submitted values/provider bodies. A publication error can follow a processed request, so exit 2 does not always mean no billable work occurred.

## Actual verification and next evidence

- **358 tests passed**: 324 unchanged existing tests plus **34 focused service/prompt/CLI test methods**. API calls use injected clients or actual SDK parsing through in-memory transports; no external model was contacted.
- Tests cover all three preliminary actions, abstention, invalid structures/identities/citations, false/unsupported claims, refusal/incomplete/missing output, error categories, absent usage, exact-one concurrency/reuse, disabled execution, no reference/policy access, preservation, redaction and no-overwrite publication.
- Dependency-review correction: fresh constrained installation and the complete suite passed on Python 3.11.9, Pydantic 2.14.1 and SDK 3.40.0; the existing environment also passed. All 14 runtime pins match the previously tested versions. Targeted 3.11 Windows/Linux wheel resolution/download and six target metadata-closure checks passed. The table above records 3.12/3.13 download timeouts; remote CI was not checked.
- AST syntax checks passed for all 26 Python files. `git diff --check`, explicit whitespace checks on untracked files, and documentation link checks passed. Existing code/test/fixture hashes were compared with the clean starting tree; this dependency correction also preserved all service/prompt/CLI/test source hashes from the reviewed implementation.
- The CLI dry run reported zero attempts. A separately marked mocked G02 demonstration saved an ignored bundle, made exactly one in-memory transport call and rejected the second attempt. Supplied mock usage values were test metadata, not measured model usage or billed cost. All three mechanical checks passed; semantic evaluation stayed unevaluated.

Before the first live smoke test: independently review this code/prompt, approve the exact model and token/call/spend limits, confirm credentials outside Git, select a new artifact path, and authorize one invocation. Record actual request/response IDs, model/SDK settings, original candidate, validation/audit results, usage and failures. Do not interpret a valid citation or a completed request as factual grounding or AML accuracy. Provisional labels and formal semantic adjudication remain open; this does not complete Phase 2 or Week 4's hosted experiments.
