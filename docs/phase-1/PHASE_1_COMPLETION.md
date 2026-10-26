# Phase 1 learning checkpoint — 26 October 2026

## Covered in the learning sequence
- AML alert lifecycle; analyst and authorized reporting boundaries.
- Structuring, layering and context-dependent indicators.
- Evidence vs red flags vs conclusions; plausible benign explanations.
- Risk, precision/recall, monitoring false positives and queue prioritization.
- KYC, CDD, EDD, beneficial ownership, SoF and SoW.
- Missing/stale/inconsistent data, lineage and uncertainty.
- Investigation case anatomy, narrative and claim grounding.
- Operational failure modes and engineering problem synthesis.

## Established project constraints
Synthetic data; no real-bank decisions or filing; three *recommended* actions; deterministic baseline before LLM; single hosted model to start; avoid RAG without a demonstrated need; evidence-grounded narrative; staged eight-phase roadmap; preserve GitHub traceability.

## Unverified hypotheses
- The approach will reduce investigative drafting work.
- Model-assisted triage will outperform rules baseline.
- Narrative grounding checks will reliably catch all significant hallucinations.
All remain experiments, not accomplishments.

## Phase 1 closeout checklist
- [x] Consolidated learning manual created.
- [x] Engineering reference drafts prepared.
- [ ] Review the drafts against the existing GitHub charter and current project files.
- [ ] Record approved decisions and unresolved questions in the canonical decision log.
- [ ] Commit agreed files to GitHub and verify commit and passing tests.
- [ ] Update project status to mark Phase 1 complete.

**Repository review note (26 October 2026):** Public `main` contains `PROJECT_CHARTER.md` and `PROJECT_STATUS.md`. The charter aligns with the synthetic-data, human-review, baseline-first scope. `PROJECT_STATUS.md` still describes the GitHub repository as not created and only old local Python verification; this conflicts with the confirmed public repository and reported later Python 3.11 testing. Verify actual current tests and commit status, then correct those stale statements without guessing implementation progress.

**Current status:** Documentation prepared locally; approval, status reconciliation and commit not yet completed. Do not mark Phase 1 fully closed until those steps occur.
