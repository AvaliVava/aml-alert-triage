# G02 claim annotation format - DRAFT 0.1

**DRAFT / NOT AN APPROVED ANNOTATION STANDARD OR IMPLEMENTED CONTRACT.**

This documents the evaluation-only JSON prepared for the [paired pilot](G02_PAIRED_EVALUATION_PILOT_DRAFT.md). It does not modify investigation contracts or the G04 annotation schema, introduce an evaluator, or approve D-01 through D-08.

## 1. Packet and identity

The local packet is under `outputs/evaluation/g02-paired-pilot-20261029/`. The proposed claim-review format identifier is `g02_claim_review_draft_0.1`.

| Field | Proposed meaning |
| --- | --- |
| format_version, status, case_id | Version, DRAFT_NOT_APPROVED marker and investigation identity. |
| input_file_sha256 | Digest of original G02 file bytes. Field pointers resolve against this snapshot. |
| source_inventory_sha256 | Digest of the inventory frozen before paired annotation. |
| candidate_hashes | Exact hosted candidate UTF-8 and deterministic baseline file-byte digests. |
| author | Codex AI engineering assistant; no independent AML expertise or human approval implied. |
| statements | Registry of every prose location with exact statement, submitted citations and unit IDs. |
| units | Proposed factual/attributive/numeric units, questions, interpretations, process claims and scope limitations. |
| contradiction_description_inventory | Counts/descriptions actually submitted, with completeness explicitly unadjudicated. |
| disagreement_log | Human reviews, disagreements, adjudicator and rationale; currently empty/unassigned. |
| pending_owner_questions, decision_status | Specific unresolved readings and D-01 through D-08 status. |
| scores, performance_ranking | Null; neither is computed by this pilot. |

Original-file and canonical validated-input digests are distinct. JSON reformatting changes byte identity even when meaning is unchanged. Case ID or unchanged statement text cannot substitute for the candidate/input digests.

## 2. Proposed review unit

| Field | Proposed meaning and limit |
| --- | --- |
| unit_id, candidate_id, candidate_sha256 | Unique unit and exact frozen candidate binding. |
| location.json_pointer | Exact path to the decoded candidate statement string. |
| location.start, end, exact_text | Zero-based Unicode code-point offsets; end exclusive; slicing must equal exact_text. |
| location.exact_statement, statement_sha256 | Full unchanged statement and SHA-256 of its decoded text encoded as UTF-8. |
| atomic_proposition, kind | AI-authored normalized proposition and role. These are review proposals, never a rewrite of the candidate. |
| supporting_input | Typed record ID, record-relative JSON Pointer and observed value supporting the proposed reading. These are consulted fields, not approved minimal citation sets. |
| context_input | Relevant fields that do not establish the proposition, such as profile bounds without personal-source attribution. |
| opposing_or_alternative_reading_input | Possible counterevidence or records relevant to an explicitly retained alternative reading. Presence does not automatically mean a source conflict. |
| input_scope_evidence | Original input-root pointer and complete snapshot used for scoped absence claims; no global absence is asserted. |
| submitted_citations | Exact containing-statement citation list, copied without trimming, deduplication or inheritance. |
| proposed_judgments | Separate factual_support and submitted_citation_adequacy categories, each with a reason. |
| review_state, human_review_status, approval_status | AI draft_proposal or pending_adjudication; human_review_status is not_reviewed and all approval is pending. |
| human_reviewers, adjudication | Actual human reviews and rationale only; empty/null now. |
| pending_decisions, issue_group | Applicable decision IDs and shared issue linkage; repeated occurrences do not become independent case findings. |
| source_conflict | Separate draft observation; uncertainty is not silently resolved. |
| derivation | Explicit arithmetic, date or selection assumptions where applicable. |
| implementation_context | Evaluation-side code revision/hash for process statements; not a new candidate citation namespace. |

A monetary value is treated as currency plus amount. Profile bounds are separate propositions. An attributive component may overlap a numeric-clause span: support for the number does not approve the attribution. Granularity requires owner review before any denominator is defined.

## 3. Proposed category vocabulary and applicability

Factual support follows the draft protocol vocabulary: `supported`, `partly_supported`, `contradicted`, `not_established` and `unassessable`. Submitted-citation adequacy uses `adequate`, `partial`, `inadequate` and `unassessable` as a proposal.

These values are AI proposals, not approved judgments. A draft supported value means proposed support within supplied synthetic records, not authenticity or real-world truth. Not established does not mean proven false.

A proposed unassessable value must name the unresolved interpretation/source rule. It must not stand in for unreviewed. Human-review absence is recorded separately for every unit. Null means no factual category proposed for a question, recommendation or contract requirement; it is not an automatic pass or an approved metric exclusion.

Open questions do not assert their requested answers. Embedded factual premises are listed separately. Empty question citations remain structurally permitted; semantic requirements for such premises are pending.

Reporting a recorded check conclusion differs from independently establishing its underlying conclusion. Scoped inventory absence differs from global nonexistence. Case-only citations may anchor context without proving implementation claims; owner adjudication is required, without changing output contracts.

## 4. Concrete example: proposed profile-attribution review

The following is a real draft unit from the frozen hosted candidate. It is an annotation example, not an accepted verdict or a new validator.

```json
{
  "adjudication": null,
  "approval_status": "pending_project_owner_review",
  "atomic_proposition": "The customer personally stated the profile maximum.",
  "candidate_id": "hosted",
  "candidate_sha256": "c44c89e49dc82443b2a5af45e8b0bb249e35551298764706355061099c62e82b",
  "case_id": "CASE-G02",
  "context_input": [
    {
      "field_pointer": "/expected_monthly_activity/maximum",
      "observed_value": "25000.00",
      "record_id": "CUST-G02",
      "record_type": "customer"
    },
    {
      "field_pointer": "/expected_monthly_activity/currency",
      "observed_value": "USD",
      "record_id": "CUST-G02",
      "record_type": "customer"
    }
  ],
  "derivation": null,
  "human_reviewers": [],
  "input_file_sha256": "60cbf66dbbb24b59f0ae0a86e03a92d6f0dac0e68511ec05cd1953b96763326f",
  "input_scope_evidence": [],
  "issue_group": "P01_PROFILE_ATTRIBUTION",
  "kind": "attribution_claim",
  "location": {
    "end": 127,
    "exact_statement": "Further investigation is warranted because the recorded incoming payment exceeds the customer's stated maximum monthly activity, while the customer-supplied commercial-purpose explanation is not corroborated by the recorded check. The supplied information does not establish that the payment lacks a legitimate purpose.",
    "exact_text": "customer's stated maximum monthly activity",
    "json_pointer": "/rationale/statement",
    "offset_unit": "Unicode code points; zero-based; end exclusive",
    "start": 85,
    "statement_sha256": "040e49076c640b54c6137c56c3983b0689ede5741eccf7e6812de713bccc7a6f"
  },
  "opposing_or_alternative_reading_input": [],
  "pending_decisions": [
    "D-04",
    "D-07"
  ],
  "proposed_judgments": {
    "factual_support": {
      "category": "not_established",
      "reason": "The profile gives a maximum but does not identify its personal speaker/source. This does not prove the attribution false outside the snapshot."
    },
    "submitted_citation_adequacy": {
      "category": "inadequate",
      "reason": "CUST-G02 supplies the range, not the claimed personal attribution; none of the submitted citations establishes it."
    }
  },
  "review_state": "draft_proposal",
  "source_conflict": "No direct source-value conflict identified in this draft; wording ambiguity is recorded separately.",
  "submitted_citations": [
    {
      "record_id": "TX-G02-01",
      "record_type": "transaction"
    },
    {
      "record_id": "CUST-G02",
      "record_type": "customer"
    },
    {
      "record_id": "EV-G02-02",
      "record_type": "evidence"
    },
    {
      "record_id": "CHK-G02-01",
      "record_type": "verification_check"
    }
  ],
  "supporting_input": [],
  "unit_id": "H004",
  "human_review_status": "not_reviewed"
}
```

## 5. Integrity and human-review procedure proposal

1. Verify input/candidate digests and declared serialization bases.
2. Resolve each statement pointer, check the text hash, and verify every exact span.
3. Copy citations from the containing statement; do not use support elsewhere to silently repair submitted citations.
4. Resolve typed input records and field pointers; inspect observed values and scope snapshots.
5. Independently review normalized propositions, source attribution, alternative readings, citation sufficiency and materiality.
6. Record real reviewer roles/qualifications, proposed judgments, disagreements and the adjudicator's actual rationale.
7. Preserve unresolved decisions rather than filling in approval or converting missing review into a score.
8. Release annotations for any later metrics only after owner approval of categories, support sets, applicability and denominators.

Hash binding prevents stale accidental reuse; it does not certify honest authorship, correct decomposition or semantic judgments. Do not let candidates produce their own evaluation annotations.

## 6. Separation and non-goals

These records stay outside InvestigationInput and InvestigationOutput. They are not model input, reference replacements, finalized labels or a policy interpreter. The existing G04 checker accepts only its own unreviewed development schema; this draft is not passed into it.

No loader/scorer implementation, LLM judge, automatic semantic extraction, weighted score, threshold, new dependency or additional hosted request is introduced. Source, reference and candidate artifacts remain frozen. The [protocol decision register](../phase-2/EVALUATION_PROTOCOL_DRAFT.md#9-decision-register--working-directions-and-remaining-adjudication) governs pending approvals.

This pilot records no human disagreement because no human reviews have yet been supplied. That is not a finding of agreement. The next step is independent review of this format and the paired pilot.
