# Project Charter — AML Alert Triage Agent

**Created:** 2026-10-26  
**Stage:** Phase 1 domain study completed; documentation review and formal phase closure pending.

## Objective

Develop a reproducible research prototype that assists a human with reviewing *synthetic* AML transaction alerts. Test whether LLM-assisted assessment and factual narrative drafting provide measurable advantages over a simpler deterministic approach.

## Why this matters

Rule-triggered alerts require contextual review. The prototype focuses on the labor of collecting relevant records, interpreting transaction patterns, and documenting an investigation—not automating an institution's regulatory filing decisions.

## People and responsibilities

- **Project owner:** sets goals, studies concepts, accepts scope changes, reviews code and assesses experimental evidence.
- **ChatGPT (discussion role):** explains concepts, helps plan, critiques evidence and documents decisions; does not replace repository inspection.
- **Codex (implementation role):** inspects repository before edits; builds, runs tests, records changes and asks before significant changes to interfaces, architecture or dependencies.
- **Human AML subject-matter reviewer:** optional external feedback, not assumed to exist.

## In scope for the initial eight weeks

1. AML workflow study and written specifications.
2. Synthetic alert/customer/transaction generation.
3. Reproducible labeling method and non-LLM baseline.
4. Structured hosted-LLM assessment with failures handled safely.
5. Transaction evidence assembly and validation.
6. Narrative drafting from verified evidence.
7. Honest held-out evaluation and cost/latency measurements.
8. GitHub-ready source, technical documentation, tests and demo.

## Explicitly out of scope for version one

- Production bank data or institutional system integration.
- Automated alert closure, regulatory determination or SAR submission.
- Production-grade regulatory compliance claims.
- RAG/vector database, multi-agent systems, fine-tuning or multi-model competition without an approved experiment showing they are necessary.
- Web app, cloud deployment or extensive infrastructure before the research prototype has been evaluated.

## Rules and success criteria

- A working, reproducible end-to-end prototype with visible, verified limitations.
- Evidence references must resolve to actual synthetic transaction records.
- No precommitted performance target or claimed human time savings without direct measurement.
- Report precision/recall by class and serious error cases; don't rely only on overall accuracy.
- Preserve development/evaluation independence and disclose synthetic-data limitations.
- All material changes must pass relevant tests and document tradeoffs.
- Repo code and files are authoritative; AI-chat memory is not.

## Change-control policy

When the owner raises a concern or results are poor:

1. State the **current week/milestone** and accepted objective.
2. Identify the observed failure versus the interpretation or hypothesis.
3. Inspect evidence: tests, sample inputs, metrics and code.
4. Consider smallest local correction first; list alternatives and tradeoffs.
5. Do **not** switch the architecture or roadmap reflexively.
6. Significant architecture or roadmap changes require evidence, a `DECISIONS.md` entry and owner agreement.

An unsuccessful experiment is documented; it is not by itself a reason to abandon the roadmap.

## Resource limits

- **Planning assumption:** roughly 15–20 hours/week over eight weeks, with up to two contingency weeks. This is a planning estimate, not a verified commitment.
- **LLM spend:** amount **not yet agreed**. Never begin large paid experiments before setting an approved budget.
- **Privacy:** use fully synthetic identities; do not commit API keys, real customer data or private records.

## Decision checkpoints

- **End of Week 2:** problem/schemas/labeling design review.
- **End of Week 5:** compare classifier against deterministic baseline; decide with evidence whether further experiments are warranted.
- **End of Week 7:** release-readiness review based on tests, grounding and evaluation.

## Regulatory reference boundary

The initial workflow draws from publicly available **US FFIEC and FinCEN material**. These sources explain the domain but do not constitute advice about actual filing obligations or certify the prototype's compliance.
