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
