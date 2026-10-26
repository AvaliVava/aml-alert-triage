# AML Alert Triage Agent

**Status:** Week 1 — research and project foundation (started 2026-10-26)

An evaluation-driven **research prototype** for assisting human reviewers with synthetic anti-money-laundering (AML) transaction alerts. The intended future pipeline will produce a recommended action, supporting evidence, a factual rationale, and, when appropriate, a draft investigation narrative.

> **Important:** This is not a bank product, automated SAR filing system, or compliance-certified investigation tool. No real customer data is used. No classifier, evidence assembler, or narrative generator has been implemented yet.

## The problem

Monitoring systems generate alerts that require contextual investigation. A triggered rule is a signal to review activity, not a determination that the customer committed a crime. The prototype will explore whether a validated LLM workflow can support parts of that review while preserving evidence traceability and human decision-making.

Regulatory-workflow reference: [FFIEC BSA/AML Examination Manual — Suspicious Activity Reporting](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04).

## Planned scope

- **Input:** Synthetic alert, customer profile, transaction history and rule metadata.
- **Analysis:** Deterministic transaction features, then a rules baseline and structured LLM assessment.
- **Output:** Recommendation (`recommend_close`, `investigate`, `recommend_escalation`), rationale, validated transaction references, missing information and optional narrative draft.
- **Assurance:** Contract tests, reproducible evaluation, safe failures, documented limitations and human review.
- **Out of scope for v1:** Real bank integrations, autonomous case closure, real SAR filings, production deployment and RAG.

## Try the Day 1 foundation

Requires **Python 3.11–3.13**. The foundation has no third-party package dependencies.

```bash
python scripts/check_setup.py
python -m unittest discover -s tests -v
```

The first command checks the local Python environment and repository scaffolding. The second runs foundation tests. They **do not** execute AML analysis or call an LLM.

## Project documents

| File | Why it exists |
| --- | --- |
| [PROJECT_CHARTER.md](PROJECT_CHARTER.md) | Scope, success standards and change controls |
| [ROADMAP.md](ROADMAP.md) | Eight-week development plan |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Current verified state and next task |
| [AGENTS.md](AGENTS.md) | Operating instructions for Codex and future sessions |
| [DECISIONS.md](DECISIONS.md) | Why major engineering choices were made |
| [WORKLOG.md](WORKLOG.md) | What actually happened in each working session |
| [specs/aml_workflow.md](specs/aml_workflow.md) | Initial AML workflow research |
| [research/primary_sources.md](research/primary_sources.md) | Official sources and research boundaries |

## Engineering and evaluation principles

1. The repository—not prior AI chats—is the source of truth.
2. Inspect existing code and tests before changing anything.
3. Compare the LLM against a simpler baseline; never fabricate an accuracy claim.
4. Separate the development set from held-out evaluation cases.
5. No unverified transaction IDs or invented evidence in accepted output.
6. Record failed experiments, not only the successful ones.
7. A complaint or a low score triggers **diagnosis**, not an automatic redesign.

## Current progress

See [PROJECT_STATUS.md](PROJECT_STATUS.md). Week 1 foundation is in progress; this is **not** a finished AML implementation.

## References

- [FFIEC BSA/AML Manual: Suspicious Activity Reporting](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04)
- [FFIEC examiner procedures](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04_ep)
- [FinCEN guidance on complete SAR narratives](https://www.fincen.gov/resources/statutes-regulations/guidance/suggestions-addressing-common-errors-noted-suspicious)
