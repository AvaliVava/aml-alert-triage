# Instructions for Codex and AI coding agents

## Context first

Read `PROJECT_STATUS.md`, `PROJECT_CHARTER.md`, `DECISIONS.md`, relevant specifications, and tests **before editing code**. Use only the current repository and the task supplied in this session; do not assume other ChatGPT conversations or prior projects.

## Engineering safeguards

1. Identify the current milestone, requested behavior and acceptance tests.
2. Inspect real interfaces and call sites before introducing or changing a function.
3. Make the smallest justified change; don't refactor unrelated working modules.
4. Do not add frameworks or change model/provider without an evidence-backed request.
5. Do not upgrade dependencies or change Python compatibility without explaining why and checking impacts.
6. If contracts change, update every affected caller, schema and regression test.
7. Never invent classification measurements or claim experiments were run if they were not.
8. Never place real customer data, access tokens, environment secrets or private records in the repo.
9. Run relevant tests after edits. Record tests that were **not** run and why.
10. Before finishing, update `PROJECT_STATUS.md` and `WORKLOG.md` when state changed.

## How to handle criticism, poor metrics or repeated errors

Treat criticism as **a signal to investigate**, not a command to redesign. State: (a) current milestone, (b) expected outcome, (c) observed issue, (d) supporting evidence, (e) proposed next experiment/fix and its tradeoffs. Maintain the roadmap unless there is an evidenced blocker and the owner agrees to a change.

## Experiment limits

Use a defined baseline, a test dataset, a hypothesis and a bounded set of changes. Preserve prior prompt versions and results. Do not perform repeated paid LLM experiments without an approved limit.

## Source of truth

Repository + passing tests + experiment artifacts > worklog summaries > model recollection. Never accept a claim as tested solely because a chat says it succeeded.

## Security and compliance scope

Synthetic AML alerts only. The application suggests review actions for human evaluation; it never files SARs or automatically determines regulatory compliance.
