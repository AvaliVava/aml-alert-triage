# Week 4, Checkpoint 3A — G02 Live OpenAI Assessment: Evidence and Independent Desk Review

**Status:** First successful hosted-API smoke test documented; formal semantic evaluation **not yet performed**.

**Review date:** 2026-10-29

**Repository location:** `docs/week-4/G02_LIVE_ASSESSMENT_REVIEW.md`

**Scope:** One synthetic case (`CASE-G02`), one failed connection attempt followed by one separately authorized successful assessment, as reported by the owner. This is an inspectable *execution record*, not a model benchmark, approved semantic annotation, compliance determination, or claim of production readiness.

## 1. Objective and evidence hierarchy

The accepted Week 4 goal was to demonstrate that the guarded OpenAI Responses adapter can submit a valid synthetic `InvestigationInput`, receive a hosted model output, preserve the original candidate text, enforce the existing `InvestigationOutput` schema and reference checks, and record the mechanical auditor's result **without treating mechanical acceptance as factual accuracy**.

On 2026-10-29, this review inspected both original local JSON bundles, the repository's versioned G02 input, provisional G02 reference, fictional labeling policy, and existing draft evaluation protocol at Git revision `c6afb7149c0b0722e4638618ba41d2db8599e2ff`. Claims below distinguish *recorded execution evidence*, *manual record comparison*, *provisional reference agreement*, and *not evaluated*. This assistant's desk review is **not** a human AML subject-matter adjudication.

Relevant repository sources:

- [G02 input](../../data/golden_cases/inputs/G02.json) — authoritative synthetic input for record comparisons.
- [G02 reference](../../data/golden_cases/references/G02_reference.json) — **provisional** reference, for evaluation only; never supply to the candidate-generating model.
- [Fictional labeling policy](../../specs/labeling_policy_v1.json) — fictional evaluation rubric, not banking law.
- [Evaluation protocol](../phase-2/EVALUATION_PROTOCOL_DRAFT.md) — semantic scoring **draft**, not an approved evaluator.
- [Integration documentation](OPENAI_INTEGRATION.md) — adapter behavior and known boundaries.
- Local ignored artifacts, at repository-root paths: `outputs/openai/G02-live-attempt2-20261029-113851.json` (successful run) and `outputs/openai/G02-live-luna-20261029-111651.json` (failed run). Both exist locally; **neither is included in this documentation change**. Their absence from Git means a public checkout cannot independently inspect them.

The service implementation was merged in PR #11, `main` merge commit `c6afb7149c0b0722e4638618ba41d2db8599e2ff`. The report itself was prepared after the merge and is not evidence of an additional test run.

## 2. Run inventory: keep failed and successful attempts distinct

| Attempt | UTC start | Outcome | Local operation latency | Recorded usage | Evidence and uncertainty |
| --- | --- | --- | ---: | --- | --- |
| First authorized hosted attempt | 2026-10-29 08:16:55 | `failed` / `connection` | 11,464.831 ms | all null | `request_attempts=1`, retries `0`; assessment, candidate text and audit are null, with no request ID or usage returned. Server processing and billing **cannot be ruled out**. This is a failure record, **not** an AML abstention or model-quality outcome. Source: original local `G02-live-luna-20261029-111651.json` bundle. |
| Second, separately authorized hosted attempt | 2026-10-29 08:38:53 | `validated` — structural/reference/mechanical only | 10,905.025 ms | 1,491 input; 1,163 output; 2,654 total tokens | A candidate, audit and execution record were saved and inspected. Source: original local `G02-live-attempt2-20261029-113851.json` bundle. |

Each bundle records one request attempt, allowance `1` and zero SDK/application retries; the failure also records `retry_performed=false`. Separate authorization is owner-reported, not established by the bundles. Intervening connectivity diagnostics described in the earlier draft are not preserved in these artifacts and were not independently verified here. The cause of the first failure remains unknown. This checkpoint made no network requests or credential checks.

### Successful run: immutable recorded identifiers and configuration

| Field | Value |
| --- | --- |
| Case / alert | `CASE-G02` / `ALT-G02` |
| Model identifier **as recorded** | `gpt-6-luna` |
| SDK / service | `openai==3.40.0` / service `0.1.0` |
| Prompt | version `aml-preliminary-1.0` |
| Prompt instructions SHA-256 | `f6472c5d27337626e113cfa982297b0c6b317282eefc4a600f049fa025bb6c83` |
| Canonical validated input SHA-256 | `7f077f89d97f17fac644273d0a53c5b108b519d00adcddba0c21a9122f6a58da` |
| Original input *file bytes* SHA-256 | `60cbf66dbbb24b59f0ae0a86e03a92d6f0dac0e68511ec05cd1953b96763326f` |
| Exact candidate JSON UTF-8 SHA-256 | `c44c89e49dc82443b2a5af45e8b0bb249e35551298764706355061099c62e82b` |
| Successful bundle *file bytes* SHA-256 | `95e6cbd8053929c3aea6de5ba5c72c9e443352554e2ea3d0ead5d39b6567de9b` |
| Request ID | `req_37467712110b451c836d82dc4ada851b` |
| Settings | `store=False`; `reasoning_effort=none`; output cap `2400`; timeout `60s`; allowance `1`; SDK/application retries `0` |
| Response state | `validated`; `error=null`; one attempt recorded |
| Semantic evaluation state | `not_evaluated` |

**Integrity inspection performed for this review:** Both original bundles parsed as JSON. Recomputed the original G02 file-byte hash, canonical validated-input hash, current prompt version/instructions hash and exact candidate UTF-8 hash; all match the successful execution record and available audit digests. `json.loads(candidate_json)` equals the saved assessment and the validated output's JSON representation. Input/output Pydantic validation and contextual reference validation succeeded locally; all 17 submitted citation occurrences resolve. Re-running the existing auditor offline on the canonical input and original candidate reproduced the saved audit exactly. The failed bundle's file-byte SHA-256 is `b7471dbfacf7af9b21b92a95d80e07581b8a08aa43260a2fd83de107fc52c963`; it records the same model, settings, prompt and input identities. Both bundles were preserved unchanged.

These checks establish local artifact consistency and reproducible mechanical auditing, not factual correctness, a repeatable hosted response or a verified server-side trace. Latency and usage are recorded values, not independently remeasured or reconciled. The audit's `source_revision` is null; the Git revision above is the inspected checkout, not a captured execution revision or resolved hosted-model snapshot.

**Billing:** Token usage is a server-returned recorded value. The exact amount charged has **not** been independently reconciled with the API billing ledger; the first connection failure has no usage record. Do not present a precise experiment cost as a verified charge. Local token/call allowances are not an account-wide hard spending cap.

## 3. Mechanical acceptance and its limits

The successful bundle records:

| Component | Reported status | What the result establishes |
| --- | --- | --- |
| Input structure | `passed` | Input accepted by the existing contract. |
| Output structure | `passed` | Returned candidate accepted by the `InvestigationOutput` schema. |
| Contextual references | `passed` | Exact case/alert identities and cited typed IDs resolve. |
| Service `mechanical_checks` | `passed` | Existing auditor stages completed successfully. |
| Restricted deterministic transaction-amount check | **`not_evaluated`** | **0 of 6 findings** matched the checker's whole-statement grammar; no factual amounts were verified automatically by this check. |
| Nine broad semantic audit dimensions | **`not_evaluated`** | No claim-grounding, citation-adequacy, coverage, recommendation, abstention, scope-in-prose or dataset-independence score was produced. |

The factual-check coverage object reads `total_findings=6`, `checked=0`, `matches_record=0`, `conflicts_with_record=0`, `not_checked=6`. These zeros must **not** be interpreted as zero factual errors or six verified facts. A compound sentence containing a false amount could remain outside the current supported grammar. This is an **observed coverage limit**, not proof that the current checker violated its designed contract.

The existing contextual citation validator establishes **identity and existence**, not entailment or material relevance. `validated` must never be surfaced as synonymous with *factually verified*, *approved disposition*, or *AML compliant*.

## 4. Candidate recommendation and provenance-sensitive desk review

The model returned:

- `assessment_status="recommendation_provided"`
- `recommended_action="investigate"`
- `recommendation_scope="preliminary"`
- `human_review_required=true`
- `contradictions=[]`

Its reasoning was that the USD 48,500 incoming payment exceeds the profile's recorded USD 25,000 expected monthly maximum, while the customer's wholesale-goods explanation lacks corroboration according to a supplied unresolved commercial-purpose check. It expressly avoided treating the lack of corroboration as proof that the payment had no legitimate purpose. The *action label* agrees with the **provisional** `G02_reference.json` action `investigate`; this is **not** adjudicated accuracy.

### Six factual findings compared with the G02 source

| Finding path | Candidate claim, abridged | Submitted cited IDs | Desk-review observation |
| --- | --- | --- | --- |
| `factual_findings[0]` | Alert flags a USD 48,500 domestic credit on 2026-10-13 to `ACC-G02` with `CP-G02-01`. | `ALT-G02`, `TX-G02-01` | Agrees with alert `/transaction_ids` and transaction `/amount`, `/currency`, `/transaction_type`, `/direction`, `/account_id`, `/occurred_at`, `/counterparty_id`. `EV-G02-01` `/facts/recorded_amount` agrees numerically but is **not cited**; this is no independent authenticity check. |
| `factual_findings[1]` | Profile expects monthly USD 15,000–25,000. | `CUST-G02` | Agrees with `/expected_monthly_activity/minimum`, `/expected_monthly_activity/maximum` and `/expected_monthly_activity/currency`. The source does not explicitly establish who supplied the range; it is an expected profile range, not a payment limit. |
| `factual_findings[2]` | Customer explanation says wholesale goods; invoice reference absent. | `EV-G02-02` | Agrees with `/source`, `/facts/claim` and `/facts/invoice_reference` (null). Supports attribution of the claim to customer-supplied evidence, not independent proof of business purpose or global absence of an invoice. |
| `factual_findings[3]` | Supplied commercial-purpose check unresolved; corroborating invoice/PO/independent record not present. | `CHK-G02-01` | Agrees with `/check_type`, `/status` and `/findings/0` as a **recorded check conclusion**, not new verification by this software. Absence is bounded to supplied review scope. |
| `factual_findings[4]` | Orchid Distribution LLC is displayed for `CP-G02-01`; relationship unverified. | `CP-G02-01` | Agrees with `/display_name` and `/relationship_status`; does not authenticate the counterparty or its relationship. |
| `factual_findings[5]` | Additional USD 1,200 domestic credit from `CP-G02-02` dated 2026-10-14. | `TX-G02-02` | Agrees with `/amount`, `/currency`, `/transaction_type`, `/direction`, `/counterparty_id` and `/occurred_at`. "From" is a plausible description of the recorded credit/counterparty association; an authenticated ultimate payer identity is not established. |

**Review status of this table:** Preliminary assistant-performed comparison against the supplied synthetic input. No clear contradiction was found among these six written findings; **no independent AML subject-matter adjudication or claim-level approved annotation set exists**. More subtle attribution and evidence-sufficiency judgments remain provisional.

### Material wording and coverage observations

1. **Attribution nuance in the rationale and `interpretations[0]`:** Both say the "customer's stated maximum monthly activity." The input stores `expected_monthly_activity` in the **customer profile**, but does **not** explicitly establish that the customer personally stated the figures. USD 48,500 exceeds the profile's USD 25,000 expected monthly maximum numerically; this does not make the range a hard limit or prove wrongdoing. The provenance wording is stronger than the source supports. Flag for **human adjudication as a possible attribution overstatement**; no severity rubric is approved. Preserve the original assessment unchanged.
2. **Missing direct payment-evidence citation:** `EV-G02-01` is not cited in the answer's key flagged-payment finding, although `TX-G02-01` and `ALT-G02` do support it. The provisional reference points to `EV-G02-01`. This is a **candidate evidence-coverage difference**, not automatic citation invalidity: existing contracts do not require citing every available supporting record.
3. **Counterparty question:** The model asks who the "underlying payer" is, while the input already supplies `CP-G02-01` as the recorded counterparty and a display name. The underlying identity/relationship remains unverified; reviewers should ensure this question does not imply the recorded counterparty ID is missing.
4. **No contradictions listed:** This is **defensible**, not independently certified complete. An uncorroborated explanation is not necessarily contradicted by another record.
5. **Unresolved questions and missing information:** Questions about commercial documentation, sender relationship and profile fit align with the supplied check and provisional reference. The model appropriately limits document-absence claims to review materials.

## 5. Provisional reference alignment — not scoring

| Reference expectation | Observed response | Interpretation |
| --- | --- | --- |
| Expected action `investigate` | `investigate` | Agreement with **provisional** label. |
| Material USD 48,500 flagged incoming payment | Present | Observed claim supported by input; direct `EV-G02-01` citation absent. |
| Customer purpose uncorroborated | Present | Cites customer explanation and unresolved check. |
| Seek commercial records and establish sender relationship | Present as unresolved questions | Consistent with reference theme. |
| Human review required | `true` | Literal contract requirement met; **does not prove review actually occurred**. |

The draft evaluation protocol prohibits treating the current provisional reference set as approved ground truth. No action precision/recall, success rate, confusion matrix or held-out performance is justified by this single reviewed live case.

## 6. What was **not** established

- No automated general fact grounding or general prose entailment assessment. The restricted checker evaluated zero findings.
- No approved claim-level support/citation-adequacy annotation, material-finding inventory, recommendation rubric adjudication, or abstention eligibility decision.
- No independently authenticated customer identity, underlying payer, invoice, commercial purpose, payment-record provenance or actual AML/financial-crime outcome. Data are **synthetic**.
- No demonstrated semantic reliability across G01–G05, 50 development cases, counterfactuals, unseen cases, other models or repeated stochastic runs.
- No held-out independence proof: the code path is designed not to load golden answers into model inputs, but no full independent exposure/history audit was performed. This G02 case is an examined development smoke example, **not** a held-out evaluation sample.
- No measured benefit over the deterministic baseline; baseline output was **not** compared in this experiment.
- No confirmed exact billing charge, global spending cap or proof that the earlier failed request was not processed remotely.

## 7. Engineering disposition and next checkpoint

**Checkpoint 3A hosted smoke-test result: the saved successful execution demonstrates a hosted response accepted for structure, reference resolution, artifact capture and existing mechanical validation on one synthetic case.** Scope ends there. Retain the failed connection attempt as a separate operational result and don't reinterpret either result as model accuracy.

**Observed issue:** The live answer's prose falls outside the restricted amount-check grammar; the checker evaluated `0/6` findings. The potential attribution overstatement and uncited additional payment record are **review questions** rather than instructions to expand the validator or change its contract. The existing transaction/alert citations already support the flagged-payment observation; no universal requirement to cite the payment evidence is introduced.

**Proposed follow-up, requiring separate authorization:** A read-only evaluation scoping audit could compare the draft protocol, decisions, actual G02 artifact, input, provisional reference and deterministic baseline, and propose claim-level annotations and denominator definitions. Separate automatable exact-field checks from human adjudication; no LLM-as-judge, new model/provider, scoring weights, new action classes, reference-label changes or additional paid calls are approved here. Proposed changes must state objective, observed limitation, evidence, smallest options/tradeoffs, required human decisions and acceptance tests **before implementation**.

Do not commit the secret key or raw ignored runtime artifacts. For reproducibility, preserve the original local bundle, hashes, prompt version, model identifier, input snapshot identity and review decisions. If a sanitized/exported candidate artifact is later committed, review its disclosure, provenance and scope separately.

## 8. Independent verification checklist for incorporation into Git

- [x] Verified parseability of supplied successful bundle and consistency of candidate hash and candidate/assessment objects.
- [x] Compared all six factual findings with the repository's G02 synthetic input and identified source pointers.
- [x] Confirmed the recorded mechanical-auditor coverage is `0/6` and semantic dimensions are not evaluated.
- [x] Compared action and material themes **descriptively** with the provisional G02 reference.
- [x] Repository collaborator (Codex) checked both **local original artifacts**, recomputed available hashes and reproduced the saved audit offline at `c6afb71` on 2026-10-29.
- [x] Checked local source links and documentation consistency; no API requests, credentials access or unit-test run during this documentation-only checkpoint. The recorded 358-test baseline and existing CI coverage remain applicable to unchanged implementation files; remote CI results were not fetched or independently verified here.
- [ ] Owner reviews attribution nuance and provisional nature of the factual desk review.
- [ ] Any Git change to add this document, project status or worklog is examined, tested appropriately and separately approved before commit/merge.
- [ ] Any future formal evaluation rubric/semantic annotations are approved and versioned before reporting scores.
