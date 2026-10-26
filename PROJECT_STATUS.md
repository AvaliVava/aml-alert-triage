# Project Status — source of truth

**Date:** 2026-10-26  
**Current milestone:** Week 1 — domain understanding and repository foundation.  
**Current scope:** Scaffolding only; no production or research classifier exists.

## What exists

- Initial project charter and eight-week roadmap.
- First AML workflow specification grounded in published FFIEC/FinCEN references.
- Documentation for Codex continuity, decisions and ongoing engineering work.
- Dependency-free Python command-line **status check only**.
- Foundation unit tests and CI workflow definition.

## What is explicitly NOT done

- No GitHub repository has been created or populated by this local scaffold.
- No AML classifier, synthetic data generator, input/output schema or LLM integration exists yet.
- No paid model calls or AML evaluation results have been recorded.
- The workflow study and charter are drafts pending project-owner review.
- Python 3.11 compatibility must be checked in the owner's environment or in CI after publishing.

## Verified local commands

```bash
python scripts/check_setup.py
python -m unittest discover -s tests -v
```

Local verification on **Python 3.13.5**: setup check passed and **3/3 foundation unit tests passed**. Python 3.11/3.12 and remote CI are not yet verified.

## Next action

1. Read `specs/aml_workflow.md` and the official FFIEC link.
2. Identify the human investigation decisions and limits of automation.
3. Review the charter for omissions; adjust scope only with written reasons.
4. Create GitHub repository `aml-alert-triage` using the reviewed starter files.
5. Push an initial commit, then connect Codex to the same repo.

## Continuity protocol for a new ChatGPT or Codex session

- Inspect THIS file and `DECISIONS.md` first; verify against actual files, Git status and tests.
- Don't assume conversation history, undocumented implementations or old experiments.
- Show the current milestone before recommending changes.
- If reports disagree, trust the verified code/test output over prose and fix stale status.
