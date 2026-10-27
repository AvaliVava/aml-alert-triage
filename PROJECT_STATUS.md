# Project Status — Source of Truth

- **Last updated:** 2026-10-27
- **Current milestone:** Phase 2 — Input and Output Contracts Implemented; Output Documentation Review
- **Next milestone:** Output-contract PR review and CI; formal evaluation protocol and provisional-label review
- **Project:** AML Alert Triage Agent
- **Repository:** https://github.com/AvaliVava/aml-alert-triage

## 1. Current Project Status

The foundational repository has been created and published on GitHub.

Phase 1 is complete, including the domain studies and documentation closeout. The Phase 1 documentation pull request was merged into `main` as PR #1 (`a5c68d0`).

Phase 2 has started. Its individual input records and complete Pydantic V2 `InvestigationInput` contract are implemented in [contracts.py](src/aml_triage/contracts.py) and were merged into `main` through PR #3 (`327e600`). All five valid golden-case inputs pass validation, and the deliberately invalid duplicate-transaction fixture is rejected.

Output contracts and separate input/output reference validation are committed locally on `feature/phase-2-output-contracts` at checkpoints `a538063` and `ce0cd4a`. They have **not been merged**. The latest implementation checkpoint is `ce0cd4a`, with a freshly confirmed local baseline of **144 passing tests**.

Phase 2 as a whole is not complete. A formal evaluation protocol and review of the provisional fictional labels remain pending. No AML classifier, LLM investigation agent, automated verification system, or end-to-end triage pipeline has been implemented. Remote GitHub Actions results for the output-contract branch remain unverified.

## 2. Completed Work

### Repository and Development Environment

- GitHub repository created and populated.
- Project charter and eight-week roadmap established.
- Project continuity and engineering decision documentation established.
- Python 3.11.9 installed and a virtual environment created.
- Local setup verification completed successfully using Python 3.11.
- Historical foundation checkpoint: three unit tests passed before the contract work; the current local baseline is 144 passing tests.
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

Phase 1 documentation review and closure are complete. Historical reports retain their earlier checkpoint context; this document records the current status.

### Phase 2 — Input Contracts and Golden Cases

- Pydantic V2 is declared as an application dependency in [pyproject.toml](pyproject.toml).
- Individual contracts are implemented for `Customer`, `Account`, `Transaction`, `Counterparty`, `Alert`, `CaseMetadata`, `Evidence`, and `VerificationCheck`, with an `ExpectedMonthlyActivity` helper.
- `InvestigationInput` composes the nine existing top-level fields, requires schema version `"1.0"`, forbids unknown top-level fields, and requires actual lists for collections.
- Aggregate validation rejects duplicate record IDs, duplicate identifiers within reference lists, mismatched customer/alert relationships, and unresolved explicit record references. Standalone record models remain usable independently.
- Evidence facts preserve heterogeneous JSON values. The aggregate contract recursively rejects the four approved evaluation-only keys inside facts; reference answers remain separate from input records.
- All five valid inputs in [data/golden_cases/inputs/](data/golden_cases/inputs/) pass Python and JSON validation. The intentionally malformed [G05_invalid_duplicate.json](data/golden_cases/inputs/G05_invalid_duplicate.json) is rejected for its duplicate transaction ID.
- Empty counterparty collections, explicitly null counterparty IDs, contextual evidence, and valid-but-incomplete beneficiary information remain acceptable. Supplied verification records are synthetic recorded inputs, not banking verification performed by this system.
- The fictional [labeling policy](specs/labeling_policy_v1.json) and separate golden-case reference answers exist; their labels remain provisional pending review.

### Phase 2 — Preliminary Output Contracts and Reference Validation

- `RecordCitation`, `CitedStatement`, `Contradiction`, and `InvestigationOutput` are implemented in [contracts.py](src/aml_triage/contracts.py). They validate submitted output structure and internal consistency, with required fields, strict text/list types, and unknown-field rejection.
- Outputs separate factual findings, interpretations, unresolved questions, missing information, and contradictions. Typed citations identify supplied records; duplicate citations within one statement are rejected, while citation reuse across statements is permitted.
- An output with `assessment_status="recommendation_provided"` uses the provisional vocabulary `close`, `investigate`, or `escalate`, with cited rationale and at least one cited factual finding. Explicit abstention uses `assessment_status="unable_to_recommend"` and `recommended_action=null`; its rationale may be uncited and its findings may be empty.
- Every factual finding, interpretation, and contradiction side requires citations. Questions and missing-information statements may have none. All outputs require `recommendation_scope="preliminary"` and `human_review_required=True`.
- `validate_investigation_output_references` separately checks exact case/alert identities and resolves citations across all statement locations in eight namespaces: case, customer, account, counterparty, transaction, alert, evidence, and verification_check. It accepts already-validated models, raises contextual `ValueError` errors with field paths, and returns the original output without mutating either object.
- Resolution establishes only that a supplied record exists. It does not establish factual support, verify recorded claims, select a disposition, read reference answers, or evaluate the fictional policy. Reference answers remain separate from candidate outputs.
- The two implementation checkpoints are committed locally and remain unmerged; remote branch CI is unverified.

## 3. Agreed Engineering Direction

The implemented functionality validates input structure and relationships, submitted output structure and internal consistency, and input/output identities and citation existence. The future investigation pipeline is planned to:

- Use synthetic AML alert, customer, transaction, and evidence data.
- Implement deterministic preprocessing and a rules-based baseline before introducing LLM classification.
- Use a single hosted LLM initially.
- Generate structured preliminary recommendations using the implemented output contract and current provisional vocabulary: `close`, `investigate`, or `escalate`, with explicit abstention when a recommendation cannot be supported.
- Assemble relevant evidence for review, building on the implemented input-reference checks.
- Generate factual investigation narrative drafts.
- Preserve missing information, uncertainty, and contradictory evidence.
- Maintain reproducible experiments and documented technical decisions.
- Require human review for consequential decisions.

The initial prototype will not perform automatic SAR filing, real banking decisions, or production bank integrations.

RAG, multi-agent architectures, and additional infrastructure remain outside the initial scope unless justified by evidence and approved through the established change-control process.

## 4. What Has Not Been Implemented

- Synthetic AML data generator.
- A formal evaluation protocol.
- Rules-based AML triage baseline.
- Hosted LLM classifier.
- End-to-end evidence assembly pipeline.
- Investigation narrative generator.
- Automated evidence verification or substantive claim-support evaluation.
- End-to-end triage pipeline.
- Held-out evaluation framework and experimental results.

No classification accuracy, real analyst time savings, or model performance results have been established.

## 5. Verification Status

### Current Local Implementation Baseline

At `ce0cd4a`, the complete unit suite was rerun during this output documentation checkpoint: **144 tests passed**. This includes the existing input and golden-fixture tests, 26 standalone output-contract tests, and 19 input/output reference-validation tests. No code or tests were changed for this documentation task.

### Historical Input-Contract Readiness Audit

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

The 99-test, setup, and dependency-check results above are historical input-contract audit results. Only the complete unit suite was rerun for this output documentation checkpoint. See [README.md](README.md) and [START_HERE.md](START_HERE.md) for environment creation and editable installation.

### Historical Foundation Verification

The October 26, 2026 foundation record reported:

- Python 3.11.9 environment: working.
- Setup check: passed.
- Foundation tests: 3 passed.

The historical three-test result describes the initial foundation and is superseded by the current 144-test baseline above.

### Remote Verification

The [GitHub Actions workflow](.github/workflows/foundation-tests.yml) installs the project and configures Python 3.11, 3.12, and 3.13 jobs. Remote GitHub Actions results for `feature/phase-2-output-contracts` remain **unverified**. Passing local tests and the earlier input-contract PR merge do not establish successful remote CI for the output branch.

The original smoke-check CLI still reports the historical phase label `week-1-foundation`. Use this document for the current project milestone; no CLI behavior is changed by this documentation checkpoint.

## 6. Immediate Next Actions

1. Review and finalize this output-contract documentation checkpoint.
2. Commit the approved documentation and push the output-contract feature branch when authorized.
3. Open an output-contract pull request from `feature/phase-2-output-contracts` into `main`.
4. Check GitHub Actions for the PR and verify that all configured CI jobs succeed.
5. Merge only after successful human review and CI.
6. Define and review the formal evaluation protocol.
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
- **Phase 2:** Started; input and output contracts implemented and locally tested.
- **Input contracts:** Merged into `main` through PR #3 (`327e600`).
- **Output implementation checkpoint:** `ce0cd4a` on `feature/phase-2-output-contracts`; both output checkpoints committed locally, not merged.
- **Local test baseline:** 144 passing tests.
- **Remote output-branch CI:** Unverified.
- **Pending Phase 2 work:** Output PR review/merge, formal evaluation protocol, and review of provisional labeling artifacts.

**Next action:** Review this documentation checkpoint, then prepare the output-contract PR and verify its remote CI when authorized. Do not mark all of Phase 2 complete.
