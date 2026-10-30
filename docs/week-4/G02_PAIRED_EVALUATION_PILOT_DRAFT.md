# G02 paired evaluation pilot - DRAFT

**DRAFT / HUMAN REVIEW REQUIRED / NOT APPROVED SEMANTIC ANNOTATIONS.**

Date: 2026-10-29. Case: CASE-G02. This is one exposed synthetic development case, with one saved hosted assessment and one reproducible deterministic baseline assessment. No benchmark, semantic score, accuracy claim, performance ranking or label approval is produced.

Codex authored this engineering draft. Codex is an AI assistant, not an independent AML subject-matter reviewer. No human claim judgments, disagreements or adjudication have yet been recorded. Prior exposure to G02 and its provisional reference is disclosed; this is not a blinded review.

## 1. Scope, ordering and source authority

The checkout was clean on research/week-4-evaluation-design at revision `010147592fd4e308063121eb411f900c52e8808c`. PR #12 merged the earlier live review; the implementation is unchanged.

The source inventory was authored from the original input and saved before this pilot's candidate-annotation stage. The author had prior exposure to G02; that ordering does not restore evaluation independence. The original hosted candidate was then copied without rewriting; the baseline was generated solely from the validated input. Only after both candidates were frozen was the reference parsed for descriptive comparison. Preservation checks also hashed tracked files; those hashes and reference content were not passed to baseline generation.

Sources:

- [G02 investigation](../../data/golden_cases/inputs/G02.json), the sole case-data input to baseline generation.
- [Existing live review](G02_LIVE_ASSESSMENT_REVIEW.md), including separate successful/failed attempts and coverage limits.
- [Evaluation protocol draft](../phase-2/EVALUATION_PROTOCOL_DRAFT.md), especially D-03 through D-07 and the proposed support categories.
- [Engineering decisions](../../DECISIONS.md), especially ADR-010 and ADR-012 through ADR-015.
- [Contracts](../../src/aml_triage/contracts.py), [auditor](../../src/aml_triage/auditor.py), [amount checker](../../src/aml_triage/transaction_amount_checks.py), [G04 relationship checker](../../src/aml_triage/evidence_relation_checks.py) and [baseline](../../src/aml_triage/deterministic_baseline.py).
- [G02 provisional reference](../../data/golden_cases/references/G02_reference.json), consulted only on the evaluation side.

Only new draft documentation and ignored local artifacts are created. Existing [project status](../../PROJECT_STATUS.md) and [worklog](../../WORKLOG.md) are preserved under this assignment's draft-only scope. No code, prompt, contract, dependency, existing evaluator, dataset, reference answer or architecture changes are made.

## 2. Frozen candidate and input identities

All SHA-256 values below cover the declared bytes. A case ID is not an artifact identity.
| Artifact or version | Value |
| --- | --- |
| Original input file bytes | `60cbf66dbbb24b59f0ae0a86e03a92d6f0dac0e68511ec05cd1953b96763326f` |
| Validated canonical input UTF-8 | `7f077f89d97f17fac644273d0a53c5b108b519d00adcddba0c21a9122f6a58da` |
| Original hosted execution bundle bytes | `95e6cbd8053929c3aea6de5ba5c72c9e443352554e2ea3d0ead5d39b6567de9b` |
| Hosted candidate exact UTF-8 | `c44c89e49dc82443b2a5af45e8b0bb249e35551298764706355061099c62e82b` |
| Hosted model / SDK | `gpt-6-luna / 3.40.0` |
| Hosted prompt version / instructions SHA-256 | `aml-preliminary-1.0 / f6472c5d27337626e113cfa982297b0c6b317282eefc4a600f049fa025bb6c83` |
| Baseline candidate bytes | `4ad63a4c19e2c71a3cf8dbcc7ddf14aee30cafc198a93b32bea9ea5356918b07` |
| Baseline implementation version | `0.1.0` |
| Baseline last source commit | `73fee08e42a3482010ee258bb3dbf17d3165dd88` |
| Baseline source file SHA-256 | `e3d9746e980dc6c11f8bdecff4279389baa3952fac119b0994a9db35087271a0` |
| Baseline execution checkout | `010147592fd4e308063121eb411f900c52e8808c` |
| Runtime used for this local preparation | `Python 3.11.9 / Pydantic 2.14.1` |

Local originals/copies are not committed:

| Repository-root local path | Purpose |
| --- | --- |
| `outputs/openai/G02-live-attempt2-20261029-113851.json` | Original successful execution bundle, preserved unchanged. |
| `outputs/evaluation/g02-paired-pilot-20261029/hosted_candidate.json` | Exact original candidate_json encoded as UTF-8, with no added newline. |
| `outputs/evaluation/g02-paired-pilot-20261029/baseline_candidate.json` | Reproducible baseline assessment. |
| `outputs/evaluation/g02-paired-pilot-20261029/source_inventory.draft.json` | Frozen input-only source inventory and raw record snapshots. |
| `outputs/evaluation/g02-paired-pilot-20261029/claim_annotations.draft.json` | Full proposed units, exact spans, source pointers, submitted citations and unresolved judgments. |
| `outputs/evaluation/g02-paired-pilot-20261029/hosted_audit.json` and `baseline_audit.json` in that directory | Existing auditor reports, kept separate from candidates. |
| `outputs/evaluation/g02-paired-pilot-20261029/reference_comparison.draft.json` | Descriptive provisional-reference comparison after freezing candidates. |
| `outputs/evaluation/g02-paired-pilot-20261029/packet_manifest.draft.json` | Initial freeze identities, versions, source hashes and execution ordering. |
| `outputs/evaluation/g02-paired-pilot-20261029/evaluation_manifest.draft.json` | Final draft-document/artifact digests and verification record. |

The public documentation identifies these local files without making their ignored bytes available in a fresh checkout. No raw execution bundle is added to Git.

Baseline generation called the existing assessment function twice with file/network access blocked during generation. Both serializations were identical. Serialization is UTF-8, model_dump(mode=json), sorted keys, two-space indent, ensure_ascii=False, allow_nan=False, and one trailing LF. Both outputs pass the existing input/output contracts and contextual references. This reproducibility is for the deterministic candidate, not a guarantee of repeating the hosted response.

The recorded hosted model name is not a resolved immutable provider snapshot. The original audit records source_revision=null. The current checkout is evidence of what was inspected, not a captured Git revision from the hosted execution.

## 3. Input-only source inventory

These are recorded values or explicitly scoped observations, not independently authenticated events. Exact original record snapshots are in the ignored inventory. The following typed pointers are relative to each named record.
| ID / source kind | Record and exact fields | Observation |
| --- | --- | --- |
| I01 / Recorded alert | `alert:ALT-G02` `/transaction_ids`, `/rule_id` | ALT-G02 flags TX-G02-01; TX-G02-02 is supplied context outside the flagged subset. |
| I02 / Recorded transaction | `transaction:TX-G02-01` `/amount`, `/currency`, `/direction`, `/transaction_type`, `/account_id`, `/occurred_at`, `/counterparty_id` | TX-G02-01 records USD 48500.00, domestic_transfer, credit, ACC-G02, 2026-10-13T11:00:00Z and CP-G02-01. |
| I03 / Recorded profile | `customer:CUST-G02` `/expected_monthly_activity/minimum`, `/expected_monthly_activity/maximum`, `/expected_monthly_activity/currency` | The profile records USD 15000.00-25000.00 expected monthly activity. It does not identify who personally supplied the range, its directional definition, or a hard payment limit. |
| I04 / Recorded ledger/status | `evidence:EV-G02-01` `/source`, `/verification_status`, `/facts/recorded_amount`, `/facts/currency`, `/facts/sender_reference` | EV-G02-01 is a synthetic_bank_ledger payment_record with recorded_amount 48500.00, currency USD and sender_reference CP-G02-01. Its verified status is supplied data, not authentication performed by this pilot. |
| I05 / Customer claim | `evidence:EV-G02-02` `/source`, `/facts/claim`, `/facts/invoice_reference`, `/related_transaction_ids` | EV-G02-02, source customer_supplied, records Payment for wholesale goods, with invoice_reference null. The claim does not establish actual purpose. |
| I06 / Recorded check conclusion | `verification_check:CHK-G02-01` `/check_type`, `/status`, `/findings/0`, `/subject_evidence_ids` | CHK-G02-01 records commercial_purpose, unresolved, and no corroborating invoice, purchase order or independent record. It is not a check executed by this pilot. |
| I07 / Recorded counterparty | `counterparty:CP-G02-01` `/display_name`, `/relationship_status` | CP-G02-01 has display name Orchid Distribution LLC and relationship_status unverified. A counterparty identifier is supplied; independent identity and commercial relationship are not established. |
| I08 / Context transaction | `transaction:TX-G02-02` `/amount`, `/currency`, `/direction`, `/transaction_type`, `/occurred_at`, `/counterparty_id` | TX-G02-02 records USD 1200.00 domestic_transfer credit, CP-G02-02 and 2026-10-14T12:00:00Z. CP-G02-02 relationship_status is unverified. |

I09: The whole input `/evidence` contains only EV-G02-01 and EV-G02-02. No invoice, purchase-order or dispatch evidence is supplied. A null invoice reference alone would not prove global invoice absence.

I10: The same-currency numeric comparison is Decimal(48500.00) > Decimal(25000.00). The range is expected monthly profile activity; neither a hard payment limit nor personal customer authorship is established.

I11: No supplier instruction or authorization register is supplied. That inventory observation is distinct from a complete policy judgment or a claim that no referral condition could exist outside the snapshot.

The input also supplies the case/policy ID, account ownership, customer profile dates, and CP-G02-02's unverified relationship status. Policy ID alone does not supply policy text. No direct conflicting field values were identified in this input pass; conflict-inventory completeness is not certified.

Proposed review items, frozen before the paired annotation stage:

| Item | Input-derived topic | Status |
| --- | --- | --- |
| M01 | Flagged incoming transaction and amount | Proposed material item; approval pending. |
| M02 | Customer purpose claim, recorded no-corroboration conclusion and scoped document gap | Proposed material item; approval pending. |
| M03 | Supplied counterparty and unresolved commercial relationship | Proposed material item; approval pending. |
| M04 | Expected profile range and properly scoped comparison | Context; materiality pending. |
| M05 | Additional unflagged credit | Context; not automatically required. |

No completeness denominator is approved. Additional facts, repeated wording and longer answers do not automatically earn greater coverage.

## 4. Mechanical results and recognition coverage

| Existing check | Hosted | Baseline |
| --- | --- | --- |
| Input structure | passed | passed |
| Output structure | passed | passed |
| Contextual references | passed | passed |
| Factual findings supplied | 6 | 3 |
| Restricted amount findings checked | 0 | 2 |
| Restricted amount matches / conflicts | 0 / 0 | 2 / 0 |
| Findings outside or otherwise unchecked by the restricted grammar | 6 | 1 |
| Nine broad semantic auditor dimensions | all not_evaluated | all not_evaluated |

The live audit was reproduced exactly offline on the original canonical input and candidate text. The new saved audit reports explicitly label the paired artifacts, so their identity/digest-basis fields differ from the historical report where labels were null.

The baseline writes exact amount-check sentences, while the hosted prose falls outside that grammar. These counts measure recognizer coverage and selected field consistency, not model accuracy or overall factual support. No G04 relationship annotation applies to G02; its two-direct-source policy is not generalized here.

## 5. Proposed qualitative paired review

All observations below are AI-authored proposals requiring human review.

| Topic | Hosted assessment | Baseline assessment | Pending interpretation |
| --- | --- | --- | --- |
| M01: flagged payment | Explicitly states flagged transaction, amount, credit direction, account, date and counterparty. | States the amount with the transaction citation; does not explicitly explain the alert linkage or incoming direction. | Whether omitted context is material must be adjudicated; no omission score. |
| M02: purpose and records | Attributes the wholesale claim and reports the unresolved check; asks for commercial support. | Attributes the customer claim and identifies no linked invoice/order/dispatch evidence; asks for documents. | Both preserve a gap. Check-based reporting and inventory-based absence are distinct support routes. |
| M03: relationship | Reports unverified relationship and asks about business relationship/underlying payer. | Does not explicitly discuss CP-G02-01 relationship or request its establishment. | Potential baseline coverage gap against a proposed item; hosted payer wording also needs scope review. |
| M04: profile | States both bounds and the numeric comparison. | Does not mention the profile range. | Materiality is pending; no hard-limit violation is inferred. |
| M05: second credit | Records amount, type, direction, counterparty and date. | Records amount with transaction citation. | Extra context is not automatically required or a quality advantage. |
| Contradictions | Empty list. | Empty list. | No obvious conflicting input values identified; neither empty list certifies completeness. |
| Action / human review | Preliminary investigate; review required. | Preliminary investigate; review required. | Descriptive agreement, not approved recommendation quality. |

### 5.1 Hosted wording questions

- H004 and H034: rationale and first interpretation attribute the profile maximum to the customer's personal statement. The profile supplies the numbers but not that provenance. Proposed input judgment: not_established; proposed citation judgment: inadequate for the attribution component. The separate numeric comparison remains supported under the draft reading. No severity or score is approved.
- H029 and H042: recorded credit/counterparty association is supplied, but authenticated ultimate payer identity is not. The open question must not imply the counterparty record is missing.
- H040: an uncited question contains an amount premise. Empty question citations are permitted structurally; whether the premise requires its own citations is pending.
- H044-H049: snapshot-absence claims are distinct from quoting the recorded check. H049's wording about no supporting records addressing purpose is ambiguous: corroborating commercial documents are absent, but EV-G02-02 does address purpose as a customer claim. Both readings are retained for adjudication; no silent false-claim verdict.
- EV-G02-01 is uncited. TX-G02-01 and ALT-G02 already support the flagged-payment observation; the reference's extra evidence pointer does not create a universal requirement to cite all available evidence.

### 5.2 Baseline wording and comparable questions

- B006-B007 correctly attribute the purpose claim to the supplied customer explanation; no corresponding claim that the customer personally supplied the monthly range appears.
- B001/B003 call questions material and describe the detector's REF-01 outcome. Their normative/process content is not adjudicated merely because relevant transaction/explanation citations exist.
- B009-B014 describe fixed rules, no independent verification, no fraud/fund tracing, scope limitations and required review. These agree with the inspected implementation's stated scope, but the sole CASE-G02 citation does not establish software behavior. Treatment of implementation disclaimers within input support/citation adequacy remains pending; this is not an allegation that new verification was fabricated.
- B017-B020 and B023-B026 describe missing recognized document types and a limited inventory inference. Inventory-absence citation policy and inference sufficiency need the same human treatment as hosted absence claims.
- Baseline unresolved_questions[0] and missing_information[0] repeat the same statement. Both occurrences are preserved; the material item must not be counted twice.

## 6. Reference, fairness and one-case limits

The provisional reference was consulted only in the evaluation stage. It records investigate, two required-findings themes (flagged incoming amount and uncorroborated purpose), and a question about commercial records/sender relationship. Both candidates return investigate; neither receives an action-quality score. Baseline relationship coverage and alert-description differences are proposals for review, not finalized errors.

The baseline encodes a limited fictional REF-01 interpretation. The hosted prompt supplies no REF-01 criterion text and explicitly does not turn a policy ID into policy text. This pilot compares configured systems; it cannot isolate reasoning quality under equal policy information. No generic policy access is newly authorized here.

G02 is an exposed development example. The author has prior exposure to candidate/reference discussions. There is one existing hosted output, no new hosted experiment, no independent held-out population and no approved semantic denominator. No model ranking, calibrated abstention, statistical reliability, real-world AML effectiveness, analyst savings or monetary cost is established.

The earlier connection failure remains separate from this candidate pair; it produced no assessment and is not an abstention. No billing or server-processing conclusion is derived from its absent usage.

## 7. Proposed annotation format and review controls

See [G02_ANNOTATION_FORMAT_DRAFT.md](G02_ANNOTATION_FORMAT_DRAFT.md). The ignored JSON stores all 21 prose statements and 75 proposed review units (49 hosted, 26 baseline), including nonfactual questions, recommendations and process/scope statements so exclusions are visible.

Offsets are zero-based Unicode code points within the decoded statement, with an exclusive end. Each unit retains exact text, full statement, candidate hash and copied submitted citations. Overlapping spans isolate attribution or modifiers without rewriting the candidate. Money is a currency/amount value; changing granularity remains an owner decision.

The unit totals are annotation-accounting counts, not semantic scores or approved metric denominators. All units lack human approval. A proposed unassessable category identifies a specific unresolved interpretation rule; lack of human approval alone is not converted to unassessability. Null categories mean no factual category proposed for a question/recommendation/requirement, not a pass.

Human-review/disagreement arrays are empty with status not_yet_solicited. Alternative readings are annotation-author uncertainties, not invented disagreements between reviewers.

## 8. Decisions requiring owner approval

- D-04: unit granularity, attribution categories, source/citation support sets, permissible question presuppositions, scoped absence and implementation-disclaimer treatment.
- D-07: named reviewer roles, actual qualifications, disagreement procedure, adjudication rationale and approval authority.
- D-03/D-05: materiality, recommendation eligibility, acceptable alternative actions and abstention treatment before action scoring.
- D-06: generic rubric access and full generation-context/exposure safeguards before any broader hosted comparison.
- D-01/D-02: closure/referral source sufficiency remain pending; this pilot does not settle them.
- D-08: family isolation and future held-out data remain pending; this case cannot become held-out retroactively.

P01-P07 in the annotation file preserve specific questions about profile attribution, question citations, payer wording, absence citations, ambiguous purpose wording, epistemic scope and process claims.

## 9. Verification and review status

Preparation checked input/output contracts, contextual citations, repeat baseline bytes, original candidate equality/hash and exact historical-audit reproduction. Draft integrity checks verify every annotation span, copied citation list, typed source pointer/value, artifact digest and local document link. Original live/input/reference/source files are preserved.

No unit-test suite was run because no implementation/test/dependency changes were authorized. The repository's recorded 358-test baseline is historical; no fresh suite or remote CI result is claimed. No API requests, credentials access, paid experiments, new dependencies or framework were used.

Only these two new draft documents and ignored local pilot artifacts are created. Existing status/worklog and all implementation files remain unchanged. Nothing is staged, committed, pushed or merged. The next action is independent human review of the draft inventory, proposed units and pending decisions.

## Appendix A. Complete proposed review units

Every row below is a proposed AI judgment; human_review_status is not_reviewed for every unit. Source pointers refer to the frozen original input. Exact observed values are retained in the input inventory and annotation JSON, without repeating them in each row. A citation list is copied from the containing statement without inheriting citations from elsewhere. Exact full statements, quoted spans and offsets make the normalized proposition traceable. Input-context pointers are not asserted to support a proposition when support is not established.

### hosted `/rationale/statement`

Original statement (unchanged):

> Further investigation is warranted because the recorded incoming payment exceeds the customer's stated maximum monthly activity, while the customer-supplied commercial-purpose explanation is not corroborated by the recorded check. The supplied information does not establish that the payment lacks a legitimate purpose.

Submitted citations: `transaction:TX-G02-01`; `customer:CUST-G02`; `evidence:EV-G02-02`; `verification_check:CHK-G02-01`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H001 `0:34` `Further investigation is warranted`; Further investigation is warranted. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `verification_check:CHK-G02-01 /check_type`; `verification_check:CHK-G02-01 /status`; `verification_check:CHK-G02-01 /findings/0`; `verification_check:CHK-G02-01 /subject_evidence_ids` | No factual category proposed | `unassessable` | Recommendation quality/materiality is not adjudicated. Relevant records are cited; recommendation adequacy is not scored. |
| H002 `47:72` `recorded incoming payment`; The referred-to payment is recorded as incoming/credit. | `transaction:TX-G02-01 /direction` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H003 `47:127` `recorded incoming payment exceeds the customer's stated maximum monthly activity`; The payment amount exceeds the profile maximum numerically. | `transaction:TX-G02-01 /amount`; `transaction:TX-G02-01 /currency`; `customer:CUST-G02 /expected_monthly_activity/maximum`; `customer:CUST-G02 /expected_monthly_activity/currency` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. Derivation: Decimal(48500.00) > Decimal(25000.00), with USD recorded for both. Expected monthly range is not a hard payment limit. |
| H004 `85:127` `customer's stated maximum monthly activity`; The customer personally stated the profile maximum. | Context only: `customer:CUST-G02 /expected_monthly_activity/maximum`; Context only: `customer:CUST-G02 /expected_monthly_activity/currency` | `not_established` | `inadequate` | The profile gives a maximum but does not identify its personal speaker/source. This does not prove the attribution false outside the snapshot. CUST-G02 supplies the range, not the claimed personal attribution; none of the submitted citations establishes it. Pending P01_PROFILE_ATTRIBUTION. |
| H005 `139:187` `customer-supplied commercial-purpose explanation`; A customer-supplied purpose explanation is recorded. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H006 `188:229` `is not corroborated by the recorded check`; The supplied check records no corroboration of the claimed purpose. | `verification_check:CHK-G02-01 /check_type`; `verification_check:CHK-G02-01 /status`; `verification_check:CHK-G02-01 /findings/0`; `verification_check:CHK-G02-01 /subject_evidence_ids` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H007 `231:319` `The supplied information does not establish that the payment lacks a legitimate purpose.`; The snapshot does not establish illegitimate purpose. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `verification_check:CHK-G02-01 /check_type`; `verification_check:CHK-G02-01 /status`; `verification_check:CHK-G02-01 /findings/0`; `verification_check:CHK-G02-01 /subject_evidence_ids` | `unassessable` | `unassessable` | A cautious epistemic limitation, not proof of legitimate purpose. Approve how such negative inferences are judged. The cited explanation/check support caution; no general semantic-entailment rule is approved. Pending P06_EPISTEMIC_SCOPE. |

### hosted `/factual_findings/0/statement`

Original statement (unchanged):

> The alert identifies TX-G02-01, a $48,500.00 USD domestic transfer credit to ACC-G02 on 2026-10-13, with CP-G02-01 as the recorded counterparty.

Submitted citations: `alert:ALT-G02`; `transaction:TX-G02-01`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H008 `0:30` `The alert identifies TX-G02-01`; The alert identifies TX-G02-01. | `alert:ALT-G02 /transaction_ids` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H009 `34:48` `$48,500.00 USD`; TX-G02-01 records USD 48,500.00. | `transaction:TX-G02-01 /amount`; `transaction:TX-G02-01 /currency` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H010 `49:66` `domestic transfer`; TX-G02-01 is recorded as domestic_transfer. | `transaction:TX-G02-01 /transaction_type` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H011 `67:73` `credit`; TX-G02-01 is recorded as a credit. | `transaction:TX-G02-01 /direction` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H012 `74:84` `to ACC-G02`; TX-G02-01 references ACC-G02. | `transaction:TX-G02-01 /account_id` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H013 `85:98` `on 2026-10-13`; TX-G02-01 occurred on recorded UTC date 2026-10-13. | `transaction:TX-G02-01 /occurred_at` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. Derivation: Date component of 2026-10-13T11:00:00Z. |
| H014 `100:143` `with CP-G02-01 as the recorded counterparty`; TX-G02-01 records counterparty CP-G02-01. | `transaction:TX-G02-01 /counterparty_id` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |

### hosted `/factual_findings/1/statement`

Original statement (unchanged):

> The customer profile records expected monthly activity of $15,000.00 to $25,000.00 USD.

Submitted citations: `customer:CUST-G02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H015 `58:68` `$15,000.00`; The expected monthly profile minimum is USD 15,000.00. | `customer:CUST-G02 /expected_monthly_activity/minimum`; `customer:CUST-G02 /expected_monthly_activity/currency` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H016 `72:86` `$25,000.00 USD`; The expected monthly profile maximum is USD 25,000.00. | `customer:CUST-G02 /expected_monthly_activity/maximum`; `customer:CUST-G02 /expected_monthly_activity/currency` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |

### hosted `/factual_findings/2/statement`

Original statement (unchanged):

> Customer-supplied evidence states that the payment was for wholesale goods and has no invoice reference recorded.

Submitted citations: `evidence:EV-G02-02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H017 `0:74` `Customer-supplied evidence states that the payment was for wholesale goods`; Customer-supplied evidence records the wholesale-goods purpose claim. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H018 `79:112` `has no invoice reference recorded`; EV-G02-02 has a null invoice_reference. | `evidence:EV-G02-02 /facts/invoice_reference` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |

### hosted `/factual_findings/3/statement`

Original statement (unchanged):

> The recorded commercial-purpose check is unresolved and states that no invoice, purchase order, or independent record corroborates the claimed purpose.

Submitted citations: `verification_check:CHK-G02-01`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H019 `4:37` `recorded commercial-purpose check`; CHK-G02-01 is a recorded commercial_purpose check. | `verification_check:CHK-G02-01 /check_type` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H020 `38:51` `is unresolved`; CHK-G02-01 records status unresolved. | `verification_check:CHK-G02-01 /status` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H021 `68:78` `no invoice`; The supplied check records no invoice corroborating the claimed purpose. | `verification_check:CHK-G02-01 /findings/0` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H022 `80:94` `purchase order`; The supplied check records no purchase order corroborating the claimed purpose. | `verification_check:CHK-G02-01 /findings/0` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H023 `99:117` `independent record`; The supplied check records no independent record corroborating the claimed purpose. | `verification_check:CHK-G02-01 /findings/0` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |

### hosted `/factual_findings/4/statement`

Original statement (unchanged):

> CP-G02-01, displayed as Orchid Distribution LLC, has a recorded relationship status of unverified.

Submitted citations: `counterparty:CP-G02-01`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H024 `11:47` `displayed as Orchid Distribution LLC`; CP-G02-01 has recorded display name Orchid Distribution LLC. | `counterparty:CP-G02-01 /display_name` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H025 `55:97` `recorded relationship status of unverified`; CP-G02-01 has recorded relationship_status unverified. | `counterparty:CP-G02-01 /relationship_status` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |

### hosted `/factual_findings/5/statement`

Original statement (unchanged):

> The supplied transaction records also include a $1,200.00 USD domestic transfer credit from CP-G02-02 on 2026-10-14.

Submitted citations: `transaction:TX-G02-02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H026 `48:61` `$1,200.00 USD`; TX-G02-02 records USD 1,200.00. | `transaction:TX-G02-02 /amount`; `transaction:TX-G02-02 /currency` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H027 `62:79` `domestic transfer`; TX-G02-02 is recorded as domestic_transfer. | `transaction:TX-G02-02 /transaction_type` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H028 `80:86` `credit`; TX-G02-02 is recorded as a credit. | `transaction:TX-G02-02 /direction` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H029 `87:101` `from CP-G02-02`; TX-G02-02 associates the recorded credit with CP-G02-02. | `transaction:TX-G02-02 /direction`; `transaction:TX-G02-02 /counterparty_id` | `supported` | `adequate` | Supported under a recorded-association reading of from. It does not establish an authenticated ultimate payer; stronger readings remain pending. Submitted citations include those sources; other citations remain preserved. Pending P03_PAYER_WORDING. |
| H030 `102:115` `on 2026-10-14`; TX-G02-02 occurred on recorded UTC date 2026-10-14. | `transaction:TX-G02-02 /occurred_at` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. Derivation: Date component of 2026-10-14T12:00:00Z. |

### hosted `/interpretations/0/statement`

Original statement (unchanged):

> The $48,500.00 payment is materially above the customer's stated maximum monthly activity; this is a reason to clarify the activity, not by itself proof of wrongdoing.

Submitted citations: `transaction:TX-G02-01`; `customer:CUST-G02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H031 `4:22` `$48,500.00 payment`; The referenced payment amount is USD 48,500.00. | `transaction:TX-G02-01 /amount`; `transaction:TX-G02-01 /currency` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H032 `37:89` `above the customer's stated maximum monthly activity`; The payment exceeds the profile maximum numerically. | `transaction:TX-G02-01 /amount`; `transaction:TX-G02-01 /currency`; `customer:CUST-G02 /expected_monthly_activity/maximum`; `customer:CUST-G02 /expected_monthly_activity/currency` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. Derivation: Decimal(48500.00) > Decimal(25000.00), with USD recorded for both. Expected monthly range is not a hard payment limit. |
| H033 `26:36` `materially`; The numerical difference is material to investigation. | `transaction:TX-G02-01 /amount`; `transaction:TX-G02-01 /currency`; `customer:CUST-G02 /expected_monthly_activity/maximum`; `customer:CUST-G02 /expected_monthly_activity/currency` | `unassessable` | `unassessable` | Materiality is an interpretive policy question, not implied by a numeric comparison alone. Submitted citations include those sources; other citations remain preserved. |
| H034 `47:89` `customer's stated maximum monthly activity`; The customer personally stated the profile maximum. | Context only: `customer:CUST-G02 /expected_monthly_activity/maximum`; Context only: `customer:CUST-G02 /expected_monthly_activity/currency` | `not_established` | `inadequate` | Same unsupported personal attribution as H004; retain this occurrence without counting it as a second material omission. The profile citation does not establish who stated the range. Pending P01_PROFILE_ATTRIBUTION. |
| H035 `91:131` `this is a reason to clarify the activity`; The difference warrants clarification. | `transaction:TX-G02-01 /amount`; `transaction:TX-G02-01 /currency`; `customer:CUST-G02 /expected_monthly_activity/maximum`; `customer:CUST-G02 /expected_monthly_activity/currency` | No factual category proposed | `unassessable` | Interpretive recommendation; no factual support score proposed. Submitted citations include those sources; other citations remain preserved. |
| H036 `133:166` `not by itself proof of wrongdoing`; The amount comparison alone does not establish wrongdoing. | `transaction:TX-G02-01 /amount`; `transaction:TX-G02-01 /currency`; `customer:CUST-G02 /expected_monthly_activity/maximum`; `customer:CUST-G02 /expected_monthly_activity/currency` | `unassessable` | `unassessable` | Appropriate caution on its face; treatment of epistemic limitations is pending rather than a categorical truth score. Submitted citations include those sources; other citations remain preserved. Pending P06_EPISTEMIC_SCOPE. |

### hosted `/interpretations/1/statement`

Original statement (unchanged):

> The customer's stated wholesale-goods purpose remains uncorroborated in the supplied record, so the commercial rationale is unresolved.

Submitted citations: `evidence:EV-G02-02`; `verification_check:CHK-G02-01`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H037 `4:45` `customer's stated wholesale-goods purpose`; Customer-supplied evidence records a wholesale-goods purpose claim. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| H038 `46:91` `remains uncorroborated in the supplied record`; The supplied check and evidence snapshot provide no commercial-purpose corroboration. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `verification_check:CHK-G02-01 /check_type`; `verification_check:CHK-G02-01 /status`; `verification_check:CHK-G02-01 /findings/0`; `verification_check:CHK-G02-01 /subject_evidence_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Both the customer claim and supplied no-corroboration conclusion are cited; external absence is not inferred. |
| H039 `96:134` `the commercial rationale is unresolved`; The commercial rationale remains unresolved. | `verification_check:CHK-G02-01 /check_type`; `verification_check:CHK-G02-01 /status`; `verification_check:CHK-G02-01 /findings/0`; `verification_check:CHK-G02-01 /subject_evidence_ids` | `unassessable` | `unassessable` | Consistent with the check, but broader rationale/materiality treatment requires adjudication. Submitted citations include those sources; other citations remain preserved. |

### hosted `/unresolved_questions/0/statement`

Original statement (unchanged):

> What goods, order, or commercial arrangement does the $48,500.00 payment relate to, and can the customer provide supporting records?

Submitted citations: None submitted.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H040 `54:72` `$48,500.00 payment`; The question presupposes a USD 48,500.00 payment. | `transaction:TX-G02-01 /amount`; `transaction:TX-G02-01 /currency` | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. This question has no citations, which the contract permits. Whether factual presuppositions need local citations is pending. Pending P02_QUESTION_CITATIONS. |
| H041 `0:132` `What goods, order, or commercial arrangement does the $48,500.00 payment relate to, and can the customer provide supporting records?`; Requests commercial explanation/supporting records; does not assert the actual purpose. | Context only: `evidence:EV-G02-02 /source`; Context only: `evidence:EV-G02-02 /evidence_type`; Context only: `evidence:EV-G02-02 /facts/claim`; Context only: `evidence:EV-G02-02 /related_transaction_ids`; Context only: `verification_check:CHK-G02-01 /check_type`; Context only: `verification_check:CHK-G02-01 /status`; Context only: `verification_check:CHK-G02-01 /findings/0`; Context only: `verification_check:CHK-G02-01 /subject_evidence_ids` | No factual category proposed | No factual category proposed | No affirmative factual proposition beyond separately listed premises; no factual support category assigned. Empty citations are structurally permitted; semantic usefulness remains for review. |

### hosted `/unresolved_questions/1/statement`

Original statement (unchanged):

> What is the business relationship between the customer and CP-G02-01, and who is the underlying payer?

Submitted citations: None submitted.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H042 `0:102` `What is the business relationship between the customer and CP-G02-01, and who is the underlying payer?`; Requests business relationship and underlying payer clarification; does not assert that the recorded counterparty is absent. | Context only: `counterparty:CP-G02-01 /display_name`; Context only: `counterparty:CP-G02-01 /relationship_status` | No factual category proposed | No factual category proposed | No affirmative factual proposition beyond separately listed premises; no factual support category assigned. Empty citations are structurally permitted; semantic usefulness remains for review. Pending P03_PAYER_WORDING. |

### hosted `/unresolved_questions/2/statement`

Original statement (unchanged):

> Does the payment fit the customer's current business activity and profile?

Submitted citations: None submitted.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H043 `0:74` `Does the payment fit the customer's current business activity and profile?`; Asks whether activity fits the profile; does not assert that it fits or fails. | Context only: `customer:CUST-G02 /expected_monthly_activity/minimum`; Context only: `customer:CUST-G02 /expected_monthly_activity/currency`; Context only: `customer:CUST-G02 /expected_monthly_activity/maximum`; Context only: `customer:CUST-G02 /expected_monthly_activity/currency` | No factual category proposed | No factual category proposed | No affirmative factual proposition beyond separately listed premises; no factual support category assigned. Empty citations are structurally permitted; semantic usefulness remains for review. |

### hosted `/missing_information/0/statement`

Original statement (unchanged):

> No invoice, purchase order, or independent corroborating record is included in the supplied review materials, and the recorded check specifically notes their absence for the claimed purpose.

Submitted citations: `verification_check:CHK-G02-01`; `evidence:EV-G02-02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H044 `0:10` `No invoice`; No invoice is included in the supplied review materials. | `verification_check:CHK-G02-01 /check_type`; `verification_check:CHK-G02-01 /status`; `verification_check:CHK-G02-01 /findings/0`; `verification_check:CHK-G02-01 /subject_evidence_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. Input support uses the complete supplied snapshot. Whether a recorded check or selected record citations suffice for an inventory-absence claim requires P01/D-04 adjudication. Pending P04_ABSENCE_CITATIONS. |
| H045 `12:26` `purchase order`; No purchase order is included in the supplied review materials. | `verification_check:CHK-G02-01 /check_type`; `verification_check:CHK-G02-01 /status`; `verification_check:CHK-G02-01 /findings/0`; `verification_check:CHK-G02-01 /subject_evidence_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. Input support uses the complete supplied snapshot. Whether a recorded check or selected record citations suffice for an inventory-absence claim requires P01/D-04 adjudication. Pending P04_ABSENCE_CITATIONS. |
| H046 `31:63` `independent corroborating record`; No independent purpose-corroborating record is included in the supplied review materials. | `verification_check:CHK-G02-01 /check_type`; `verification_check:CHK-G02-01 /status`; `verification_check:CHK-G02-01 /findings/0`; `verification_check:CHK-G02-01 /subject_evidence_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. Input support uses the complete supplied snapshot. Whether a recorded check or selected record citations suffice for an inventory-absence claim requires P01/D-04 adjudication. Pending P04_ABSENCE_CITATIONS. |
| H047 `114:189` `the recorded check specifically notes their absence for the claimed purpose`; The supplied check records no such corroboration of the claimed purpose. | `verification_check:CHK-G02-01 /findings/0` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |

### hosted `/missing_information/1/statement`

Original statement (unchanged):

> The supplied review materials do not include further detail about the commercial relationship with CP-G02-01 or supporting records addressing the payment's purpose.

Submitted citations: None submitted.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| H048 `30:108` `do not include further detail about the commercial relationship with CP-G02-01`; No further commercial-relationship details with CP-G02-01 are supplied. | `counterparty:CP-G02-01 /relationship_status`; `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. No citations are submitted here. Contract allowance does not settle adequacy of a snapshot-absence assertion. Pending P04_ABSENCE_CITATIONS. |
| H049 `112:163` `supporting records addressing the payment's purpose`; No supporting records addressing the payment purpose are supplied. | `verification_check:CHK-G02-01 /check_type`; `verification_check:CHK-G02-01 /status`; `verification_check:CHK-G02-01 /findings/0`; `verification_check:CHK-G02-01 /subject_evidence_ids`; Alternative reading: `evidence:EV-G02-02 /source`; Alternative reading: `evidence:EV-G02-02 /evidence_type`; Alternative reading: `evidence:EV-G02-02 /facts/claim`; Alternative reading: `evidence:EV-G02-02 /related_transaction_ids`; `input:/evidence` complete snapshot (I09/I11) | `unassessable` | `unassessable` | If supporting records means corroborating commercial documents, the snapshot supports the absence. If it includes any purpose-addressing record, EV-G02-02 supplies a customer claim. Do not choose a reading silently. No citations are submitted. Ambiguous supporting-record scope requires adjudication. Pending P05_PURPOSE_WORDING. |

### baseline `/rationale/statement`

Original statement (unchanged):

> [BASE-01] Specific material questions remain in the supplied scope, identified below. No complete REF-01 conjunction was established by this limited detector. Recommend preliminary investigation for human review.

Submitted citations: `transaction:TX-G02-01`; `evidence:EV-G02-02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| B001 `10:66` `Specific material questions remain in the supplied scope`; The remaining questions are material. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `input:/evidence` complete snapshot (I09/I11) | `unassessable` | `unassessable` | Missing documents are observable; materiality remains a provisional rule interpretation. Submitted citations include those sources; other citations remain preserved. |
| B002 `68:84` `identified below`; The assessment lists the questions it refers to. | Implementation context: versioned baseline source identified in section 2 | `unassessable` | `unassessable` | Observable in candidate /unresolved_questions; outside input-record factual support alone. Input citations do not prove output navigation; scope for such process statements is pending. Pending P07_PROCESS_CLAIMS. |
| B003 `86:158` `No complete REF-01 conjunction was established by this limited detector.`; The implemented detector did not establish its REF-01 conjunction. | `input:/evidence` complete snapshot (I09/I11); Implementation context: versioned baseline source identified in section 2 | `unassessable` | `unassessable` | Input contains no register/instruction and reviewed code returns no referral. How to assess a detector-execution assertion separately from policy truth is pending. TX-G02-01 and EV-G02-02 alone do not establish code behavior or an entire scope inventory; do not infer that REF-01 is globally impossible. Pending P07_PROCESS_CLAIMS. |
| B004 `159:212` `Recommend preliminary investigation for human review.`; Recommends preliminary investigation and human review. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids` | No factual category proposed | `unassessable` | Action quality is not adjudicated. Submitted citations include those sources; other citations remain preserved. |

### baseline `/factual_findings/0/statement`

Original statement (unchanged):

> Transaction TX-G02-01 amount was USD 48,500.00.

Submitted citations: `transaction:TX-G02-01`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| B005 `33:46` `USD 48,500.00`; TX-G02-01 records USD 48,500.00. | `transaction:TX-G02-01 /amount`; `transaction:TX-G02-01 /currency` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |

### baseline `/factual_findings/1/statement`

Original statement (unchanged):

> [MI-02] Customer-supplied explanation EV-G02-02 records the claim 'Payment for wholesale goods'.

Submitted citations: `evidence:EV-G02-02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| B006 `8:47` `Customer-supplied explanation EV-G02-02`; EV-G02-02 is recorded as customer-supplied explanation. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| B007 `48:95` `records the claim 'Payment for wholesale goods'`; EV-G02-02 records the wholesale-goods purpose claim. | `evidence:EV-G02-02 /facts/claim` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |

### baseline `/factual_findings/2/statement`

Original statement (unchanged):

> Transaction TX-G02-02 amount was USD 1,200.00.

Submitted citations: `transaction:TX-G02-02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| B008 `33:45` `USD 1,200.00`; TX-G02-02 records USD 1,200.00. | `transaction:TX-G02-02 /amount`; `transaction:TX-G02-02 /currency` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |

### baseline `/interpretations/0/statement`

Original statement (unchanged):

> [BASE-01] This preliminary assessment applies limited fixed rules to supplied records. It performs no independent verification and establishes no fraud or fund tracing. Unreported issues are not certified absent. Human review is required.

Submitted citations: `case:CASE-G02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| B009 `38:85` `applies limited fixed rules to supplied records`; The baseline applies fixed rules to supplied records. | Implementation context: versioned baseline source identified in section 2 | `unassessable` | `unassessable` | This concerns implementation behavior or an epistemic limitation, not solely a fact in investigation records. Reviewed code provides context, but treatment in the input-support dimension remains pending. Only CASE-G02 is cited. A case identifier provides context but does not establish implementation behavior. No new output citation namespace is proposed. Pending P07_PROCESS_CLAIMS. |
| B010 `87:126` `It performs no independent verification`; The baseline performs no independent verification. | Implementation context: versioned baseline source identified in section 2 | `unassessable` | `unassessable` | This concerns implementation behavior or an epistemic limitation, not solely a fact in investigation records. Reviewed code provides context, but treatment in the input-support dimension remains pending. Only CASE-G02 is cited. A case identifier provides context but does not establish implementation behavior. No new output citation namespace is proposed. Pending P07_PROCESS_CLAIMS. |
| B011 `131:151` `establishes no fraud`; The baseline does not establish fraud. | Implementation context: versioned baseline source identified in section 2 | `unassessable` | `unassessable` | This concerns implementation behavior or an epistemic limitation, not solely a fact in investigation records. Reviewed code provides context, but treatment in the input-support dimension remains pending. Only CASE-G02 is cited. A case identifier provides context but does not establish implementation behavior. No new output citation namespace is proposed. Pending P07_PROCESS_CLAIMS. |
| B012 `155:167` `fund tracing`; The baseline does not establish fund tracing. | Implementation context: versioned baseline source identified in section 2 | `unassessable` | `unassessable` | This concerns implementation behavior or an epistemic limitation, not solely a fact in investigation records. Reviewed code provides context, but treatment in the input-support dimension remains pending. Only CASE-G02 is cited. A case identifier provides context but does not establish implementation behavior. No new output citation namespace is proposed. Pending P07_PROCESS_CLAIMS. |
| B013 `169:212` `Unreported issues are not certified absent.`; Unreported issues are not certified absent. | Implementation context: versioned baseline source identified in section 2 | `unassessable` | `unassessable` | This concerns implementation behavior or an epistemic limitation, not solely a fact in investigation records. Reviewed code provides context, but treatment in the input-support dimension remains pending. Only CASE-G02 is cited. A case identifier provides context but does not establish implementation behavior. No new output citation namespace is proposed. Pending P07_PROCESS_CLAIMS. |
| B014 `213:238` `Human review is required.`; Human review is required, not claimed completed. | Implementation context: versioned baseline source identified in section 2 | No factual category proposed | `unassessable` | The output flag and contract establish the requirement; this is not an input-record fact or proof review occurred. Case citation does not certify a review event. Treatment of contract-scope statements needs a common policy. Pending P07_PROCESS_CLAIMS. |

### baseline `/unresolved_questions/0/statement`

Original statement (unchanged):

> [MI-02] What document supports the customer explanation for TX-G02-01? No linked invoice, purchase order or dispatch record is supplied; this limited inventory check does not establish the claimed purpose.

Submitted citations: `transaction:TX-G02-01`; `evidence:EV-G02-02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| B015 `8:70` `What document supports the customer explanation for TX-G02-01?`; Requests support for the recorded customer explanation. | Context only: `evidence:EV-G02-02 /source`; Context only: `evidence:EV-G02-02 /evidence_type`; Context only: `evidence:EV-G02-02 /facts/claim`; Context only: `evidence:EV-G02-02 /related_transaction_ids` | No factual category proposed | No factual category proposed | Open request; no factual correctness category. Submitted transaction/explanation citations provide context. |
| B016 `35:69` `customer explanation for TX-G02-01`; A supplied customer explanation is linked to TX-G02-01. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| B017 `71:88` `No linked invoice`; No supplied supplier_invoice evidence is linked to TX-G02-01. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. Input support uses the complete supplied snapshot. Whether a recorded check or selected record citations suffice for an inventory-absence claim requires P01/D-04 adjudication. Pending P04_ABSENCE_CITATIONS. |
| B018 `90:104` `purchase order`; No supplied purchase_order evidence is linked to TX-G02-01. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. Input support uses the complete supplied snapshot. Whether a recorded check or selected record citations suffice for an inventory-absence claim requires P01/D-04 adjudication. Pending P04_ABSENCE_CITATIONS. |
| B019 `108:123` `dispatch record`; No supplied dispatch_record evidence is linked to TX-G02-01. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. Input support uses the complete supplied snapshot. Whether a recorded check or selected record citations suffice for an inventory-absence claim requires P01/D-04 adjudication. Pending P04_ABSENCE_CITATIONS. |
| B020 `137:204` `this limited inventory check does not establish the claimed purpose`; The limited inventory check does not establish actual purpose. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; Implementation context: versioned baseline source identified in section 2 | `unassessable` | `unassessable` | Consistent with limited missing-document detection; epistemic sufficiency is not adjudicated. The explanation/transaction give context; they do not independently certify the scope of software inference. Pending P06_EPISTEMIC_SCOPE. |

### baseline `/missing_information/0/statement`

Original statement (unchanged):

> [MI-02] What document supports the customer explanation for TX-G02-01? No linked invoice, purchase order or dispatch record is supplied; this limited inventory check does not establish the claimed purpose.

Submitted citations: `transaction:TX-G02-01`; `evidence:EV-G02-02`.

| Unit / span / exact excerpt and atomic proposition | Supporting fields and context | Proposed input support | Proposed citation adequacy | Review caveat |
| --- | --- | --- | --- | --- |
| B021 `8:70` `What document supports the customer explanation for TX-G02-01?`; Requests support for the recorded customer explanation. | Context only: `evidence:EV-G02-02 /source`; Context only: `evidence:EV-G02-02 /evidence_type`; Context only: `evidence:EV-G02-02 /facts/claim`; Context only: `evidence:EV-G02-02 /related_transaction_ids` | No factual category proposed | No factual category proposed | Open request; no factual correctness category. Submitted transaction/explanation citations provide context. |
| B022 `35:69` `customer explanation for TX-G02-01`; A supplied customer explanation is linked to TX-G02-01. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids` | `supported` | `adequate` | Recorded fields support this proposed reading; no authentication is inferred. Submitted citations include those sources; other citations remain preserved. |
| B023 `71:88` `No linked invoice`; No supplied supplier_invoice evidence is linked to TX-G02-01. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. Input support uses the complete supplied snapshot. Whether a recorded check or selected record citations suffice for an inventory-absence claim requires P01/D-04 adjudication. Pending P04_ABSENCE_CITATIONS. |
| B024 `90:104` `purchase order`; No supplied purchase_order evidence is linked to TX-G02-01. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. Input support uses the complete supplied snapshot. Whether a recorded check or selected record citations suffice for an inventory-absence claim requires P01/D-04 adjudication. Pending P04_ABSENCE_CITATIONS. |
| B025 `108:123` `dispatch record`; No supplied dispatch_record evidence is linked to TX-G02-01. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; `input:/evidence` complete snapshot (I09/I11) | `supported` | `unassessable` | Recorded fields support this proposed reading; no authentication is inferred. Input support uses the complete supplied snapshot. Whether a recorded check or selected record citations suffice for an inventory-absence claim requires P01/D-04 adjudication. Pending P04_ABSENCE_CITATIONS. |
| B026 `137:204` `this limited inventory check does not establish the claimed purpose`; The limited inventory check does not establish actual purpose. | `evidence:EV-G02-02 /source`; `evidence:EV-G02-02 /evidence_type`; `evidence:EV-G02-02 /facts/claim`; `evidence:EV-G02-02 /related_transaction_ids`; Implementation context: versioned baseline source identified in section 2 | `unassessable` | `unassessable` | Consistent with limited missing-document detection; epistemic sufficiency is not adjudicated. The explanation/transaction give context; they do not independently certify the scope of software inference. Pending P06_EPISTEMIC_SCOPE. |

Both candidates contain zero contradiction descriptions. This is a submitted-output fact, not a completeness judgment. Pending human review applies to this entire appendix.
