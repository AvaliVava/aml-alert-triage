# Eight-week roadmap

**Planning baseline:** October 26–December 20, 2026, with optional contingency through January 3, 2027.

**Scheduling principle:** The eight-week roadmap defines the intended development sequence. Calendar dates are planning estimates, not hard deadlines. Progression depends on completing and verifying the relevant milestone.

| Week | Dates | Objective | Evidence required |
| --- | --- | --- | --- |
| 1 | Oct 26–Nov 1 | Understand AML workflow and initialize repo | Charter, workflow draft, source log, runnable foundation, worklog |
| 2 | Nov 2–8 | Input/output schemas, labeling rubric, 5 golden cases, evaluation plan | Tests for contracts, written specs |
| 3 | Nov 9–15 | Synthetic alerts and deterministic baseline | Seeded generator, 50 development alerts, baseline tests |
| 4 | Nov 16–22 | Structured first LLM classifier | Logged calls, validated responses, first results and failure log |
| 5 | Nov 23–29 | Bounded classification experiments | Fixed eval set, prompt versions, comparisons, decision record |
| 6 | Nov 30–Dec 6 | Evidence validation, narrative drafting and integration | Full pipeline, integration tests, grounded report examples |
| 7 | Dec 7–13 | Held-out evaluation and safety/failure analysis | Reproducible quantitative report and limitations |
| 8 | Dec 14–20 | Release and recruiter-ready case study | CI checks, README, tagged release, demo and technical report |

## Current roadmap progress

**Authoritative progress update - November 1, 2026:** Week 5 remains closed under its [owner-approved engineering-comparison decision](docs/week-5/WEEK_5_MILESTONE_CLOSURE_DECISION_v0.1_2026-11-01.md). Week 6's bounded engineering objective is now formally accepted under the [Week 6 decision](docs/week-6/WEEK_6_MILESTONE_CLOSURE_DECISION_v0.1_2026-11-01.md) and [ADR-017](DECISIONS.md#adr-017--close-week-6-on-bounded-evidence-report-and-library-integration-evidence). [PR #18](https://github.com/AvaliVava/aml-alert-triage/pull/18) supplies source-traceable evidence/narrative composition; [PR #19](https://github.com/AvaliVava/aml-alert-triage/pull/19) supplies baseline and mocked-hosted library integration, tests and [grounded/qualified examples](docs/week-6/WEEK_6_INTEGRATION_EVIDENCE_v0.1_DRAFT.md). This is not a production deployment or semantic-performance result. Week 7 held-out evaluation remains pending and unauthorized; P03 scoring methodology and P04/P05 evaluation/release controls remain unresolved or separately controlled. Phase 2 is not declared complete. The original eight-week table, planning dates and acceptance requirements above are unchanged.

**Historical progress notice:** The following narrative and checklist are preserved from earlier checkpoints. Their pending-integration and authorization statements describe those historical points; the current update above records subsequent bounded Week 5/6 acceptance without approving the formal semantic-evaluation protocol.

Phase 1 is complete; its documentation review and merge are recorded in PR #1 (`a5c68d0`). Phase 2 input contracts were merged through PR #3 (`327e600`), output contracts and reference validation through PR #4 (`ee03f08`), and the mechanical auditor and restricted factual checks through PRs #5–#7. The Week 3 generator was merged through PR #8 (`eeef96f`) and the first limited deterministic baseline through PR #9 (`3c4e3fd`). Week 4 schema compatibility was merged through PR #10 (`4e95484`), and the [OpenAI assessment service](docs/week-4/OPENAI_INTEGRATION.md) through PR #11 (`c6afb71`). The first [hosted G02 smoke test](docs/week-4/G02_LIVE_ASSESSMENT_REVIEW.md) has a saved, mechanically validated response and a separate earlier connection-failure record. Semantic evaluation remains unperformed. The sequence and planning dates above remain unchanged; milestone verification governs progression.

- [x] Create five synthetic golden-case inputs and five separate reference-answer artifacts, merged through PR #2 (`db212d4`); see [golden cases](data/golden_cases/).
- [x] Implement individual Pydantic V2 input contracts and the `ExpectedMonthlyActivity` helper in [contracts.py](src/aml_triage/contracts.py).
- [x] Implement the complete `InvestigationInput` contract using those records, with duplicate-ID, duplicate-reference, and explicit cross-record relationship validation.
- [x] Accept all five valid cases through Python and JSON validation and reject the intentionally invalid [duplicate-transaction fixture](data/golden_cases/inputs/G05_invalid_duplicate.json).
- [x] Verify **99 passing tests** in the historical local input-contract readiness audit at `1375d9f`; see [contract tests](tests/test_contracts.py) and the verification record in [PROJECT_STATUS.md](PROJECT_STATUS.md).
- [x] Implement the approved preliminary output contracts at `a538063`: `RecordCitation`, `CitedStatement`, `Contradiction`, and `InvestigationOutput`, with provisional actions `close`/`investigate`/`escalate`, explicit abstention, preliminary scope, and required human review.
- [x] Implement separate input/output reference validation at `ce0cd4a`, checking exact case/alert identities and typed citation existence in all eight record namespaces without assessing factual support.
- [x] Confirm **144 passing local tests** at `ce0cd4a` during the output documentation checkpoint.
- [x] Implement a seeded generator and publish 50 validated development investigations, with five scenario families, separate lineage/hash manifest and byte reproducibility checks; **269 local tests passed** during the historical generator checkpoint, subsequently merged through PR #8.
- [x] Implement the first limited deterministic baseline, producing preliminary, cited outputs and abstention from supplied records; **316 local tests passed** at its initial checkpoint and **324 passed** after the REF-01 bank-recipient reconciliation correction, subsequently merged through PR #9. Closure and general semantic scoring remain outside its scope.
- [x] Implement the first guarded Responses API service, versioned prompt, original-text validation/auditing, execution bundles and safe default CLI; **358 local tests passed**, including 34 new mocked tests. Merged through PR #11.
- [x] Record the first successful hosted G02 assessment and the separate initial connection failure. Offline verification reproduced the successful mechanical audit; the amount checker compared **0/6 findings** and broad semantic dimensions remain `not_evaluated`. The preliminary `investigate` agrees with a provisional reference, not adjudicated ground truth. This is smoke-test evidence, not a performance benchmark.
- [ ] Approve the formal evaluation protocol; an evaluation draft exists, with semantic judgments still pending.
- [ ] Review the fictional [labeling vocabulary](specs/labeling_policy_v1.json) (`close`, `investigate`, `escalate`) and provisional [golden-case labels](data/golden_cases/references/).

Phase 2 as a whole remains incomplete. The baseline, schema compatibility and Week 4 service work are merged. Remote GitHub Actions results have not been independently verified in this documentation checkpoint; no unit tests were rerun because implementation files are unchanged. The generated cases share development-template lineage and are not held-out evaluation data. Broader hosted experiments require separate authorization; later integration work, semantic adjudication and held-out evaluation remain pending. The one-case smoke test establishes no classification-performance result or verified billing cost.

## Development rhythm

1. Start by reading `PROJECT_STATUS.md`, `DECISIONS.md`, applicable code/tests and the current issue.
2. Work on one well-scoped task and explain the reason for it.
3. Run tests and record relevant results, including failures.
4. Update `WORKLOG.md` and `PROJECT_STATUS.md` after accepted work.
5. Use reviewed commits/PRs as evidence; don't claim a feature works without verification.

### Historical Phase 1 documentation checkpoint — October 26, 2026

- [x] Establish the project charter and roadmap.
- [x] Create and publish the GitHub repository.
- [x] Establish the Python 3.11 development environment.
- [x] Pass the three initial foundation tests locally.
- [x] Complete the Phase 1 AML domain learning sequence.
- [x] Prepare and commit six Phase 1 engineering documents to the documentation branch.
- [x] Update PROJECT_STATUS.md on the documentation branch.
- [ ] Complete the Phase 1 documentation review.
- [ ] Merge the approved documentation pull request.
- [ ] Verify the repository and formally close Phase 1.
- [ ] Begin Phase 2 specifications and evaluation design.

This pre-review checklist is retained as a historical snapshot. The Phase 1 review and merge steps were subsequently completed, and Phase 2 began with golden-case artifacts and input contracts. The formal evaluation protocol remains pending, as shown in the current progress section above.
