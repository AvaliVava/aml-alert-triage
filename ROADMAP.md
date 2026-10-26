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

## Development rhythm

1. Start by reading `PROJECT_STATUS.md`, `DECISIONS.md`, applicable code/tests and the current issue.
2. Work on one well-scoped task and explain the reason for it.
3. Run tests and record relevant results, including failures.
4. Update `WORKLOG.md` and `PROJECT_STATUS.md` after accepted work.
5. Use reviewed commits/PRs as evidence; don't claim a feature works without verification.

### Phase 1 documentation checkpoint — October 26, 2026

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
The unchecked tasks are not claimed completed.
