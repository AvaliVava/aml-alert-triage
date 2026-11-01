# G02 P01 fidelity decision addendum - v0.1

**Decision ID:** G02-P01-FIDELITY-2026-11-01-v0.1

**Owner approval date:** November 1, 2026, as explicitly supplied in the current engineering conversation. The exact approval time was not supplied.

**Status:** Owner-approved P01 ruling recorded as a local documentation addendum. This is not approval of the full evaluation protocol, semantic scoring, a formal adjudication-register/report release, or milestone completion.

## 1. Authority and preservation

The project owner approved the eight-part ruling in section 4 through the current instruction, "CODEX - RECORD OWNER-APPROVED P01 FIDELITY RULING." Codex records that instruction and the frozen evidence; it does not independently authenticate the conversation or provide independent AML expert validation.

Read this dated addendum alongside the unchanged [v0.1 adjudication register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json) and [reconciliation specification](G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md). Their original P01 pending language remains historical evidence. The owner ruling below is additional documentation; it does not rewrite those records or change the existing reconciler's behavior.

Frozen candidates, original annotations, source inventory and the saved reconciliation report are local-only, Git-ignored evidence. Their paths below are not repository download links. They may be unavailable in an ordinary checkout.

## 2. Exact original occurrences

Both occurrences belong to the frozen hosted G02 candidate at the local-only path `outputs/evaluation/g02-paired-pilot-20261029/hosted_candidate.json`.

### H004

**Candidate JSON pointer:** `/rationale/statement`

> Further investigation is warranted because the recorded incoming payment exceeds the customer's stated maximum monthly activity, while the customer-supplied commercial-purpose explanation is not corroborated by the recorded check. The supplied information does not establish that the payment lacks a legitimate purpose.

**Original span:** "customer's stated maximum monthly activity"

**Offsets:** `[85,127)`, zero-based start-inclusive/end-exclusive character offsets in the exact statement.

**Actual submitted typed citations, in original order:**

- `transaction:TX-G02-01`
- `customer:CUST-G02`
- `evidence:EV-G02-02`
- `verification_check:CHK-G02-01`

### H034

**Candidate JSON pointer:** `/interpretations/0/statement`

> The $48,500.00 payment is materially above the customer's stated maximum monthly activity; this is a reason to clarify the activity, not by itself proof of wrongdoing.

**Original span:** "customer's stated maximum monthly activity"

**Offsets:** `[47,89)`, using the same offset convention.

**Actual submitted typed citations, in original order:**

- `transaction:TX-G02-01`
- `customer:CUST-G02`

### Stronger draft atomic proposition

The unchanged register and original annotation draft use the following proposition for both occurrences:

> The customer personally stated the profile maximum.

That proposition and its judgments must remain distinguishable from the exact original candidate wording. Neither source text nor submitted citations are repaired or replaced by this addendum.

## 3. Supplied evidence and competing readings

The [frozen G02 input](../../data/golden_cases/inputs/G02.json) supplies these relevant fields:

| Record | Input JSON pointer | Recorded value and scope |
| --- | --- | --- |
| `customer:CUST-G02` | `/customer/expected_monthly_activity/maximum` | `"25000.00"` |
| `customer:CUST-G02` | `/customer/expected_monthly_activity/currency` | `"USD"` |
| `transaction:TX-G02-01` | `/transactions/0/amount`, `/transactions/0/currency`, `/transactions/0/direction` | `"48500.00"`, `"USD"`, `"credit"` |
| `evidence:EV-G02-02` | `/evidence/1/source`, `/evidence/1/facts/claim` | `"customer_supplied"`; `"Payment for wholesale goods"` |
| `verification_check:CHK-G02-01` | `/verification_checks/0/findings/0` | `"No invoice, purchase order, or independent record corroborates the claimed purpose"` |

The input records the profile maximum and incoming payment, supporting the numerical comparison `48500.00 > 25000.00`. It does not establish personal authorship of the profile maximum. The explicitly customer-supplied explanation concerns payment purpose. The supplied check concerns corroboration of that purpose; it does not establish who supplied the monthly profile value.

The competing readings considered for fidelity are:

- **Personal-authorship reading:** "customer's stated" attributes the maximum to a personal customer statement. The stronger drafted proposition makes that attribution explicit, but the supplied records do not establish it.
- **Recorded-profile reading:** the phrase refers to the maximum stated in the customer's recorded profile. This reading distinguishes possession of a customer profile from personal authorship of its contents.
- **Qualified wording:** the original phrase is insufficiently precise to convert the stronger drafted proposition into an automatic candidate-level error or an unconditional whole-statement pass.

These readings explain the annotation-fidelity issue. They do not authorize a replacement atomic claim, new citation judgments, a new score, or a final resolution of M04.

## 4. Owner-approved ruling

1. The frozen G02 input supports the recorded USD 25,000 maximum expected monthly activity.
2. The frozen input supports the USD 48,500 incoming payment and their numerical comparison.
3. The frozen input does not establish that the customer personally supplied the monthly-activity maximum.
4. The draft atomic proposition, "The customer personally stated the profile maximum," strengthens the original candidate phrase, "customer's stated maximum monthly activity."
5. That stronger drafted personal-authorship proposition must not automatically determine candidate-level factual-error scoring.
6. The original customer-attribution wording remains qualified; do not award an unconditional whole-statement factual/citation pass.
7. Retain the existing judgments for the stronger drafted proposition and preserve the prior adjudication history.
8. Keep M04 independent materiality unresolved and outside the mandatory coverage denominator.

This records the approved fidelity ruling; it does not authorize numerical scoring.

## 5. Effect on existing records and remaining limits

For H004 and H034, retain the register's existing `not_established` factual-support and `inadequate` submitted-citation judgments for the **stronger drafted proposition**. Do not transfer those judgments automatically to a newly asserted interpretation of the original candidate.

Both containing statement occurrences retain `reviewed_not_cleared_unconditional_pass`. This addendum awards no unconditional factual or citation pass. The register's literal `withheld_pending_original_fidelity` markers and the saved report's P01 entry remain unchanged as historical machine-readable records. The current implementation does not consume this addendum or gain permission to score from it.

M04 remains `contextual_independent_materiality_pending`, outside the three-item mandatory coverage population. A monthly expected-activity maximum is not automatically a per-transfer limit or an independently material recommendation criterion. The existing M01-M03 coverage decisions, M05 contextual treatment, G02 preliminary action and other approved judgments are unchanged.

The remaining formal report-category, applicability, denominator and release decisions are separate from this owner-approved P01 ruling. No full protocol approval, scoring eligibility promotion, percentage, model ranking, independent held-out result, expert validation or completed human AML review is asserted. Any future versioned machine-readable release or implementation change requires separate authorization; the approved ruling itself is not being submitted for reapproval.

## 6. Evidence identities and verification

All SHA-256 values below identify original file bytes, including existing line endings and serialization. They are not substituted canonical-input hashes.

| Artifact | Original-byte SHA-256 |
| --- | --- |
| [G02 input](../../data/golden_cases/inputs/G02.json) | `60cbf66dbbb24b59f0ae0a86e03a92d6f0dac0e68511ec05cd1953b96763326f` |
| [v0.1 adjudication register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json) | `51396c9f87d6781cf55ae72380327b815e35a8d08e0ac3b3614512ff99c226ef` |
| [v0.1 reconciliation specification](G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md) | `5dccec7479980d8f78aee442469cb3839370eb12cbba0edcdcfaf20aa7440ed6` |
| Local-only `outputs/evaluation/g02-paired-pilot-20261029/hosted_candidate.json` | `c44c89e49dc82443b2a5af45e8b0bb249e35551298764706355061099c62e82b` |
| Local-only `outputs/evaluation/g02-paired-pilot-20261029/claim_annotations.draft.json` | `034b7a42e3a3f0b7361c6415654c531710091a8432a6fd4246e0a56cc1ea4ff1` |
| Local-only `outputs/evaluation/g02-paired-pilot-20261029/source_inventory.draft.json` | `8ac79e804346b510a374259154eaa36d6880530b2ac3339354bfc6ad0ed40cd5` |
| Local-only `outputs/evaluation/g02-reconciliation-20261030/reconciliation_report.json` | `5346a20ed22bf99752c208a9b1598198fad7276de4e1ff322e6382f53faf932f` |

The existing read-only packet/catalog/register checks passed before this addition: 75 units, 21 statement occurrences, 203 source pointers and both frozen candidate identities. Exact H004/H034 text spans, offsets and submitted citation lists match the frozen candidate. The saved report's 75 owner records and 21 whole-statement records match the unchanged register.

These are integrity and reconciliation checks, not a new semantic experiment or independent re-adjudication. No full unit-suite rerun is claimed for this documentation-only addition.
