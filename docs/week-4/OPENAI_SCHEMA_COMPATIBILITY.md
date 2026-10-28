# Week 4, Checkpoint 1 — OpenAI Structured Outputs compatibility

**Date:** 2026-10-28. **Status:** local investigation; no live API request, credentials or model-performance result.

Preflight: clean working tree on `feature/week-4-openai-schema` at `3c4e3fd58e3ac6b6c0676431528741957a7bb5a6`, the PR #9 merge. The deterministic baseline is already merged. Current repository code and tests, rather than earlier conversations, were inspected.

## Recommendation and implementation scope

Keep the existing `InvestigationOutput` class. Prefer `client.responses.parse(..., text_format=InvestigationOutput)` for the first separately authorized smoke test. Local inspection found no need for an adapter or a second transport model. This checkpoint adds documentation only; no SDK or dependency was installed, and no compatibility runtime code or new test methods were added.

Server schema enforcement, client-side Pydantic validation, contextual citation resolution and factual support are separate boundaries. Passing the schema through the SDK does not encode our custom validators into the server grammar or establish live request acceptance.

## Actual generated schema

Generated with Python 3.11.9 and Pydantic 2.14.1 from [contracts.py](../../src/aml_triage/contracts.py), including every nested definition. Reproduce from the repository root:

```powershell
.\.venv\Scripts\python.exe -c 'import json; from aml_triage.contracts import InvestigationOutput; print(json.dumps(InvestigationOutput.model_json_schema(), indent=2))'
```

| Feature | Observed schema | Compatibility finding |
| --- | --- | --- |
| Root | Object, no root union | Matches the documented root requirement [O1]. |
| Required fields | All 13 root fields and all seven properties across three definitions are required | Matches strict required-field rules [O1]. |
| Extra fields | `additionalProperties: false` on all four object schemas | Matches strict object rules [O1]. |
| References | Three `$defs`: `RecordCitation`, `CitedStatement`, `Contradiction`; nine `$ref` occurrences | Definitions/references are documented [O1]; no cycles or reference siblings here. |
| Arrays/nesting | Six arrays; deepest object chain is output → contradiction → statement → citation | Documented structures [O1]; small local schema. |
| Enums | Eight namespaces, two statuses, three action strings | Documented enum type [O1]. |
| Nullable action | Nested `anyOf`: action-string enum or JSON null; key remains required | Documented nested unions/nullability [O1]. |
| Literals | Three `const` values: `"1.0"`, `"preliminary"`, boolean `true` | Guide mentions constant values in schema limits; inspected SDK preserves them. Exact server behavior remains untested. |
| String length | Five `minLength: 1` occurrences: identifiers, statement and contradiction description | SDK preserves these. Guide explicitly excludes string lengths for fine-tuned models; selected-model acceptance/enforcement needs verification. |

There are 20 declared properties across the four object schemas, 13 enum values and no `allOf`, `not`, `dependentRequired`, `dependentSchemas`, `if`, `then`, `else`, defaults or array-size constraints. Unsupported composition keywords are documented [O1] but absent here. Do not treat omitted keywords as automatic request rejection, or fine-tuned limitations as proof that every base model rejects the same schema. The guide's positive string-keyword list does not explicitly establish a universal `minLength` guarantee.

Canonical schema: **2,866 UTF-8 bytes**, SHA-256 `4e6a81a31aa2450418303a55617ca10d7cb0260af30a14399f582a461f91338b`, using `json.dumps(schema, ensure_ascii=False, sort_keys=True, separators=(",", ":"))` without a final newline. This identifies the local schema, not a live compatibility certification; Pydantic upgrades may change it.

## Python SDK inspection: parse helper versus direct schema submission

The project environment has no OpenAI SDK. Inspected the published `openai-3.40.0-py3-none-any.whl` without installing it or its dependencies. Wheel SHA-256: `dfcfd4f65ee5a8bb824da90c9ad7fa0dda7f3bd472a7c564dffc6183f0a0b55c`. A package download is not a model request. SDK version 3.40.0 is an inspected artifact, not a new project version requirement.

Source inspected inside that wheel:

- `openai/lib/_pydantic.py`: `to_strict_json_schema` recursively handles definitions, required properties, object restrictions, arrays and unions; it removes null defaults and can inline references with siblings. It is not a general server-schema compatibility validator and does not remove every unsupported keyword.
- `openai/lib/_parsing/_completions.py` and `openai/lib/_parsing/_responses.py`: the Pydantic class becomes a format containing `type="json_schema"`, `name="InvestigationOutput"`, `strict=True` and the normalized schema. Response text parsing delegates to Pydantic.
- `openai/lib/_response_resources.py`, `openai/resources/responses/responses.py` and `openai/_compat.py`: `responses.parse` supplies `text.format`, then parses response text through `model_validate_json` on Pydantic V2. Supplying both `text_format` and `text.format` is rejected. The inspected parser skips explicit non-final text phases and leaves refusal content unparsed; `output_parsed` can be absent.

Executed the actual schema-normalization and format-helper function bodies in isolation, supplying only their package-import dependencies through local shims. **Normalized schema equals the raw `model_json_schema()` dictionary exactly**, including `const` and `minLength`. The request format adds the name/type/strict envelope; it does not change this schema. The raw schema was not mutated. An isolated `parse_text` check accepted a valid abstention and propagated our custom `ValidationError` for numeric `human_review_required=1`; non-final commentary returned no parsed assessment. These checks do not exercise a complete installed SDK, HTTP serialization or API client.

For a different Pydantic model, SDK normalization may change its schema; do not generalize this equality to every class. These are private helpers inspected as evidence, not recommended application imports. No helper code was copied into the repository.

Direct Responses submission instead requires an explicit `text.format` object containing `type`, `name`, `strict` and `schema`; a bare schema dictionary is not the request envelope. It also requires the caller to validate returned candidate JSON. Responses uses `text.format`, not Chat Completions' `response_format` [O2]. No manual conversion from constants to enums or removal of length rules is justified by the present local evidence.

## Validation boundaries and local demonstrations

Every candidate must still use the existing contract and contextual validator, with the original candidate text preserved for auditing:

```python
from aml_triage.auditor import audit_packet
from aml_triage.contracts import (
    InvestigationInput, InvestigationOutput,
    validate_investigation_output_references,
)

investigation = InvestigationInput.model_validate_json(input_json)
output = InvestigationOutput.model_validate_json(candidate_json)
validate_investigation_output_references(investigation, output)
report = audit_packet(input_json, candidate_json)
```

An SDK-parsed assessment already runs the Pydantic step locally; it never runs our contextual validator automatically. Pydantic enforces non-whitespace text, duplicate typed citations, status/action consistency, conditional factual-finding and rationale requirements, cited interpretations/contradiction sides and exact boolean review. Those custom rules are not present in the generated schema. No transport model may bypass them.

Ran 32 independently authored JSON probes against the supplied G02 input. Each was checked through Pydantic, contextual validation where valid, and the existing auditor. No reference answers were read to author the candidates.

| Probe group | Count | Observed result |
| --- | ---: | --- |
| Three preliminary actions and explicit abstention | 4 | All three mechanical stages passed; no action-quality judgment. |
| Invalid action; incompatible status/action combinations | 3 | Pydantic rejection; auditor output stage failed, context not evaluated. |
| Missing findings key, empty findings, uncited finding/rationale | 4 | Same structural rejection. |
| Duplicate typed citations | 1 | Structural rejection. |
| Review flag false, numeric 1 or string `"true"` | 3 | Structural rejection, including the custom exact-boolean guard. |
| Empty/whitespace statements and identifiers | 4 | Structural rejection. |
| Wrong/numeric schema version, final scope or malformed list | 4 | Structural rejection. |
| Extra root/nested fields or unsupported citation namespace | 3 | Structural rejection. |
| Unknown ID, wrong namespace, mismatched case/alert | 4 | Structure passed; contextual stage failed with existing diagnostic paths. |
| False amount and invented independent-authentication assertion with existing IDs | 2 | All mechanical stages passed; factual support was not established. |

Totals: **22 structural rejections, four contextual rejections, six mechanically accepted examples**, with no submitted-data mutation. All nine broad semantic dimensions remained `not_evaluated` in all reports. The existing restricted amount checker separately found a conflict for `The incoming transaction was USD 99,999.00.` against `TX-G02-01`'s USD 48,500.00. The invented authentication assertion was outside that grammar and remained unchecked. These different outcomes must not be collapsed into a factual-quality pass.

The merged baseline's G03 assessment also passed a complete output JSON round-trip and contextual validation. That verifies contract integration, not agreement with adjudicated labels or classification accuracy.

## Recommended first live smoke test — not performed

After separate authorization, agree the model, SDK/dependency version, synthetic prompt, token/cost limit and retry limit. Use the existing class through the documented `responses.parse` helper [O1], for example this illustrative call with an already configured client:

```python
response = client.responses.parse(
    model=approved_model,
    input=synthetic_request_messages,
    text_format=InvestigationOutput,
)
```

This call was not executed. Before accepting an assessment, handle request errors, refusals, incomplete/truncated responses and absent parsed output. Select the actual final assessment text part, preserve its original JSON for the auditor and artifact digest, then run contextual validation and mechanical auditing. Do not treat concatenated commentary, the entire API response envelope or a reserialized replacement as the original candidate artifact. Do not repair invalid outputs, invent citations, insert safety fields or silently retry.

Record exact model/SDK versions, transmitted schema, request settings, response status, available usage/diagnostics and validation outcomes without credentials. Request acceptance, grammar adherence, custom validation, citation existence and factual support must be reported separately. If a specific schema feature fails, isolate that failure before proposing a small adapter and focused tests.

Unverified: selected-model schema acceptance/enforcement (especially length/literal behavior), full installed SDK compatibility, HTTP/client handling, account availability, live refusal/truncation behavior, remote CI and semantic output quality. No classifier, hosted client, multi-provider architecture or completed semantic evaluation is introduced.

## Verification and sources

- Full suite: **324 tests passed** on Python 3.11.9, including existing [contract tests](../../tests/test_contracts.py), [auditor tests](../../tests/test_auditor.py) and [baseline tests](../../tests/test_deterministic_baseline.py).
- `python -m pip check`: no broken requirements. AST syntax checks passed for all **22 tracked Python files**, without writing bytecode for that check.
- Local helper and 32-probe checks passed. No compatibility implementation was introduced, so no new unit-test methods were needed. Existing contracts, source, tests, policy, synthetic datasets and dependencies remain unchanged.
- **[O1]** [Official OpenAI Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses), including supported schemas, Pydantic parsing, refusals and incomplete responses; consulted 2026-10-28.
- **[O2]** [Official Responses migration guide](https://developers.openai.com/api/docs/guides/migrate-to-responses#6-update-structured-outputs-definitions), confirming the Responses format location; consulted 2026-10-28.
- **[O3]** [Official Python library documentation](https://developers.openai.com/api/reference/python) identifies the published Python SDK and PyPI distribution. Local source findings above are explicitly tied to the inspected wheel rather than a claim that the public documentation specifies all helper internals.

This documentation remains uncommitted for independent review. Phase 2 semantic adjudication and provisional labels remain open.
