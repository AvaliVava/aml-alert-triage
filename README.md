# AML Alert Triage Agent

**Status:** Phase 2 — input contracts merged through PR #3; output contracts implemented and committed locally, not merged. The formal evaluation protocol and provisional-label review remain pending.

A **synthetic AML investigation engineering project** and research prototype for assisting human reviewers with anti-money-laundering (AML) transaction alerts. Current functionality validates supplied input records, submitted preliminary output structure, and typed citation references. The intended future pipeline will explore generating preliminary review recommendations, evidence assembly, and factual narrative drafting.

> **Important:** This is not a bank product, automated SAR filing system, or compliance-certified investigation tool. No real customer data is used. No AML decision engine, classifier, LLM investigation agent, automated verification system, evidence assembler, or complete triage pipeline has been implemented.

## The problem

Monitoring systems generate alerts that require contextual investigation. A triggered rule is a signal to review activity, not a determination that the customer committed a crime. The prototype will explore whether a validated LLM workflow can support parts of that review while preserving evidence traceability and human decision-making.

Regulatory-workflow reference: [FFIEC BSA/AML Examination Manual — Suspicious Activity Reporting](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04).

## Implemented input validation

The [Pydantic V2 contracts](src/aml_triage/contracts.py) include `Customer`, `Account`, `Transaction`, `Counterparty`, `Alert`, `CaseMetadata`, `Evidence`, and `VerificationCheck`, plus an `ExpectedMonthlyActivity` helper.

The complete `InvestigationInput` contract composes the existing nine-field input structure. It requires schema version `"1.0"` and collection lists, rejects unexpected outer record fields and duplicate identifiers or references, and validates explicit relationships across the supplied records. Evidence facts remain heterogeneous JSON; the aggregate contract also rejects the four approved evaluation-only keys inside facts.

Valid incomplete records remain acceptable: the required counterparty collection may be empty when references permit it, transaction counterparty IDs may be null, and contextual evidence may have no transaction references. Supplied verification statuses and check findings are synthetic recorded inputs, not verification performed by this system.

All five valid golden cases pass validation and the intentionally invalid duplicate-transaction fixture is rejected. The [contract tests](tests/test_contracts.py) exercise individual records and aggregate validation; [golden-case documentation](data/golden_cases/README.md) explains the synthetic-data limitations. This validation does not perform an AML investigation or generate a recommendation.

## Implemented preliminary output validation

The [output contracts](src/aml_triage/contracts.py) add `RecordCitation`, `CitedStatement`, `Contradiction`, and `InvestigationOutput`. Outputs separate factual findings, interpretations, unresolved questions, missing information, and contradictions, using typed record citations. Every output requires `recommendation_scope="preliminary"` and `human_review_required=True`.

The provisional actions are `close`, `investigate`, and `escalate`. A recommendation requires a cited rationale and at least one cited factual finding. Explicit abstention uses `assessment_status="unable_to_recommend"` and `recommended_action=null`; its rationale may be uncited and its findings empty. All factual findings, interpretations, and contradiction sides require citations; questions and missing-information statements may have none.

The separate `validate_investigation_output_references` function accepts already-validated input and output models, checks exact case/alert identities, and resolves citations in all statement locations against eight supplied record namespaces: case, customer, account, counterparty, transaction, alert, evidence, and verification_check. It returns the original output without mutating either object. Resolving an identifier proves record existence only, not factual support or independent verification. No disposition is chosen and no reference answers or labeling policy are read by this validation.

Input contracts were merged into `main` through PR #3 (`327e600`). The output work is committed locally at `a538063` and `ce0cd4a` on `feature/phase-2-output-contracts` and has not been merged. Candidate outputs in tests are authored independently of the separate reference answers; the contracts do not generate assessments.

## Planned scope

- **Input:** Synthetic alert, customer profile, transaction history and rule metadata.
- **Analysis:** Deterministic transaction features, then a rules baseline and structured LLM assessment.
- **Future generation:** Preliminary assessments using the implemented output contract, evidence assembly, and narrative drafting; these generation capabilities remain pending.
- **Assurance:** Contract tests, reproducible evaluation, safe failures, documented limitations and human review.
- **Out of scope for v1:** Real bank integrations, autonomous case closure, real SAR filings, production deployment and RAG.

The [fictional labeling rubric](specs/labeling_policy_v1.json) uses the provisional vocabulary `close`, `investigate`, and `escalate`, now accepted by the initial output contract. These names supersede earlier illustrative `recommend_close`/`recommend_escalation` examples; accepting them does not finalize the labels or implement decision logic. Reference answers remain separate from investigation inputs and candidate outputs, and the labels still require review. No production AML policy or regulatory decision logic is asserted.

## Install and run local checks

Requires **Python 3.11–3.13**. **Pydantic V2 is an application dependency**, declared in [pyproject.toml](pyproject.toml) and installed with the project. Run commands from the repository root. Reuse an existing virtual environment, or create one once before installation.

Windows PowerShell:

```powershell
# Run this creation step only if .venv does not already exist.
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -c constraints.txt -e .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts\check_setup.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

If the `python` command is unavailable, use `py -3.11 -m venv .venv` for the creation step instead, provided the Windows Python launcher and Python 3.11 are installed. Reuse an existing `.venv` without recreating it.

In an activated virtual environment, or Linux CI with a configured supported Python interpreter:

```bash
python -m pip install -c constraints.txt -e .
python -m pip check
python scripts/check_setup.py
python -m unittest discover -s tests -v
```

Editable installation uses [constraints.txt](constraints.txt) to pin the tested runtime dependency versions, including Pydantic and the OpenAI SDK, for development and CI. It does not pin build tools or distribution hashes. Use the constraint option whenever installing this project; a plain editable install does not reproduce the pinned environment. The smoke check exercises the original foundation CLI; the unit-test command runs the **complete suite**, including foundation, fixture-integrity, and contract tests. Neither performs AML analysis nor calls an LLM. No API keys are needed for these checks.

The complete suite was rerun at `ce0cd4a`: **144 local tests passed**. Remote GitHub Actions results for the output-contract branch remain unverified. The smoke CLI's `week-1-foundation` phase label is historical; consult [PROJECT_STATUS.md](PROJECT_STATUS.md) for the current milestone and [START_HERE.md](START_HERE.md) for detailed setup.

## Project documents

| File | Why it exists |
| --- | --- |
| [START_HERE.md](START_HERE.md) | Setup and contribution workflow for the existing repository |
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
5. No unverified transaction IDs or invented evidence in accepted output. Current citation checks establish identifier existence only; factual support remains unevaluated.
6. Record failed experiments, not only the successful ones.
7. A complaint or a low score triggers **diagnosis**, not an automatic redesign.

## Current progress

Phase 1 is complete and Phase 2 is active. Input contracts are merged into `main`; output contracts and input/output reference validation are implemented locally on the unmerged feature branch. The formal evaluation protocol and provisional-label review remain pending. See [PROJECT_STATUS.md](PROJECT_STATUS.md) for verified checkpoints and next actions. This is **not** a finished AML investigation system.

## References

- [FFIEC BSA/AML Manual: Suspicious Activity Reporting](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04)
- [FFIEC examiner procedures](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04_ep)
- [FinCEN guidance on complete SAR narratives](https://www.fincen.gov/resources/statutes-regulations/guidance/suggestions-addressing-common-errors-noted-suspicious)
