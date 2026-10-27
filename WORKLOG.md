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
