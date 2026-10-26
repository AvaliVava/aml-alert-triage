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
