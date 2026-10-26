# AML Alert Triage — Phase 2 Golden Case Draft V1

This directory contains six input files (five valid investigation fixtures and one deliberately malformed sibling), five **separate** reference-answer files, a fictional labeling policy, and fixture-integrity tests.

## Usage

From the `aml-alert-triage` repository root:

```bash
python -m unittest discover -s tests -v
```

`data/golden_cases/inputs/G05_invalid_duplicate.json` is **intentionally invalid**: the transaction ID occurs twice. It is not a sixth AML-labeled case. The related `G05.json` is a valid-but-incomplete investigation input whose expected action is investigate.

**Do not place reference files or labeling policy outcome fields in prompts sent to a classifier.** The evaluator reads the references separately.

## Status and limitations

- These are **draft, synthetic research fixtures** and a **fictional referral rubric**; no production AML rules or regulatory thresholds are asserted.
- Labels are provisional until the rubric and case evidence are reviewed.
- Transactions are a deliberately selected relevant *slice*, not fabricated comprehensive 90-day customer histories. The full 90-day synthetic-history generator is Phase 3 work.
- A supplied `verification_status` or `verification_check` is a synthetic simulation of a review result, not a real verification performed by the assistant.
- `G03` has a deliberately explicit policy trigger: `REF-01` requires two transactions after an internal instruction, a non-approved payee account and no registered authorized change. The reference must not be generalized to real bank reporting policy.
- This fixture test validates selected consistency invariants, not every constraint of the forthcoming final Pydantic data contract. Counterparty relationships and typed evidence payloads are subject to further specification.
- The original Meridian case is G04: deposits TX-101 through TX-104 total USD 37,300 and TX-105 is a separate USD 32,000 outgoing transfer. **Do not claim the deposits funded that wire**; available information does not establish fund tracing.
- These fixtures have not been committed to GitHub.
