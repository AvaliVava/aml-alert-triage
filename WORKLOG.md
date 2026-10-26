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
