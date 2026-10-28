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
