# G02 Seven-Bundle Hybrid Calibration Plan — DRAFT

**Project:** AML Alert Triage Agent

**Scope:** D-04 claim semantics and D-07 review design; case-level materiality only as a *proposal*.

**Status:** Engineering draft, not adjudicated ground truth.

**Approved direction:** hybrid evaluation (atomic assertions + whole-statement meaning + separate case-level review).
**Source:** read-only review of frozen G02 paired pilot; Codex's independent evaluation-design review on 29 October 2026.

## Why the earlier five examples changed

Codex independently reviewed actual G02 input, 21 candidate statement locations, 75 proposed review units, 203 typed source pointers and both candidate files. The two candidates' source/context requirements are different: the deterministic baseline implements limited fixed-rule logic including REF-01; the hosted candidate was not supplied the complete REF-01 policy rule. Comparing the systems as configured is possible; attributing differences to pure model reasoning is not.

The calibration shortlist is expanded to **seven bundles (38 registered review units)**. A bundle deliberately spans several units when the *interaction between claims* is the issue. These are **not 38 independent factual claims**, benchmark cases or approved evaluations.

## Review order and sources

| Rank | Bundle | Actual unit references | Main calibration risk |
|---:|---|---|---|
| 1 | C01: Absence vs corroboration | H044–H047 | Normalization of H047 could erase the distinction between documents absent and documents not corroborating purpose |
| 2 | C02: Numeric comparison / attribution | H003–H004, H031–H036 | H003/H032 spans contain `customer's stated`, while their normalized numeric propositions omit it; `materially` and caveat need separate treatment |
| 3 | C03: Ambiguous purpose support | H048–H049 | EV-G02-02 explains the *claimed* purpose without independently corroborating it |
| 4 | C04: Premises inside questions | H040–H041 | An interrogative sentence contains a verifiable payment-amount premise, even with permitted empty citations |
| 5 | C05: Process / implementation claims | B003, B009–B014 | Case-level evidence cannot establish source-code behavior or actual execution; `review required` differs from `review completed` |
| 6 | C06: Repetition and type scope | B015–B026 | Identical baseline text occurs twice; `invoice` is not necessarily identical to the baseline's `supplier_invoice` type recognition |
| 7 | C07: Counterparty relationship coverage | H024–H025, H042 and proposed inventory item M03 | The baseline's *omission* has no candidate annotation ID; case-level materiality remains to be adjudicated |

Every cited unit includes its frozen candidate, original statement, source pointer, exact Unicode span, candidate SHA-256 and submitted citations in `calibration_cases.draft.json`. The original G02 packet remains byte-identical.

## Rule hypotheses — for calibration, not approval

**H-00 — Annotation fidelity.** A normalized atomic proposition must not change the original sentence's negation, attribution, scope, modality, source, or certainty. Keep the original exact statement. When normalization resolves an ambiguity or omits a disputed qualifier, require human fidelity review before evaluating support. G02 anchors: H047 and H032.

**H-01 — Atomicity with whole-statement preservation.** Register separately verifiable propositions, questions, interpretations and non-case claims, but preserve their text context. A factual proposition can be supported even if the whole statement is potentially misleading. A question's requested information is not automatically an asserted fact.

**H-02 — Scoped absence vs corroboration vs ambiguity.** Differentiate `no record in the supplied snapshot`, `a recorded check says none corroborated`, and `no independent corroboration actually exists`. Define source-selection boundaries. If multiple materially plausible readings remain, record the alternatives and evidence for each rather than silently choosing the favorable reading.

**H-03 — Input support vs submitted citations.** Resolve two separate questions: (a) is the proposition supported somewhere in the input? (b) do the *submitted* citations support it? A numeric comparison may require a transaction and profile jointly. A missing submitted source cannot be repaired by silently borrowing another record from the full input. Citation-ID validity alone is not adequate support.

**H-04 — Proposition authority/applicability.** Distinguish transaction/customer input propositions, question premises, implementation descriptions, execution claims, contractual requirements and policy decisions. Use the corresponding authorities. The contract permits uncited questions, but factual premises may still require an evidence review; the exact semantic citation policy is pending.

**H-05 — Occurrences vs underlying issues.** Keep each original occurrence and its location. Link repeated occurrences without assuming they are independent factual opportunities or separate material findings. Never automatically apply both a statement penalty and an atomic penalty for the same issue. No penalty formula is approved.

**H-06 — Review provenance.** Proposal ≠ human review ≠ adjudication. Actual reviewer, competence scope, conflicts, reasons, disagreements and approval authority must be recorded. An AI-generated draft is never labeled expert-reviewed by inference; incomplete review is not a finding of `unassessable`.

**H-07 — Case-level coverage is a separate evaluation.** Derive potential material items from the input independently of candidate-specific assertions; adjudicate materiality before omission scoring. The absence of a baseline unit cannot be replaced with an invented unit ID. Report omissions, claim correctness and recommendation quality separately.

## Counterfactuals and technical test gates

The [calibration catalog](../../research/evaluation_calibration/calibration_cases.draft.json) stores each proposed counterfactual with the *one meaningful change*, what must stay fixed, the expected behavior and whether machine or human review is required. The archive supplied 26 executable tests for mechanical invariants, exact binding, duplication detection, structural citation membership, currency preconditions, review status safety and source integrity. Repository integration adds directory-adapter, artifact-identity, draft-state, offline-view and CLI safeguards; see the [research tool instructions](../../research/evaluation_calibration/README.md). **These tests do not execute semantic counterfactual entailment tests or certify any categorical verdict.** Those need approved human-labeled fixtures and separate authorized implementation.

### Priority review gates

1. **D-07 interim responsibility:** establish actual project reviewer/adjudicator role IDs and disclose limited synthetic-domain qualifications; do not imply independent AML validation. Drafting can proceed before role approval; releasing adjudicated labels cannot.
2. **Fidelity (H-00):** compare H047 and H032 original sentences side-by-side with normalized propositions; explicitly resolve potential meaning loss, not just text-offset validity.
3. **Absence and attribution (H-01/H-02):** adjudicate the original wording and its plausible readings. Test document-present-but-noncorroborating and profile-sourced-versus-personally-stated counterfactuals.
4. **Citation sets (H-03):** record source sets sufficient for each reviewed proposition, including conjunctions and alternatives; run citation-only perturbations holding evidence constant.
5. **Applicability (H-04):** determine who can substantiate implementation/contract claims and factual question premises; leave unresolved authorities explicitly open.
6. **Accounting (H-05/H-07):** link identical baseline text while retaining both occurrences; judge proposed M03 materiality before any counterparty-omission verdict.
7. **Calibration approval:** only after reviewer decisions, disagreement treatment and example counterfactual verdicts are documented, finalize category precedence and population denominators. No aggregate score or model ranking before then.

## Deliberately deferred to later datasets

G02 cannot alone calibrate conflicting authentic sources; certified verification; a genuine closure decision; an established referral condition; justified abstention; acceptable alternate dispositions; or held-out generalization. G01–G05 are exposed development examples and should never be relabeled as clean held-out data. The source inventory's M03 item is an *input-derived proposed material item*, not approved truth.

## Review outcome record

Use the [blank review worksheet](../../research/evaluation_calibration/blank_review_worksheet.json) or generate a local offline HTML worksheet. The following cannot be prefilled by the draft-generation tool: named human reviewer, adjudicator, final source sufficiency, meaning-preservation judgment, materiality, rule approval or scoring. Any reviewer decision must document evidence, alternative readings, unresolved disagreement and date/revision, then be independently checked against the original candidate and input.

**No original G02 candidate, reference answer, frozen annotation draft, AML contract, prompt, baseline logic or existing auditor is modified by this calibration package.**
