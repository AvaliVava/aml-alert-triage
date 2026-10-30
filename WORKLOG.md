# Engineering Work Log

## 2026-10-26 — Week 1, Day 1: project foundation

**Goal:** Establish a reproducible starting point and create a written domain/engineering boundary before implementing the LLM workflow.

**Completed in this working environment:**
- Prepared initial project charter, roadmap, status and decision records.
- Drafted AML alert lifecycle and primary-source research notes.
- Created small Python package skeleton with a status CLI (no AML logic).
- Added dependency-free setup check, unit tests and an initial GitHub Actions workflow.

**Verified locally:** See the test results recorded below. The test environment and Python version may differ from the project owner's machine.

**Not completed:** No remote repository or GitHub commit; no classifier; no synthetic data; no model experiments. No claims of accuracy or time savings.

**Research evidence:** FFIEC BSA/AML Examination Manual and FinCEN narrative guidance links in `research/primary_sources.md`.

**Next:** Owner reviews `specs/aml_workflow.md` and charter. Publish reviewed scaffold into a new GitHub repository, then connect Codex.

**Local test result:** Python 3.13.5; `python scripts/check_setup.py` passed, and `python -m unittest discover -s tests -v` passed **3 of 3 tests**. Python 3.11/3.12 and GitHub CI have not yet been executed.

## 2026-10-26 — Phase 1 closeout and Phase 2 golden cases (retrospective)

**Record basis:** This and the following retrospective entries use commit dates from Git (UTC+03:00). Commit dates establish checkpoint chronology, not exact editing or test-execution times. The original foundation entry above remains a historical snapshot.

**Completed:** Phase 1 documentation was reviewed and merged through PR #1 as `a5c68d0`. Phase 1 is complete, as recorded in [PROJECT_STATUS.md](PROJECT_STATUS.md).

**Phase 2 artifacts:** Commit `7438b40` added five valid synthetic golden-case inputs, one deliberately invalid duplicate-transaction sibling, five separate reference-answer artifacts, a fictional labeling policy, and fixture-integrity tests. PR #2 merged this work as `db212d4`. The files are present under [golden cases](data/golden_cases/) and [labeling policy](specs/labeling_policy_v1.json).

**Boundary:** These are draft synthetic artifacts, not a full synthetic-history generator or finalized evaluation labels. Reference answers remain separate from investigation inputs.

## 2026-10-27 — Phase 2 input-contract implementation (retrospective)

**Goal:** Implement the existing golden-case input structure as Pydantic V2 contracts without adding AML classification, SAR decisions, LLM logic, or new verification activities.

**Implementation checkpoints, in Git order:**

| Checkpoint | Completed scope |
| --- | --- |
| `6fab3bc` | Customer and Account contracts, with the ExpectedMonthlyActivity helper; Pydantic V2 application dependency and project installation in CI |
| `a68e858` | Transaction contract, including amount and timezone-aware timestamp validation |
| `21137bf` | Counterparty, Alert, and CaseMetadata contracts |
| `e6094f9` | Evidence and VerificationCheck contracts, preserving heterogeneous JSON facts and supplied synthetic check results |
| `1375d9f` | Complete InvestigationInput contract, composing the existing records with duplicate-ID, duplicate-reference, cross-record integrity, and input/reference-boundary checks |

**Implementation evidence:** [contracts.py](src/aml_triage/contracts.py), [contract tests](tests/test_contracts.py), and [fixture-integrity tests](tests/test_golden_fixtures.py). Earlier test assertions were retained as the contract suite expanded.

**Local readiness-audit results at `1375d9f`:** The audit recorded Python 3.11.9, Pydantic 2.14.1, and **99 passing tests** for `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`. The setup smoke check and installed dependency consistency check also passed. These are the previously verified audit results recorded in [PROJECT_STATUS.md](PROJECT_STATUS.md), not new test runs performed during documentation reconciliation; the exact audit execution time is not recorded here.

**Completion-audit findings:**

- All five valid golden cases are accepted through Python and JSON validation. The intentionally invalid [duplicate fixture](data/golden_cases/inputs/G05_invalid_duplicate.json) is rejected.
- Standalone record contracts remain usable; aggregate validation enforces duplicate-ID and explicit-reference integrity while preserving valid incomplete investigations.
- Valid incomplete and contextual inputs remain supported, including null counterparty references, missing beneficiary information, and G04 evidence referring to `TX-105` outside the alert's flagged subset.
- Reference answers and provisional labels remain separate from inputs. Input validation performs no AML classification, SAR determination, LLM reasoning, or real banking verification.
- Pydantic is declared as an application dependency, and the [CI workflow](.github/workflows/foundation-tests.yml) installs the project before running checks on Python 3.11, 3.12, and 3.13. Remote feature-branch GitHub Actions results remain **unverified**; local success does not prove remote CI success.
- No blocker was identified in the approved input-contract implementation scope. Stale documentation required reconciliation; the CLI's historical `week-1-foundation` label remains unchanged and is explained in current setup documentation.

**Remaining Phase 2 work:** Output contracts, a formal evaluation protocol, and review of the fictional labeling vocabulary and provisional labels. Input-contract completion does not close all of Phase 2 or establish model-performance results.

## 2026-10-27 — Documentation Checkpoint A

**Committed checkpoint:** `f983cbc9ad03e35a3a1a3e774e4a2b4a1c8a974a` (`f983cbc`), confirmed from local Git history with the message `docs: align project setup and status with Phase 2 contracts`.

**Completed and human reviewed:** Reconciled [PROJECT_STATUS.md](PROJECT_STATUS.md), [README.md](README.md), and [START_HERE.md](START_HERE.md) with the implemented input contracts and pending Phase 2 work. Documented editable installation, virtual-environment reuse, the Windows Python launcher alternative, complete-suite commands, and the existing-repository workflow. Corrected the contract-test link label and made the PR workflow explicit: finalize documentation, push the feature branch, open the PR, check GitHub Actions, and merge only after successful review and CI.

**Verification:** Documentation diff checks passed. Source code and tests were unchanged, and the suite was not rerun for those documentation edits. The 99-test baseline remains the earlier local audit result; this documentation commit does not establish remote CI success.

## 2026-10-27 — Documentation Checkpoint B1

**Goal:** Reconcile only [ROADMAP.md](ROADMAP.md), [DECISIONS.md](DECISIONS.md), and this worklog with the completed input-contract work.

**Preflight:** The working tree was clean on `feature/phase-2-pydantic-contracts`, and Documentation Checkpoint A was already committed as `f983cbc`.

**Completed:** Added current roadmap progress while preserving the broader sequence and the historical Phase 1 snapshot. Appended ADR-005 through ADR-011 for the accepted contract decisions and their tradeoffs, preserving earlier decision records. Added the retrospective implementation and Documentation Checkpoint A records above without changing earlier worklog entries or dates.

**Documentation checks:** `git diff --check` passed; `git status --short` and `git diff --stat` confirmed changes only in the three authorized documents. Local links resolve, and earlier ADR and worklog text is preserved.

**Verification boundary:** These are documentation-only edits. The unit suite, setup check, dependency check, and remote Actions are not rerun in this checkpoint; no implementation or remote CI status is changed. Human review is required before committing this documentation checkpoint.

## 2026-10-27 — Input contracts merged through PR #3

**Git evidence:** PR #3 merged the input-contract branch into `main` as `327e600308874dfb1ab6394308a5e8e03998be6c` (`327e600`). This records the merge, not a newly verified GitHub Actions result.

## 2026-10-27 — Output Contract Implementation Checkpoint 1

**Committed checkpoint:** `a538063a47b381f74af87a6c77b7055703ced6bc` (`a538063`), `feat: add standalone AML investigation output contracts`.

**Completed:** Added `RecordCitation`, `CitedStatement`, `Contradiction`, and `InvestigationOutput` in [contracts.py](src/aml_triage/contracts.py). The models separate factual findings, interpretations, unresolved questions, missing information, and contradictions. They accept the provisional actions `close`, `investigate`, and `escalate`, or explicit abstention with `assessment_status="unable_to_recommend"` and `recommended_action=null`. Every output requires preliminary scope and human review. Strict field/list validation, citation requirements, duplicate-citation rejection, and preserved text/order are covered by [contract tests](tests/test_contracts.py).

**Testing history:** Added 26 test methods, expanding the 99-test baseline to the reported **125 passing local tests**. The checkpoint's Git date establishes implementation chronology, not the exact time of that earlier test run. The complete current suite is confirmed separately below.

## 2026-10-27 — Output Contract Implementation Checkpoint 2

**Committed checkpoint:** `ce0cd4a3edbdb5d1f9a5698639ccebe893b794d8` (`ce0cd4a`), `feat: validate AML investigation output references`.

**Completed:** Added the separate `validate_investigation_output_references` function for already-validated input and output models. It checks exact case/alert identities and citations in every statement location against eight namespaces: case, customer, account, counterparty, transaction, alert, evidence, and verification_check. Contextual errors include field paths; successful validation returns the same output and mutates neither object.

**Testing history:** Added 19 dedicated relationship-validation test methods, bringing the suite to **144 local tests**. Coverage includes all namespaces and statement locations, wrong or unknown references, exact matching, G04's supplied `TX-105` outside the alert subset, contextual evidence, nullable counterparties, abstention, no mutation, and no policy/reference-answer reads by contextual validation. Existing code and test assertions were preserved while adding this function and its tests.

**Boundary:** Resolving a citation establishes record existence only. Neither checkpoint evaluates factual support, verifies supplied claims, generates an assessment, chooses a disposition, or implements AML/SAR decision logic. Candidate test outputs are independent of reference-answer artifacts.

## 2026-10-27 — Output Contract Documentation Checkpoint

**Preflight:** Confirmed a clean working tree on `feature/phase-2-output-contracts`, HEAD `ce0cd4a`, and both implementation commits present. Input contracts are merged into `main` through PR #3; both output checkpoints are committed locally and remain unmerged.

**Documentation:** Reconciled [PROJECT_STATUS.md](PROJECT_STATUS.md), [README.md](README.md), [ROADMAP.md](ROADMAP.md), [DECISIONS.md](DECISIONS.md), and this worklog with the implemented output structure, separate contextual validation, and their limits. Preserved historical worklog entries, ADRs, and earlier test results.

**Fresh local verification:** `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` passed **144 of 144 tests** at `ce0cd4a` during this checkpoint. No code or tests were changed. Setup/dependency checks were not rerun, and remote GitHub Actions results for the output-contract branch remain **unverified**.

**Still pending:** Output documentation review and the output-contract PR workflow, the formal evaluation protocol, and review of provisional labels. Phase 2 is not complete. No AML classifier, LLM investigation agent, automated verification system, or complete triage pipeline has been implemented. Stop for human review before committing these documentation changes.

## Local Phase 2 checkpoint — evidence relationships after PR #6

**Preflight:** Clean working tree on `feature/phase-2-evidence-relation-checks` at `54b0cf87b78763ddb21a593a2678925137cb7acc`, the PR #6 merge commit also identified by local `main` and `origin/main`.

**Implemented:** Added the standalone [evidence relationship evaluator](src/aml_triage/evidence_relation_checks.py) and [33 development tests](tests/test_evidence_relation_checks.py). Reused existing input/output contracts and contextual citation validation. The restricted predicate compares the actual beneficiary-reference fields in `EV-004` and `EV-005`, checks evidence types and their explicit `TX-105` links, and independently reports consistency with the annotated equality/difference proposition and citation coverage of both direct records.

**Annotation boundary:** Version 1.0 evaluation-only annotations are supplied separately and bound to exact payload digests, case identity, finding index and statement text. They remain unreviewed development examples. Invalid or stale annotation configuration, ineligible sources and unannotated findings produce no factual judgment. Candidate prose is not interpreted, and annotation authorship is not authenticated. Check-record citations do not replace the two direct sources under this narrow policy.

**Fresh local verification:** The complete unittest suite passed **237 tests**, including all 204 existing tests and 33 new tests. `python -m pip check` reported no broken requirements. Existing source files, tests, golden artifacts, dependencies, auditor reports and CLI exit codes are unchanged. No policy, reference-answer or LLM access is used by the evaluator; no new fixtures or finalized annotations were created.

**State and limits:** Implementation is uncommitted and awaiting independent review. These comparisons establish neither authenticity, fraud, fund tracing, violated supplier instructions nor recommendation quality. No remote GitHub Actions result or model-performance result is claimed, and Phase 2 remains open. Earlier worklog entries are retained as historical records.

## Week 3 local checkpoint — seeded synthetic investigation generator

**Preflight and chronology:** PR #7 merged the evidence-relationship work into `main` as `d0b8a6a`. The working tree was clean at that base; `feature/week-3-synthetic-generator` did not yet exist and was created before editing. The existing 237-test suite passed before implementation. Earlier entries retain their original checkpoint context.

**Implemented:** Added [synthetic_generator.py](src/aml_triage/synthetic_generator.py), [generate_dev_cases.py](scripts/generate_dev_cases.py) and [32 generator tests](tests/test_synthetic_generator.py). A local seeded random instance builds five fictional template families with 18 source-condition variants. Stable IDs, timezone-aware chronology, decimal monetary strings and explicit references are validated by the unchanged `InvestigationInput` model. Publication rejects existing destinations and stages the entire validated batch, checking written bytes before publishing the directory; ordinary failures clean up staging and the exclusive publication lock. Process interruption may leave hidden staging/lock artifacts for inspection.

**Actual deliverable:** [50 development investigations](data/generated/development/) generated with seed `20261027`, ten per family. Their separate [manifest](data/generated/development/manifest.json) records generator/template versions, family lineage, source conditions, case IDs and input SHA-256 digests; its SHA-256 is `6b4342f3a98c6426723f22ee2f5816540dc8f0bd0bd2e166fbde09a23c38bfb9`. Regeneration into a separate temporary directory reproduced all 51 files byte for byte. All 50 delivered inputs validate and all input digests match the manifest. Added a narrowly scoped [.gitattributes](.gitattributes) rule because local `core.autocrlf=true` would otherwise transform generated JSON bytes on checkout.

**Fresh local verification:** Full unittest discovery passed **269 tests**, including all 237 existing tests and 32 new generator/publication/CLI tests. Dependency verification reported no broken requirements. Tests cover meaningful source variation, nullable and contextual records, missing information, chronology, references, no label leakage, no golden mutation, no generation-time file/network/model access, deterministic bytes and failure-safe publication. No existing contracts, tests, golden artifacts, dependencies, auditor interfaces or policy were changed.

**Documentation and boundaries:** Updated only directly relevant current progress in [PROJECT_STATUS.md](PROJECT_STATUS.md) and [ROADMAP.md](ROADMAP.md); preserved earlier history and decisions. These cases share generator/template lineage, have no adjudicated AML actions and are not independently authored or held-out data. No classifier, recommendation baseline, LLM, banking verification or general semantic evaluator was added. The historical foundation status command was left unchanged. Week 3 baseline implementation and remaining evaluation adjudication are pending; remote CI is unverified. This checkpoint is uncommitted and stops for independent review.

## Week 3 local checkpoint — first deterministic triage baseline

**Preflight:** Clean working tree on the requested `feature/week-3-deterministic-baseline` branch at `eeef96f`, the PR #8 merge of the synthetic generator. The unchanged 269-test suite passed before implementation. Prior worklog entries preserve the state at their respective checkpoints.

**Implemented:** Added [deterministic_baseline.py](src/aml_triage/deterministic_baseline.py), [run_baseline.py](scripts/run_baseline.py), and [47 focused regression/CLI tests](tests/test_deterministic_baseline.py). The public `assess_investigation` function accepts a validated input, derives findings from actual supplied fields, builds the existing preliminary/human-review output contract and resolves typed citations before returning. Rule IDs appear in statement text; no schema fields were added. Fixed rules cover scoped information gaps, direct invoice/wire comparisons, flagged cash sums and individual daily-range comparisons, reconciliation/POS gaps, and the narrow fictional REF-01 conjunction in both supplied payment formats.

**Interpretation and limits:** REF-01 relies on recognized supplied synthetic ledger/internal-log/procurement provenance; it performs no independent authentication. The detector requires matching account mappings, linked transfers after an aware instruction timestamp, explicit register approval/change fields and an exact supported review-instruction form. It ignores check-status conclusions, distinguishes supplier from payee-account identity, and adds no bypass requirement or senior-review exception. Unsupported/mixed/conflicting records cannot establish referral; historical/future authorization snapshot semantics and arbitrary instruction prose remain unsupported. Missing-information investigation requires a concrete supplied-scope question; unflagged context transactions do not create a universal document requirement. Decision priority is supported escalation, then a material unresolved question, then abstention. No automatic closure is implemented, and the provisional labels and semantic evaluation protocol are not finalized by this work.

**Actual demonstrations:** Used the new CLI with explicit destinations to create five local candidate artifacts under ignored `outputs/baseline-v0.1.0-development/`: G03 → `escalate` (`REF-01`); authorized-change case `0008` → `unable_to_recommend` with null action; partial-sales `0007` → `investigate` (`CASH-03`); beneficiary mismatch `0015` → `investigate` (`BEN-01`); incomplete-beneficiary `0009` → `investigate` (`MI-01`). Outputs include full factual findings, typed citations, unresolved questions and applicable rule IDs in text. The partial-sales input's four deposits total GBP 31,564.23 with a recorded GBP 9,246.11 unmatched amount; individual daily-range statements cite the customer profile. The existing auditor CLI accepted G03's candidate structurally/contextually and retained all nine broad semantic dimensions as `not_evaluated`. No accuracy, precision, recall or savings were measured.

**Fresh verification:** Full unittest discovery passed **316 tests**, all 269 existing plus 47 new. `python -m pip check` found no broken requirements. Tests cover all five golden inputs and 50 generated development inputs, contextual citations, determinism/nonmutation, counterfactual referral conditions, missing/unknown/conflicting records, Decimal arithmetic, timezone comparisons, explicit abstention, no baseline-time file/network/reference/manifest/policy access, and safe CLI publication/overwrite rejection. Existing contracts, tests, fixtures, manifest, policy, dependencies and auditor/checker interfaces were not changed. Local demonstration outputs are separate from inputs/references and are not tracked dataset artifacts.

**Review state:** Updated directly relevant status and roadmap progress while preserving earlier records. No LLM, RAG, agent, extensive policy engine, real banking verification, general evaluator or regulatory decision logic was introduced. The CLI uses same-filesystem hard-link publication and fails safely if that operation is unsupported. Remote CI remains unverified. This work is unstaged, uncommitted and stops for independent review.

## Week 3 review correction — REF-01 bank-recipient reconciliation

**Observed and reproduced:** A directly linked bank wire could contradict the supported payment ledger's recipient without blocking referral. Added eight counterfactual tests in [test_deterministic_baseline.py](tests/test_deterministic_baseline.py); the conflicting-wire tests reproduced false escalation in both the original G03 aggregate format and the generated row format before the fix.

**Targeted correction:** [deterministic_baseline.py](src/aml_triage/deterministic_baseline.py) now checks explicit beneficiary-account references in directly linked `synthetic_bank_ledger` wire records against qualifying ledger mappings. A disagreement blocks REF-01 escalation and records an unresolved question citing both bank records and the affected transaction. Existing mapping construction remains unchanged: wires cannot independently establish referral, and unrelated wires or invoice instructions do not override recorded recipients. Exact account equality is preserved; unsupported sources and formats are not new referral evidence.

**Fresh verification:** Full unittest discovery passed **324 tests**, including all previous 316 tests and eight new methods. All 55 baseline tests passed; every new counterfactual validates the complete investigation, output and contextual references. Dependency verification found no broken requirements. All five original CLI demonstrations reproduced unchanged outputs, and the existing auditor CLI retained its mechanical success and nine unevaluated semantic dimensions. A temporary G03 conflicting-wire CLI example recommended `investigate`, citing `REVIEW-CONFLICTING-WIRE`, `EV-G03-03` and `TX-G03-01`. No persistent fixtures or demonstration outputs were changed.

**Scope and limits:** Only the baseline module, its test module, current project status and this appended worklog entry changed during the correction. Earlier implementation records above remain historical. No contracts, policy, auditor, generator, fixtures, dependencies, CLI or roadmap changes were made during this correction. The guard reports the first blocking supported wire conflict; it does not enumerate every discrepancy, authenticate sources or provide general semantic evaluation. Work remains unstaged and uncommitted for independent review; remote CI is unverified.

## 2026-10-28 — Week 4, Checkpoint 1: OpenAI Structured Outputs compatibility

**Preflight and chronology:** Clean working tree on `feature/week-4-openai-schema` at `3c4e3fd58e3ac6b6c0676431528741957a7bb5a6`, confirmed in local Git as the PR #9 merge of the deterministic baseline. Earlier pending review/merge entries remain historical. Corrected directly relevant current status and roadmap descriptions of that merge.

**Compatibility investigation:** Added the [OpenAI-specific report](docs/week-4/OPENAI_SCHEMA_COMPATIBILITY.md), covering the full generated schema, official strict Structured Outputs requirements, nullable/reference structures and custom-validator boundaries. Inspected the published SDK 3.40.0 wheel without installing it or its dependencies. Isolated normalization and request-format helpers produced a schema exactly equal to the raw Pydantic schema, with name/type/strict in the request envelope. An isolated text-parser check accepted valid abstention and propagated the custom boolean-True validation error. No adapter, transport model, production client or compatibility code was needed or introduced. The report distinguishes these helper checks from full SDK or live API compatibility.

**Fresh verification:** All **324 existing unit tests passed** on Python 3.11.9/Pydantic 2.14.1. Dependency verification found no broken requirements; syntax checks passed for all 22 tracked Python files. Another 32 independently authored JSON probes exercised Pydantic, contextual validation and mechanical auditing: 22 structural rejections, four contextual rejections and six mechanically accepted examples. Existing-ID false/unsupported assertions retained unevaluated broad semantic dimensions; the existing amount checker separately detected the G02 USD 99,999.00 versus USD 48,500.00 conflict. The merged G03 baseline output passed complete JSON round-trip/contextual validation. No new unit-test methods were added because no compatibility implementation was introduced.

**Boundaries and review state:** No credentials were generated/accessed, no hosted-model requests were made and no dependency was added. SDK artifacts were inspected as package contents; the project environment still has no OpenAI SDK installed. Existing contracts, domain rules, baseline, evaluator, tests, fixtures and policy remain unchanged. Live request acceptance, target-model constraint enforcement, full installed-SDK handling and remote CI remain unverified. Semantic adjudication and provisional-label review remain pending. Documentation changes are unstaged and uncommitted; stop for independent review before committing.

## 2026-10-28 — Week 4, Checkpoint 2: guarded OpenAI assessment service

**Preflight:** Clean working tree on `feature/week-4-openai-integration` at `4e95484c479f5a73234bcd293b23468a84365891`, the PR #10 merge. Earlier compatibility and implementation entries preserve their historical state.

**Implemented:** Added [openai_prompt.py](src/aml_triage/openai_prompt.py), [openai_service.py](src/aml_triage/openai_service.py), [run_openai_assessment.py](scripts/run_openai_assessment.py), [34 focused tests](tests/test_openai_service.py) and [integration documentation](docs/week-4/OPENAI_INTEGRATION.md). Prompt `aml-preliminary-1.0` separates stable instructions from actual supplied JSON, with SHA-256 identities. The service uses existing Pydantic Structured Outputs, snapshots the input, validates original final candidate text, resolves citations and preserves the separate auditor report. Refusal, incomplete/missing output, structure/reference failures and API categories return structured outcomes without provider-message/credential logging.

**Dependency evidence:** Checked published SDK 3.40.0 metadata, pinned `openai==3.40.0` and installed the editable project. Existing Pydantic 2.14.1 and Python compatibility constraints were retained; no unrelated installed package was upgraded. Dependency metadata evaluated consistently for Python 3.11–3.13, and relevant jiter/pydantic-core Windows wheels exist for each. Runtime testing used 3.11.9. Cross-version pip resolution for 3.12 timed out twice (including the network-permission retry), so no successful 3.12/3.13 installation or runtime test is claimed.

**Fresh verification:** Full unittest discovery passed **358 tests**, all 324 existing plus 34 new methods. `pip check` found no broken requirements. Syntax checks passed for all 26 Python files; Git whitespace checks included untracked files, local documentation links resolve and existing source/test/fixture hashes are unchanged. Tests exercise real installed SDK parsing over in-memory transports, prompt/data separation, validation boundaries, redaction, one-request concurrency/reuse, disabled defaults and safe CLI/publication paths. No hosted request occurred; API-path tests inject mock boundaries and block socket connections. The CLI dry run reported zero attempts. A marked mocked G02 demonstration saved an ignored bundle under `outputs/openai/`, made exactly one in-memory transport call, preserved raw candidate text and refused a second attempt. Its token counts are supplied mock metadata, not measured model usage or billed costs.

**Limits and review state:** Live mode remains off by default; explicit model, output ceiling, allowance 1 and opt-in are required, with `store=False` and zero automatic retries. Timeouts can follow billable server processing; the local guard is not a billing cap. SDK Pydantic exceptions can hide original response text/status/request ID/usage; these are recorded as unavailable. General semantic evaluation, approved model/spend choices, the first live smoke test and provisional-label adjudication remain pending. Updated only directly relevant current status/roadmap; contracts, baseline, auditor, existing tests, golden/development datasets and policy are unchanged. Work is unstaged and uncommitted for independent review; remote CI is unverified and Phase 2 is not declared complete.

## 2026-10-28 — Checkpoint 2 review correction: reproducible runtime dependencies

**Observed issue and scope:** The reviewed service already pinned SDK 3.40.0, but its transitive dependencies and Pydantic resolution were unconstrained. Continued on `feature/week-4-openai-integration` at `4e95484`, preserving the existing unstaged implementation. No service, prompt, CLI, contract, test, fixture or policy behavior changed.

**Correction:** Added [constraints.txt](constraints.txt), derived from the 14-package SDK/Pydantic dependency closure at the already tested versions, rather than a whole-environment freeze. The [CI matrix](.github/workflows/foundation-tests.yml), [README](README.md), [setup guide](START_HERE.md) and [integration guide](docs/week-4/OPENAI_INTEGRATION.md) now consume it through `python -m pip install -c constraints.txt -e .` and include dependency checks. Replaced the stale future-lock comment in [pyproject.toml](pyproject.toml); the SDK pin, Pydantic requirement and Python range are unchanged. Documented the update procedure and the limits: runtime versions are pinned, while interpreter patches, build tools, distribution hashes and optional SDK extras are not.

**Executed verification:** A fresh temporary Python 3.11.9 environment installed the constrained editable project, passed the smoke check and `pip check`, and passed all **358 tests**. The existing environment also passed all 358 tests and `pip check`; installed runtime versions did not change. With pip 24.0, targeted resolution/download obtained all 14 wheels for both Windows amd64 and Linux x86_64 on 3.11. Requirement-graph/marker and `Requires-Python` checks passed for all six Python/platform combinations; relevant binary wheels are published for 3.11, 3.12 and 3.13. Four 3.12/3.13 target download probes timed out after 150 seconds each; the Windows 3.12 retry outside the sandbox also timed out during a wheel download. These are not completed cross-version installs or runtime tests, nor evidence of an incompatible dependency graph. Remote GitHub Actions remains unverified.

**Review boundaries:** Syntax, local documentation links and whitespace checks passed. No existing runtime package was upgraded, no dependency manager was added and no credentials or hosted-model calls were used. The constrained CI matrix is configured for future actual Linux 3.11/3.12/3.13 testing. Changes remain unstaged and uncommitted for independent review.

## 2026-10-29 — Week 4, Checkpoint 3A: verify the first hosted G02 assessment

**Repository and scope:** PR #11 merged the service as `c6afb7149c0b0722e4638618ba41d2db8599e2ff`. Began this documentation review on `docs/week-4-g02-live-review` at that revision, with only the supplied [G02 review](docs/week-4/G02_LIVE_ASSESSMENT_REVIEW.md) untracked. Earlier service entries retain their historical pre-merge and mock-only state. No new API requests, network diagnostics or credential access occurred in this checkpoint.

**Two separately recorded attempts:** Inspected original ignored local bundles `outputs/openai/G02-live-luna-20261029-111651.json` and `outputs/openai/G02-live-attempt2-20261029-113851.json`. The first records a connection failure at `2026-10-29T08:16:55.030131+00:00`, latency **11,464.831 ms**, no candidate/audit, and null request ID and usage. The successful attempt began at `2026-10-29T08:38:53.080395+00:00`: `CASE-G02`, recorded model `gpt-6-luna`, SDK `3.40.0`, prompt `aml-preliminary-1.0`, **10,905.025 ms**, **1,491 input / 1,163 output / 2,654 total tokens**, status `validated` and preliminary action `investigate`, with human review required. Both record `store=False`, reasoning effort `none`, output cap `2400`, timeout `60s`, allowance `1`, one attempt and zero SDK/application retries. Separate authorization is owner-reported; no authorization or intervening diagnostic trace is captured in these bundles. Failure processing/billing cannot be excluded, and no exact charge is established.

**Offline evidence verification:** Recomputed original input-file, canonical-input, prompt-instructions and candidate hashes; checked candidate/assessment equality, input/output contracts and typed citations; reproduced the saved auditor report exactly using the existing local interface. All three mechanical stages passed. The amount checker compared **zero of six** factual findings: all complete statements were outside its restricted grammar, so coverage is `checked=0`, `not_checked=6`, with zero recorded matches/conflicts. All nine broad semantic categories remain `not_evaluated`. Hashes identify local artifacts; the audit contains no source Git revision or independently verified server-side trace. Both original bundles and source/reference records remain unchanged; the raw bundles remain ignored.

**Manual comparison and corrections:** Compared all six factual findings against [G02 input records](data/golden_cases/inputs/G02.json), retaining customer-claim/check attribution and supplied-scope limits. Flagged "customer's stated maximum monthly activity" in both rationale and `interpretations[0]`: the profile range exists but its personal attribution is not explicit. Retained payer-identity ambiguity and citation/completeness questions without approving severity scores or rewriting the candidate. Compared the action descriptively with the [provisional G02 reference](data/golden_cases/references/G02_reference.json); agreement is not adjudicated accuracy. Corrected the review's failed-attempt evidence source, marked unverified diagnostics as such, added exact record/field pointers and artifact hashes, and distinguished manual review from automated checking. Updated current status and only directly relevant roadmap progress, and labeled the integration guide's mock-only account as historical, preserving earlier checkpoints and objectives.

**Verification and limits:** Checked local links, documentation consistency, changed-file scope and `git diff --check`. No unit tests were run: only documentation changed, leaving the recorded **358-test** implementation baseline and existing CI coverage applicable. Remote CI results were not fetched or independently verified; no fresh CI or test pass is claimed. Formal semantics, labels, completeness, reference leakage/history, billing reconciliation, baseline comparison and generalization remain unadjudicated or unmeasured. No implementation, evaluator framework, prompt, dependency, dataset or architecture changed. Raw execution bundles remain ignored; nothing is staged, committed, pushed or merged. Stop for independent review.

## 2026-10-29 — G02 research calibration handoff integration

**Preflight and provenance:** Continued on `research/week-4-evaluation-design` at `010147592fd4e308063121eb411f900c52e8808c`. The uploaded `G02_Codex_Calibration_Implementation.zip` and two existing G02 pilot draft documents were untracked before this task. Read the archive README and integration instructions, inspected its Python tools/tests and catalog, and compared every nested packet file against the existing ignored pilot directory: all nine were byte-identical. Preserved the root README and relocated repository-specific instructions into the [research area](research/evaluation_calibration/README.md). The supplied ZIP and earlier drafts remain unchanged.

**Bounded integration:** Added the [draft seven-bundle plan](docs/week-4/G02_SEVEN_BUNDLE_CALIBRATION_PLAN_DRAFT.md), archived integration handoff, catalog, blank worksheet, integrity/preview tools, offline HTML builder and two research test modules. Preserved all 38 selected source-unit values and draft judgments. Added a directory adapter and nine artifact digests instead of introducing a duplicate editable packet; ZIP compatibility remains explicit. Reports distinguish directory artifact verification from historical container provenance. Additional guards reject altered bindings and fabricated review/scoring claims. HTML displays exact source values and proposed associations, exports draft notes only, and requires a new output destination. No application code or existing test assertions were changed.

**Executed offline verification:** All **403 unit tests passed** on Python 3.11.9: 358 existing plus 45 research tests, comprising the 26 supplied tests and 19 added integration checks. `pip check` found no broken requirements; syntax checks passed for all five new Python files. CLI smoke tests produced fresh inspection/preview JSON, a blank identity-bound worksheet and an HTML view under ignored `outputs/evaluation/g02-calibration-integration-20261029/`; overwrite-refusal tests preserved existing target bytes. Browser inspection confirmed local rendering, exact source expansion and bundle navigation. Tests verify 75 source units, 21 statements and 203 typed pointers mechanically, without certifying entailment or executing the 13 conceptual semantic challenges. Packet-dependent test classes explicitly skip on checkouts lacking the ignored local packet; portable adapter tests remain runnable.

**Review limits:** H-00 through H-07, category policy, source sufficiency, whole-statement fidelity, M03 materiality, reviewer responsibilities and all semantic adjudication remain pending. No semantic score, performance ranking, independent AML review or provisional-label approval is implied. Existing contracts, baseline, hosted service/prompt, auditors, frozen candidates, inputs, references, policy and dependencies remain unchanged. No network/model requests, credentials access or installation occurred. Remote CI is not verified; no files are staged, committed, pushed or merged. Stop for independent review.

## 2026-10-30 — G02 non-scoring semantic reconciliation implementation

**Scope and sources:** Continued on `research/week-4-evaluation-design` at `010147592fd4e308063121eb411f900c52e8808c`, preserving the existing modified and untracked work. Implemented the owner-authorized non-scoring reconciliation scope from the supplied [reporting specification](docs/phase-2/G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md) and [draft adjudication register](data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json). Both sources remain unchanged. Recorded owner-in-conversation decisions remain distinct from original AI-draft annotations and from independent AML expert review, which was not performed.

**Implementation:** Added the research-only [reconciler](research/evaluation_calibration/g02_reconciliation.py) and [35 focused tests](tests/test_g02_reconciliation.py), and extended the [research instructions](research/evaluation_calibration/README.md). Reused existing packet verification, catalog hash bindings and mechanical auditing. Validates 75 atomic identities, spans, offsets, pointers and submitted citations, all 21 original statements, source hashes, batch membership and declared populations. Reports original records alongside recorded decisions, separate factual/citation/process/whole-statement dimensions, M01–M05 coverage, action adjudication, provenance, exclusions and pending gates. Original-file digests and validated canonical digests remain separate. No application model or evaluator behavior was changed.

**Observed report:** Generated an ignored [representative report](outputs/evaluation/g02-reconciliation-20261030/reconciliation_report.json), 576,928 bytes, SHA-256 `5346a20ed22bf99752c208a9b1598198fad7276de4e1ff322e6382f53faf932f`; a second build reproduced its exact bytes. All 75 owner records and 21 whole-statement records match the register verbatim. Recorded atomic dispositions are 54 supported, 2 not established, 1 unassessable and 18 not applicable. Whole statements reconcile as 10 qualified factual passes, 3 qualified investigative questions and 8 reviewed but not cleared. Hosted M01/M02/M03 are covered; baseline M01 is partly covered, M02 covered and M03 omitted. M04 remains contextual with materiality pending; M05 is nonmandatory. Repeated M02 statements retain both occurrences without duplicate coverage credit. The recorded preliminary action is `investigate`, with no approved alternatives; the golden reference remains provisional and unchanged.

**Executed verification:** On Python 3.11.9, `.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_g02_reconciliation.py -v` passed all **35 new tests**; full discovery with `.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v` passed **438 tests**, including all 403 pre-existing tests, with no failures or skips. `.\.venv\Scripts\python.exe -B -m pip check` reported no broken requirements. New files passed syntax checks; `git diff --check`, separate untracked-file whitespace checks and local documentation-link checks passed. Comparing SHA-256 digests for 144 pre-existing paths found only the three intended documentation edits; the other 141 paths, including the frozen packet and supplied register/specification, were unchanged. Negative tests reject stale identities, hashes, spans, citations, populations and unsupported scoring fields; existing frozen draft guards remain active. A direct scoring request raised `scoring: numerical scoring is not authorized`. All nine broad auditor semantic dimensions remain `not_evaluated`; no numerical performance rate or ranking is produced.

**Limitations and review:** H004/H034 original-wording fidelity remains unresolved; H047's supported atom does not clear its complete statement, and H049 retains its ambiguity. Process assertions use separate authority and do not certify runtime execution or completed human review. Missing structured review state, reviewer/event IDs, revision history and rubric version are explicit limitations. The register's pending P01–P05 records remain verbatim; implementing this layer does not release the draft schema, settle denominator eligibility or authenticate conversation approvals. Original frozen sources, unrelated work, contracts, baseline, hosted behavior, policy and dependencies are preserved. No API requests, credential access, installation, staging, commit, push or merge occurred. Remote CI is unverified; stop for project-owner review.

## 2026-10-30 — Week 5, Checkpoint 1A: controlled experiment specification draft

**Scope and provenance:** Prepared the [controlled experiment specification](docs/week-5/CONTROLLED_EXPERIMENT_SPEC_DRAFT.md) on `research/week-5-experiment-readiness` at `e5e73054cfef7488862a38b3b27ecaae28af37a6`, the PR #14 merge. The owner approved specification/provenance work before any runner implementation. Preserved the existing untracked handoff ZIP and all local G02 artifacts.

**Proposed plan:** The draft defines an operational question, first-occurrence-per-family selection, five named development inputs, ten planned baseline/hosted slots, source/configuration identities, policy-access differences, manual attempt accounting, existing CLI procedure, separate mechanical/descriptive reports, stop rules and pending approvals. These are development smoke-test observations, not classification accuracy or equivalent-policy/held-out comparisons. Proposed model, call/token limits and monetary authorization remain unapproved; all ten slots remain unexecuted.

**Source checks:** Freshly validated all 50 development inputs against the existing contract and verified their manifest hashes. Confirmed five families and 18 family/condition combinations; the selected five cover five combinations. Recorded selected raw/canonical digests, implementation/prompt/environment identities and separately hashed the historical G02 bundles and frozen candidates. Historical G02 attempts remain retrospective; no prior execution is represented as prospectively registered, and no settled owner adjudication is reopened.

**Verification and next step:** Checked documentation links, example syntax/arguments, hashes, whitespace and changed-file scope. No unit tests were added or rerun for documentation-only changes; **438 passing tests** remains historical evidence. No new candidates, experiment ledger or run reports were generated, and no API calls, credential access or dependency installation occurred. Existing interfaces suffice for a small serial run after owner approval; software automation is deferred. Current status was updated without changing the roadmap or earlier worklog entries. No staging, commit, push, merge or GitHub action occurred; stop for review of the draft and its pending releases.
