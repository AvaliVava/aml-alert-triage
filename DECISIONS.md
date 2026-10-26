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
