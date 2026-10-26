# Initial GitHub issues (create after repository is published)

## Issue 1 — Study AML alert workflow and complete Week 1 specification

**Why:** Correct system behavior depends on understanding the real analyst workflow before coding.

**Acceptance criteria:**
- Review `specs/aml_workflow.md` against the linked FFIEC and FinCEN references.
- Describe each stage and the institution-vs-prototype responsibility boundary.
- Identify three investigation data needs and at least two ambiguities.
- Update research notes and `PROJECT_STATUS.md` with evidence.

## Issue 2 — Verify repository foundation in GitHub/Codex

**Why:** We need an independently reproducible environment and a durable source of truth.

**Acceptance criteria:**
- Initialize/push repo and inspect first commit.
- Run setup and unit-test commands in Codex or local IDE.
- Verify GitHub Actions workflow passes on supported Python versions.
- Record accepted repository URL, commit SHA and observed test results.

## Issue 3 — Week 2: design input and output schemas

**Why:** Component compatibility is easier to enforce with explicit contracts before model integration.

**Acceptance criteria:**
- Input/output specifications and validation tests.
- Explain allowed recommendation categories and failure states.
- No model integration needed for this issue.
