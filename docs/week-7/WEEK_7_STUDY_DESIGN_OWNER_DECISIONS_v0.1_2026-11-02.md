# Week 7 owner-approved study-design directions - v0.1

**Decision record:** W7-STUDY-DIRECTIONS-v0.1

**Preparation date:** November 2, 2026. This is not an asserted approval timestamp.

**Status:** Owner-approved methodological directions recorded locally; detailed study preparation, implementation, execution, scoring and evaluation release are not authorized.

## 1. Purpose and status

This record documents the project owner's subsequent approval of W7-S01 through
W7-S07, with the qualifications identified in the preceding Codex engineering
audit. It records accepted directions, not a complete executable study protocol.

The original [Week 7 methodology draft](WEEK_7_EVALUATION_ELIGIBILITY_AND_STUDY_DESIGN_v0.1_DRAFT.md)
remains a historical **DRAFT** proposal. This record approves only the directions
and safeguards stated below, not every detail, measurement, denominator or
recommendation in that draft. The general [evaluation protocol](../phase-2/EVALUATION_PROTOCOL_DRAFT.md)
also remains a draft subject to its accepted working rules and unresolved decisions.

The approval is for an as-configured comparison on eligible, separately controlled
synthetic families, with initial qualitative review of factual support,
submitted-citation adequacy and whole-statement fidelity/safety. It does not
establish a held-out population, approve a complete annotation guide, release
numerical scoring or authorize an experiment.

## 2. Checkpoint, approval provenance and scope

- **Checkpoint:** Week 7, Checkpoint 2 - versioned owner-approved study-design
  decision record.
- **Authority:** The project owner's conversation instruction titled
  "WEEK 7 - CHECKPOINT 2 VERSIONED OWNER-APPROVED STUDY DESIGN DECISION RECORD"
  explicitly directs recording the seven approvals and audit qualifications.
  Exact timestamps for the preceding conversation approvals were not supplied.
- **Audit provenance:** A preceding read-only Codex engineering review reported no
  substantive contradiction or reason to reverse the directions. This is
  assistant-supported technical review, not independent human or AML expert sign-off.
- **Verified starting checkout:** `docs/week-7-study-decisions` at
  `e45976de93374d9883f4be06ae706c633e7364ca`, the PR #21 merge. Local history shows
  the merged methodology document. No tracked changes or staged files existed;
  the existing G02 handoff ZIP was present and untracked.
- **Authorized repository write:** This one new decision document only. The owner
  retains Git integration and publication authority. Recording this document is
  not staging, committing, an evaluation release or external publication.

Conversation approval is recorded as supplied owner authority. This document does
not independently authenticate that conversation or invent an approval receipt.
Prior Week 5/6 decisions and historical authorization notices are preserved. The
subsequent approvals here establish a limited design scope, not a new live allowance.

The [roadmap](../../ROADMAP.md) still defines Week 7 as **"Held-out evaluation and
safety/failure analysis"**, with **"Reproducible quantitative report and limitations."**
The [charter](../../PROJECT_CHARTER.md) retains its evaluation aims, including
class-specific reporting and serious failure examples. These directions neither
waive those aims nor automatically satisfy Week 7 completion.

## 3. Relevant repository sources

| Source | Role and authority boundary |
| --- | --- |
| [Week 7 methodology draft](WEEK_7_EVALUATION_ELIGIBILITY_AND_STUDY_DESIGN_v0.1_DRAFT.md) | Merged PR #21 design basis; detailed proposals remain unapproved except for the subsequent directions recorded here. |
| [ROADMAP.md](../../ROADMAP.md), [PROJECT_CHARTER.md](../../PROJECT_CHARTER.md), [PROJECT_STATUS.md](../../PROJECT_STATUS.md), [DECISIONS.md](../../DECISIONS.md) | Original milestone scope, project limits and accepted engineering history. This task changes none of them. |
| [Evaluation protocol draft](../phase-2/EVALUATION_PROTOCOL_DRAFT.md) | Accepted mechanical boundaries and D-01-D-08 working directions; general semantic categories, scoring and held-out details remain controlled. |
| [Fictional policy](../../specs/labeling_policy_v1.json), [golden-case guidance](../../data/golden_cases/README.md), [development manifest](../../data/generated/development/manifest.json) | Synthetic rubric and exposed development lineage, not an approved new held-out population. |
| [G02 adjudication register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json) and [reconciliation specification](../phase-2/G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md) | Frozen case-specific judgments, source bindings, limitations and historical pending markers. |
| [P01 fidelity addendum](../phase-2/G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) and [P02 materiality addendum](../phase-2/G02_P02_MATERIALITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) | Subsequent owner-approved G02 rulings; preserved without reopening or generalizing them. |
| [G02 annotation draft](../week-4/G02_ANNOTATION_FORMAT_DRAFT.md), [calibration plan](../week-4/G02_SEVEN_BUNDLE_CALIBRATION_PLAN_DRAFT.md), [research utilities](../../research/evaluation_calibration/README.md), [G02 reconciler](../../research/evaluation_calibration/g02_reconciliation.py) | Existing hybrid review/integrity tools and non-scoring implementation; not a general semantic scoring release. |
| [Baseline assessment interface](../../src/aml_triage/deterministic_baseline.py), [hosted service](../../src/aml_triage/openai_service.py), [prompt builder](../../src/aml_triage/openai_prompt.py), [contracts](../../src/aml_triage/contracts.py) | Implemented input, assessment, serialization and contextual-validation boundaries; inspected without running a producer. |

## 4. Summary of approved directions

| ID | Approved direction | Not settled or authorized by that approval |
| --- | --- | --- |
| W7-S01 | Compare current systems as configured; initial factual-support, citation-adequacy and whole-statement review. | Action/abstention quality scoring, intrinsic model superiority or Week 7 completion. |
| W7-S02 | New separately controlled synthetic families, subject to evidenced eligibility and six safeguards. | Actual population, size, family criteria, assignments, partitions or operational chronology. |
| W7-S03 | Preserve current rules/instructions and shared frozen investigation data; exclude evaluation answers/feedback. | Equivalent-policy conditions, byte-identical prompts or complete provider-exposure knowledge. |
| W7-S04 | Bounded qualitative semantic framework with original-text fidelity and distinct review/applicability axes. | Complete operational annotation guide, P03 applicability/denominators or numerical semantic scoring. |
| W7-S05 | Owner-led synthetic adjudication with disclosed overlap, provenance and corrections. | Actual assignments, detailed procedures, invented reviewers or independent expert validation. |
| W7-S06 | Separate evidence preservation, review, adjudication, report release and stronger claims. | Automatic P04/P05 satisfaction or external publication. |
| W7-S07 | Separate bounded-experiment authorization; zero default execution rights and preserved available evidence. | Any new baseline/model experiment, evaluation execution, spending or reuse of consumed allowances. |

## 5. Detailed approved decisions

### W7-S01 - Initial research question

**APPROVED:** Compare the existing deterministic baseline and hosted assessment
system **as configured**, using identical prospectively frozen, eligible
investigation data while acknowledging their different implementation and policy
contexts. Initially examine factual support, submitted-citation adequacy and
whole-statement fidelity/safety. Recommendation and abstention outcomes remain
descriptive until corresponding quality rules are approved.

Disclose unequal REF-01 access, the baseline's limited rule coverage and inability
to recommend `close`, synthetic-data limitations and the absence of independent
AML expert validation. Differences cannot be attributed to intrinsic model quality
alone. Action agreement or disagreement does not identify a correct winner.

Retain paired case-level observations, failures, output scope and visible material
omissions. Fewer asserted or unsupported claims do not automatically establish
greater usefulness: a sparse assessment can omit important information. Keep that
limitation visible without silently approving a completeness score. The initial
study is not automatically sufficient for the full Week 7 milestone.

### W7-S02 - Evaluation population

**APPROVED:** Use new, separately controlled synthetic investigation families,
subject to documented held-out eligibility. The six approved safeguards are:

1. Family/template lineage isolation.
2. Prospective population and selection rules.
3. Source-first reference adjudication.
4. Frozen system identities and configurations.
5. Exposure, contamination and authorship records.
6. Qualified conclusions about the declared synthetic population.

Existing development families, renamed templates or new random-seed variants do
not automatically qualify as independently held-out. New storylines may share
answer-bearing recipes. Keep counterfactual siblings in the same partition and
record material ancestry; shared generic contracts and fictional policy do not
automatically make every family identical.

Actual family/lineage rules must be defined before authoring/selection. Distinguish
the development freeze, source/reference freeze and pre-dispatch identity
verification. The actual chronology and exposure handling remain pending; a late
hash check alone does not prove absence of earlier evaluation-informed adaptation.

No exact population, sample size, family criteria, assignments or partition is
approved here. No current development data is relabeled. Independence claims must
identify the demonstrated local development/exposure boundary and synthetic scope,
not assert independence from unknown provider pretraining exposure.

### W7-S03 - Policy access and leakage controls

**APPROVED:** Preserve current baseline rules and hosted instructions. The five
approved controls are:

1. No unapproved rule or prompt changes.
2. The same frozen investigation data for both systems.
3. Exclusion of reference answers, labels and evaluation feedback from generation
   context, including expected answers, adjudications and scoring metadata.
4. Records of actual observable generation exposure, versions and configuration
   identities.
5. Disclosure of policy-access and implementation asymmetry.

The baseline consumes a validated investigation model. The hosted path consumes
canonical serialized investigation data with developer instructions and the output
schema. Shared frozen **data** does not mean identical prompts or transport bytes.
Preserve original input-byte and canonical validated-input identities separately.

Legitimate investigation evidence can include supplied check conclusions. Do not
automatically call those records reference leakage; they may nevertheless provide
outcome cues and do not establish independent verification. Record controlled
context exposure without claiming complete provider-side knowledge. An equivalent-
policy study would require a separately approved treatment, not an implicit change
to this comparison.

### W7-S04 - Initial qualitative semantic review

**APPROVED:** A bounded qualitative framework for factual support, submitted-citation
adequacy and whole-statement meaning, fidelity and safety. Five safeguards apply:

1. Preserve original candidate wording and atomic spans.
2. Respect evidence authority and attribution.
3. Examine applicable assertions throughout the output.
4. Represent external process-authority claims separately pending applicability
   decisions.
5. Prevent misleading aggregation and duplicate penalties.

Retain the proposed factual-support vocabulary: `supported`, `partly_supported`,
`contradicted`, `not_established` and `unassessable`. Preserve separate axes:

| Axis | Distinction to preserve |
| --- | --- |
| Review status | An `unreviewed` item has no completed support judgment. |
| Applicability | `not_applicable` is not a factual-support outcome or an automatic pass. |
| Factual support | Reviewed support categories remain distinct, including partial support, contradiction and lack of establishment. |
| Submitted-citation adequacy | Assess the submitted sources separately from support found elsewhere in the input. |

Do not collapse these axes into one label list. Original whole-statement meaning
cannot be replaced by a stronger or more convenient normalized proposition.
Preserve citations, source identity, opposing evidence and statement context,
including factual premises in applicable questions or other output fields.

The qualitative framework is approved. A complete operational annotation guide,
general category applicability, precedence and denominator release are not approved.
Consistent working annotation rules are required before systematic use. P03 remains
open; no numerical semantic scoring is authorized. Whole-statement review and
material omissions remain visible without creating a completeness score or duplicate
atomic/statement penalties.

### W7-S05 - Reviewers and adjudication

**APPROVED:** Owner-led synthetic adjudication with disclosed role overlap and
limitations. The six approved safeguards are:

1. Source-first review.
2. Preservation of alternative interpretations and disagreements.
3. Preservation of original candidate wording.
4. Records of actual reviewer roles and overlap.
5. Treatment of AI suggestions as proposals, not human approval.
6. Versioning of later amendments and corrections.

Practical masking of system identity is optional. Do not claim blinding unless
verified; recognizable writing can reveal a producer even if its label is hidden.
Do not invent additional human reviewers, independent agreement, qualified AML
expert participation or completed adjudication records. Actual role assignments
and detailed reviewer procedures remain pending.

Source-first inventories are prepared before generation; candidate-specific
semantic judgments can be made only after an actual candidate exists. Source
author intent cannot supply facts absent from the records. Preserve uncertainty,
reviewer reasons and versioned corrections rather than silently rewriting evidence
or treating AI analysis as a second human review.

### W7-S06 - Artifacts, release and independence

**APPROVED:** Preserve evidence before separately approving judgments, reports and
stronger performance claims. The six safeguards are:

1. Immutable source/candidate/configuration identities.
2. Separation of original evidence from interpretations.
3. Versioned reviewer adjudication and amendments.
4. Distinct preservation and formal-release decisions.
5. Independence claims supported by actual lineage, exposure and reviewer evidence.
6. Separate authorization for external publication.

Preserve these five distinctions; none automatically promotes an artifact to the
next level:

| State or claim | Meaning and boundary |
| --- | --- |
| Evidence preserved | Available original evidence and identities retained; not a judgment of truth or approval. |
| Review draft | Proposed interpretations/judgments, with unresolved matters and provenance. |
| Adjudicated review | Actual authorized review decisions recorded, with scope, limitations and amendment history. |
| Approved evaluation report | An explicit report/release decision, separate from preserving inputs or approving individual judgments. |
| Qualified independent performance claim | Requires evidence for the stated independence and applicable evaluation/release requirements; not inferred from report existence. |

A hash establishes identity, not factual truth, approval or reviewer independence.
Preserve raw and canonical identities, original outputs, configurations, evidence
pointers and actual reviewer decisions. Preserve accessible original candidate text
exactly and label its digest basis. Explicitly record unavailable original evidence;
do not reconstruct missing originals from parsed representations. No provider
receipt or immutable provider behavior is inferred from a configured model name.

P04 remains a separate formal release gate. P05 eligibility must be established
for the actual population and claims. Owner-led synthetic evaluation is not
independent human AML expert validation.

### W7-S07 - Execution governance

**APPROVED:** Each bounded evaluation experiment requires separate owner
authorization. Seven safeguards apply:

1. Zero default execution authorization.
2. A specific experiment plan and frozen identities.
3. Explicit request, retry and monetary ceilings.
4. Identified operator and approval authority.
5. Stop conditions and incident preservation.
6. Actual available attempt, usage and receipt records.
7. Separation of exploratory work from released held-out evaluation evidence.

Current rights are **zero new baseline experiments, zero hosted requests, zero new
spending authorization and zero new evaluation execution**. Historical request
allowances remain consumed and cannot be reused. No cases, models or request
settings receive an execution release through these design directions.

The hosted service's request allowance and disabled automatic SDK retries do not
constitute a persistent provider-enforced billing ceiling. Financial ceilings are
administrative unless technical enforcement is demonstrated. Baseline zero
authorization is a governance decision, not a universal existing CLI guard.

Provider usage, request IDs, receipts and billing information can be absent or
uncertain. Preserve actual available records and unknowns; do not invent complete
provider receipts, guaranteed hard caps or zero-cost conclusions. Request reservation,
an observed SDK attempt, an available output and provider billing are different
observations. The future plan must specify stop conditions and permitted attempts;
no retry, fallback or replacement is authorized by this record.

## 6. Audit qualifications and methodological safeguards

The owner's instruction incorporates these findings from the preceding review:

1. **Claim-volume bias:** Fewer asserted claims can produce misleading apparent
   factual accuracy while important case information is omitted. Preserve paired
   case context, failures, output scope and omissions; do not infer usefulness from
   supported-claim counts alone.
2. **Independence is evidenced:** New family labels are insufficient. Actual
   ancestry, exposure and freeze chronology must support eligibility. Correlated
   siblings and repeated assertions are not independent samples.
3. **Data identity differs from transport identity:** Shared validated source data
   does not imply identical system prompts. Keep raw and canonical digest labels
   distinct; never normalize original evidence to make an expected hash match.
4. **Qualitative consistency precedes systematic review:** Approving the framework
   does not approve every working category rule or an operational guide. Keep
   numerical release gated by P03 and authority-dependent claims separately visible.
5. **Controls have operational limits:** Request allowances and administrative
   spending ceilings do not guarantee provider billing caps or complete receipts.

These are qualifications of the approved directions, not new experimental results.
No observed candidate is regenerated or relabeled. Preserve the distinction between
source-first inventories and later candidate-specific judgments, and between a
technical validation pass and substantive factual support. No general semantic
evaluator or independent expert review is claimed.

## 7. Remaining decisions and dependencies

| Pending matter | Required before the affected activity |
| --- | --- |
| Population envelope, sample-size justification, actual families, family criteria, lineage rules, selection, authors and partitions | Approve the applicable plan before new authoring/selection. No new held-out population is established by this record. |
| Development freeze, source/reference freeze, exposure handling and pre-dispatch verification chronology | Define actual events, ownership and order before claiming held-out eligibility; a dispatch-time checksum is not retrospective proof of an earlier freeze. |
| Working annotation guide: units, fidelity, support/adequacy distinctions, ambiguity, process authority and disagreement handling | Approve a bounded consistent guide and authorize work before systematic annotation. This need not settle every future numerical denominator. |
| Actual reviewers, source preparers, operators, adjudicator/release roles and overlap | Record real assignments and access before their respective work/release; do not fill missing metadata by assumption. |
| P03 applicability, denominators, process-domain representation and explicit scoring permission | Before corresponding numerical semantic reporting; qualitative-framework approval alone is insufficient. |
| P04 formal versioned adjudication/report release and actual P05 independence evidence | Before the corresponding release or stronger claims. External publication requires separate permission. |
| Specific experiment plan, exact cases/configurations, request/retry/monetary ceilings, operator, authority, stop conditions and evidence destinations | Separate release before any new baseline or hosted experiment or evaluation execution. All current rights remain zero. |
| Recommendation/abstention quality, applicable case actions and alternatives, and eventual Week 7 completion evidence | Separately resolve relevant rules and acceptance evidence. Descriptive actions do not approve quality scoring or close the milestone. |

Applicable planning can be scoped without resolving every future evaluation
decision at once. Source-first factual review does not require approval of all
action-quality metrics. Conversely, resolving G02 P03 would not itself establish
new family independence or authorize execution. Any parallel future work needs
its own approval and must keep held-out feedback out of development/tuning.

## 8. Prior decisions and release gates remain preserved

### P01 and P02

- **P01:** Preserve the [approved fidelity ruling](../phase-2/G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md).
  Do not automatically transfer the stronger drafted personal-authorship proposition
  into a candidate-level factual-error judgment. The original wording remains
  qualified; existing draft-proposition judgments and adjudication history remain.
- **P02:** Preserve the [approved materiality ruling](../phase-2/G02_P02_MATERIALITY_DECISION_ADDENDUM_v0.1_2026-11-01.md).
  G02 M04 remains contextual/nonmandatory for the frozen case, not inherently or
  universally immaterial. M01-M03 remain mandatory and M05 contextual. No universal
  monthly-versus-transaction threshold, automatic disposition or unconditional
  whole-statement pass is created.

No G02 unit judgment, candidate, citation, reference, source packet or historical
report is changed. The original register's pending markers remain historical;
the later addenda are not erased or resubmitted for approval.

### P03, P04 and P05

| Gate | Existing register description and preserved boundary |
| --- | --- |
| P03 | "Sign off final report category applicability/denominators and external process-domain representation." These remain unresolved; numerical semantic scoring and denominator release remain unauthorized. |
| P04 | "Codex implementation approval and versioned repository adjudication release." Existing non-scoring G02 reconciliation implementation is already present. Formal versioned adjudication/report release is separate; this decision record is not that release. |
| P05 | "Independent held-out data and expert review." Actual held-out family eligibility and qualified independent AML expert validation are different claims. Neither follows automatically from these approvals. |

The [register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json)
retains its historical `CONSOLIDATED_DRAFT_NOT_REPOSITORY_RELEASE` status and
`not_performed` independent AML expert review. Recording design approvals does
not populate missing review metadata or change reconciliation behavior.

### D-01 through D-08

Preserve the [existing working directions](../phase-2/EVALUATION_PROTOCOL_DRAFT.md)
and applicable unresolved requirements:

- **D-01:** Concern-specific corroboration and explicit source reliance; consistency
  is not authenticity. No closure-quality judgment is silently approved.
- **D-02:** Literal REF-01; no invented bypass prerequisite or senior-review
  exception, and same supplier account is distinct from same counterparty.
- **D-03:** Specific material unanswered questions, with case answerability distinct
  from candidate inability; recommendation/abstention quality remains separately gated.
- **D-04:** Separate existence, support, adequacy, completeness, conflict and review
  state. The qualitative framework here does not approve numerical categories or rates.
- **D-05:** Version acceptable alternatives consistently; no favored-candidate
  exceptions or silent reference-label changes.
- **D-06:** Keep reference answers separate and audit actual observable context,
  tools, retrieval, history and feedback. Preserve current unequal policy access.
- **D-07:** Owner-led synthetic adjudication with actual roles and disclosed limits;
  intended facts absent from supplied records are not evidence.
- **D-08:** Distinguish random draws, new templates/combinations and independent
  authorship; isolate related families and qualify generalization claims.

This record does not silently supersede those rules, close the general protocol
or reopen settled G02 decisions.

## 9. Current authorization ledger

This is a record of present permissions, not an experiment plan, request ledger
or provider receipt. Methodological approval is separate from execution rights.

| Activity | Current authorization from this record/instruction |
| --- | --- |
| Create this one local Markdown decision record | Authorized documentation task only. |
| New baseline experiments | **ZERO** |
| Hosted requests or model calls | **ZERO** |
| New monetary spending | **ZERO** |
| New evaluation execution | **ZERO** |
| New dataset creation or candidate generation | Not authorized. |
| New systematic annotation or scoring artifacts | Not authorized. |
| Numerical semantic scoring/denominator release | Not authorized; P03 remains open. |
| Retry, fallback or replacement invocation | Not authorized. |
| Formal adjudication/report release or external publication | Not authorized; applicable gates and separate permission remain. |
| Git staging, committing, pushing, merging or branch changes | Not authorized; owner controls Git operations. |

All historical request allowances remain consumed. No earlier authorization is
reopened, transferred or reset. No execution is implied by preparing this record.

## 10. What this record does not approve

- Every proposal in the merged methodology draft or the full evaluation protocol.
- An actual held-out dataset, sample size, family assignment or independence result.
- A complete annotation guide, final category applicability/precedence, numerical
  denominators, weighted quality score, model ranking or performance threshold.
- New case/reference adjudications, modified golden labels or repaired citations.
- Equivalent-policy conditions, prompt changes, baseline extensions, model/configuration
  selection for a future run, new dependencies or architecture.
- Baseline/hosted experiments, tests, new evaluation execution, API calls, spending
  or credential access under this documentation task.
- Complete provider-side exposure knowledge, billing receipts, guaranteed monetary
  caps, independently verified real-world facts or independent AML expert validation.
- Full Week 7 completion, a new milestone transition or Week 8 release work.

The present record adds no evidence that fewer unsupported claims mean greater
usefulness, that a valid citation supports a proposition, or that technical
validation establishes semantic correctness.

## 11. Next bounded checkpoint and completion criteria

First, the owner and supervising assistant review this complete document for
faithfulness before deciding on selective Git integration. No Git action is
performed or authorized for Codex by this record.

**Proposed next substantive checkpoint, requiring separate authorization:** a
prospective population-eligibility and freeze-plan specification. It would define
family/lineage eligibility, selection and partition controls, actual responsibilities
and the distinct freeze/exposure events before any dataset authoring or execution.
It would not generate investigations, candidates, annotations or scores.

Proposed completion criteria for that later planning checkpoint are:

1. A bounded population envelope and documented family/lineage criteria, with
   related variants grouped and known development ancestry treated explicitly.
2. Prospective selection/partition rules and a sample-size justification process,
   without claiming eligibility solely from new IDs, seeds or storylines.
3. Named responsibilities, recorded role overlap, exposure/contamination handling
   and explicit development/source-reference/dispatch verification chronology.
4. Clear dependencies on the still-pending annotation guide, applicable P03/P04/P05
   decisions and separate experiment execution approval.
5. Preserved historical evidence and zero execution/spending rights until released
   under a specific later authorization.

These criteria are a proposal, not authorization to start that checkpoint. The
current task ends with creation and verification of this one decision record.
**STOP for owner review.**
