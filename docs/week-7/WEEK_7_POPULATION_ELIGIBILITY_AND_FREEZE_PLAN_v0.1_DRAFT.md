# Week 7 prospective population eligibility and freeze plan - v0.1 DRAFT

**DRAFT - NOT APPROVED AS AN OPERATIONAL POPULATION RELEASE.**

Only preparation of this document is authorized. No population authoring, case
selection, source/reference adjudication, systematic annotation, implementation,
baseline/hosted assessment, numerical semantic scoring or spending is authorized.
No freeze event, eligible new family, participant assignment or experiment is
established by this plan.

Prepared November 2, 2026, on `research/week-7-population-freeze-plan`, starting at
`0879d1a81320df2c28b7c7ff41db0c64efa52f78`. Preparation date is not an asserted
owner-approval timestamp. The owner performs Git operations; this task stages,
commits and publishes nothing.

## 1. Purpose and authority

The [roadmap](../../ROADMAP.md) defines Week 7 as **"Held-out evaluation and
safety/failure analysis"**, with **"Reproducible quantitative report and limitations."**
The [charter](../../PROJECT_CHARTER.md) retains its evaluation and human-review
boundaries, including class-specific reporting and serious error analysis. This
planning slice does not complete Week 7 or waive later acceptance evidence.

The [owner decision record](WEEK_7_STUDY_DESIGN_OWNER_DECISIONS_v0.1_2026-11-02.md),
merged through PR #22, approves W7-S01-W7-S07: an as-configured comparison, eligible
new synthetic families, controlled context, qualitative semantic review, owner-led
adjudication, separate preservation/release and zero default execution rights.
Those directions remain unchanged. The original
[methodology draft](WEEK_7_EVALUATION_ELIGIBILITY_AND_STUDY_DESIGN_v0.1_DRAFT.md)
and [general protocol](../phase-2/EVALUATION_PROTOCOL_DRAFT.md) retain their draft
and approval limitations. [Status](../../PROJECT_STATUS.md) and
[decisions](../../DECISIONS.md) preserve earlier milestone and authorization history;
later narrow planning permissions do not grant experiment execution.

Checkpoint 3A was a read-only engineering audit reported in conversation, not a
new repository report file. Its material findings were checked against the actual
generator, manifest, fixtures, tests and exposure records referenced below. This
document turns those findings into options and proposed procedures; it creates
neither a dataset nor a competing evaluation protocol.

**Status legend used throughout:**

- **Approved principle:** already accepted in W7-S01-W7-S07 or the applicable
  existing decision. It is not being resubmitted for approval.
- **Verified capability/fact:** observed in current files or code; static test
  inspection is not a fresh passing-test result.
- **Proposed control/recommendation:** operational choice requiring owner approval.
- **PENDING:** unresolved choice or release gate, not implied authorization.
- **Blocked activity:** cannot proceed until its particular requirements and
  permission are established; this does not block unrelated authorized planning.

Except for explicitly identified existing facts and approved principles, the
operational requirements below are proposals. Every decision in section 13 is
**PENDING**. The present authorization is one Markdown file only.

## 2. Existing development population and lineage

### 2.1 Verified generator and manifest facts

The inspected [generator](../../src/aml_triage/synthetic_generator.py) exposes
`generate_development_batch(seed, count)` as keyword arguments and
`write_development_batch(output_dir, seed, count)`. Its versions are generator
`1.0.0` and template `1.0`. The actual Python signature and keyword-only behavior
remain as implemented; this notation does not introduce a new interface.

The [development manifest](../../data/generated/development/manifest.json) records
seed `20261027`, partition `development`, 50 cases, ten per family and 18
family/condition combinations. Read-only checks for this document found no
original-byte hash or case-ID mismatches across those 50 files. Its current
original-byte SHA-256 is
`6b4342f3a98c6426723f22ee2f5816540dc8f0bd0bd2e166fbde09a23c38bfb9`.
These are existing development counts, not proposed evaluation quantities.

| Existing family | Existing source-condition variants | Recorded conceptual golden ancestry |
| --- | --- | --- |
| `incoming_transfer` | `invoice_and_dispatch`, `invoice_only`, `explanation_only` | [G02 input](../../data/golden_cases/inputs/G02.json) |
| `cash_sales` | `complete_sales`, `partial_sales`, `no_sales_records` | [G01 input](../../data/golden_cases/inputs/G01.json), [G04 input](../../data/golden_cases/inputs/G04.json) |
| `supplier_authorization` | `before_instruction`, `after_instruction`, `authorized_change`, `split_timing`, `different_accounts_same_supplier` | [G03 input](../../data/golden_cases/inputs/G03.json) |
| `incomplete_outgoing` | `missing_account`, `missing_purpose`, `missing_both`, `partial_reply` | [G05 input](../../data/golden_cases/inputs/G05.json) |
| `beneficiary_comparison` | `equal_references`, `different_references`, `invoice_reference_absent` | [G04 input](../../data/golden_cases/inputs/G04.json) |

The manifest declares shared templates, no independent authorship, no runtime use
of reference answers and no adjudicated labels. Each entry records case/family IDs,
template version, source condition, input path and raw hash. It is bookkeeping,
not generation input for the assessment systems. The five separate golden
[reference files](../../data/golden_cases/references/) remain marked provisional;
later G02 decisions have separate provenance and do not finalize the other labels.

### 2.2 Shared construction and seed effects

The generator assigns families in a fixed round-robin sequence. Seeded starting
offsets and cycling choose predefined conditions. A local random generator varies
amounts, currencies, dates and some contextual details. It does not invent new
family mechanisms or policy definitions.

The shared `_Case` helper inserts profile defaults, account/context records and
common source conventions. Incoming document amounts are copied from the payment;
cash reconciliation is computed from generated deposits; supplier variants change
REF-01-related timing/account/change facts; other builders alter missing fields
or account-reference equality. Source agreement can therefore be constructed from
one recipe. It is not independent real-world corroboration.

All generated cases use `POLICY-AML-V1`; common profile amounts are template data,
not universal materiality thresholds. Generated evidence/check statuses are
`recorded`, not verification newly performed by the program. JSON is serialized
with sorted keys, indentation, UTF-8, decimal-string money and an LF terminator.
Byte reproduction depends on the same implementation/template/configuration and
compatible serialization/runtime behavior; a seed alone is not the full identity.

The [tests](../../tests/test_synthetic_generator.py) cover deterministic bytes,
different-seed condition/date changes, coherent references, manifest lineage,
absence of reserved answer fields, and non-overwriting publication. They were
inspected, not run. Runtime reference separation does not prove that authors never
saw references during development.

### 2.3 Inferences and historical exposure limits

**Supported inference:** new IDs, amounts, dates, seeds or output directories still
exercise known recipes. They cannot alone justify unseen-family eligibility.
Combining exposed recipes also retains relevant ancestry; a new family name does
not settle the materiality of that sharing.

The current generator always produces development artifacts and offers no
approved new-family or held-out-partition configuration. Do not relabel its output
or reuse its publisher as though it accepted arbitrary new source families.

Historical local-only evidence includes
`outputs/evaluation/g02-paired-pilot-20261029/source_inventory.draft.json`, which
discloses prior input/candidate/reference/review exposure, and
`outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/04-controls-and-interpretation-limits.json`,
which records known development exposure and application-context limits. These
paths identify ignored evidence, not repository-accessible links. The G02 original
inventory is not blinded or held-out; its initial draft state is distinct from
later owner adjudications. Week 5 remains historical operational evidence.

No complete author/provider exposure history or new-population independence is
established. This plan does not infer contamination of hypothetical future cases.

## 3. Proposed population envelope

**Approved boundaries:** synthetic investigations, current as-configured systems,
unchanged input/output contracts and unequal REF-01 access. Initial review covers
factual support, submitted-citation adequacy and whole-statement safety. Actions
and abstention remain descriptive.

| Candidate envelope | Benefit | Risk/tradeoff | Recommendation status |
| --- | --- | --- | --- |
| Contract-compatible, separately controlled new families within the current fictional AML scope, with source-bounded factual/citation/safety review | Advances the approved initial question without requiring new rules or a general policy-quality evaluator. | Novelty still needs evidence; limited baseline coverage and author overlap constrain interpretation. | Recommended initial envelope; PENDING. |
| A narrower policy-predicate-focused population within the same contracts | Easier to document the relevant supplied policy facts and fixed-rule coverage. | Can overemphasize known REF-01 constructions or favor baseline coverage; is not automatically a new-family population or equivalent-policy study. | Alternative requiring a justified question/eligibility assessment. |
| A broader mixed-mechanism population, still within current contracts and fictional policy | Could expose wider source ambiguity and safety issues. | More authoring/review work and policy/materiality dependencies; combinations can inherit exposed ancestry. No representativeness guarantee. | Defer unless scope and capacity justify it. |

Independently authored sources could strengthen authorial separation for any
envelope, but no independent author is assumed. They would still require lineage,
exposure and adjudication evidence. That is an authorship choice, not automatic
proof of a distinct population.

**Proposed initial envelope:** supplied fictional records that support a traceable
review within current `InvestigationInput` semantics and `POLICY-AML-V1` context,
including valid incomplete and contradictory information. Require identified
record sources, explicit attribution and bounded observations. Do not require all
questions to be resolved or invent hidden facts to make a case answerable.

A **case** is one versioned investigation snapshot with its case/alert identities
and exact supplied records. A **family** is a reviewed grouping by material source
construction and evidence-dependency mechanism, not simply industry, alert name,
case ID or expected action. Variants and counterfactual siblings are subordinate
relationships; a family may have ancestry connecting it to other groups.

An eligible case may contain nulls, missing documents, competing sources or
unresolved claims. It need not have an approved action label for the initial
descriptive action table. Pure structural negative fixtures, if ever desired, must
have a separately declared safety-test scope, not be counted as ordinary labeled
investigations. No such new fixtures are selected here.

Potential conclusions concern only the frozen synthetic population, review rules
and audited local exposure boundary. They do not establish real-world AML
effectiveness, criminal intent, regulatory compliance, source authenticity,
intrinsic model superiority or complete provider training independence.

## 4. Proposed operational family eligibility

This is a review procedure proposal, not an automated novelty test or an approved
decision on any actual new family.

### 4.1 Eligibility evidence

Require a family dossier identifying the proposed mechanism, supplied source roles,
what relationships make its questions assessable, all known ancestors, reused
helpers/recipes, construction aids and author exposure. Compare it explicitly with
the existing five families and any other proposed related group. Explain substantive
differences; do not rely only on a narrative of novelty.

| Sharing or construction | Proposed interpretation |
| --- | --- |
| Generic schemas, JSON serialization, identifier conventions or the authorized fictional policy | Permissible common infrastructure in principle; record versions. Sharing alone does not make all families identical. |
| Renamed entities, paraphrases, changed currency/date/amount, shuffled records or renamed fields | Insufficient alone for a new-family claim. May be useful robustness/development variation under another declared question. |
| Reused answer-bearing mechanism or source-construction recipe | Material ancestry requiring grouping/review; do not classify as independent just because prose differs. |
| Counterfactual siblings | Keep within the same related group/partition; document the changed condition and dependent records. |
| Combinations of exposed mechanisms | Retain all parents. Combination novelty does not automatically erase material development ancestry. Uncertain materiality goes to quarantine, not an automatic pass. |
| Independently constructed source relationships | Potential evidence for a new family, conditional on the other controls; independent authorship is neither required by assumption nor sufficient by itself. |
| Known author/developer familiarity | Record what was known and whether it influenced source construction or system changes. Familiarity is not automatically runtime leakage, but limits claims and may establish material ancestry. |
| Unknown/unverifiable ancestry or missing exposure records | Preserve uncertainty and quarantine the claimed eligibility until reviewed; do not label absence of a record as clean exposure. |

The dossier should show whether the claimed distinction changes the material
evidence dependencies or uncertainty problem rather than reproducing the old
answer-bearing structure. No universal similarity threshold or automatic family
score is proposed. The actual criteria and boundary examples need owner approval
before authoring/selection.

### 4.2 Proposed dispositions

- **Eligible under specified controls:** documented population fit, sufficiently
  justified family distinction, grouping/partition compliance, appropriate freeze
  and observable exposure evidence. Name the exact local development boundary and
  remaining limitations; do not claim universal independence.
- **Ineligible for an unseen-family claim:** demonstrated material development
  ancestry or conflicting exposure/tuning history defeats that particular claim.
  Preserve the dossier and reason; the material may remain development/exploratory
  evidence if separately authorized, not silently become a replacement held-out case.
- **Quarantined pending evidence or review:** unresolved lineage, exposure, identity
  or release requirements. No held-out result is attributed while the relevant
  claim remains unresolved. Approval authority decides later disposition.

Eligibility is claim- and version-specific. No impossible proof of total absence
from hosted-provider pretraining is required. Record that information as unavailable
and limit conclusions to demonstrable controls.

## 5. Prospective lineage records and related-case grouping

**Proposed record contract, not an implemented schema:** use a small versioned
manifest and review ledger, with immutable references to source artifacts.

| Record group | Proposed content |
| --- | --- |
| Identity/version | Plan/population version; case ID; proposed family ID; template/construction version; related-group ID; source paths and raw hashes. |
| Parentage | Source/template/example ancestors and versions; explicit relation kind; counterfactual parent; shared construction recipe; generic-only sharing distinguished from material sharing. |
| Source conditions | Descriptive condition/variation, known unknowns and intended scope; never treat construction metadata as an approved outcome label. |
| Authoring provenance | Actual author/preparer role ID, tools/aids and versions, permitted context and known exposure to inputs, references, outputs or failure analyses. |
| Partition and eligibility | Proposed/released partition; rationale; related-group membership; eligible/ineligible/quarantined disposition, limitations and actual reviewer/authority. |
| Freeze/access events | Development/source/reference/population release identifiers; observed creation/exposure times where known; references to approvals and incident amendments. |
| Representation identities | Separate original-byte SHA-256 and canonical validated-input UTF-8 SHA-256 when later available; contract/canonicalization identity and exact digest labels. |
| Review history | Original proposal, actual decisions, opposing interpretations, approval provenance, revisions and links to superseded versions. Unknowns stay explicit. |

Existing manifest field names remain unchanged in historical files. A new record
format would need its own version and approval; these proposed fields are not
added to `InvestigationInput` or model prompts. Before authoring, only planned
metadata may exist; do not populate hashes or approvals for nonexistent artifacts.

**Grouping options:**

- Flat family labels are easy to maintain but can hide shared ancestors.
- Explicit parent edges plus a related-group register reveal siblings and material
  connections, at a modest manual review cost.
- A graph database/service could automate larger genealogies but is unnecessary
  for the current bounded task.

**Recommendation, PENDING:** document parent edges and keep the connected group
of material relationships in one partition. Generic schema/policy sharing alone
does not create a material edge. If an asserted connection is unresolved, preserve
it as uncertain and quarantine affected eligibility rather than splitting groups
to obtain more apparently independent families. Review the grouping rule before
any partition release; no groups are assigned here.

## 6. Prospective selection and partitions

The actual roster and partition are not chosen by this plan. Proposed sequence:

1. Approve envelope, eligibility/grouping rules, selection strategy, authoring
   limits and exposure responsibilities before creating new source material.
2. After separate authorization, record every proposed family/case and its dossier,
   including rejected or quarantined proposals. Apply source/lineage checks without
   seeing new candidate outputs.
3. Apply the approved grouping and inclusion/exclusion rules. Confirm input
   structure and source/reference identities under separately authorized preparation.
4. Freeze the eligible roster and selection rationale before generation. Keep
   evaluation metadata/references separate from producer input.
5. Release population/partition identities through an explicit owner decision;
   dispatch remains separately gated.

| Selection rule question | Proposed treatment |
| --- | --- |
| Inclusion | Declared envelope, approved source structure, documented lineage/grouping, required provenance and eligibility. No requirement that a particular system recommend an action. |
| Exclusion | Out-of-envelope or structurally unsuitable material, or established ineligibility for the stated claim; retain reasons and versions. |
| Quarantine | Unresolved lineage, identity, approval or exposure; no silent promotion into the eligible roster. |
| Difficult/ambiguous evidence | Retain when valid and within scope. Distinguish case eligibility from assessability of individual propositions. Do not exclude solely to improve outcomes or create apparently clear labels. |
| Baseline predicate coverage | Record/disclose limited coverage; do not remove cases because the frozen baseline lacks a rule or abstains. |
| Rejected proposals | Preserve intake ID, reason, authority and relationships. No discretionary replacement after candidate inspection. |
| Contamination after selection | Hold the affected claim/release, append an incident and preserve all actual attempts. Any amended roster or replacement requires a new prospective decision. |

**Alternatives:** review a complete bounded eligible roster, or use prespecified
family-level sampling from a documented eligible frame. The former is transparent
for a small reviewable roster; the latter can control workload but needs a justified
selection mechanism, probabilities where relevant and an audit trail. Handpicking
after outputs is neither option.

**Recommendation, PENDING:** use a complete, prospectively bounded eligible roster
if the justified review capacity permits. If it does not, approve a reproducible
family-level selection rule before generation, with related variants grouped and
any condition strata documented. No rule, seed, quantity or actual case is selected
here. Neither approach implies representative sampling from real AML alerts.

## 7. Sample-size justification process

No target count, class quota, deadline, statistical power or promised precision is
assigned. The owner must first decide whether the initial study is descriptive
failure analysis or supports a particular inferential question.

Proposed justification steps:

1. State the measurement scope and eligible population/frame, distinguishing
   family-level variation, case-level outcomes, reviewed statements and atomic claims.
2. Describe meaningful family diversity and within-family conditions. More variants
   of one recipe are not equivalent to more independent families.
3. Estimate actual preparation/adjudication capacity and review burden, with the
   basis disclosed. Use development-only calibration where authorized, not held-out
   candidate performance to choose a favorable size.
4. Specify how quarantine, unreviewed text, unassessable propositions, failures and
   missing outputs will be retained and disclosed. Do not invent an exclusion rate.
5. For descriptive work, justify the finite scope and show case/family coverage,
   conditional review coverage and concrete limitations. Avoid extrapolating prevalence.
6. For inference, first establish a sampling frame/process, target estimand,
   dependence assumptions, desired uncertainty and a justified analysis method.
   Only then assess size needs; related cases/claims cannot be treated as independent
   observations merely to narrow uncertainty.

Additional evidence needed to justify a number includes feasible distinct-family
availability, source-condition scope, review-time evidence, uncertainty/exclusion
handling and later execution-resource limits. Class-specific metrics additionally
need approved actions/alternatives and meaningful class denominators; construction
metadata cannot supply them. P03 and explicit scoring permission remain gates.
Small synthetic samples may support useful bounded descriptions without supporting
confidence, significance, model ranking or generalization claims.

## 8. Proposed prospective freeze chronology

**No freeze event has occurred under this plan.** Stages below are proposed events,
not reports of execution. Role labels are responsibilities, not assigned people.

### 8.1 Preferred default and alternatives

For overlapping author/developer roles, recommend freezing the measured candidate
systems and configuration specification **before new source authoring**. This
reduces opportunities for evaluation-informed system adaptation and is simpler to
explain than retrospective separation. The owner must choose actual identities,
configuration and chronology; this draft chooses no model or settings for a run.

An alternative is separate source preparation while system development continues,
with an auditable access barrier and system freeze before developer/operator
exposure. It can permit parallel work, but actual separation must be evidenced;
role overlap or informal discussions can defeat it. A third alternative, freezing
only at dispatch after shared source exposure, offers weaker assurance and cannot
by itself establish the proposed unseen-family claim. Do not silently substitute
it for the approved independence direction.

Preserve both a repository revision and the measured component identities. Future
data/documentation commits need not constitute a producer change if every frozen
component remains unchanged and allowed differences are recorded. Conversely, a
new HEAD or identical version string alone cannot certify component equivalence.
Track actual source-byte and Git representation bases without normalizing original
evidence. A provider model identifier does not prove immutable provider weights.

### 8.2 Stage F1 - development-system freeze

- **Purpose:** establish the system/configuration evaluated before the declared
  exposure boundary, without making a request.
- **Required evidence:** producer source revision and relevant component hashes;
  baseline rules; prompt version/exact instructions hash; schemas/contracts;
  auditor/composer identities; dependency/runtime specification; intended model
  and settings specification; actual known developer exposure and freeze approval.
- **Responsible roles:** system custodian/preparer and owner release authority,
  with overlap disclosed.
- **Gate:** approved chronology, identities, roles and authoring plan; no execution
  or spending follows from a technical freeze.
- **May change:** separately versioned source-authoring material and permitted
  documentation/metadata, with changes listed outside frozen producer components.
- **Immutable for the claim:** selected measured components/configuration and
  declared exposure boundary; necessary changes require a new version/decision.
- **Invalidating/qualifying exposure:** evaluation-informed system tuning or
  undisclosed source/reference feedback across the boundary. Record and hold the
  affected claim; a later checksum cannot establish earlier non-exposure.

### 8.3 Stage F2 - source/reference preparation and freeze

- **Purpose:** prepare traceable source records and reference inventories before
  seeing newly generated candidates.
- **Required evidence:** separately authorized source artifacts, input validation,
  original-byte and canonical identities, family dossiers/parentage, source authority
  and uncertainty inventory, applicable reference decisions, unresolved items,
  actual reviewer/approval provenance and construction-tool versions.
- **Responsible roles:** source preparer, lineage reviewer and source-first
  adjudicator. Owner-led overlap is allowed only as actually disclosed.
- **Gate:** authoring permission and a bounded source/reference review procedure;
  adjudication permission is distinct from permission merely to author records.
- **May change:** draft source/reference versions before freeze through recorded
  corrections, with all relevant lineage/exposure updated.
- **Immutable after freeze:** released source bytes, identities and reference
  versions. A new correction creates a superseding version, not a silent rewrite.
- **Invalidating/qualifying exposure:** candidate feedback used to tailor source
  facts, expected judgments or source sufficiency. Hidden author intent is not
  evidence. Candidate-specific atoms/judgments are not invented at this stage.

Initial reference scope may describe source facts, attribution, known unknowns and
approved derivations without an action-quality label. If actions remain descriptive,
do not silently approve new reference actions or treat provisional labels as truth.
Material-item expectations require actual case review, not a universal threshold.

### 8.4 Stage F3 - population eligibility and partition release

- **Purpose:** decide which versioned material is eligible for the stated local
  held-out claim and freeze the prospective roster/grouping.
- **Required evidence:** family dossiers, material parent edges, dispositions,
  frozen source/reference bindings, selection/partition rationale, rejected and
  quarantined intake history, exposure register and actual eligibility decisions.
- **Responsible roles:** eligibility/lineage reviewer and owner release authority.
- **Gate:** explicit population/partition release, including scope and limitations;
  this is not a provider request authorization, report release or external publication.
- **May change:** supplementary procedural records that do not alter the released
  roster, evidence or claim; substantive amendments require a new release.
- **Immutable:** released population manifest, group assignments, source/reference
  versions and selection rationale.
- **Invalidating/qualifying exposure:** material development ancestry concealed by
  labels, ungrouped siblings or outcome-driven inclusion. Quarantine/hold affected
  claims and preserve the original release record.

### 8.5 Stage F4 - pre-dispatch identity verification

- **Purpose:** confirm the specific proposed run matches the released artifacts
  and separately approved experiment plan.
- **Required evidence:** actual checkout and permitted differences; frozen component,
  instruction/schema/runtime identities; selected raw/canonical input bindings;
  available provider/configuration information; operator, request/retry and monetary
  authorization; stop rules; unused non-overwriting destination and write-ahead intent.
- **Responsible roles:** offline preparer/reviewer, named operator and owner authority.
  Preserve owner-operated hosted execution unless separately changed.
- **Gate:** explicit bounded baseline/hosted execution release. All rights remain
  zero until that later release; no model support or pricing is verified here.
- **May change:** verified procedural observations such as record-creation time;
  configuration changes need approval and consistency with the earlier freeze.
- **Immutable:** approved command/settings, input and component identities, approved
  allowances and stop conditions for the invocation.
- **Invalidating/qualifying exposure:** unexpected messages/tools/history, identity
  mismatch, absent authorization or unresolved publication. Hold dispatch; do not
  silently normalize evidence, change settings or inspect credentials in this task.

F4 proves current agreement with a prior release, not that exposure never occurred
before F1/F3. A hard provider billing ceiling is not established by local allowances.

### 8.6 Stage F5 - separately authorized generation and post-run review

- **Purpose:** observe the released systems and preserve outcomes before reviewing
  candidate-specific factual support, citations and whole statements.
- **Required evidence:** actual attempted invocation and available execution record;
  original accessible candidate text/hash; parsed-output consistency and mechanical
  diagnostics; request/usage/latency where supplied; terminal observations only when
  actually observed; candidate-bound review proposals and actual adjudication records.
- **Responsible roles:** authorized operator, evidence preparer and candidate reviewer.
- **Gate:** the specific execution release and separately authorized review scope.
  A successful response does not authorize another request or numerical scoring.
- **May change:** append-only diagnostics/review records and explicit unresolved
  interpretations; AI suggestions do not become owner decisions automatically.
- **Immutable:** source/reference release, original candidate/bundle bytes and
  observed failures. Keep raw and canonical audit representations correctly bound.
- **Invalidating/qualifying exposure:** previous candidates, references or reviewer
  feedback entering another generation context; adaptive retries or favored-result
  selection. Preserve every actual attempt and hold the affected independence claim.

Failures/refusals/incompleteness are not valid assessment abstentions. Missing or
unpublished output and uncertain billing remain explicit; no replacement call is
inferred. Unavailable original text is recorded as unavailable, never reconstructed
from a parsed model and presented as original.

### 8.7 Stage F6 - revisions, incidents and later release

- **Purpose:** correct records transparently and decide which claims remain justified.
- **Required evidence:** incident ID, affected artifacts/versions/units, original and
  proposed disposition, source pointers, exposure impact, dissent, authority and
  superseding manifest/report references when actually approved.
- **Responsible roles:** relevant reviewer/adjudicator and owner release authority.
- **Gate:** explicit amendment and applicable P03/P04/P05/report/publication decisions;
  new execution always needs its own authorization.
- **May change:** new versioned interpretations, exclusion explanations or future
  systems outside the original frozen evaluation. Do not overwrite original results.
- **Immutable:** original evidence, approvals, attempts and prior judgment versions.
- **Invalidating/qualifying exposure:** fixes informed by held-out outcomes consume
  that feedback for subsequent use. Reuse must be disclosed as exploratory/exposed
  or justified under a newly approved design, not silently called independent again.

An error correction is not permission to repair a candidate or improve both cases
and results retrospectively. Apply approved annotation amendments consistently to
affected arms and retain the old decisions and actual execution accounting.

## 9. Authorship and reviewer responsibilities

The owner-led model is approved; actual assignments are not. This plan names
responsibilities only, not people or qualifications.

| Responsibility | Required assignment/evidence |
| --- | --- |
| Source preparation | Actual preparer/author ID, tools/aids, source assumptions and known development/reference/output exposure; no hidden author intent as truth. |
| Lineage review | Actual reviewer and rationale for material/generic parent links, related groups and uncertainty. |
| Eligibility assessment | Actual decision authority/reviewer, dispositions and claim limitations before population release. |
| Source-first reference adjudication | Actual owner-led adjudicator/reviewer, source pointers, applicable judgments, uncertainty and versioned approval before candidate inspection. |
| Candidate-generation operation | Named authorized operator, approved plan, context and actual invocation evidence; owner-only hosted arrangement retained unless separately changed. |
| Candidate-specific semantic review | Actual reviewer, candidate identity, exact original statements/spans/citations, opposing interpretations and approval state. |
| Release approval | Actual owner authority, version, scope, limitations and separate population, report and external-publication decisions. |

A person may hold multiple roles if the overlap and exposure are recorded. That
does not establish independent authorship or independent review. Source and
candidate review can involve different phases even when the person is the same;
record the phase and actual knowledge boundary rather than claiming blinding.

AI aids may propose source text, lineage questions or review interpretations only
under separately authorized work. Record any such assistance and its supplied
context. AI output is not a second human reviewer, owner approval or AML expert
validation. Optional practical masking or additional reviewers could improve
credibility but are not assumed available or required by an invented rule.

## 10. Exposure and contamination procedures

**Proposed practical register:** a small versioned ledger, separate from investigation
input, referencing artifacts rather than copying evaluation answers into prompts.
Record event ID, actual role/person where known, time when observed or explicitly
unknown, family/case/artifact/version, access channel, information exposed, purpose,
evidence reference, eligibility impact, reviewer/authority and amendment history.
These are proposed fields, not an implemented schema or independently authenticated
access-monitoring service.

| Exposure category | Proposed handling |
| --- | --- |
| Golden/development input or generator familiarity | Record known scope; assess material ancestry rather than treating all familiarity as automatic runtime leakage. |
| Reference labels/rationales or source adjudications | Restrict to source/review roles; keep out of producer context. Record actual author/role overlap. |
| Prior candidates/failure analyses | Record whether source construction or system choice was influenced. Targeted stress design must be declared; no representative or unforeseen-failure claim follows. |
| Prompt/history/tools/retrieval | Record exact observable authorized context and channels; investigate unexpected additions. The current hosted two-message path is not proof of all historical/provider isolation. |
| Reviewer feedback | Keep out of future held-out generation; record recipients and affected groups/versions. |
| Evaluation-informed tuning | Version the changed system and mark subsequent reuse/exposure honestly; preserve original evaluation results. |
| Missing access history | Mark uncertain or unaudited, not clean. Quarantine the relevant independence claim until disposition. |

Keep separate context descriptions: **no observed unauthorized exposure within an
audited boundary**, **confirmed contamination**, **uncertain exposure** and
**unaudited context**. The first is a scoped observation, not absolute cleanliness
or provider pretraining independence. A source check conclusion can be legitimate
input and an outcome cue; do not relabel it forbidden reference leakage solely
because it is useful, and do not treat it as verification executed by the system.

For an incident: preserve available originals, stop the affected release/dispatch,
identify all related units/groups and append the evidence and provisional impact.
The owner decides quarantine, rejection of the held-out claim or openly labeled
reclassification. Retain actual failed or contaminated attempts in accounting;
exclude them from a particular independent claim only with an explicit reason,
not deletion from the study history. Corrections and replacements require new
versions/approval; do not secretly remove difficult results or retry for success.

## 11. Existing capabilities, procedural gaps and engineering choices

Control classes: **A** existing usable capability; **B** manual/procedural control
needed; **C** demonstrated engineering change; **D** optional enhancement. Coverage
below maps the proposed controls, not a promise that software certifies methodology.

| Operational control | Existing support and limits | Class and smallest remaining work |
| --- | --- | --- |
| Input shape and explicit relationships | [Pydantic contracts](../../src/aml_triage/contracts.py) validate records/references and permit valid incomplete data. | A+B: use unchanged after authorization; source sufficiency still needs review. |
| New family/source construction | Current generator has only fixed development builders and seed/count settings. | B: separately authorized manual source preparation is feasible. A dedicated authoring tool is D until a reproducibility/workload need is demonstrated; selecting it would require separate implementation authorization, not establish that C is already necessary. |
| Source identities and canonical input | Manifest raw hashes and [prompt canonicalization](../../src/aml_triage/openai_prompt.py) distinguish original bytes from validated serialization. | A+B: freeze actual new artifacts and digest bases when authorized; no hashes for nonexistent cases. |
| Family parentage/grouping, selection and size | Existing manifest records simple development ancestry, not a full eligibility or selection procedure. | B: versioned dossiers/manifest and owner decisions. A database/graph service is D, not necessary. |
| Development/source/population freeze | Git/component identities and historical experiment manifests show usable provenance patterns. | A+B: actual freeze events, permitted changes, roles and approvals are missing. Hashes do not prove access chronology. |
| Preservation/non-overwrite | Existing [development writer](../../src/aml_triage/synthetic_generator.py) stages/checks generated bytes and refuses existing targets; [hosted publication](../../src/aml_triage/openai_service.py) publishes new bundles without overwrite. | A+B: reuse principles and an approved procedure; do not call the development writer to publish arbitrary new cases. Manual protected versioning can suffice; tamper-proof infrastructure is D. |
| Context separation/exposure ledger | Existing [prompt](../../src/aml_triage/openai_prompt.py) and [service](../../src/aml_triage/openai_service.py) expose the application request boundary. | A+B: prospective role/history/tool records and review. No complete provider exposure proof is available or required. |
| Execution accounting and safety | Existing service settings/attempt records, request guard and separate historical intents/closures. | A+B: new plan, authorizations and manual accounting. Persistent automation is D unless scale/concurrency makes manual limits unacceptable. |
| Mechanical audit and evidence pointers | [Auditor](../../src/aml_triage/auditor.py), [restricted amount checker](../../src/aml_triage/transaction_amount_checks.py), [companion composer](../../src/aml_triage/evidence_report.py) bind supplied representations and bounded source observations. | A+B: reuse exact scopes; unchecked assertions remain unchecked. No general entailment or policy-quality guarantee. |
| Review/adjudication integrity | [Hybrid preview](../../research/evaluation_calibration/hybrid_review_preview.py) and [G02 reconciliation](../../research/evaluation_calibration/g02_reconciliation.py) verify specific frozen packets and consume owner decisions. | A+B as patterns and existing calibration tools; they are not general new-population validators. Actual guide/roles/releases are procedural gaps. |
| Quarantine/revisions/report release | Existing versioned addenda, manifests and original evidence demonstrate separation patterns. | B: approved incident/amendment decisions and P gates. Automated eligibility/scoring engine is D, not a current prerequisite. |

**No new runtime architecture or mandatory engineering change is demonstrated for
this planning checkpoint.** If later authoring demands a tool, its objective would
be reproducible source production or reliable non-overwriting publication, not
manufactured independence. Alternatives are a bounded manual process or a small
versioned authoring helper. The tradeoff is manual review burden versus code/test
maintenance and additional lineage. The owner must approve the demonstrated scope
before code is written; no general generator framework or evaluator is mandated.

The [generator tests](../../tests/test_synthetic_generator.py) and existing tracked
[integration fixtures/tests](../../tests/test_week6_pipeline_integration.py) provide
engineering regression evidence, not held-out examples. Historical test counts
are not fresh results. No suite or producer was run for this document. G02
packet-dependent tests can skip without ignored evidence; ordinary CI success
alone cannot certify a packet-dependent reproduction.

## 12. Dependencies and distinct approval gates

Preserve W7-S01-W7-S07, the as-configured comparison, current unequal REF-01 access
and all frozen Week 5/6 evidence. None of the gates below is satisfied merely by
creating this draft.

| Gate | Required before activity; dependencies |
| --- | --- |
| A - population authoring | Approve envelope, family/lineage rules, selection/size/authoring limits, actual preparer/access roles, authoring method, preferred freeze chronology and preservation procedure; explicitly authorize bounded authoring. No source files are created here. |
| B - source/reference adjudication | Approve applicable source-reliance/review procedure and actual roles; identify source artifacts, uncertainty and approval provenance; separately authorize review. Permission to author is not adjudication. Full numerical denominators need not be settled for a bounded source inventory. |
| C - population eligibility release | Inspect actual dossiers, validation, parent groups, frozen sources/references, selection, exposure history and unresolved dispositions; explicitly approve versioned roster/partition and qualified claim. This is not execution or external publication. |
| D - baseline/hosted execution | Specific frozen experiment plan, exact cases and as-configured identities/settings, named operator, request/retry/spending ceilings, stop rules, fresh destinations, write-ahead intent and explicit owner release. Historical allowances remain consumed. |
| E - numerical semantic reporting | Resolve applicable P03 category/applicability/denominator/process-authority decisions, actual review eligibility and explicit calculation/reporting permission. No score is authorized by qualitative-framework approval. |
| F - formal report/stronger claims | Applicable P04 versioned adjudication/report release; actual P05 evidence for the stated independence; separate qualified expert evidence if claimed; separate owner authorization for external publication. No automatic Week 7 closure. |

[P01](../phase-2/G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) remains settled:
the stronger drafted personal-authorship reading must not automatically become a
candidate-level factual error. [P02](../phase-2/G02_P02_MATERIALITY_DECISION_ADDENDUM_v0.1_2026-11-01.md)
keeps M04 contextual/nonmandatory for frozen G02 without declaring the subject
universally immaterial. Preserve original qualifications and all prior judgments.

P03 remains unresolved. P04 formal release remains distinct from the already
implemented non-scoring reconciliation. P05 held-out eligibility and independent
AML expert validation are separate claims; owner-led review establishes neither
automatically. The [register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json)
and historical pending markers are not rewritten.

D-01-D-08 continue to govern applicable source reliance, literal REF-01,
recommendation/abstention eligibility, category distinctions, alternatives,
generation isolation, roles and family independence. Do not require irrelevant
action-quality decisions merely to plan factual review, and do not infer policy
truth or approved labels from generator conditions. Candidate-specific systematic
review still requires its operational guide and authorization.

**Current authorization ledger:** one draft document only; ZERO new baseline
experiments, ZERO hosted requests, ZERO new spending and ZERO new evaluation
execution. No dataset creation, source/candidate adjudication, scoring artifact,
retry, fallback, publication or Git operation is authorized. Request guards are
not persistent provider billing caps; missing receipts or billing stay unknown.

## 13. Owner decision register - all PENDING

These are proposed operational decision IDs, not replacements for W7-S01-W7-S07
or P01-P05. No recommendation below is an owner approval. Section references supply
the repository evidence and rationale; dependencies are decision dependencies,
not instructions to begin work.

| Proposed ID | Question and alternatives | Recommended option and evidence/rationale | Risks/tradeoffs | Dependencies | Approval status |
| --- | --- | --- | --- | --- | --- |
| W7-PF01 | Which population envelope: initial source-bounded review, narrower predicate focus, or broader mixed mechanisms? | Initial contract-compatible new-family envelope in section 3; matches approved factual/citation/safety focus without changing systems. | Limited conclusions; broader scope adds review/policy uncertainty. | W7-S01/S02 | PENDING |
| W7-PF02 | Use a prespecified mechanism checklist, a detailed ancestry dossier, or both to assess material novelty? | Combine dossier-based comparison with explicit mechanism criteria and three dispositions in section 4; existing builders show why IDs/seeds are insufficient. | Human judgment remains; criteria can be too lax or overgroup generic sharing. | PF01, D-08 | PENDING |
| W7-PF03 | Flat family labels or explicit material parent links with related-group isolation? | Explicit links and connected material groups, section 5; preserves sibling/combination ancestry. | More bookkeeping; generic sharing must not collapse every group. | PF02 | PENDING |
| W7-PF04 | Complete bounded eligible roster or prespecified family-level sampling? | Complete frozen roster if justified capacity permits; otherwise a separately approved reproducible selection rule, section 6. | Census still reflects author selection; sampling needs frame/method and dependence disclosure. | PF01-PF03, PF05 | PENDING |
| W7-PF05 | Descriptive coverage/capacity justification or an inferential precision-based size design? | Start with section 7's descriptive scope/dependence/capacity/uncertainty justification; choose no numbers until evidence supports them. | Small samples limit inference; larger related samples can create false precision and review burden. | PF01, provisional selection assumptions and actual capacity evidence | PENDING |
| W7-PF06 | Manual source preparation or separately implemented authoring helper? | Bounded manual preparation with existing validation/hashing first; current generator is development-only, section 11. | Manual mistakes versus code/lineage maintenance; helper needs demonstrated need and separate authorization. | PF01-PF05, PF09/PF12 | PENDING |
| W7-PF07 | Freeze before authoring or use separately controlled preparation with later pre-exposure freeze? What exact component/configuration identities are frozen? | Before new authoring for overlapping roles; distinguish F1-F4 and allowed data/docs advancement, section 8. | Restricts adaptation; parallelism requires real separation. Provider weights remain unavailable. | PF01/PF09; actual system/configuration choices | PENDING |
| W7-PF08 | Separate F2/F3 approval records, or one approval package retaining distinct freezes and decisions? | Keep explicit F2 and F3 decisions/bindings, unresolved items and rejection/quarantine history; packaging can be combined without conflating meanings. | Additional approval work; collapsing releases can hide unsettled eligibility. | PF02-PF07, PF09-PF12 | PENDING |
| W7-PF09 | Which actual people hold roles: disclosed owner overlap or additional reviewers if genuinely available? | Named responsibility/access matrix under the approved owner-led model, section 9; disclose qualifications and overlap. | Single-reviewer bias remains; extra reviewers may be unavailable and are not invented. | W7-S05; actual owner assignments | PENDING |
| W7-PF10 | Quarantine uncertain exposure for evidence review or immediately reject the affected independence claim? | Versioned register and incident triage in section 10: quarantine uncertainty, reject established ineligibility and retain all history. | Incomplete observation limits assurance; permissive reclassification could hide contamination. | PF02/PF03/PF07/PF09 | PENDING |
| W7-PF11 | A bounded guide for initial dimensions or a complete semantic handbook before review? | Bounded consistent guide, source authority/fidelity and distinct review/applicability axes; action quality remains descriptive. | Operational details not yet approved; source review must not invent candidate judgments or settle numerical P03 implicitly. | W7-S04/S05, PF01/PF09; applicable D decisions | PENDING |
| W7-PF12 | Small versioned manifests/ledgers or expanded automated preservation/release tooling; which exact formats/destinations? | Small versioned files, explicit raw/canonical bases and non-overwrite checks, sections 5/11; no database. | Manual traceability effort; hashes are not truth, independent timestamps or access proof. | PF03/PF07/PF09/PF10; W7-S06/P04 | PENDING |
| W7-PF13 | Which later quantitative outputs and Week 7 acceptance evidence are justified: bounded descriptions or approved semantic rates/inference? | Defer numerical semantic outputs until applicable P03/review/sample requirements are approved; retain roadmap/charter obligations. | Descriptive work alone may not satisfy final acceptance; inference needs more evidence. | PF05/PF11, P03/P04/P05 as applicable | PENDING |
| W7-PF14 | Separate arm releases or one bounded experiment release with distinct baseline/hosted allowances; what exact cases/settings, operator and stop rules? | Explicit bounded owner release under section 12D, preserving arm-specific limits and records under either packaging; current rights remain zero. | Administrative caps do not guarantee billing; uncertainty and absent receipts must remain visible. | F1-F3, F4 verification evidence, PF08/PF09/PF12, W7-S07 | PENDING |

Authoring gate A needs applicable PF01-PF07, actual PF09 responsibilities,
PF10 exposure handling and PF12 preservation details plus explicit bounded work
permission. Source review adds PF11 and gate B. Population release needs the actual
evidence under PF08/C. PF13 numerical decisions and PF14 execution are not silently
required to approve this draft, nor silently satisfied by approving earlier steps.
Each later release must list which decisions it resolves and which remain pending.
Size and selection proposals may be refined together before their joint approval;
that planning iteration authorizes neither authoring nor exploratory model runs.

## 14. Limitations and next bounded checkpoint

This draft establishes no actual sample size, case, family membership, partition,
author/reviewer assignment, held-out eligibility verdict, source label, freeze
event, experiment, semantic result or independent expertise. Static inspection and
raw-hash checks do not replace future source review or prove historical non-exposure.
No new API compatibility, current pricing or billing evidence is claimed.

Evidence required for later progress is distinct:

- **Population protocol approval:** owner decisions on envelope, novelty/grouping,
  selection/size process, chronology, roles, exposure and evidence procedures, with
  precise unresolved dependencies retained.
- **Authoring permission:** actual bounded scope/preparer and permitted method,
  freeze/access prerequisites and explicit work authorization; protocol discussion
  alone is insufficient.
- **Local held-out eligibility:** actual dossiers, artifacts, lineage, population
  release and observed exposure/freeze history for the exact claim and versions.
- **Experiment permission:** a separate exact execution plan and owner authorization;
  no historical allowance or preparation record supplies it.
- **Quantitative results:** real preserved observations and approved measurement,
  review/denominator/release conditions. No synthetic independence or quality score
  is inferred from the size of the manifest or number of claims.

**Recommended smallest next checkpoint, not started:** owner review and disposition
of this draft's pre-authoring population/eligibility/freeze choices, identifying
accepted options and remaining gates in a versioned decision record if separately
authorized. Resolve operational rules and actual responsibilities before creating
source material. Do not combine that review with dataset creation or an experiment.

Completion of that proposed decision checkpoint would mean explicit decisions or
documented holds for the applicable pre-authoring items, an accepted chronology
and access boundary, and an unambiguous statement of any next permitted work.
It would not automatically authorize authoring, scoring, execution, publication,
Week 7 closure or a milestone transition. **STOP for owner review.**
