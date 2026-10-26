# Candidate domain and engineering requirements

**Status:** Phase 1 candidates. Phase 2 will decide exact schemas, rubric, tests and acceptance thresholds.

## Functional
- **FR-01:** Accept a well-defined synthetic alert package.
- **FR-02:** Validate required fields; preserve unknowns explicitly.
- **FR-03:** Compute transaction totals, patterns and historical comparisons in deterministic Python.
- **FR-04:** Produce structured `close/investigate/escalate` recommendations.
- **FR-05:** Assemble evidence references from supplied records.
- **FR-06:** Surface missing or contradictory material information.
- **FR-07:** Draft a factual internal narrative with material evidence and limitations.
- **FR-08:** Validate schema, reference existence and supported material factual claims.
- **FR-09:** Return a consolidated package for human review and useful execution metadata.

## Non-functional
- **NFR-01:** Reproducible evaluations and recorded prompt/model/data versions.
- **NFR-02:** Traceable evidence and transformation lineage.
- **NFR-03:** Controlled behavior on malformed input and LLM/API errors.
- **NFR-04:** Modular interfaces and contract tests.
- **NFR-05:** Measure per-run latency, tokens, estimated cost and errors.
- **NFR-06:** Keep credentials out of source control and logs; use synthetic records.

## Evaluation questions (NOT yet measured)
- Does it outperform a deterministic rules baseline on a held-out, properly labeled case set?
- Does it preserve contradictory evidence and distinguish missing/unknown?
- Are transaction and document IDs real references in the supplied dataset?
- Do the cited sources actually support each material narrative claim?
- Which error classes occur, at what frequency, and what do fixes regress?
- What are measured latency and API cost?
- Could a qualified analyst validate usefulness and review effort? This is optional until feasible; do not claim real-world time savings without one.

## Open decisions for Phase 2
Exact entity schemas; required vs nullable fields; business rules and labels; golden cases; train/dev/test split; metrics and error taxonomy; authoritative treatment of contradictory fields; claim-level validation depth; minimum acceptance thresholds.
