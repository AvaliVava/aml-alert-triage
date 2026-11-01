# Engineering Decisions

Record proposals, evidence, alternatives and consequences here. A decision can be revisited only with new evidence or explicit owner approval.

## ADR-001 — Repository is the durable source of truth
**Date:** 2026-10-26  
**Status:** Accepted as a working rule.

**Decision:** Persist source code, specifications, testing instructions, current status and key reasoning in version-controlled files. Do not rely on long-lived chat memory.

**Why:** Conversation context is not a reliable, inspectable project state. A fresh engineering session must reconstruct the project from actual repository state.

**Consequence:** Every accepted engineering session updates verified status and relevant decision records.

## ADR-002 — Start with a controlled workflow, not autonomous orchestration
**Date:** 2026-10-26  
**Status:** Accepted as initial scope.

**Decision:** Begin with deterministic preprocessing + baseline + structured LLM assessment. Postpone RAG and multi-agent orchestration.

**Why:** We need measurable evidence that each added capability helps before introducing complexity.

**Revisit if:** Error analysis shows unmet requirements specifically tied to absent external information or dynamically selected tools.

## ADR-003 — Criticism triggers diagnosis, not automatic redirection
**Date:** 2026-10-26  
**Status:** Accepted as project policy.

**Decision:** Maintain an agreed roadmap and bounded experiments. Revisions require an identified failure, evidence, an impact assessment, and agreement.

**Why:** Reflexive architecture shifts make results difficult to interpret and can break working code.

## ADR-004 — Dependency-free Week 1 foundation
**Date:** 2026-10-26  
**Status:** Temporary implementation decision.

**Decision:** Use Python standard library only for initial repository smoke check and tests. Delay model SDK and Pydantic installation until their interfaces are needed and verified.

**Why:** We can prove the environment, commands and CI structure work without prematurely introducing dependency compatibility risks.

**Revisit:** Week 2 for schemas and Week 4 for model integration; record exact versions and run compatibility tests.

---

The following accepted Phase 2 decisions are recorded retrospectively in Documentation Checkpoint B1. Dates refer to implementation commit dates in Git, not reconstructed dates of design discussions or test execution. ADR-001 through ADR-004 remain unchanged as historical records.

## ADR-005 — Adopt Pydantic V2 for input contracts

**Date:** 2026-10-27

**Status:** Accepted; implemented beginning at `6fab3bc`.

**Decision:** Adopt Pydantic V2 as an application dependency when the Phase 2 record interfaces are needed. This revisits ADR-004's temporary dependency deferral without changing the historical foundation decision. The declared dependency is `pydantic>=2.14.1,<3` in [pyproject.toml](pyproject.toml); the local readiness audit used Pydantic 2.14.1.

**Why:** Typed nested models, date and decimal parsing, and Pydantic validation errors provide a consistent contract boundary for the existing synthetic inputs instead of maintaining bespoke validation for every record.

**Tradeoff:** Contributors and CI must install the project and its dependency before running the full suite. The [CI workflow](.github/workflows/foundation-tests.yml) includes editable installation; passing the local suite does not establish remote compatibility results. No model SDK or LLM capability is introduced by this choice.

## ADR-006 — Separate record validation from investigation validation

**Date:** 2026-10-27

**Status:** Accepted; standalone contracts completed through `e6094f9`, with aggregate validation added at `1375d9f`.

**Decision:** Keep the individual contracts in [contracts.py](src/aml_triage/contracts.py) independently usable for their own field types and record constraints. Resolve relationships between supplied records only in `InvestigationInput`.

**Why:** An isolated transaction or evidence record can be checked before a complete investigation is available. Record parsing should not require unrelated files, a policy lookup, or access to other records.

**Tradeoff:** A record that passes its standalone contract may still contain an unresolved reference or participate in a duplicate-ID conflict when composed into an investigation. Complete input acceptance therefore requires aggregate validation, as exercised by [contract tests](tests/test_contracts.py).

## ADR-007 — Compose InvestigationInput from existing contracts

**Date:** 2026-10-27

**Status:** Accepted; implemented at `1375d9f`.

**Decision:** Reuse the individual models inside the existing nine-field `InvestigationInput` structure rather than duplicate their fields. Require the exact string schema version `"1.0"`, reject unknown top-level fields, and require actual lists for collection fields. Apply list strictness without blanket strict mode that would reject supported JSON date and timestamp strings.

**Why:** Composition keeps standalone and nested record validation consistent and preserves the real golden-case interfaces.

**Tradeoff:** Changes to a shared record contract also affect complete investigations. The existing standalone tests and Python/JSON aggregate tests check both entry points; no parallel investigation-only record schema is maintained.

## ADR-008 — Enforce duplicate and explicit-reference integrity in the aggregate

**Date:** 2026-10-27

**Status:** Accepted; implemented at `1375d9f`.

**Decision:** Reject duplicate account, counterparty, transaction, evidence, and check IDs, including identical repeated records. Enforce case-to-alert and alert-to-customer matches, account ownership, transaction account and non-null counterparty references, alert and evidence transaction references, and verification-check evidence references against the supplied records.

**Reference-list policy:** Reject duplicate identifiers within each alert transaction list, evidence transaction-reference list, and check evidence-reference list. Do not silently deduplicate. References may recur across separate records, and repeated free-text findings remain permitted.

**Why:** Unique identifiers and resolvable explicit references prevent ambiguous records and repeated references from being accepted as distinct support. These are structural integrity checks, not AML judgments.

**Tradeoff:** The validator reports the first failing relationship as a Pydantic validation error with record context. It does not reconcile finances, infer fund flows, impose new temporal or currency relationships, or require every supplied transaction to be flagged by the alert.

## ADR-009 — Preserve valid incomplete investigations

**Date:** 2026-10-27

**Status:** Accepted; protected by tests at `1375d9f`.

**Decision:** Add no new collection minimums beyond existing record rules; allow empty collections wherever references permit them. Preserve G01/G05 empty counterparty collections, explicit null counterparty references, contextual evidence with no transaction references, and G05's missing beneficiary information. Preserve empty check evidence-reference and findings lists, supplied but unreferenced records, and G04 evidence referencing supplied `TX-105` outside the alert's flagged subset.

**Why:** Missing information and contextual records are valid features of the synthetic investigations. Requiring complete beneficiary data, completed checks, or an alert containing every transaction would invent requirements absent from the approved input structure.

**Tradeoff:** Contract acceptance establishes structural validity, not investigative completeness or sufficient support for a recommendation. Supplied verification statuses and findings remain recorded synthetic inputs; validation does not execute verification or generate missing facts.

## ADR-010 — Keep reference answers and provisional labels outside inputs

**Date:** 2026-10-27

**Status:** Accepted; separate artifacts introduced at `7438b40`, with aggregate guards implemented at `1375d9f`.

**Decision:** Keep [reference answers](data/golden_cases/references/) and the [fictional labeling policy](specs/labeling_policy_v1.json) separate from investigation inputs. Aggregate validation rejects unknown top-level fields and recursively rejects the exact keys `expected_action`, `recommended_action`, `reference_rationale`, and `rubric_version` inside evidence facts, including objects nested in lists. It does not ban ordinary words in descriptions or findings, or load reference answers or the policy to decide input validity.

**Why:** Expected outcomes must not become supplied evidence. The current vocabulary `close`, `investigate`, and `escalate` remains provisional and requires review; it is not a finalized output contract or implemented classification behavior.

**Tradeoff:** This is an explicit structural boundary, not a general detector of answer information hidden in arbitrary prose. Validation does not choose an AML disposition, determine SAR obligations, or certify the provisional labels.

## ADR-011 — Preserve heterogeneous evidence within JSON-compatible facts

**Date:** 2026-10-27

**Status:** Accepted; implemented at `e6094f9` and reused by `InvestigationInput` at `1375d9f`.

**Decision:** Model evidence facts as a dictionary with string keys and nested JSON-compatible values: strings, finite numbers, booleans, null, lists, and objects. Reject non-JSON Python values and non-finite numbers rather than silently stringifying them. Preserve heterogeneous facts without inventing a universal fact-specific schema. Evidence types and verification statuses remain nonempty strings rather than a new controlled vocabulary.

**Why:** The fixtures contain different kinds of evidence. A single mandatory facts schema would invent unsupported fields and could erase valid contextual or incomplete information.

**Tradeoff:** JSON compatibility does not prove factual truth, independent verification, or domain-specific completeness. Fact-specific evidence schemas are outside the approved input-contract scope; Phase 2 output contracts remain pending.

---

The following records document the approved output-contract choices implemented on 2026-10-27 at `a538063` and `ce0cd4a`. They update the earlier output-contract deferral without rewriting the historical ADRs. Both checkpoints are committed locally on `feature/phase-2-output-contracts` and remain unmerged.

## ADR-012 — Preliminary structured outputs with explicit abstention

**Date:** 2026-10-27

**Status:** Accepted; implemented at `a538063`.

**Decision:** Add `RecordCitation`, `CitedStatement`, `Contradiction`, and `InvestigationOutput` in [contracts.py](src/aml_triage/contracts.py). Separate factual findings, interpretations, unresolved questions, missing information, and contradictions. Require every output field, reject unknown fields, and preserve submitted text and list order. Recommendations use the provisional actions `close`, `investigate`, or `escalate`, with a cited rationale and at least one cited factual finding. Explicit abstention uses `assessment_status="unable_to_recommend"` and required `recommended_action=null`, rather than a fourth disposition. All outputs require `recommendation_scope="preliminary"` and `human_review_required=True`.

**Citation rules:** Require citations for factual findings, interpretations, and both contradiction sides. Questions, missing-information statements, and an abstention rationale may have none. Reject duplicate typed citations within one statement, but permit citation reuse across statements and contradiction sides. Do not silently trim, deduplicate, or insert data.

**Why:** A shared structure makes submitted assessments inspectable while distinguishing recorded facts from interpretations and unresolved issues. Explicit abstention preserves an inability to recommend without inventing a new AML disposition. Preliminary scope and human review keep the contract within the synthetic project's decision-support boundary.

**Tradeoff:** Structural and internal-consistency checks cannot establish that a rationale explains its conclusion, that a contradiction is real, or that an assessment is complete. The provisional labels still require review; no recommendation generator or finalized labeling policy is implemented.

## ADR-013 — Separate typed citation resolution from output structure

**Date:** 2026-10-27

**Status:** Accepted; typed citations implemented at `a538063`, with contextual validation at `ce0cd4a`.

**Decision:** A citation identifies a `record_type` and exact `record_id` in one of eight namespaces: case, customer, account, counterparty, transaction, alert, evidence, or verification_check. Keep standalone Pydantic output validation separate from `validate_investigation_output_references`, which takes already-validated input and output models. The function checks exact case/alert identities and every citation in the rationale, statement collections, and both contradiction sides. Contextual mismatches raise `ValueError` with field paths; success returns the original output without mutating either object.

**Why:** Output structure can be validated without an investigation, while record existence requires the supplied input. Exact typed lookup avoids guessing relationships, normalizing identifiers, or substituting namespaces. The same textual ID may exist in more than one namespace.

**Tradeoff:** Callers must invoke contextual validation separately when accepting an output against an investigation. It permits supplied transactions outside the alert subset, contextual evidence, nullable counterparties, uncited questions, and abstention without fabricated citations. It neither requires every record to be cited nor imposes a relationship between separately cited evidence and transactions.

## ADR-014 — Citation existence does not establish factual support

**Date:** 2026-10-27

**Status:** Accepted; enforced as the boundary of both output checkpoints.

**Decision:** Treat successful reference resolution only as evidence that a record identifier exists in the supplied investigation. Validation does not judge suspiciousness, choose or alter a disposition, verify claims or recorded verification statuses, or determine whether a citation supports a statement. It does not load reference answers or interpret the fictional labeling policy. Candidate outputs in [tests](tests/test_contracts.py) are authored independently of reference-answer labels and JSON.

**Why:** Conflating existence with support would assert certainty the implemented checks cannot provide. Keeping reference answers separate also protects later evaluation from answer leakage.

**Tradeoff:** A structurally valid statement with existing citations can still be unsupported or false. Substantive grounding evaluation and the formal evaluation protocol remain unimplemented. These contracts introduce no AML classifier, LLM investigation agent, automated verification system, SAR logic, or production regulatory policy.

## ADR-015 — Begin evaluation with a thin mechanical candidate-packet auditor

**Date:** 2026-10-27

**Status:** Accepted implementation scope; documentation consolidated, auditor not yet implemented.

**Decision:** The first auditor will take explicitly supplied investigation and candidate output payloads, apply existing `InvestigationInput` and `InvestigationOutput` validation independently where possible, and invoke `validate_investigation_output_references` only when both validate. Produce a separate machine-readable report with artifact/version identities, available diagnostics and `passed`, `failed`, `not_evaluated` or `error` stage statuses. Preserve fail-fast limitations, distinguish expected rejection from evaluator errors, and mark semantic dimensions `not_evaluated` with reasons. See the [protocol's mechanical-auditor contract](docs/phase-2/EVALUATION_PROTOCOL_DRAFT.md#81-accepted-first-implementation-thin-candidate-packet-auditor).

**Why:** Existing contracts provide a bounded, testable foundation while closure corroboration, grounding, completeness, abstention and alternative actions still need adjudication. Mechanical reporting can proceed without pretending these semantic decisions are settled.

**Limits and tradeoffs:** The auditor will not access reference answers, adjudication annotations or the fictional policy, change contracts, interpret policy, or judge claim support. Valid identifiers can accompany false claims. No overall semantic score, unqualified assessment pass, exhaustive-error promise or inferred generation/retry counts is approved. D-01 through D-08 have accepted working directions, not complete semantic adjudication; labels, semantic scoring, held-out design and any LLM judge remain unapproved. This documentation checkpoint adds no code, tests, dependencies, fixtures, model calls or performance claims and does not complete Phase 2.

## ADR-016 — Close Week 5 on the bounded engineering comparison

**Date:** 2026-11-01

**Status:** Accepted by the project owner in the current conversation on November 1, 2026; recorded locally. Exact approval time was not supplied. Week 6 is not authorized.

**Decision:** Close Week 5 - Bounded Classification Experiments - on its bounded engineering-comparison objective. Accept the fixed five-case development selection, frozen prompt/configuration provenance, five preserved baseline observations, five validated hosted assessments, seven recorded SDK operations including two failures, descriptive comparisons, mechanical validation, accounting and disclosed limitations. No additional hosted calls are justified solely to complete this milestone. See the [versioned closure decision](docs/week-5/WEEK_5_MILESTONE_CLOSURE_DECISION_v0.1_2026-11-01.md) for source identities and local-only evidence paths.

**Why:** The [roadmap](ROADMAP.md) requires a fixed evaluation set, prompt versions, comparisons and a decision record; the [charter](PROJECT_CHARTER.md) requires comparison with the baseline and a decision on further experiments. The owner accepted the controlled operational comparison as sufficient evidence. More outputs without a new evaluation question would not establish stronger conclusions.

**Limits and consequences:** This does not demonstrate classification accuracy, semantic correctness, superiority, independent AML expert validation or held-out generalization. All five hosted actions were investigate, without established correctness; REF-01 policy access differed. Nine broad semantic dimensions remain not_evaluated; no multi-prompt optimization is claimed. Unknown billing/terminal observations remain unknown. P01/P02 stay approved; P03 remains under review with scoring disabled, P04 release stays separately controlled, and P05 conditions remain applicable to later independent evaluation/expert claims. No new calls, spending, allowance reset, code change, scoring, publication or Week 6 work is authorized. Further experiments need a defined question and separate approval. Preserve all prior records and uncommitted work.

## ADR-017 — Close Week 6 on bounded evidence-report and library-integration evidence

**Date:** 2026-11-01

**Status:** Formally accepted by the project owner on November 1, 2026; exact approval time was not supplied. Week 7 is not authorized.

**Decision:** Close Week 6 on the original [roadmap](ROADMAP.md) objective, "Evidence validation, narrative drafting and integration", with "Full pipeline, integration tests, grounded report examples". Accept the bounded library-level baseline/mocked-hosted -> audit -> evidence-report flow. [PR #18](https://github.com/AvaliVava/aml-alert-triage/pull/18) supplies the composer, E01-E06, design/implementation contract and focused tests; [PR #19](https://github.com/AvaliVava/aml-alert-triage/pull/19) supplies executable integration tests and [reproducible evidence examples](docs/week-6/WEEK_6_INTEGRATION_EVIDENCE_v0.1_DRAFT.md). See the [versioned closure record](docs/week-6/WEEK_6_MILESTONE_CLOSURE_DECISION_v0.1_2026-11-01.md) for exact source/merge identities, acceptance matrix and provenance.

**Evidence:** Historical local reports record 45 composer tests, 16 integration tests and 499 complete-suite passes. The owner reports successful PR #19 GitHub Actions Python 3.11, 3.12 and 3.13 jobs, including dependency, foundation smoke and unit checks. Local history/workflow inspection is distinct from independently retrieving remote CI logs; no runtime tests or CI jobs were executed in this documentation checkpoint.

**Why and tradeoff:** The owner accepts an executable library-level full pipeline under the original bounded milestone. No new CLI, deployment, publication layer or runtime coordinator is necessary merely to satisfy that acceptance. Their operational responsibilities and maintenance costs would require a separate justified scope. Test-local outcome mapping and synthetic mocked responses demonstrate engineering behavior, not a new public production interface or provider receipt.

**Limits and controls:** Restricted source-field checks and qualified narrative units do not establish general factual support, source authenticity, semantic correctness, classification accuracy/precision/recall, model superiority, regulatory compliance or independent AML expertise. All nine broader semantic dimensions remain `not_evaluated`; unsupported/unchecked candidate assertions remain attributed. P01/P02 stay approved; P03 remains under review with numerical scoring disabled, and P04 release/P05 independence and expert-review conditions remain separately controlled. Week 5 frozen artifacts and consumed live allowances are unchanged. No new model request, spending, scoring, evaluation release or implementation is authorized. This is not closure of the entire Phase 2 program.

**Historical and next-milestone boundary:** ADR-016 and earlier entries remain unchanged; their Week 6 authorization statements describe their historical checkpoints and are superseded only by subsequent owner approvals. **Week 7 has not started and is not automatically authorized.** A separate readiness review, applicable evaluation-protocol decisions and explicit owner authorization are required before Week 7 work begins.
