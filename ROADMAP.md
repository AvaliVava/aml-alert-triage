# Eight-week roadmap

**Start:** Monday, 2026-10-26. **Core end:** Sunday, 2026-12-20. **Optional contingency:** 2026-12-21 through 2027-01-03.

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

### Today (Week 1, Day 1)

- [x] Draft initial charter, status, work log, research sources and AML lifecycle.
- [x] Create dependency-free Python foundation with smoke and unit tests.
- [ ] Project owner reviews the AML lifecycle and charter.
- [ ] Create a GitHub repository and publish reviewed files.
- [ ] Configure the selected Codex environment against the repository.
- [ ] Record the first authenticated GitHub commit and issue link.

The unchecked tasks are not claimed completed.
