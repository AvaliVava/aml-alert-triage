# Project Status — Source of Truth

**Last updated:** 2026-10-26  
**Current milestone:** Phase 1 — Documentation Review and Closeout  
**Next milestone:** Phase 2 — Specifications, Data Contracts, Labeling, and Evaluation Design  
**Project:** AML Alert Triage Agent  
**Repository:** https://github.com/AvaliVava/aml-alert-triage

## 1. Current Project Status

The foundational repository has been created and published on GitHub.

Phase 1 AML domain studies have been completed. The project is currently consolidating and reviewing its documentation before formally entering Phase 2.

The implementation remains at the foundation/scaffolding stage. No AML classifier or end-to-end triage pipeline has been implemented.

## 2. Completed Work

### Repository and Development Environment

- GitHub repository created and populated.
- Project charter and eight-week roadmap established.
- Project continuity and engineering decision documentation established.
- Python 3.11.9 installed and a virtual environment created.
- Local setup verification completed successfully using Python 3.11.
- Three foundation unit tests passed in the local environment.
- GitHub Actions CI workflow configuration included in the repository.
- `docs/phase-1-completion` branch created for the documentation review.

### Phase 1 — AML Domain Understanding

Completed study topics include:

1. AML monitoring and investigation fundamentals.
2. Structuring and layering.
3. Red flags, evidence, and investigative conclusions.
4. Case recommendations, escalation, and SAR boundaries.
5. Transaction-monitoring rules, false positives, precision, and recall.
6. KYC, CDD, EDD, and beneficial ownership.
7. Source of Funds versus Source of Wealth.
8. AML data quality and missing information.
9. AML alert investigation lifecycle.
10. Anatomy of an AML case file and investigation narrative.
11. AML operational failure modes.
12. Domain-to-engineering synthesis.

### Phase 1 Documentation

Six engineering documents have been committed to the `docs/phase-1-completion` branch under `docs/phase-1/`:

- `AML_DOMAIN_FOUNDATIONS.md`
- `INVESTIGATION_WORKFLOW.md`
- `CASE_STUDY.md`
- `PROBLEM_DEFINITION.md`
- `DOMAIN_REQUIREMENTS.md`
- `PHASE_1_COMPLETION.md`

A separate Phase 1 learning manual has also been prepared.

These documents require final review before Phase 1 is formally closed.

## 3. Agreed Engineering Direction

The initial prototype will:

- Use synthetic AML alert, customer, transaction, and evidence data.
- Implement deterministic preprocessing and a rules-based baseline before introducing LLM classification.
- Use a single hosted LLM initially.
- Produce structured preliminary recommendations: `close`, `investigate`, or `escalate`.
- Assemble relevant evidence and validate references.
- Generate factual investigation narrative drafts.
- Preserve missing information, uncertainty, and contradictory evidence.
- Maintain reproducible experiments and documented technical decisions.
- Require human review for consequential decisions.

The initial prototype will not perform automatic SAR filing, real banking decisions, or production bank integrations.

RAG, multi-agent architectures, and additional infrastructure remain outside the initial scope unless justified by evidence and approved through the established change-control process.

## 4. What Has Not Been Implemented

- Synthetic AML data generator.
- Formal customer, transaction, alert, and evidence schemas.
- Rules-based AML triage baseline.
- Hosted LLM classifier.
- Evidence assembly and validation pipeline.
- Investigation narrative generator.
- End-to-end triage pipeline.
- Held-out evaluation framework and experimental results.

No classification accuracy, real analyst time savings, or model performance results have been established.

## 5. Verification Status

Previously completed local checks:

```bash
.\.venv\Scripts\python.exe scripts\check_setup.py

.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

At the time of local verification:

- Python 3.11.9 environment: working.
- Setup check: passed.
- Foundation tests: 3 passed.

These results are historical local verification results, not a claim that the latest repository commit has been retested.

The GitHub Actions workflow exists, but its latest execution status has not been independently confirmed in this update.

## 6. Immediate Next Actions

1. Review the six Phase 1 engineering documents.
2. Confirm consistency with `PROJECT_CHARTER.md`, `ROADMAP.md`, and `DECISIONS.md`.
3. Correct documentation omissions or contradictions without introducing unapproved architectural changes.
4. Open a pull request from `docs/phase-1-completion` into `main`.
5. Review and merge the documentation after approval.
6. Mark Phase 1 formally complete.
7. Begin Phase 2 with data contracts, labeling rules, golden cases, and the evaluation protocol.

## 7. Project Continuity Rules

- GitHub repository files are the source of truth.
- ChatGPT supports learning, planning, technical reasoning, and review.
- Codex supports implementation, testing, and repository development.
- Significant changes require technical justification and documented decisions.
- Failed experiments must be investigated rather than triggering automatic architectural changes.
- Do not claim that a feature is implemented without verifying the actual code.
- Do not report performance results without reproducible evidence.
- Preserve the agreed roadmap sequence while allowing flexible time for learning and implementation.

## 8. Current Checkpoint

**Phase 1 domain learning:** Completed.  
**Phase 1 documentation:** Created; final review pending.  
**Phase 1 formal closure:** Pending.  
**Phase 2:** Not yet started.

**Next action:** Finish Phase 1 documentation review and open the documentation pull request.
