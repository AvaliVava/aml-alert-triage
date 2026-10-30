# Codex — Controlled Repository Integration Request (not yet executed)

This is the preserved archive handoff, describing its state before repository
integration. For current paths, commands and integration limits, see the
[research tool instructions](../../research/evaluation_calibration/README.md).

The project owner approved **hybrid evaluation as an overall approach** and asked to implement the engineering *review process* suggested in your independent G02 report. **Do not construe this as approval of draft semantic verdicts, labels, category precedence, scores or policy interpretations.**

## Before changing anything

1. Inspect the active branch, `AGENTS.md`, `PROJECT_CHARTER.md`, `PROJECT_STATUS.md`, `DECISIONS.md`, `docs/phase-2/EVALUATION_PROTOCOL_DRAFT.md`, the two current Week 4 G02 drafts and current tests. Stop if repository state or target files conflict with this handoff; report differences rather than overwriting work.
2. Verify the frozen original `outputs/evaluation/g02-paired-pilot-20261029` files and reference identities. Do not replace that local ignored directory with a second source of truth or commit original ignored outputs without an explicit decision.
3. Read this package's calibration plan, source-linked catalog, inspection report, blank worksheet, Python review tools and tests. Treat this package as a candidate implementation for review, not as automatic permission to merge.

## Proposed bounded integration

- Add the calibration plan as a **draft** in `docs/week-4`, reconciling naming/location with existing docs without revising historical decisions.
- Integrate the seven-bundle catalog and read-only calibration tools in a research/evaluation-only area. Use a **path or manifest adapter** to reference the repository's *existing frozen local packet* if appropriate; avoid a second editable data source. Do not silently revise candidate bytes, recorded citations or the draft labels.
- Make tests runnable with Python 3.11+ stdlib and the supplied immutable packet. Keep integrity checks distinct from semantic assertions. Include negative tests for altered text/span/source hashes and fake approvals.
- Add a reviewer worksheet with empty status fields and source links; no invented human review or automatic scoring.
- Ensure normal repository tests still pass; state exactly which tests ran. No model calls, paid APIs, dependencies, service/contract changes, new evaluators, policy mutations or threshold setting.
- Present an implementation diff and tested behaviors for **review before committing**. Do not push/PR/merge unless separately authorized by project owner.

## What success means

A reviewer can open each of seven bundles, inspect exact original output text and linked evidence/citations, see intended adversarial counterfactuals, enter human observations while preserving disagreements, and verify immutable artifact identity. The software must refuse to transform an AI draft into approved semantic labels or a performance ranking.

## Known unfinished design tasks

- Human H047/H032 fidelity review.
- D-07 reviewer assignment and competence disclosure.
- D-04 category precedence, attribution ambiguity, source-set adequacy and questions/implementation applicability.
- Proposed M03 materiality and denominator rules.
- Meaning-level counterfactual judgments with actual reviewed fixtures.
- Held-out data, comparison fairness and any future scoring.
