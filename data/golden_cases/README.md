# AML Alert Triage — Phase 2 Golden Case Draft V1

This directory contains five valid synthetic investigation inputs, five **separate** reference-answer artifacts, and one intentionally invalid duplicate-transaction fixture. The [fictional labeling policy](../../specs/labeling_policy_v1.json) and [fixture-integrity tests](../../tests/test_golden_fixtures.py) are stored elsewhere in the repository.

## Usage

From the `aml-alert-triage` repository root, using the Python environment where the project is installed (see [setup instructions](../../README.md#install-and-run-local-checks)):

```bash
python -m unittest discover -s tests -v
```

[G05_invalid_duplicate.json](inputs/G05_invalid_duplicate.json) is **intentionally invalid**: the transaction ID occurs twice. It is not a sixth AML-labeled case. The related [G05.json](inputs/G05.json) is a valid-but-incomplete investigation input whose separate reference answer carries the provisional label `investigate`.

**Do not place reference files or labeling policy outcome fields in investigation inputs or prompts sent to a future classifier.** Reference answers stay in [references/](references/); fixture-integrity tests read them separately. The formal evaluation protocol remains pending.

## Status and limitations

- These are **draft, synthetic research fixtures** and a **fictional referral rubric**; no production AML rules or regulatory thresholds are asserted.
- The fictional labeling vocabulary (`close`, `investigate`, `escalate`) and case labels remain provisional until the rubric and case evidence are reviewed; no finalized output contract is implemented.
- Transactions are a deliberately selected relevant *slice*, not fabricated comprehensive 90-day customer histories. The full 90-day synthetic-history generator is Phase 3 work.
- A supplied `verification_status` or verification-check record is synthetic input describing a recorded review result, not a real verification performed by the software.
- `G03` has a deliberately explicit policy trigger: `REF-01` requires two transactions after an internal instruction, a non-approved payee account and no registered authorized change. The reference must not be generalized to real bank reporting policy.
- Individual Pydantic V2 record contracts and the complete `InvestigationInput` contract are implemented in [contracts.py](../../src/aml_triage/contracts.py), with [contract tests](../../tests/test_contracts.py). Aggregate validation composes the existing records and rejects duplicate record IDs, repeated identifiers within reference lists, unknown outer fields, mismatched case/alert/customer relationships, and unresolved explicit references. Heterogeneous JSON evidence facts and valid incomplete inputs remain supported.
- The original Meridian case is G04: deposits TX-101 through TX-104 total USD 37,300 and TX-105 is a separate USD 32,000 outgoing transfer. **Do not claim the deposits funded that wire**; available information does not establish fund tracing.
- The golden-case artifacts were committed and merged through PR #2 (`db212d4`).
- At `1375d9f`, the local readiness audit recorded **99 passing tests**, accepting all five valid inputs through Python and JSON validation and rejecting the duplicate fixture. See [PROJECT_STATUS.md](../../PROJECT_STATUS.md) for the recorded results. Remote feature-branch GitHub Actions results remain unverified.
