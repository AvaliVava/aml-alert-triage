# Project Status — Source of Truth

- **Last updated:** 2026-10-27
- **Current milestone:** Phase 2 — Input Contracts Implemented; Documentation Reconciliation
- **Next milestone:** Phase 2 — Output Contracts and Formal Evaluation Protocol
- **Project:** AML Alert Triage Agent
- **Repository:** https://github.com/AvaliVava/aml-alert-triage

## 1. Current Project Status

The foundational repository has been created and published on GitHub.

Phase 1 is complete, including the domain studies and documentation closeout. The Phase 1 documentation pull request was merged into `main` as PR #1 (`a5c68d0`).

Phase 2 has started. Its input-contract implementation is complete and locally tested: the individual record models and complete Pydantic V2 `InvestigationInput` contract are implemented in [contracts.py](src/aml_triage/contracts.py).

The latest implementation checkpoint is `1375d9f` on `feature/phase-2-pydantic-contracts`, with a verified local baseline of **99 passing tests**. All five valid golden-case inputs pass validation, and the deliberately invalid duplicate-transaction fixture is rejected.

Phase 2 as a whole is not complete. Output contracts and a formal evaluation protocol remain pending, and the fictional labeling vocabulary remains provisional. No AML classifier, investigation agent, or end-to-end triage pipeline has been implemented. Remote GitHub Actions results for this feature branch remain unverified.

## 2. Completed Work

### Repository and Development Environment

- GitHub repository created and populated.
- Project charter and eight-week roadmap established.
- Project continuity and engineering decision documentation established.
- Python 3.11.9 installed and a virtual environment created.
- Local setup verification completed successfully using Python 3.11.
- Historical foundation checkpoint: three unit tests passed before the contract work; the current local baseline is 99 passing tests.
- GitHub Actions CI workflow configuration included in the repository.
- Historical Phase 1 workflow: `docs/phase-1-completion` was created for the documentation review and its pull request was subsequently merged.

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

The six Phase 1 engineering documents were originally committed on `docs/phase-1-completion` and are now present in `main` under [docs/phase-1/](docs/phase-1/):

- [AML_DOMAIN_FOUNDATIONS.md](docs/phase-1/AML_DOMAIN_FOUNDATIONS.md)
- [INVESTIGATION_WORKFLOW.md](docs/phase-1/INVESTIGATION_WORKFLOW.md)
- [CASE_STUDY.md](docs/phase-1/CASE_STUDY.md)
- [PROBLEM_DEFINITION.md](docs/phase-1/PROBLEM_DEFINITION.md)
- [DOMAIN_REQUIREMENTS.md](docs/phase-1/DOMAIN_REQUIREMENTS.md)
- [PHASE_1_COMPLETION.md](docs/phase-1/PHASE_1_COMPLETION.md)

The historical Phase 1 record also notes preparation of a separate learning manual. This is retained as project history, not a newly verified repository artifact.

Phase 1 documentation review and closure are complete. Some historical documents still contain starter-era status wording; reconciliation of documents outside this checkpoint's three-file scope remains separate work.

### Phase 2 — Input Contracts and Golden Cases

- Pydantic V2 is declared as an application dependency in [pyproject.toml](pyproject.toml).
- Individual contracts are implemented for `Customer`, `Account`, `Transaction`, `Counterparty`, `Alert`, `CaseMetadata`, `Evidence`, and `VerificationCheck`, with an `ExpectedMonthlyActivity` helper.
- `InvestigationInput` composes the nine existing top-level fields, requires schema version `"1.0"`, forbids unknown top-level fields, and requires actual lists for collections.
- Aggregate validation rejects duplicate record IDs, duplicate identifiers within reference lists, mismatched customer/alert relationships, and unresolved explicit record references. Standalone record models remain usable independently.
- Evidence facts preserve heterogeneous JSON values. The aggregate contract recursively rejects the four approved evaluation-only keys inside facts; reference answers remain separate from input records.
- All five valid inputs in [data/golden_cases/inputs/](data/golden_cases/inputs/) pass Python and JSON validation. The intentionally malformed [G05_invalid_duplicate.json](data/golden_cases/inputs/G05_invalid_duplicate.json) is rejected for its duplicate transaction ID.
- Empty counterparty collections, explicitly null counterparty IDs, contextual evidence, and valid-but-incomplete beneficiary information remain acceptable. Supplied verification records are synthetic recorded inputs, not banking verification performed by this system.
- The fictional [labeling policy](specs/labeling_policy_v1.json) and separate golden-case reference answers exist; their labels remain provisional pending review.

## 3. Agreed Engineering Direction

The implemented functionality currently validates input structure and explicit record relationships. The future investigation pipeline is planned to:

- Use synthetic AML alert, customer, transaction, and evidence data.
- Implement deterministic preprocessing and a rules-based baseline before introducing LLM classification.
- Use a single hosted LLM initially.
- Explore structured preliminary recommendations using the current provisional rubric vocabulary: `close`, `investigate`, or `escalate`. A final output contract has not been defined.
- Assemble relevant evidence for review, building on the implemented input-reference checks.
- Generate factual investigation narrative drafts.
- Preserve missing information, uncertainty, and contradictory evidence.
- Maintain reproducible experiments and documented technical decisions.
- Require human review for consequential decisions.

The initial prototype will not perform automatic SAR filing, real banking decisions, or production bank integrations.

RAG, multi-agent architectures, and additional infrastructure remain outside the initial scope unless justified by evidence and approved through the established change-control process.

## 4. What Has Not Been Implemented

- Synthetic AML data generator.
- Output contracts and a finalized output schema.
- A formal evaluation protocol.
- Rules-based AML triage baseline.
- Hosted LLM classifier.
- End-to-end evidence assembly pipeline.
- Investigation narrative generator.
- End-to-end triage pipeline.
- Held-out evaluation framework and experimental results.

No classification accuracy, real analyst time savings, or model performance results have been established.

## 5. Verification Status

### Current Local Implementation Baseline

The local readiness audit at implementation checkpoint `1375d9f` verified:

- Python 3.11.9 and Pydantic 2.14.1.
- Complete unit test suite: **99 passed**.
- Five valid golden-case inputs accepted and the duplicate-transaction fixture rejected.
- Setup smoke check and installed dependency consistency check: passed.

To reproduce the setup check and complete suite after editable installation, run from the repository root in Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe scripts\check_setup.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

These are implementation-checkpoint results from the local readiness audit. Documentation reconciliation Checkpoint A does not rerun the suite or change the implementation. See [README.md](README.md) and [START_HERE.md](START_HERE.md) for environment creation and editable installation.

### Historical Foundation Verification

The October 26, 2026 foundation record reported:

- Python 3.11.9 environment: working.
- Setup check: passed.
- Foundation tests: 3 passed.

The historical three-test result describes the initial foundation and is superseded by the 99-test implementation baseline above.

### Remote Verification

The [GitHub Actions workflow](.github/workflows/foundation-tests.yml) installs the project and configures Python 3.11, 3.12, and 3.13 jobs. Remote GitHub Actions results for `feature/phase-2-pydantic-contracts` remain **unverified**. Passing local tests do not establish successful remote CI.

The original smoke-check CLI still reports the historical phase label `week-1-foundation`. Use this document for the current project milestone; no CLI behavior is changed by this documentation checkpoint.

## 6. Immediate Next Actions

1. Finalize and review documentation reconciliation Checkpoint A, with any remaining documentation updates separately authorized.
2. Push the feature branch after documentation approval.
3. Open an input-contract pull request from `feature/phase-2-pydantic-contracts` into `main`.
4. Check GitHub Actions for the PR and verify that all configured CI jobs succeed.
5. Merge only after successful human review and CI.
6. Define and review output contracts and the formal evaluation protocol.
7. Review the provisional fictional rubric and golden-case labels; do not treat them as finalized evaluation labels.
8. Confirm the remaining Phase 2 deliverables before formally closing Phase 2 and proceeding along the agreed roadmap.

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

- **Phase 1 domain learning:** Completed.
- **Phase 1 documentation and closure:** Completed.
- **Phase 2:** Started; input-contract implementation complete and locally tested.
- **Implementation checkpoint:** `1375d9f` on `feature/phase-2-pydantic-contracts`.
- **Local test baseline:** 99 passing tests.
- **Remote feature-branch CI:** Unverified.
- **Pending Phase 2 work:** Output contracts, formal evaluation protocol, and review of provisional labeling artifacts.

**Next action:** Review this documentation checkpoint and verify remote CI for the input-contract PR. Do not mark all of Phase 2 complete.
