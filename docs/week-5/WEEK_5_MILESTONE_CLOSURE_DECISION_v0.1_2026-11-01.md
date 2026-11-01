# Week 5 milestone closure decision - v0.1

**Decision ID:** W5-MILESTONE-CLOSURE-2026-11-01-v0.1

**Owner approval date:** November 1, 2026. The exact approval time was not supplied.

**Status:** Week 5 - Bounded Classification Experiments - formally closed by the project owner on its bounded engineering-comparison objective. Week 6 has not started and is not authorized.

## 1. Approval provenance and original objective

The current instruction, "CODEX - FORMALLY RECORD OWNER-APPROVED WEEK 5 MILESTONE CLOSURE," states that the project owner accepted the previously reviewed milestone decision proposal, evidence and limitations. This document records that explicit approval. Codex verifies local artifacts; owner approval in conversation is not independent AML expert validation or an independently authenticated approval receipt. This is local documentation, not a Git commit or publication.

The authoritative [roadmap](../../ROADMAP.md) defines Week 5 as "Bounded classification experiments," with "Fixed eval set, prompt versions, comparisons, decision record." The [charter](../../PROJECT_CHARTER.md) requires comparison against the deterministic baseline and an evidence-based decision on further experiments. The approved interpretation requires a bounded, controlled engineering comparison; demonstrated superiority, published numerical semantic scores and independent held-out evaluation are not Week 5 acceptance requirements.

The [controlled experiment specification](CONTROLLED_EXPERIMENT_SPEC_DRAFT.md), plan `W5-OPSMOKE-001`, asks:

> Across a prespecified development subset, what execution outcomes, mechanical validation results and descriptive assessment differences do the deterministic baseline and hosted model, as currently configured, produce?

Week 6 remains evidence validation, narrative drafting and integration; Week 7 remains held-out evaluation and safety/failure analysis. Those roadmap objectives are not rewritten or declared complete by this decision.

## 2. Owner-approved milestone conclusion

Week 5's bounded engineering-comparison objective is satisfied. The accepted work includes:

1. A fixed five-case development experiment selection.
2. Frozen prompt/configuration provenance.
3. Five preserved baseline observations.
4. Five validated hosted assessments.
5. Seven recorded SDK operations, including two failed operations.
6. Descriptive comparisons of recorded outputs.
7. Mechanical validation, accounting and preserved operational limitations.
8. The owner-reviewed decision that no additional hosted calls are justified solely to complete this milestone.

This is an engineering-comparison milestone closure. Classification accuracy, semantic correctness, model superiority, independent AML expert validation and held-out generalization remain unproven. The hosted classifier returned `investigate` in all five cases, but those outputs have not been established as correct or incorrect classification decisions.

Additional outputs without a defined evaluation question are not a justified next experiment. A future study requires a prespecified question, suitable selection and evaluation eligibility, provenance/exposure controls, bounded attempts and separate owner authorization. No such study or spending is authorized here.

## 3. Fixed selection and frozen comparison

The [development manifest](../../data/generated/development/manifest.json) records seed `20261027`, generator `1.0.0`, template lineage, 50 development inputs and 18 family/condition combinations. Selection was the first occurrence of each family in manifest order: the literal first five cases. Scenario metadata is not an adjudicated action label.

| Case ID | Scenario family | Frozen baseline | Hosted action |
| --- | --- | --- | --- |
| CASE-DEV-S20261027-0001 | `incoming_transfer` | `unable_to_recommend`, action `null` | `investigate` |
| CASE-DEV-S20261027-0002 | `cash_sales` | `unable_to_recommend`, action `null` | `investigate` |
| CASE-DEV-S20261027-0003 | `supplier_authorization` | `escalate` | `investigate` |
| CASE-DEV-S20261027-0004 | `incomplete_outgoing` | `investigate` | `investigate` |
| CASE-DEV-S20261027-0005 | `beneficiary_comparison` | `investigate` | `investigate` |

All ten assessments retain preliminary scope and required human review. The baseline observations are the five original offline-preflight artifacts, openly reused rather than regenerated or presented as newly executed prospective assessments.

The cases share synthetic generator/template lineage, including exposed golden-input concepts. They are not independently authored, representative or held-out evidence. No adjudicated action labels for these five cases or performance-cohort approval is implied.

### Original-byte and canonical validated-input identities

Each input is under `data/generated/development/` with its case ID as the JSON filename. Canonical hashes use the unchanged validated-model prompt serialization. They do not replace original-byte identities or normalize line endings.

| Case ID | Original-byte SHA-256 | Canonical validated-input SHA-256 |
| --- | --- | --- |
| CASE-DEV-S20261027-0001 | `61b0ec1bd414cc62052c3f0bd57e31474d9a5e72adb455dfb296cc6e50b0e613` | `e167f50429731373e2bec7bd630751344b26225bacc7a1f0962529b1ec60895e` |
| CASE-DEV-S20261027-0002 | `11370ba0cd8338fc6d4884c9fc1427e7de1d7d1213d7dc7efbab899f1de5b1d2` | `efc2f9e4066854aaa74feb5e13d266a505fb4dfffd60d6549ac2d31b9575db64` |
| CASE-DEV-S20261027-0003 | `1e5995d8f46cc8828239d342669f4934529b5a7ddea0ab28d486cc01ae938240` | `99d223d1dac7d1268ffdbbff93c8760744ec452b36d36977f76be29b9d935ccd` |
| CASE-DEV-S20261027-0004 | `5e5efdc25cf00ed67751f659a21f107339684ef88d7a18a0db504b2d97b1d49f` | `6f04a08bfb63c75c93be5c901a3ded2b02971a4f5f4ca9f4594b16bd9d00967d` |
| CASE-DEV-S20261027-0005 | `85d021c72ceed201dadd4f2161ce2289240743ddc003ef7e771f0e57c765424f` | `a37b2a3a9f58145fcb2b635bc8e07cbabf3db0e1fdd246ba367fb12f24dff797` |

## 4. Prompt, configuration and source provenance

- Deterministic baseline: `0.1.0`; hosted service: `0.1.0`; mechanical auditor: `0.2.0`; restricted amount predicate: `1.0`.
- Hosted model identifier: `gpt-6-luna`; SDK: `3.40.0`; inspected runtime: Python `3.11.9` and Pydantic `2.14.1`.
- Prompt: `aml-preliminary-1.0`. Instructions SHA-256: `f6472c5d27337626e113cfa982297b0c6b317282eefc4a600f049fa025bb6c83`.
- Pydantic output-schema SHA-256: `4e6a81a31aa2450418303a55617ca10d7cb0260af30a14399f582a461f91338b`, over UTF-8 sorted compact JSON with `ensure_ascii=False` and `allow_nan=False`.
- All five successful hosted requests used a 4,800-output-token ceiling, 60-second timeout, reasoning `none`, request allowance one, zero SDK/application retries and `store=false`.
- The two earlier Case 0001 operations used a 2,400-token ceiling. Later calls had separate owner approvals; the original draft proposal and its pending language are preserved historically.
- One frozen prompt version was used. No multi-prompt optimization comparison is claimed.
- The baseline implemented REF-01 logic not supplied in full to the hosted instructions. This unequal policy access precludes an equal-policy performance interpretation.

The source/evidence index records the actual checkout, eleven pinned source hashes, fourteen dependency versions, prompt/schema identities and artifact paths. Those identities were freshly verified before recording this closure on `main` at `c8e2f53540776ba2ec1bb3079d8d40043606173b`. A configured model name is not an immutable provider snapshot.

The unchanged application supplies developer instructions, validated investigation JSON and the structured-output schema. It does not add baseline assessments, manifest condition labels, references, adjudications, prior candidates or review feedback to generation. Application-level verification does not establish complete provider-side exposure isolation.

## 5. Execution, validation and accounting

Ten logical slots comprise five historical baseline observations and five hosted assessments. Seven recorded SDK operations include Case 0001's authentication failure, incomplete response and later validated assessment, plus one validated assessment for each remaining case. Every release is consumed; remaining owner and Codex live allowances are zero. No allowance is reopened or transferred.

All five hosted bundles preserve original candidate text, candidate SHA-256 and parsed assessment. All ten input/output/contextual-reference checks and original audits replay successfully offline. Hosted embedded audits reproduce using canonical input; raw-input audit outcomes agree. Baseline audits reproduce through their original file interface.

| Arm | Findings | Checked | Matches | Conflicts | Unchecked |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 17 | 9 | 9 | 0 | 8 |
| Hosted | 29 | 0 | 0 | 0 | 29 |

These counts describe the restricted whole-statement transaction-amount grammar, not semantic quality. Zero conflicts does not verify unchecked findings. All nine broad experiment semantic-evaluation dimensions remained `not_evaluated`.

SDK-operation counters are not independently verified network or billed-request counts. Actual billing remains unknown. Six operations have complete returned usage, totaling a known subtotal of 11,543 input / 9,066 output / 20,609 tokens; the authentication operation has unknown usage, so this is not a complete experiment total or bill. Historical estimates remain estimates; no new pricing estimate or monetary balance is asserted.

Cases 0002-0004 terminal CLI exits remain unknown. Initial failure exit 1 is tool-recorded; incomplete Case 0001 exit 1 and successful Case 0001 exit 0 are owner reports. Case 0005 exit 0 remains owner-reported with its recorded display limitation. Validated service status is not substituted for terminal evidence. The 4,800-ceiling follow-up does not prove that increasing the ceiling caused success or establish a necessary minimum.

## 6. Existing evidence and review history

The following evidence is **local-only and Git-ignored**. Inline paths are not repository download links; a normal clone/CI environment may lack the files.

| Evidence | Exact local repository-relative path |
| --- | --- |
| Original offline baseline/dry-run inventory | `outputs/experiments/W5-OFFLINE-PREFLIGHT-20261030T182524Z/inventory.json` |
| Source, prompt, runtime and original artifact identities | `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/00-source-and-evidence-index.json` |
| All seven original bundles, releases, intents and closures | `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/01-attempt-and-authorization-accounting.json` |
| Complete descriptive comparison | `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/02-five-case-comparison.json` |
| Audit replay and restricted coverage | `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/03-mechanical-coverage.json` |
| Configuration, exposure and policy-access limits | `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/04-controls-and-interpretation-limits.json` |
| Unadjudicated observations and original pointers | `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/05-outstanding-observations.json` |
| Specification requirement reconciliation | `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/07-specification-completion-matrix.json` |
| Finalized whole-review verification | `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/09-review-verification.json` |
| Earlier owner acceptance of bounded operational closure | `outputs/experiments/W5-OPSMOKE-001-BOUNDED-CLOSURE-20261031T164640Z/00-bounded-objective-closure.json` |
| Earlier closure's final preservation record | `outputs/experiments/W5-OPSMOKE-001-BOUNDED-CLOSURE-20261031T164640Z/02-closure-verification.json` |

The historical whole-review matrix's pending owner-closure row was followed by the bounded operational acceptance. This new dated decision records the subsequent broader Week 5 engineering-milestone approval. Prior pending, unexecuted, no-broader-closure and backup-status statements describe their original checkpoints; none are rewritten as prospective or current evidence.

| Evidence binding | Original-byte SHA-256 |
| --- | --- |
| [Controlled experiment specification](CONTROLLED_EXPERIMENT_SPEC_DRAFT.md) | `415e71c2500ef528c57853d616be2d095d266bab5cbb4710a4ee571787799baa` |
| [Development manifest](../../data/generated/development/manifest.json) | `6b4342f3a98c6426723f22ee2f5816540dc8f0bd0bd2e166fbde09a23c38bfb9` |
| Local-only `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/SHA256SUMS.txt` | `99100ff97bcd22e1f11be92369aca7d4a487817651ec91b3dd6908867fe0a31e` |
| Local-only `outputs/experiments/W5-OPSMOKE-001-BOUNDED-CLOSURE-20261031T164640Z/SHA256SUMS.txt` | `725e13d5392819465b723d02cab9670efbcfc7f6f40ee0d024a2ddccc07292b6` |
| [P01 fidelity addendum](../phase-2/G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) | `34acbce3f39a6844afc99030687dfa308150659020cb8ee7643c066c5a6bdcfc` |
| [P02 materiality addendum](../phase-2/G02_P02_MATERIALITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) | `2fc6ec4bbaa2352a74382ebd2823f2e2daa5e51001999335e700817dff04ad8b` |

The unchanged whole-review checksum manifest binds its other eleven packet files; the unchanged bounded-closure checksum manifest binds its three other supplement files. No circular self-hash is introduced.

## 7. Evaluation restrictions and remaining responsibilities

- **P01:** Owner-approved [fidelity ruling](../phase-2/G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) remains intact. Stronger drafted personal-authorship claims do not automatically become candidate factual errors or unconditional statement passes.
- **P02:** Owner-approved [materiality ruling](../phase-2/G02_P02_MATERIALITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) remains intact. M04 is contextual and nonmandatory for frozen G02, not inherently immaterial. M01-M03 remain mandatory; the qualified profile-fit question and wording restrictions remain.
- **P03:** Reporting methodology, category applicability, denominator eligibility and scoring permission remain under review. The saved reconciliation still has `scoring.authorized=false` and `rates=null`. No numerical semantic-performance scoring or ranking is released.
- **P04:** Formal versioned adjudication/report release remains separately controlled. This is not a new semantic-evaluator implementation approval or a machine-readable adjudication release.
- **P05:** Independent evaluation and expert-review conditions remain subject to their applicable later milestones. No independent AML expertise, held-out result or generalization is claimed.

The [adjudication register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json), [reconciliation specification](../phase-2/G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md), original annotations and saved reports are unchanged. Their historical pending fields are not automatically reconciled by this document. G02 decisions are not transferred to the five experiment cases.

Case-specific wording, attribution, materiality, missing-information, completeness and policy questions remain in the existing observation registry without adjudication. Case 0003's action difference does not identify a winner; Case 0004's missing purpose does not prove illegitimacy; Case 0005's absent invoice account reference establishes an unknown comparison rather than a proven mismatch.

Continue preserving ignored evidence and backup coverage under separately approved procedures. This closure performs no backup or cloud operation and does not recertify existing backups. Later evidence/narrative integration and held-out quantitative work require their own approved scope. No outstanding issue is silently converted into a successful semantic result.

## 8. Documentation preservation and verification

Before writing, checks passed for all 20 historical checksum manifests / 266 entries, the 315-path bounded checkpoint, 164 original experiment artifacts, all 12 finalized review files, five baselines, seven bundles, five hosted candidate identities, ten assessment audit replays, eleven source hashes and fourteen dependency versions. Existing G02 integrity checks also passed for 75 units, 21 statements and 203 source pointers.

Existing uncommitted status/worklog content matched the accepted checkpoint, with no conflicting edits or merge markers. The only authorized existing-file changes are an inserted current-status notice and appended worklog/ADR entries. All earlier status text is recoverable by removing only the inserted block; the worklog and decisions retain their complete previous bytes as prefixes.

| Authorized existing document | Before original-byte SHA-256 | After original-byte SHA-256 |
| --- | --- | --- |
| [PROJECT_STATUS.md](../../PROJECT_STATUS.md) | `eab6cc275aeece78a68ff09e476d9b7161ccbc1ca42a3277465c2f1f80e2da4e` | `17db9ac1f666ed6a7b55132669a58ff8237c7eee7cf16af08f9d461c39f0e31e` |
| [WORKLOG.md](../../WORKLOG.md) | `8f0754f45465c233038ce7f7ebc176f0fb4016dd40039c64dd837701eb6ed3dc` | `cd9c72988cad9b6a1830650dc6acd56ef846f1926b00ee27c82d79d4a4d5fbbf` |
| [DECISIONS.md](../../DECISIONS.md) | `69effccb18bbb089cea5574879e5d3be6602e663ed529671f1f08f09ef9c9c9b` | `cd59433d0d195220cd281938b37f5976f9801083f5474d0a26dc1d0c9aef5538` |

The unchanged 315-path historical reference includes these three documents. Their old recorded hashes remain historical; current hashes change only through this newly authorized documentation step. The table records that distinction rather than rewriting the frozen reference or treating authorized changes as corruption. Every other pre-existing project file must remain byte-for-byte unchanged; the new decision document is outside that historical inventory.

No application tests were changed or run, and no fresh full-suite or remote CI result is claimed for this documentation-only checkpoint. Fresh checks validate local identities and existing validator/auditor behavior, not semantic truth, authenticated approvals, remote model weights or provider billing. Original absolute report paths and LF/CRLF distinctions remain unchanged; no portable report-byte guarantee is added.

## 9. Stopping boundary

Week 5 is formally closed on the approved bounded engineering objective. **Week 6 has not started and is not authorized.**

No new experiment, hosted call, retry, fallback, spending, allowance reset, numerical scoring, model ranking, code/prompt/contract/policy/dataset change, architecture change, external-backup change, Git staging/commit/push/pull/fetch/reset/merge/branch change, or publication is authorized or performed by this documentation task.

The next action is owner review of the recorded closure. Any Week 6 work requires a separate explicit owner instruction with its scope and acceptance checks.
