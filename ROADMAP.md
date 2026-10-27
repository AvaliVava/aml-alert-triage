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

Phase 1 is complete; its documentation review and merge are recorded in PR #1 (`a5c68d0`). Phase 2 input contracts were merged through PR #3 (`327e600`), output contracts and reference validation through PR #4 (`ee03f08`), and the mechanical auditor and restricted factual checks through PRs #5–#7. The Week 3 generator was merged through PR #8 (`eeef96f`). The first limited deterministic baseline is now implemented locally on `feature/week-3-deterministic-baseline`, awaiting independent review. The sequence and planning dates above remain unchanged; milestone verification governs progression.

- [x] Create five synthetic golden-case inputs and five separate reference-answer artifacts, merged through PR #2 (`db212d4`); see [golden cases](data/golden_cases/).
- [x] Implement individual Pydantic V2 input contracts and the `ExpectedMonthlyActivity` helper in [contracts.py](src/aml_triage/contracts.py).
- [x] Implement the complete `InvestigationInput` contract using those records, with duplicate-ID, duplicate-reference, and explicit cross-record relationship validation.
- [x] Accept all five valid cases through Python and JSON validation and reject the intentionally invalid [duplicate-transaction fixture](data/golden_cases/inputs/G05_invalid_duplicate.json).
- [x] Verify **99 passing tests** in the historical local input-contract readiness audit at `1375d9f`; see [contract tests](tests/test_contracts.py) and the verification record in [PROJECT_STATUS.md](PROJECT_STATUS.md).
- [x] Implement the approved preliminary output contracts at `a538063`: `RecordCitation`, `CitedStatement`, `Contradiction`, and `InvestigationOutput`, with provisional actions `close`/`investigate`/`escalate`, explicit abstention, preliminary scope, and required human review.
- [x] Implement separate input/output reference validation at `ce0cd4a`, checking exact case/alert identities and typed citation existence in all eight record namespaces without assessing factual support.
- [x] Confirm **144 passing local tests** at `ce0cd4a` during the output documentation checkpoint.
- [x] Implement a seeded generator and publish 50 validated development investigations, with five scenario families, separate lineage/hash manifest and byte reproducibility checks; **269 local tests passed** during the historical generator checkpoint, subsequently merged through PR #8.
- [x] Implement the first limited deterministic baseline, producing preliminary, cited outputs and abstention from supplied records; **316 local tests passed** during this uncommitted baseline checkpoint. Closure and general semantic scoring remain outside its scope.
- [ ] Approve the formal evaluation protocol; an evaluation draft exists, with semantic judgments still pending.
- [ ] Review the fictional [labeling vocabulary](specs/labeling_policy_v1.json) (`close`, `investigate`, `escalate`) and provisional [golden-case labels](data/golden_cases/references/).

Phase 2 as a whole remains incomplete. The baseline is local and awaiting independent review; remote GitHub Actions results for its feature branch have not been verified. Local tests are not evidence of successful remote CI. The generated cases share development-template lineage and are not held-out evaluation data. Later LLM/integration work, semantic adjudication and held-out evaluation remain pending; this checkpoint establishes no classification-performance result.

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
