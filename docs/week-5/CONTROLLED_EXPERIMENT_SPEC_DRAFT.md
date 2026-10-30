# Week 5 controlled experiment specification — v0.1 DRAFT

**DRAFT / NOT APPROVED FOR EXECUTION. This document authorizes zero new hosted requests.**

Prepared: 30 October 2026. Proposed plan identifier: `W5-OPSMOKE-001`.
Repository inspected: `research/week-5-experiment-readiness` at `e5e73054cfef7488862a38b3b27ecaae28af37a6`, the PR #14 merge.
Authority: project-owner authorization to draft this specification only. Selection, prospective execution and spending require the releases in section 8. No prospective assessment has been generated in this checkpoint.

## 1. Experiment question and hypothesis boundaries

> Across a prespecified development subset, what execution outcomes, mechanical validation results and descriptive assessment differences do the deterministic baseline and hosted model, as currently configured, produce?

This is operationally measurable after defining the population and observations:

- Population: five named existing development investigations, with one planned baseline assessment slot and one planned hosted assessment slot each: **10 slots, not 10 API requests**.
- Execution observations: authorization, observed invocation, returned response, publication and available usage/error metadata.
- Mechanical observations: input/output contract and contextual-reference stages, plus the existing restricted amount check's results and coverage.
- Descriptive assessment observations: submitted action or abstention, exact cited statements, questions, missing information and contradictions. A reviewer may identify differences for later adjudication without judging either candidate correct.
- An unavailable assessment has no submitted disposition. It is not an abstention.

Engineering expectation: existing interfaces should permit each planned slot to be traced to the same selected source bytes and its recorded configuration. Missing outcomes must remain visible. This is a traceability expectation to check, not a statistical hypothesis, numerical pass threshold or expectation that every hosted response will validate.

This experiment can characterize these two configured systems on these exposed examples. It cannot establish classification accuracy, equivalent-policy reasoning, general semantic support, calibrated abstention, causal effects, real-world AML effectiveness, analyst savings or held-out generalization. No alternate prompt, model comparison, repeated sampling or tuning is included. An identical prompt does not guarantee identical hosted responses.

## 2. Dataset and selection plan

### 2.1 Three different selection purposes

| Purpose | Appropriate selection | Interpretation |
| --- | --- | --- |
| Operational smoke test proposed here | First occurrence of each family in the existing manifest, preserving manifest order | Breadth across supplied record shapes; no prevalence or classification-performance inference |
| Specific behavioral comparison, deferred | Predeclare a question, verify relevant source fields, then select contrasting conditions; use a fixed tie-breaker such as the smallest verified input hash within each chosen condition | Purposeful diagnostic coverage. Conditions are not action labels, and different generated instances are not matched counterfactuals |
| Independent evaluation, deferred | Separately authored/frozen data, adjudication and exposure controls with approved family partitioning | Existing exposed templates and cases cannot be redesignated independent held-out evidence |

**Selection boundary:** Accepting the five-case set for operational smoke testing does not automatically approve it as a substantive classification-performance cohort. Any future behavioral comparison requires its own prespecified question, source-verified contrasting conditions, fixed selection rule, explicit evaluation eligibility and separately authorized execution. This draft retains the existing first-five operational selection; it adds no cases or paid requests.

The [development manifest](../../data/generated/development/manifest.json) records seed `20261027`, generator `1.0.0`, template `1.0`, 50 investigations, five families with ten cases each, and 18 family/condition combinations. Its raw SHA-256 is:

`6b4342f3a98c6426723f22ee2f5816540dc8f0bd0bd2e166fbde09a23c38bfb9`

The selection rule uses manifest order and family membership, without consulting candidate outputs, expected actions or reference answers. In this manifest it selects the literal first five cases. The owner/developers have already inspected the templates and related development material; this is neither blinded selection nor previously unexposed evaluation.

### 2.2 Proposed selected investigations

Each case is selected as its family's first occurrence, not because it is expected to favor either candidate. The family and condition columns are evaluator-only manifest metadata, never added to candidate input.

| Case identity | Investigation | Family | Recorded source condition | Raw-file SHA-256 |
| --- | --- | --- | --- | --- |
| CASE-DEV-S20261027-0001 | [input 0001](../../data/generated/development/CASE-DEV-S20261027-0001.json) | incoming_transfer | invoice_and_dispatch | 61b0ec1bd414cc62052c3f0bd57e31474d9a5e72adb455dfb296cc6e50b0e613 |
| CASE-DEV-S20261027-0002 | [input 0002](../../data/generated/development/CASE-DEV-S20261027-0002.json) | cash_sales | complete_sales | 11370ba0cd8338fc6d4884c9fc1427e7de1d7d1213d7dc7efbab899f1de5b1d2 |
| CASE-DEV-S20261027-0003 | [input 0003](../../data/generated/development/CASE-DEV-S20261027-0003.json) | supplier_authorization | after_instruction | 1e5995d8f46cc8828239d342669f4934529b5a7ddea0ab28d486cc01ae938240 |
| CASE-DEV-S20261027-0004 | [input 0004](../../data/generated/development/CASE-DEV-S20261027-0004.json) | incomplete_outgoing | missing_purpose | 5e5efdc25cf00ed67751f659a21f107339684ef88d7a18a0db504b2d97b1d49f |
| CASE-DEV-S20261027-0005 | [input 0005](../../data/generated/development/CASE-DEV-S20261027-0005.json) | beneficiary_comparison | invoice_reference_absent | 85d021c72ceed201dadd4f2161ce2289240743ddc003ef7e771f0e57c765424f |

The smoke-test purpose is incoming-payment support records for 0001, cash/sales/reconciliation records for 0002, instruction/register/payment records for 0003, incomplete payment information for 0004 and a missing-reference comparison for 0005. Those are coverage rationales, not findings that the records are authentic or that any action is correct.

These five cases cover five of 18 recorded combinations. They omit, among others, explanation-only support, partial/no sales records, authorized changes, different supplier accounts, missing beneficiary accounts and equal/different beneficiary-reference comparisons. In particular, 0005 does not exercise an explicit equal-versus-different comparison. This selection is sufficient only for the stated family-level operational smoke purpose. No conclusion about within-family robustness is permitted.

All 50 input files were freshly contract-validated and matched to their manifest digests while preparing this draft. This was source checking, not execution of either assessment arm.

### 2.3 Raw and canonical identities

The raw digests above bind exact file bytes. The hosted builder separately serializes the validated model using UTF-8, sorted keys, compact separators, `ensure_ascii=False` and `allow_nan=False`. The following hashes identify that canonical input content, not original file bytes:

| Case identity | Canonical validated-input SHA-256 |
| --- | --- |
| CASE-DEV-S20261027-0001 | e167f50429731373e2bec7bd630751344b26225bacc7a1f0962529b1ec60895e |
| CASE-DEV-S20261027-0002 | efc2f9e4066854aaa74feb5e13d266a505fb4dfffd60d6549ac2d31b9575db64 |
| CASE-DEV-S20261027-0003 | 99d223d1dac7d1268ffdbbff93c8760744ec452b36d36977f76be29b9d935ccd |
| CASE-DEV-S20261027-0004 | 6f04a08bfb63c75c93be5c901a3ded2b02971a4f5f4ca9f4594b16bd9d00967d |
| CASE-DEV-S20261027-0005 | a37b2a3a9f58145fcb2b635bc8e07cbabf3db0e1fdd246ba367fb12f24dff797 |

Use both identities in the experiment record. Never replace a raw digest with a canonical digest or normalize line endings to make an original-byte check pass. A case ID alone is insufficient. Recheck identities immediately before prospective execution; reject or hold mismatches rather than silently refreshing this table.

The [generator](../../src/aml_triage/synthetic_generator.py) and manifest disclose shared template lineage and no adjudicated labels. Metadata conditions must not become expected dispositions. Selection metadata, references and annotation registers remain outside both candidate-generation interfaces.

## 3. Candidate configurations and provenance

| Item | Observed configuration or proposed control |
| --- | --- |
| Baseline | Existing `assess_investigation`, version `0.1.0`. Last source commit `73fee08e42a3482010ee258bb3dbf17d3165dd88`. Uses limited fixed rules and contextual validation; does not automatically recommend `close` |
| Hosted service | Existing service `0.1.0` and execution record schema `1.0`; official SDK `3.40.0` |
| Hosted instructions | Unchanged `aml-preliminary-1.0`; instructions SHA-256 `f6472c5d27337626e113cfa982297b0c6b317282eefc4a600f049fa025bb6c83` |
| Model | Proposed configured identifier `gpt-6-luna`, based on the earlier G02 smoke test; **pending new owner approval**. The service default is no model, live disabled and allowance zero |
| Runtime inspected | Python `3.11.9`, Pydantic `2.14.1`. Record actual execution versions; no fresh 3.12/3.13 runtime result is claimed |
| Contracts and mechanical report | Input/output schema `1.0`; auditor `0.2.0`, report `1.1`; amount check `1.0` |
| Prospective settings | Proposals in section 7. Do not infer their authorization from the historical G02 configuration |
| Future execution revision | Record the actual checkout HEAD and source hashes. The inspected revision above is not a future execution claim. Documentation-only commits may change HEAD; reconcile them explicitly while checking implementation hashes |

Raw SHA-256 values of the inspected implementation, CLI, dependency and policy sources:

| Source | SHA-256 |
| --- | --- |
| [src/aml_triage/deterministic_baseline.py](../../src/aml_triage/deterministic_baseline.py) | e3d9746e980dc6c11f8bdecff4279389baa3952fac119b0994a9db35087271a0 |
| [src/aml_triage/openai_service.py](../../src/aml_triage/openai_service.py) | a339c208e07b5b768286495b95361d9a2691a0fc6ce07f8b73dbc44bb8a1e8de |
| [src/aml_triage/openai_prompt.py](../../src/aml_triage/openai_prompt.py) | a18d2639f45fe7dced47f90440b7d8d43a33068ac68d4a0965e90743911440d4 |
| [src/aml_triage/contracts.py](../../src/aml_triage/contracts.py) | 1d17ff50c4e98c7fdb1cc92aefaef83248821fd60f94ace1f57fbb4bafe7b3c6 |
| [src/aml_triage/auditor.py](../../src/aml_triage/auditor.py) | 30cc4c8af0b956c9efa660376dd01bf5fc8c463289d6c52f46c0974626879864 |
| [src/aml_triage/transaction_amount_checks.py](../../src/aml_triage/transaction_amount_checks.py) | 0a4af0aadb781cea51957d598d19af46eb89870b8362452aab7a8cc8f08aa9ef |
| [scripts/run_baseline.py](../../scripts/run_baseline.py) | 9d7c8d66d5a5888a659b0a97cb0b73e8cf71f84feee8c63b04c77ea1cb3de660 |
| [scripts/run_openai_assessment.py](../../scripts/run_openai_assessment.py) | e12eb844ef2f48d117854a05006dca5c21d38dda261e16a048d42fd1c7b1a0a9 |
| [scripts/audit_packet.py](../../scripts/audit_packet.py) | 0df38467e826439b12c519f8d5b797682b889b375e59a7933624350c461df5e9 |
| [constraints.txt](../../constraints.txt) | 250f034e56dee602760fee44e140d4a1c5dddf651e23afdc9f26780d4e548a82 |
| [specs/labeling_policy_v1.json](../../specs/labeling_policy_v1.json) | 6cdefd8400ae160163a4e0625f0b5311890ecad27967767e10459df2f1ee6352 |

Source-file digests, prompt-instruction digests and candidate-text digests have different byte bases. Preserve their labels. Record this specification's exact approved file digest at release, the development manifest digest and actual output-file digests. This draft does not contain a self-referential file digest.

### 3.1 Exposure and policy differences

The baseline implements a restricted REF-01 interpretation in code. The current hosted instructions name provisional dispositions but do not provide that full rule; they explicitly prohibit treating `policy_id` as policy text. Both candidates receive the same validated investigation, but their policy knowledge and supported behaviors differ.

An as-configured comparison can report that the two systems produced different outputs under these configurations. It cannot attribute differences solely to model reasoning, establish equal-information policy competence or treat baseline output as ground truth. Do not add policy text to the hosted arm within this plan. A matched-policy or prompt-change experiment needs a separately versioned design and approval.

Record the application context: the existing hosted builder supplies one developer instruction message and one investigation-JSON user message. The service supplies no tools, retrieval or conversation history. Preserve the source/hash of those instructions, canonical investigation, output contract source, SDK and request settings so the application request can be reconstructed. This is not a captured HTTP envelope, authenticated provider execution trace or immutable model-weight snapshot.

Record known developer/template/G02 exposure and any additional demonstrations, tools, history, grading feedback or external exposure. Mark unavailable information unknown. No new case-specific reference, condition, annotation or previous assessment may be supplied to generation. Existing supplied statuses remain input records; they do not certify newly performed verification or eliminate shortcut risks. See [protocol section 7](../phase-2/EVALUATION_PROTOCOL_DRAFT.md#7-proposed-dataset-isolation-and-leakage-controls).

## 4. Experiment-level attempt-accounting contract

This is a proposed manual accounting contract outside `InvestigationOutput`. It does not replace the service record or implement a ledger.

A logical slot is `(experiment_instance_id, case_id, arm)`, with arm `baseline` or `hosted`. Proposed slot identifiers are `0001-baseline` / `0001-hosted` through `0005-baseline` / `0005-hosted`. All ten are currently planned but unexecuted and not authorized by this document. There are zero newly authorized hosted calls.

Keep separate observations rather than one overloaded success flag:

| Ledger field | Meaning and evidence |
| --- | --- |
| Slot and input identity | Experiment, case, arm, raw/canonical input digests and source paths |
| Authorization | `pending`, `authorized` or `withdrawn`; owner identity/role, time, scope and actual approval reference where supplied. Missing approval is not inferred |
| Invocation observation | Whether an operator observed invoking the existing CLI/service, with event identity/time and configuration. An authorization is not execution evidence |
| Service counters | Copy `request_attempts` and `requests_used` when present, with their existing meanings; otherwise null with a reason |
| Response observation | Record observed completion, refusal, incompleteness, provider error or unknown response outcome; do not infer a response from an intended call |
| Service outcome | Preserve `execution.status`, error category, request ID, latency and validation fields verbatim, or identify their absence |
| Assessment outcome | Preserve submitted status/action only when an assessment is available. Absent output is not explicit abstention |
| Publication | Published, failed, missing/unavailable or not yet expected; output identity/hash and available stdout/receipt evidence |
| Usage and billing | API-reported usage when available; actual billed amount only with separate billing evidence. Unknown remains null, not zero |
| Review | Operator/reviewer role, observations, evidence references, limitations and unresolved questions. Required human review is not completed review |

Important service semantics from [the implementation](../../src/aml_triage/openai_service.py):

- `requests_used` reserves the instance allowance before client creation; it can be one even if no SDK request is invoked.
- `request_attempts` is set before `responses.parse`. It identifies an observed SDK-operation invocation, not a proven network transmission, provider acceptance or billed request.
- One service instance permits one reserved invocation. New processes/instances reset that guard. It is not an experiment-wide cap.
- A refusal or incomplete response is distinct from no returned response. A structurally valid `unable_to_recommend` assessment is distinct from any service failure.
- SDK parsing failure can hide original response text, request ID or usage. Do not reconstruct missing response text from a parsed substitute.
- Publication can fail after processing. A missing bundle is not evidence that no call occurred.

| Situation | Required experiment accounting |
| --- | --- |
| Planned, not yet authorized | Retain slot; no dispatch; do not count as an observed request |
| Authorized, unexecuted | Retain authorization and lack of observed invocation separately |
| Invocation observed, no conclusive receipt | Mark outcome unknown; reserve the authorization as consumed pending review; stop, do not repeat |
| Response completed but assessment rejected | Retain failure/diagnostics, any original candidate and usage; do not discard from the attempt inventory |
| Refusal or truncation | Preserve corresponding service category; no fabricated disposition |
| Publication missing/failed | Preserve available receipt/stdout; candidate/publication state may remain unknown |
| Validated output published | Report structure/citations/mechanics separately; no semantic approval follows |
| Baseline software failure | Retain the planned slot and actual failure; external-request counters are not applicable |

The proposed first release permits at most one intentional invocation per hosted slot. Conservatively treat every authorized live invocation as consuming its slot even if a local failure occurs before `request_attempts` becomes one. Do not issue replacement attempts under the same release. Any later repeat requires a separately approved amendment and new attempt identity while retaining prior failures and budget history.

Before each manually executed invocation, record a new authorization/intent event; afterward record its observation and receipt. Preserve event history with new event files or a versioned manual ledger under the selected ignored run directory; do not erase earlier entries or overwrite existing artifacts. Record actual times only when observed. Never invent retrospective approvals or attempt counts.

Manual accounting depends on operator discipline and is not transactionally coupled to request dispatch. A crash can leave uncertain outcomes. Unattended/batch execution, concurrent operators, automatic resumption or repeated campaigns would require persistent pre-dispatch reservation, an experiment-wide cap, durable receipts and crash recovery before automation. None is authorized here.

## 5. Operational procedure using existing interfaces

**Procedure only: no commands in this section were executed while drafting.** Run from the existing repository root with its installed environment. Approval of documentation does not authorize future execution.

1. Obtain the releases in section 8. Resolve pending limits; establish a fresh experiment instance identifier and one operator. Freeze the approved specification digest, input order/hashes, configurations, exposure record and allowed conclusions.
2. Confirm branch/HEAD, dependency versions and the source identities in sections 2–3. Preserve the existing untracked handoff ZIP and original experiment artifacts. An input/source/configuration difference places the run on hold; do not overwrite an approved plan to accommodate it.
3. Establish a previously absent directory under ignored `outputs/experiments/`. The illustrative `outputs/experiments/W5-OPSMOKE-001/` did not exist when this draft was prepared. Initialize all ten ledger slots and record pending/authorized states. Never use a pre-existing run directory for a replacement run.
4. After offline execution approval, generate each baseline once, in the selected order, using the unchanged baseline CLI. The following shows only case 0001:

```powershell
.\.venv\Scripts\python.exe -B scripts\run_baseline.py --input data\generated\development\CASE-DEV-S20261027-0001.json --output outputs\experiments\W5-OPSMOKE-001\0001\baseline.json
```

The CLI validates input/output and citations and atomically publishes with no overwrite. Record its exit, output hash, baseline/source revision and actual observations. If an offline reproducibility check is separately approved, use a different destination; it is a reproducibility check, not an additional independent case.

5. Inspect each hosted configuration through the existing dry-run path. Illustrative **proposed, unapproved** settings match the earlier G02 settings for continuity; they are not known to be sufficient for every selected case:

```powershell
.\.venv\Scripts\python.exe -B scripts\run_openai_assessment.py --input data\generated\development\CASE-DEV-S20261027-0001.json --output outputs\experiments\W5-OPSMOKE-001\0001\hosted-dry-run.json --model gpt-6-luna --max-output-tokens 2400 --timeout 60 --reasoning-effort none
```

There is no `--live` flag and allowance defaults to zero. The dry run creates no model request; it is configuration evidence and does not fill the hosted assessment slot.

6. **Only after explicit paid authorization**, use the same hosted CLI with the approved settings, a new `hosted-execution.json` destination and `--live --request-allowance 1`. Execute one case at a time, without loops or automatic retries. Record the intent before invoking and preserve the receipt afterward. Stop after a failure, refusal, incompleteness, identity mismatch or publication uncertainty; proceeding requires owner review. Remaining slots stay visible as unexecuted. No repeat of the failed slot is authorized.
7. Preserve each original service bundle. Do not rewrite `candidate_json` or replace it with serialized `assessment`. Record bundle-byte SHA-256 separately from `execution.candidate_sha256`, which hashes exact candidate text encoded as UTF-8.
8. Audit the plain baseline output using the existing auditor CLI:

```powershell
.\.venv\Scripts\python.exe -B scripts\audit_packet.py --input data\generated\development\CASE-DEV-S20261027-0001.json --candidate outputs\experiments\W5-OPSMOKE-001\0001\baseline.json
```

The hosted bundle already contains the audit of its original candidate text. **Do not pass the entire service bundle as `--candidate`**: it is not an `InvestigationOutput`. For independent hosted replay, the existing public Python interface can read the bundle and audit its exact candidate text, without another API request:

```python
from hashlib import sha256
import json
from pathlib import Path
from aml_triage.auditor import audit_packet

source = Path("data/generated/development/CASE-DEV-S20261027-0001.json")
bundle_path = Path("outputs/experiments/W5-OPSMOKE-001/0001/hosted-execution.json")
bundle = json.loads(bundle_path.read_bytes())
text = bundle.get("candidate_json")
if not isinstance(text, str):
    raise ValueError("No original candidate text is available for replay")
if sha256(text.encode("utf-8")).hexdigest() != bundle["execution"]["candidate_sha256"]:
    raise ValueError("Candidate-text identity mismatch")
report = audit_packet(
    source.read_bytes(), text,
    input_identity=str(source),
    candidate_identity=str(bundle_path) + "#candidate_json",
)
print(json.dumps(report, indent=2, allow_nan=False))
```

Retain replay reports in distinct new destinations using non-overwriting handling. Do not use blind shell redirection that can overwrite a prior artifact. A replay does not replace the original audit; differing byte bases/identity labels must be disclosed before comparing reports.

9. Complete the inventory and descriptive case-pair table before consulting any case-specific evaluator material. Review the actual submitted text and input sources; label new interpretive observations draft/unadjudicated. Close the run as completed or stopped with every slot accounted for, including unavailable artifacts. Completion does not require every candidate to validate.

CLI exits retain their existing meanings: baseline 0 is publication success and 2 is input/configuration/publication failure; hosted 0 includes dry run or mechanically validated assessment, 1 is service failure and 2 includes configuration/publication failure; auditor 0 is three mechanical stages passed, 1 is expected validation rejection and 2 is ingestion/evaluator/usage error. Exit zero alone does not prove a hosted call occurred. An amount conflict does not change the auditor's mechanical exit-zero convention.

### 5.1 Retrospective G02 inspection is separate

These local historical artifacts were checked while drafting. They are not members of the prospective five-case population:

**Local-only frozen evidence:** The four artifact links below point into Git-ignored `outputs/`. These files are not committed repository content and are unavailable in a fresh checkout or on GitHub unless the original artifacts are separately supplied. Their exact relative link targets and raw hashes are preserved for local verification; this document does not publish or copy the artifacts. The review documentation linked after the table is repository-accessible.

| Artifact (local only) | Raw-file SHA-256 | Recorded observation |
| --- | --- | --- |
| [Initial G02 bundle (local only)](../../outputs/openai/G02-live-luna-20261029-111651.json) | b7471dbfacf7af9b21b92a95d80e07581b8a08aa43260a2fd83de107fc52c963 | Connection failure; one recorded SDK invocation; no usage or request ID |
| [Successful G02 bundle (local only)](../../outputs/openai/G02-live-attempt2-20261029-113851.json) | 95e6cbd8053929c3aea6de5ba5c72c9e443352554e2ea3d0ead5d39b6567de9b | `validated`; 1,491 input / 1,163 output / 2,654 total tokens; 10,905.025 ms |
| [Frozen baseline candidate (local only)](../../outputs/evaluation/g02-paired-pilot-20261029/baseline_candidate.json) | 4ad63a4c19e2c71a3cf8dbcc7ddf14aee30cafc198a93b32bea9ea5356918b07 | Existing deterministic comparison candidate |
| [Frozen hosted candidate (local only)](../../outputs/evaluation/g02-paired-pilot-20261029/hosted_candidate.json) | c44c89e49dc82443b2a5af45e8b0bb249e35551298764706355061099c62e82b | Exact successful bundle `candidate_json` UTF-8 text, without an added newline |

Both live bundles record `aml-preliminary-1.0`, SDK `3.40.0`, model identifier `gpt-6-luna`, allowance one and zero retries. Their input identity is raw `60cbf66dbbb24b59f0ae0a86e03a92d6f0dac0e68511ec05cd1953b96763326f` and canonical `7f077f89d97f17fac644273d0a53c5b108b519d00adcddba0c21a9122f6a58da`. The first failure has uncertain processing/billing, not a zero-cost finding. The successful amount check covered zero of six findings; the frozen baseline check covered two of three. Coverage is not comparative accuracy.

Use these as historical accounting examples only. No prospective specification, experiment-wide budget or approval trace is reconstructed for them. See the [paired pilot](../week-4/G02_PAIRED_EVALUATION_PILOT_DRAFT.md), [live review](../week-4/G02_LIVE_ASSESSMENT_REVIEW.md) and [G02 owner-adjudication specification](../phase-2/G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md). The merged owner decisions, original reference and exclusions remain unchanged. G02 reconciliation is bound to its frozen candidates; it cannot adjudicate the new candidates in this plan.

## 6. Reporting schema and permissible conclusions

The proposed report is separate from candidate outputs and preserves links to existing records rather than replacing them. It may be assembled manually; no report generator is implemented here.

| Block | Required content and interpretation |
| --- | --- |
| Plan/provenance | Approved specification version/digest, instance, actual revision/environment, source hashes, ordered five-case population, arm settings and exposure record |
| Authorization/limits | Actual approval references, monetary assumptions and call/token limits; absence is explicit |
| Slot inventory | Exactly ten slot rows, with separate authorization, invocation, response, publication, service outcome and available artifact identities |
| Existing validation | Preserve input/output/context stage statuses, reasons and diagnostic paths. Use only `passed`, `failed`, `not_evaluated` and `error` for those stages |
| Restricted fact checks | Preserve named predicate/version, matches/conflicts, checked and unchecked counts, prerequisites and reasons; no general grounding claim |
| Descriptive comparison | Per-case submitted action/abstention or unavailable output, exact quoted differences and record pointers, draft review state and policy-access caveat |
| Exclusions and limitations | Every missing/failed/unexecuted slot, unimplemented judgments, unavailable usage, exposure, incomplete review and stopped-run reasons |
| Semantic scores | `null` / not evaluated; no action accuracy, weighted score, quality percentage, pass threshold or ranking |
| Billing | Available usage separate from optional documented cost estimates and actual bills; do not total unknown charges as zero |

Illustrative **unexecuted slot shape**, not an actual result:

```json
{
  "slot_id": "0001-hosted",
  "case_id": "CASE-DEV-S20261027-0001",
  "arm": "hosted",
  "authorization_status": "pending",
  "authorization_reference": null,
  "invocation_observation": "not_observed",
  "execution_bundle": null,
  "request_attempts_as_recorded": null,
  "response_observation": "not_observed",
  "publication_status": "not_yet_expected",
  "submitted_assessment": null,
  "semantic_scores": null,
  "billing_amount": null
}
```

The full report needs all ten rows; this example is not a report with nine silently omitted slots. Add the source digests from section 2, actual observations and record references when available. Unknown fields require a reason. No field in this example implies an approved JSON Schema or new application contract.

Report mechanical category counts by arm and retain a case-level table. Name the population for every count: planned slots, authorizations, observed SDK invocations, available candidates or stage results. These are different denominators. Unknown/missing responses must be disclosed beside valid outputs; invalid input is distinct from an invalid candidate. Do not fabricate exhaustive error or per-citation counts from fail-fast validators. A zero eligible population yields no rate, never a perfect result.

Statement/question/citation volume is descriptive, not completeness or quality. Unsupported prose may pass all mechanical stages. The broad nine auditor semantic dimensions remain `not_evaluated`. Do not apply the G04 relationship checker without its separately bound annotations; no new relationship annotations are authorized here. Proposed qualitative observations remain unadjudicated and cannot silently become expected labels.

Permitted conclusion example: “These configured systems produced different submitted actions or questions for this exposed case; the attached stages describe their mechanical validity.” A matched action does not establish a correct rationale. A required human-review flag does not certify completed review. The G02 M01–M03 matrix must not be copied onto the five new cases.

## 7. Failure, safety and spending boundaries

| Control | Current state / proposal for later release |
| --- | --- |
| New live requests authorized now | **0** |
| Logical hosted slots | 5 proposed |
| Maximum intentional hosted invocations | **5 proposed, pending approval**, one per slot; no replacement calls |
| Per-invocation allowance | 1 only for an explicitly authorized live invocation; default remains 0 |
| Output-token ceiling | **2,400 proposed, pending approval**, matching historical G02 configuration; truncation remains possible |
| Aggregate output allowance | At most 12,000 configured output-token units if all five proposed calls are authorized; this is arithmetic over requested ceilings, not a monetary cap or promised usage |
| Timeout | 60 seconds proposed; server processing may outlast a client timeout |
| Reasoning effort | `none` proposed; compatibility is not reverified by this draft |
| SDK/application retries | 0 / 0; no manual retry or fallback model within this release |
| Storage | `store=False`, enforced by existing service |
| Monetary budget, currency and pricing assumptions | **Pending; no amount approved and no monetary estimate asserted** |
| Credentials | Owner-controlled setup outside Git; this task does not inspect keys or environment-secret files |

Before any paid invocation, the owner must approve the model/settings, total allowance and monetary authorization, with dated pricing/reserve assumptions if estimating exposure. Frozen input sizes do not establish API input tokens: instructions, schema and provider accounting also matter. No new tokenizer dependency or speculative cost figure is required by this draft. Unknown usage/billing after failure remains unknown. The local guard cannot guarantee a hard billing cap.

Input or source mismatch, missing authorization, unresolved publication, unexpected error or exhausted allowance means hold/stop. Preserve all failures, SDK parse limitations and original diagnostics. Do not discard bad responses, silently repair them, choose a better replacement, infer absent verification, or infer fund flows. Keep raw synthetic responses and local ledgers ignored; do not publish API keys, authorization headers, payment details or raw artifacts to Git.

## 8. Required approvals

All releases below are **pending**. Approval to prepare this draft does not satisfy them.

| ID | Owner decision required | Blocks |
| --- | --- | --- |
| A01 | Accept operational question, first-per-family selection, input digests and permitted conclusions | Prospective experiment release |
| A02 | Assign operator/reviewer roles and accept manual accounting, stop rules and its crash limitations | Invocation procedure |
| A03 | Approve exact model, settings, total call allowance and one-attempt-per-slot rule | Any paid call |
| A04 | Approve monetary authorization and pricing/reserve assumptions, with uncertainty acknowledged | Any paid call |
| A05 | Record approved specification digest, actual source/runtime identity, fresh instance/path and exposure record | Prospective execution |
| A06 | Explicitly authorize the offline baseline/dry-run preparation and the separately bounded live invocations | Execution of those activities |

Generic rubric access, new prompt variants, semantic-score eligibility, further case adjudications and held-out design remain separate future decisions. They do not block this draft or non-scoring as-configured observations with the unchanged prompt. They do block the corresponding stronger comparisons or claims. No settled G02 judgment is reopened.

## 9. Acceptance criteria and source verification

This checkpoint succeeds as a documentation artifact when:

1. The question has explicit observational units, allowed reports and excluded claims.
2. The five case identities, metadata and raw hashes match the inspected manifest; all selected inputs validate and canonical digests are separately correct.
3. Version/source tables match actual files, and current configuration is distinguished from proposed settings and future authorization.
4. The ledger distinguishes every situation in section 4 without inventing execution, completed human review or billing evidence.
5. Commands match existing CLI arguments; dry run cannot be mistaken for live execution, and the hosted bundle is not mistaken for plain candidate JSON.
6. Historical G02 data stays separate; prior runs are not retroactively preregistered and merged adjudications are not overwritten.
7. Approvals, budget and paid execution stay pending; all ten proposed slots are unexecuted.
8. Links, hashes, Markdown and Git scope checks pass; original artifacts and implementation remain unchanged.

Preparing this draft included read-only validation of all 50 inputs and manifest digests, canonical-hash checks for the selected five, inspection of 18 metadata strata, source/version inspection and original historical artifact hashing. No baseline candidates, dry-run bundles, hosted responses, experiment ledger or report were created. Example commands and report records describe future actions only.

No unit tests are added or rerun for this documentation-only checkpoint. The earlier 438-test result remains historical evidence, not a fresh pass. CI is not queried or claimed green. The optional frozen-packet test behavior remains unchanged and does not provide full reconciliation coverage on an ordinary checkout lacking that packet.

## 10. Remaining engineering gaps and alternatives

For a small, serial, owner-controlled run, the existing baseline CLI, hosted CLI, public auditor and manual ledger are sufficient once the relevant approvals are granted. **No new runner, API client or preflight checker is required to approve this specification.**

A future small read-only checker could reduce repeated identity/configuration errors after the contract is accepted. A runner would be justified by repeated campaigns or demonstrated manual coordination failures, and would need explicit experiment-wide attempt controls before dispatching requests. Neither is implemented or authorized here.

Other limits remain: unequal policy access; shared/exposed development lineage; no adjudicated action labels for these generated cases; limited deterministic-check grammar; unavailable provider snapshot/HTTP evidence; missing metadata on some failures; manual-ledger crash windows; no independent expert validation or held-out findings. A configured model identifier is not an immutable provider snapshot.

Original-file hashes remain exact. Report paths retain existing caller/location behavior: stable evidence identities do not imply identical report bytes across checkout paths or line-ending changes. The LF/CRLF limitation is preserved, not normalized away. Historical documentation and draft register release flags do not become fresh runtime evidence or new semantic authorization.

After review, the next step is to accept or amend this concrete plan and approve its specified preparations. Additional live execution needs its own explicit releases. Record observed results before deciding whether software automation or a narrower behavioral experiment is warranted.
