# G02 reconciliation audit and reporting specification — v0.1 DRAFT

**Date:** 30 October 2026  
**Authority:** Project owner's approvals in this conversation; analytical consolidation by AI assistant. **No independent AML expert validation.**  
**Scope:** Frozen paired G02 development-case evaluation packet. **No source files, frozen JSON or GitHub records changed.**

## 1. Audit outcome

**No arithmetic or occurrence-membership inconsistency found in the approved decision sequence.** The frozen packet contains **75 unique atomic units**, attached to **21 unique original statement occurrences**; approved six unit groups partition all 75 exactly once. Frozen candidate statement strings, atomic spans, citation lists and annotated statement membership were checked programmatically. **Semantic judgments were not independently re-adjudicated by this mechanical check.**

- **Unit-level:** 75/75 have an approved disposition or explicit non-applicability. This is **not** 75/75 unqualified factual correctness or fully scored semantics.
- **Whole-statement:** 10 qualified factual-statement passes; 3 approved questions; 8 reviewed but not cleared for an unconditional support-and-citation pass; zero unreviewed original occurrences.
- **Case-level mandatory coverage:** hosted M01/M02/M03 = `covered/covered/covered`; baseline = `partly_covered/covered/omitted`. Contextual M04 and M05 are **excluded** from the three-item mandatory coverage population.
- **Case action:** synthetic owner-adjudicated preliminary `investigate`, **no approved alternatives**; REF-01 conjunction not established within supplied input. Original reference JSON remains `provisional` and unchanged.
- **Exposure limitation:** Source inventory author previously saw the candidate/reference/review. G02 is development calibration, **not independent held-out evidence**.

### Critical unresolved items

1. **H004/H034:** Stronger drafted claim that the customer *personally supplied* the monthly maximum is `not_established` with `inadequate` submitted citations; **original candidate wording is ambiguous and its fidelity/score eligibility remains pending**. The word-level ambiguity must not convert an annotation-invented claim into an automatic candidate error.
2. **M04:** Numerical profile comparison is recorded, but its **independent materiality** is unadjudicated. It is contextual, not a mandatory fourth coverage item. Monthly expected activity is not automatically a per-transfer limit.
3. **Process authorities:** B003 and B009–B014 have separately reviewed code/output/contract assessments; original case-record citations do not prove code behavior, execution or review completion. No independently certified runtime trace.
4. **Whole-statement citation gaps:** H044/H045 and B017–B019/B023–B025 cite records that cannot establish complete inventory absence; their approved `inadequate` judgments remain, while scoped factual support can still be `supported` using the complete frozen input. H046 remains `partial`.
5. **H049:** Narrow *no independent corroborating records* reading is supported; broad *no records at all address the purpose* reading is contradicted by the customer's explanation. Original wording remains ambiguous and not cleared.

### Exact approved mandatory-coverage matrix

| Item | Hosted | Baseline | In mandatory denominator? |
|---|---|---|---|
| M01 — Flagged incoming payment and amount | `covered` | `partly_covered` | Yes |
| M02 — Customer purpose and corroboration gap | `covered` | `covered` | Yes |
| M03 — Counterparty and unverified relationship | `covered` | `omitted` | Yes |
| M04 — Profile-range comparison | Contextual | Contextual/not discussed | **No**; materiality unresolved |
| M05 — Additional unflagged USD 1,200 credit | Contextual | Contextual | **No**; nonmandatory |

**Internal approved-count reconciliation:** hosted 3 fully covered / 3 applicable; baseline 1 fully covered / 3 applicable (with 1 partial and 1 omitted). These **are not overall model-quality rankings**, and should not be presented as held-out performance. A hypothetical rate must be labeled G02-only, exposed development case, owner-adjudicated.

## 2. Whole-statement reconciliation

| Candidate | Statement category | Qualified factual passes | Approved questions | Reviewed, not cleared |
|---|---|---:|---:|---:|
| Hosted | All 14 original occurrences | 7 | 3 | 4 |
| Baseline | All 7 original occurrences | 3 | 0 | 4 |
| **Total** | **21** | **10** | **3** | **8** |

Hosted qualified passes = `factual_findings[0–5]` plus `interpretations[1]`. Baseline qualified passes = `factual_findings[0–2]`. Hosted questions = `unresolved_questions[0–2]`. Other statements are reviewed **without unconditional support-and-citation passes**. This status classification is not a conventional binary accuracy denominator and must **not** be used as one.

## 3. Reporting specification (outside `InvestigationOutput`)

### 3.1 Required report blocks

1. **Artifact identity:** source-packet bytes digest; input, hosted, baseline canonical SHA-256; original candidate pointers and submitted citation lists; checkout revision; rubric/policy version.
2. **Execution stages:** `passed`, `failed`, `not_evaluated`, `error`, with concrete per-stage reasons, prerequisites and any missing attempts. Mechanical validation only establishes structural/typed identity validity.
3. **Review provenance:** owner-in-conversation approval, AI-proposed judgments, reviewer role, qualifications actually known, independent expert status (`not_performed`), original frozen annotation status (`DRAFT_NOT_APPROVED`), decision revision history.
4. **Atomic factual review:** applicability separate from category; exact original text location; atomic proposition and any fidelity discrepancy; support set and opposing source; `supported`, `partly_supported`, `contradicted`, `not_established`, `unassessable`; unreviewed never conflated with unassessable.
5. **Submitted citations:** structural existence separately from semantic sufficiency (`adequate`, `partial`, `inadequate`, `unassessable`); no automatically repaired citations from external evidence; empty, permitted citation lists tracked for traceability and excluded from citation sufficiency where appropriate.
6. **Whole-statement disposition:** `qualified_factual_pass`, `qualified_investigative_question`, or `reviewed_not_cleared_unconditional_pass`; recorded caveats, not just aggregated atomic labels.
7. **Material item coverage:** M01–M03 applicable once per candidate (`covered`, `partly_covered`, `omitted`, `misrepresented`, `unassessable` as needed); M04 contextual pending and M05 contextual nonmandatory. Repeated document requests produce **one** M02 issue, not two coverage credits.
8. **Action/rationale:** approved `investigate` reference decision with no approved alternative, policy version, rationale quality independent from action agreement; fictional preliminary scope; no final AML decision.
9. **Other dimensions:** unsupported certainty, contradictions, missing-information/question coverage, source-authority and process judgments, review-required versus completed, execution provenance and contamination/independence.
10. **Limitations:** G02 exposed, synthetic, N=1, no expert certification, no semantic implementation in frozen mechanical auditor, no claim of external generalization.

### 3.2 Rate calculation and gating rules

- **Atomic support rate:** `supported` over *reviewed, applicable, assessable, eligible atomic factual units*. `partly_supported`, `not_established`, `contradicted` count against the numerator but inside eligible denominator; `unassessable`, `not_reviewed`, explicit `not_applicable`, and fidelity-withheld H004/H034 **must be disclosed separately**, never silently dropped.
- **Citation adequacy rate:** `adequate` over *eligible, reviewed, assessable citation-sufficiency judgments*; `partial` and `inadequate` remain denominator members. Permitted empty citation lists, process authority routed to a separate dimension, review-unassessable and unreviewed categories are disclosed separately. Citation existence and citation sufficiency never conflated.
- **Mandatory item coverage:** fully `covered` items over adjudicated applicable mandatory items, counting each case-level issue once. Publish partial/omitted/misrepresented separately; do not convert contextual M04 or M05 into required findings.
- **Whole-statement reporting:** status category counts and original IDs, **not** raw count of atomic supported propositions as a proxy for whole-statement correctness.
- **Action agreement:** case-action comparison only against approved adjudicated action set, not mere provisional reference text; rationale and unsupported certainty assessed independently.
- **Zero denominator:** report no applicable rate, **not 100%**.
- **No weighted overall composite score** and no invented thresholds or model win claims.
- **No definitive scored report or automation claim** until separately authorized evaluator implementation, reviewed definition of denominator eligibility, and an actual verified execution. The JSON register contains approvals but **is not** a frozen output of a running semantic evaluator.

### 3.3 Minimum per-judgment record

`case_id`, source/candidate SHA, candidate, exact JSON pointer, original statement/span offsets, approved atomic proposition, `review_state`, `factual_applicability`, factual category, actual submitted citations, citation sufficiency/applicability, authority/support pointers, source conflict, whole-statement fidelity flag, material-item association, reviewer approval provenance, revision history, score eligibility/exclusion reason, explicit limitations.

### 3.4 Suggested test coverage for the subsequent *authorized* implementation

- All 75 units uniquely associated with their 21 frozen original statement occurrences, exact offsets and citation sets.
- H004/H034 drafted personal-attribution claim cannot become an unqualified candidate-level `not_established` score without original-text fidelity resolution.
- H047 check noncorroboration cannot be silently promoted into proof of physical document absence.
- H049 two readings remain distinguishable; EV-G02-02 is a counterexample to the broad zero-record claim.
- Baseline B015–B026 repeated MI-02 text remains two occurrences but a single M02 material-coverage item.
- Hosted and baseline M02 both `covered` while baseline linked-document citation gaps remain `inadequate`; don't double-penalize coverage.
- M04 stays out of mandatory denominator; M05 not mandatory.
- Code/contract assertions cannot be certified using case-only citations; required human review does not become completed review.
- Invalid inputs and mechanical failures do not become semantically unassessable, and zero denominator is not scored as 100%.
- Provenance and candidate bytes remain unchanged; independent expert/held-out flags remain false.

## 4. Release gate: short remaining action list

- **Now done (conversation):** All six unit batches (75 units), subsequent three correction groups, 21 whole-statement review outcomes, G02 action and M01–M03 coverage.
- **Still open (do not invent approval):** H004/H034 *original wording fidelity*; M04 independent materiality; formal register/report-schema owner release approval; separate Codex implementation and tests; external/held-out evaluation controls.
- **Practical next engineering step:** Review this draft register/spec as a single checkpoint, approve any justified corrections, then authorize scoped Codex work. Do not re-ask for the already approved units or whole statements.

## 5. Artifact notes

The accompanying `G02_Adjudication_Register_v0.1_DRAFT.json` records each of 75 original atomic units, exact candidate pointers, actual submitted citations, approval categories, separate whole-statement decisions, material coverage, source authority rules, corrections and pending gates. It is a **new working copy**, not an edit of the frozen `claim_annotations.draft.json`. The latter still has original AI-draft approval fields and cannot honestly be represented as updated by the in-conversation decisions.
