# Fictional case study — Meridian Electronics Ltd.

**Training only:** No real company, person, institution or transaction is represented.

## Initial customer context
Customer ID `CUST-021`, two-branch electronics retailer, account opened March 2023, typical daily cash deposits `$1,000–$3,000`, expected monthly turnover `$45,000–$65,000`.

## Alert and transactions
Alert `ALT-2026-014` concerns unusual cash deposits 12–15 October 2026:

| ID | Date | Event | USD amount |
|---|---|---|---:|
| TX-101 | 2026-10-12 | Cash deposit | +9,200 |
| TX-102 | 2026-10-13 | Cash deposit | +9,400 |
| TX-103 | 2026-10-14 | Cash deposit | +9,100 |
| TX-104 | 2026-10-15 | Cash deposit | +9,600 |
| TX-105 | 2026-10-15 | International wire | -32,000 |

Cash total: `$37,300`; cash deposit average `$9,325`. The outgoing wire is **not proven** to have been funded by those precise deposits.

## Evidence register
- `EV-001`: transaction extract — reconciled in fictional source ledger.
- `EV-002`: cash-sales records — partially corroborated.
- `EV-003`: promotional campaign record — event dates corroborated.
- `EV-004`: supplier invoice — received, beneficiary account differs from wire record.
- `EV-005`: outgoing wire record — reconciled in fictional source ledger.
- `EV-006`: supplier ownership information — not obtained.

## Draft internal narrative
The customer received four cash deposits totaling `$37,300` from 12–15 October 2026, exceeding the stated typical daily range. Promotional records partially support increased business activity, but the flagged deposits have not been fully reconciled to sales. A `$32,000` international wire dated 15 October was described as a supplier payment. The beneficiary account in the wire record differs from that on the supplied invoice. The relationship between the actual recipient and the invoicing supplier remains unverified. **Recommend further investigation** into the beneficiary discrepancy and incomplete reconciliation, subject to human review.

## Evidence validation lessons
Checking that `TX-105` exists does not establish that its beneficiary matches the invoice. Claim-level grounding may require comparing `EV-004` and `EV-005`. Never present criminal intent or the funding chain as proven.
