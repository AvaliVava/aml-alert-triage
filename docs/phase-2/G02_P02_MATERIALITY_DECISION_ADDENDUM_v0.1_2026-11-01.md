# G02 P02 materiality decision addendum - v0.1

**Decision ID:** G02-P02-MATERIALITY-2026-11-01-v0.1

**Owner approval date:** November 1, 2026, as explicitly supplied in the current engineering conversation. The exact approval time was not supplied.

**Status:** Owner-approved, case-specific P02 ruling recorded as a local documentation addendum. M04 is contextual and nonmandatory for frozen G02. This is not approval of the full evaluation protocol, numerical semantic-performance scoring, a formal adjudication-register/report release, or broader Week 5 completion.

## 1. Authority, scope and preservation

The project owner approved the eight-part ruling in section 5 through the current instruction, "CODEX - RECORD OWNER-APPROVED G02 P02 MATERIALITY RULING." Codex records that instruction and verifies the cited frozen evidence. Owner approval in conversation is not independent AML expert validation, independently authenticated approval evidence, or a formal repository release.

Read this addendum alongside the unchanged [P01 fidelity addendum](G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md), [v0.1 adjudication register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json), [reconciliation specification](G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md), [fictional labeling policy](../../specs/labeling_policy_v1.json) and [evaluation protocol draft](EVALUATION_PROTOCOL_DRAFT.md). P01 is preserved without reopening its ruling.

The P01 addendum and original register/specification/report retain their historical pending-M04 language. This dated P02 addendum records the subsequent owner decision for frozen G02; it does not overwrite that history, update machine-readable fields or change existing reconciliation behavior. The existing reconciler does not consume this addendum.

Frozen candidates, original annotations, source inventory and saved reconciliation are Git-ignored local evidence. Paths marked local-only below are not repository download links and may be unavailable in a fresh checkout.

## 2. Exact evidence and candidate occurrences

The [frozen G02 input](../../data/golden_cases/inputs/G02.json) records:

| Typed record | Input-root JSON pointer | Value or context |
| --- | --- | --- |
| `transaction:TX-G02-01` | `/transactions/0/amount`, `/transactions/0/currency`, `/transactions/0/direction` | `"48500.00"`, `"USD"`, `"credit"` |
| `transaction:TX-G02-01` | `/transactions/0/occurred_at` | `"2026-10-13T11:00:00Z"` |
| `customer:CUST-G02` | `/customer/expected_monthly_activity/minimum`, `/customer/expected_monthly_activity/maximum`, `/customer/expected_monthly_activity/currency` | `"15000.00"`, `"25000.00"`, `"USD"` |
| `customer:CUST-G02` | `/customer/profile_last_verified` | `"2026-09-20"` |
| `transaction:TX-G02-02` | `/transactions/1/amount`, `/transactions/1/currency`, `/transactions/1/direction`, `/transactions/1/occurred_at` | `"1200.00"`, `"USD"`, `"credit"`, `"2026-10-14T12:00:00Z"` |
| `alert:ALT-G02` | `/alert/rule_id`, `/alert/transaction_ids`, `/alert/created_at` | `"UNUSUAL_INCOMING_PAYMENT"`, `["TX-G02-01"]`, `"2026-10-16T09:30:00Z"` |

The same-currency numerical comparison `Decimal("48500.00") > Decimal("25000.00")` is supported. No complete monthly activity history, direction/aggregation definition, calendar-versus-rolling window or hard per-transaction limit is supplied. The profile-verification date does not establish those definitions or prove that the profile is obsolete. The alert rule name does not supply a numerical materiality threshold.

### Hosted candidate

Local-only artifact: `outputs/evaluation/g02-paired-pilot-20261029/hosted_candidate.json`.

At `/factual_findings/1/statement`:

> The customer profile records expected monthly activity of $15,000.00 to $25,000.00 USD.

Submitted citation: `customer:CUST-G02`.

At `/interpretations/0/statement`, containing H031-H036:

> The $48,500.00 payment is materially above the customer's stated maximum monthly activity; this is a reason to clarify the activity, not by itself proof of wrongdoing.

Submitted citations, in original order: `transaction:TX-G02-01`; `customer:CUST-G02`.

H033 is the exact span `materially` at offsets `[26,36)`, using zero-based start-inclusive/end-exclusive character offsets. The register routes this unit to `separate_materiality_dimension` rather than a factual-support category. The containing statement remains `reviewed_not_cleared_unconditional_pass`. This ruling does not automatically clear that wording or remove P01's attribution qualifications.

The rationale at `/rationale/statement` also uses the numerical comparison. Its original submitted citations are `transaction:TX-G02-01`, `customer:CUST-G02`, `evidence:EV-G02-02` and `verification_check:CHK-G02-01`, in that order. Its exact text and the H004/H034 fidelity ruling remain preserved in the P01 addendum.

At `/unresolved_questions/2/statement`, H043:

> Does the payment fit the customer's current business activity and profile?

Its submitted citation list is `[]`. The approved whole-statement status remains `qualified_investigative_question`: question relevance is approved, not the answer or independent mandatory coverage.

### Baseline candidate

Local-only artifact: `outputs/evaluation/g02-paired-pilot-20261029/baseline_candidate.json`.

At `/factual_findings/0/statement`:

> Transaction TX-G02-01 amount was USD 48,500.00.

Submitted citation: `transaction:TX-G02-01`.

The baseline does not discuss the monthly-profile comparison. Its preliminary `investigate` output is preserved. This addendum introduces no M04 omission penalty, coverage credit, action change or correctness ranking.

## 3. Original M04 record and preserved mandatory coverage

The local-only `outputs/evaluation/g02-paired-pilot-20261029/source_inventory.draft.json` proposed M04 as "Profile range and correctly scoped numeric comparison," based on I03 (recorded profile) and I10 (derived numerical observation), with `context_materiality_pending`. The original draft remains unchanged.

The original register entry at `/case_level_materiality_and_coverage/M04` remains:

- Requirement: `Profile-range comparison`.
- Applicability: `contextual_independent_materiality_pending`.
- Hosted: `discussed_contextually`.
- Baseline: `not_discussed`.
- Reason: `No separate mandatory finding absent approved independent materiality rule; monthly range not per-transfer limit.`

Its pending gate P02 blocks treating M04 as a fourth mandatory coverage requirement. This addendum resolves the owner's case-specific decision in documentation; those original machine-readable fields remain historical and unchanged.

| Previously approved mandatory item | Hosted | Baseline |
| --- | --- | --- |
| M01 - Flagged incoming payment and its amount | `covered` | `partly_covered` |
| M02 - Customer purpose claim and corroboration gap | `covered` | `covered` |
| M03 - Supplied counterparty and unresolved commercial relationship | `covered` | `omitted` |

There remain exactly three approved mandatory coverage items. M04 receives no mandatory coverage credit or omission penalty. M05's contextual, nonmandatory treatment is unchanged.

## 4. Competing interpretations considered

- **Relevant profile-fit context:** The recorded amount and monthly profile provide a reason to ask whether the activity fits the recorded business profile. This adds context beyond transaction identification, commercial-purpose corroboration and the counterparty relationship. The approved investigative question is preserved.
- **Independently mandatory comparison:** A deviation could warrant its own mandatory investigative item under sufficiently justified case evidence and approved criteria. The available evidence and approved evaluation criteria do not sufficiently justify that requirement for this frozen G02 case. Merely adding a distinct fact or using the word "materially" cannot establish mandatory coverage.
- **Hard-limit or disposition inference:** Treating the monthly expected maximum as an individual payment prohibition, proof of wrongdoing or an automatic escalation rule is not established by the supplied records. The fictional policy defines material unresolved questions and REF-01, but supplies no applicable monthly-profile deviation threshold.

These distinctions do not assert that profile deviations are inherently immaterial. They preserve the difference between arithmetic, relevant context, independent investigative materiality, mandatory coverage and justification for an action. The already adjudicated G02 preliminary `investigate` action and its empty approved-alternatives set are unchanged.

## 5. Owner-approved ruling

1. The frozen G02 records establish a USD 48,500 incoming credit and a USD 25,000 maximum expected monthly activity. The numerical comparison is valid.
2. The discrepancy provides relevant context for evaluating whether the transaction fits the customer's recorded business activity and profile.
3. The supplied records do not establish that the expected monthly maximum is a hard individual transaction limit.
4. The discrepancy does not, by itself, establish wrongdoing, an escalation requirement or an independently mandatory fourth coverage item.
5. M04 is contextual and nonmandatory for frozen G02.
6. M01, M02 and M03 remain the three previously approved mandatory coverage items.
7. Preserve the existing hosted profile-fit question as a qualified investigative question.
8. Do not automatically clear the hosted candidate's use of "materially", grant an unconditional whole-statement pass or authorize numerical semantic-performance scoring.

**Important qualification:** Do NOT characterize M04 as inherently immaterial. The available evidence and approved evaluation criteria do not sufficiently justify mandatory coverage for this particular frozen case. Future evidence or approved criteria may justify reassessment in other cases.

## 6. Remaining limits and release boundaries

P02 is recorded here as an owner-approved, frozen-G02 documentation decision. It creates no general materiality threshold or new policy rule. The distinction between owner synthetic-case adjudication and independent AML expertise remains explicit.

Original annotations, candidate wording/citations, input bytes, P01 decisions, existing atomic judgments, whole-statement qualifications, M01-M03 coverage, reference label provenance, process-authority limitations and prior reports remain unchanged. The provisional golden reference is not rewritten.

Report-category/applicability and denominator-release decisions, formal versioned adjudication/report release, independent held-out evidence and independent expert review remain separate. No numerical semantic score, performance percentage, model ranking, full protocol approval, broader Week 5 closure or Week 6 transition is authorized. No automatic move to P03 is made. A future machine-readable release or evaluator change requires separate authorization; this approved P02 ruling is not being resubmitted for approval.

## 7. Evidence identities and verification

All digests in the table identify original file bytes, preserving line endings and serialization. The distinct canonical validated-input SHA-256 is `7f077f89d97f17fac644273d0a53c5b108b519d00adcddba0c21a9122f6a58da`; it does not replace the original-byte input identity.

| Artifact | Original-byte SHA-256 |
| --- | --- |
| [Frozen G02 input](../../data/golden_cases/inputs/G02.json) | `60cbf66dbbb24b59f0ae0a86e03a92d6f0dac0e68511ec05cd1953b96763326f` |
| [v0.1 adjudication register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json) | `51396c9f87d6781cf55ae72380327b815e35a8d08e0ac3b3614512ff99c226ef` |
| [Fictional labeling policy](../../specs/labeling_policy_v1.json) | `6cdefd8400ae160163a4e0625f0b5311890ecad27967767e10459df2f1ee6352` |
| [v0.1 reconciliation specification](G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md) | `5dccec7479980d8f78aee442469cb3839370eb12cbba0edcdcfaf20aa7440ed6` |
| [P01 fidelity addendum](G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) | `34acbce3f39a6844afc99030687dfa308150659020cb8ee7643c066c5a6bdcfc` |
| Local-only `outputs/evaluation/g02-reconciliation-20261030/reconciliation_report.json` | `5346a20ed22bf99752c208a9b1598198fad7276de4e1ff322e6382f53faf932f` |
| Local-only `outputs/evaluation/g02-paired-pilot-20261029/hosted_candidate.json` | `c44c89e49dc82443b2a5af45e8b0bb249e35551298764706355061099c62e82b` |
| Local-only `outputs/evaluation/g02-paired-pilot-20261029/baseline_candidate.json` | `4ad63a4c19e2c71a3cf8dbcc7ddf14aee30cafc198a93b32bea9ea5356918b07` |
| Local-only `outputs/evaluation/g02-paired-pilot-20261029/claim_annotations.draft.json` | `034b7a42e3a3f0b7361c6415654c531710091a8432a6fd4246e0a56cc1ea4ff1` |
| Local-only `outputs/evaluation/g02-paired-pilot-20261029/source_inventory.draft.json` | `8ac79e804346b510a374259154eaa36d6880530b2ac3339354bfc6ad0ed40cd5` |

Existing read-only packet/catalog/register checks passed before this addition: 75 atomic units, 21 statement occurrences, 203 source pointers, eight manifest-bound artifact hashes and both frozen candidate identities. Both candidate outputs pass the unchanged Pydantic contracts and contextual citation validation. The saved reconciliation's M04 entry matches the original register and retains three mandatory items. Exact candidate statements, H033 span, submitted citations and H043's qualified question status were checked against the frozen records.

These checks verify integrity and recorded relationships; they do not independently adjudicate AML meaning or release scoring. No full unit-suite rerun is claimed for this documentation-only addition.
