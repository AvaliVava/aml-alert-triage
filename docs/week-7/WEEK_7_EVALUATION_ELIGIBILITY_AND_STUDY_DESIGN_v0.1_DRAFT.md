# Week 7 evaluation eligibility and study design - v0.1 DRAFT

**DRAFT - STUDY DESIGN NOT APPROVED. No dataset creation, implementation, semantic scoring, model execution, spending or evaluation release is authorized.**

Prepared November 2, 2026, on `research/week-7-evaluation-design` at
`ec61b98dce5e844676427f8857f8a838372136a9`. The owner authorized this single
methodology document after Checkpoint 0. That authorization approves preparation,
not the recommendations below. Week 5/6 closure remains intact. This specification
applies the existing [evaluation protocol draft](../phase-2/EVALUATION_PROTOCOL_DRAFT.md);
it does not replace that protocol or approve its unresolved definitions.

## 1. Research questions: three distinct design choices

Policy-access design and population independence are separate axes. Option A can
use the independently controlled population proposed in C; an as-configured study
does not inherently mean a development-only study. Option B is a different policy
treatment, not an automatic improvement to the existing experiment.

### A. As-configured comparison

**Proposed question:** On a prospectively frozen, separately controlled set of
previously unexposed synthetic scenario-family groups, what execution and mechanical
outcomes, reviewed factual-support and submitted-citation-adequacy dispositions,
and concrete safety failures do the unchanged deterministic baseline and hosted
assessment system produce as configured?

- **Compared/measured:** Paired outputs on identical supplied investigations;
  generation outcomes, bounded mechanical diagnostics, proposed primary semantic
  dimensions and concrete failure reviews. Actions are initially descriptive.
- **Fixed:** Input bytes, contracts, baseline source, hosted instruction version,
  output schema, auditor/composer, approved request settings and review rules.
- **Varies:** Producing system, case/family, output content, and hosted stochastic
  behavior. Baseline and hosted policy access remain deliberately unequal.
- **Permissible conclusion:** Observed behavior of these two configured systems on
  this defined synthetic population. No difference is attributed to model quality
  alone, and no winner follows from action agreement.
- **Confounders/limits:** REF-01 implementation versus absent full hosted REF-01
  instructions; baseline rule coverage and inability to recommend `close`; output
  verbosity, parsing constraints, source cues, author/reviewer overlap and limited
  synthetic-family sampling. One observation per slot cannot estimate run variability.
- **Approvals:** Population/partition, D-06 access policy, relevant review categories,
  reviewers, request settings/allowances and later release. None is granted here.
- **Implementation implication:** Existing producer, audit and report interfaces
  suffice for bounded collection. Review/aggregation requirements must be approved
  before deciding whether any new evaluator code is needed. No new runner is assumed.

### B. Controlled equivalent-policy comparison

**Alternative question:** With a predefined common fictional policy-information
specification, how do the fixed baseline and a separately versioned hosted prompt
apply that information to the same frozen investigations, and what support,
attribution and safety issues appear?

- **Fixed:** Case population, evidence, contracts, evaluation definitions and common
  policy-information specification. **Varies:** Rule-based versus hosted processing
  and an explicitly authorized hosted instruction version.
- **Permissible conclusion:** Behavior under the documented aligned-information
  treatment. Equivalent text is not proof of equivalent implementation, comprehension,
  decision coverage or an isolated causal model-quality effect.
- **Feasibility:** The baseline takes a validated investigation and implements fixed
  predicates; it has no policy-text argument. The hosted service builds a fixed
  versioned prompt and has no arbitrary policy-instruction configuration field.
  Full REF-01 instructions could be added only through a separately authorized,
  versioned prompt change with request-content/isolation tests. Existing transport
  and output contracts can be reused; no new API client is necessary.
- **Boundary:** Supplying action definitions does not give the limited baseline a
  closure rule. A narrower aligned REF-01-information study is more defensible than
  claiming whole-rubric equivalence. If the question requires new baseline behavior,
  that is a separate substantive change, not an evaluation setup adjustment.
- **Risks/approvals:** D-06 exact instruction content, interpretation of common
  information, new prompt identity, calibration exposure and applicable adjudications
  require approval. Do not insert instructions into evidence facts, reveal reference
  answers, or retrofit the Week 5 prompt/history. Added treatment and maintenance
  complicate attribution to the previous frozen system.

### C. Independent held-out synthetic-family generalization

**Population question:** For a system frozen before access to the evaluation
population, what observed behavior and reviewed failures persist across separately
controlled, previously unexposed synthetic families within the declared input and
fictional-policy scope?

- **Measured:** Eligible per-case and per-family outcomes; any approved semantic
  measures remain distinct from mechanical results. A paired baseline is a configured
  control if A or B is selected, not a reference-label authority.
- **Fixed:** System/configuration, eligibility definitions, partition, review policy
  and source scope before exposure. **Varies:** Prespecified family groups and
  source-condition variants within the population envelope.
- **Permissible conclusion:** Bounded transfer to the specified held-out synthetic
  population under audited local exposure controls. Not real-world AML generalization,
  an estimate of financial-crime prevalence, or proof of provider training independence.
- **Inputs/approvals:** D-08 partition/lineage, D-06 access, actual author/reviewer
  assignments and case-level evidence/reference review. No eligible held-out
  population currently exists in the inspected repository.
- **Effort/risk:** New source preparation and adjudication are needed; existing
  contracts can represent a prospective population without changing architecture.
  New families can fall outside baseline predicate coverage, which must be disclosed
  rather than filtered after seeing outcomes. Independence does not imply realism or
  expert validity.

**Recommendation, not approval:** Start with A on the controlled population described
in C, with factual support and submitted-citation adequacy as candidate primary
semantic dimensions and whole-statement safety review alongside them. This advances
Week 7 without altering the system being studied. Defer B and numerical action-quality
metrics until their additional dependencies are justified and approved.

## 2. Repository basis and authority

### 2.1 Original objective and existing verified capabilities

The [roadmap](../../ROADMAP.md) requires **"Held-out evaluation and safety/failure
analysis"**, evidenced by **"Reproducible quantitative report and limitations."**
The [charter](../../PROJECT_CHARTER.md) calls for baseline comparison, honest
independence, cost/latency evidence and class-specific precision/recall and serious
error examples rather than reliance on overall accuracy. This draft waives none of
those requirements and does not claim that the proposed initial study completes
Week 7. Action metrics remain conditional on approved labels, eligibility and an
appropriate population; their eventual milestone treatment needs owner review.

The current [status](../../PROJECT_STATUS.md), [decisions](../../DECISIONS.md),
[Week 5 closure](../week-5/WEEK_5_MILESTONE_CLOSURE_DECISION_v0.1_2026-11-01.md) and
[Week 6 closure](../week-6/WEEK_6_MILESTONE_CLOSURE_DECISION_v0.1_2026-11-01.md)
establish later engineering progress. Foundation-era statements that no classifier
or output contract exists are historical, not current capability descriptions.
The present authorization permits design only; historical notices withholding
Week 7 execution/scoring remain applicable to those activities.

| Existing capability | Reuse and actual boundary |
| --- | --- |
| [Contracts and contextual validation](../../src/aml_triage/contracts.py) | Validate input/output, case/alert identity and eight typed citation namespaces. Citation existence does not establish relevance. Incomplete inputs and valid abstention remain permitted. |
| [Baseline `assess_investigation`](../../src/aml_triage/deterministic_baseline.py) | Version `0.1.0`; limited fixed rules including literal REF-01, investigation questions and abstention. It does not recommend `close` or consume reference files. |
| [Hosted `OpenAIAssessmentService.assess` and `AssessmentRun`](../../src/aml_triage/openai_service.py) | Structured assessment, exact accessible candidate text, failure/usage records and bounded request guard. SDK parsing can prevent preservation of invalid original text. Service `validated` is not semantic validation. |
| [Prompt builder](../../src/aml_triage/openai_prompt.py) | `aml-preliminary-1.0`; developer instructions plus canonical validated investigation JSON. No full REF-01, reference lookup, retrieval or conversation history is supplied by this path. |
| [Auditor `audit_packet`](../../src/aml_triage/auditor.py) and [amount checker](../../src/aml_triage/transaction_amount_checks.py) | Auditor `0.2.0`, schema `1.1`; three mechanical stages and restricted whole-statement amount checks. Unrecognized wording is unchecked. The nine broad semantic entries remain `not_evaluated`. |
| [Evidence relationship checks](../../src/aml_triage/evidence_relation_checks.py) | Existing G04-specific source/citation relationship diagnostics using evaluation annotations. Not a general entailment engine or approved rule for every beneficiary case. |
| [Evidence-report composer](../../src/aml_triage/evidence_report.py) | Composer `0.1.0`, report schema `1.0`, template `1.0`; E01-E06 only, source pointers, attribution and prominent restricted conflicts. Neither an annotation release nor a general semantic evaluator. |
| [Hybrid research utilities](../../research/evaluation_calibration/README.md) and [G02 reconciler](../../research/evaluation_calibration/g02_reconciliation.py) | Existing draft integrity checks and non-scoring reconciliation of owner decisions. Preserve original annotations, whole statements and separate material coverage. Registered G02 action comparison already exists. |

The [Week 6 implementation contract](../week-6/EVIDENCE_REPORT_IMPLEMENTATION_CONTRACT_v0.1.md),
[integration evidence](../week-6/WEEK_6_INTEGRATION_EVIDENCE_v0.1_DRAFT.md),
[composer tests](../../tests/test_evidence_report.py) and
[integration tests](../../tests/test_week6_pipeline_integration.py) document the
working library flow. Historical verification records 499 complete-suite passes;
no runtime tests were rerun for this specification. CI Python 3.11-3.13 success is
recorded as owner-reported, not independently retrieved here. The
[workflow](../../.github/workflows/foundation-tests.yml) consumes
[constraints](../../constraints.txt); SDK `3.40.0` and Pydantic `2.14.1` are pinned
there. These are inspected dependency constraints, not a new runtime measurement.

### 2.2 Verified identity anchors

These hashes cover current supplied file bytes unless another basis is specified.
They identify the design basis, not approval of its semantic content.

| Artifact | SHA-256 |
| --- | --- |
| [Development manifest](../../data/generated/development/manifest.json) | `6b4342f3a98c6426723f22ee2f5816540dc8f0bd0bd2e166fbde09a23c38bfb9` |
| [Fictional policy](../../specs/labeling_policy_v1.json) | `6cdefd8400ae160163a4e0625f0b5311890ecad27967767e10459df2f1ee6352` |
| [G02 register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json) | `51396c9f87d6781cf55ae72380327b815e35a8d08e0ac3b3614512ff99c226ef` |
| Hosted instructions, exact UTF-8 string in the prompt module; not the module file | `f6472c5d27337626e113cfa982297b0c6b317282eefc4a600f049fa025bb6c83` |

The current P01/P02 checkout documents use CRLF while their committed blobs use LF;
read-only comparison found their text equal apart from line endings. Historical
creation hashes and current checkout-byte hashes must retain their respective
bases. This does not authorize normalizing frozen packet bytes to satisfy a hash.
No source or decision record was rewritten.

### 2.3 Historical evidence is context, not a new cohort

The [Week 5 specification](../week-5/CONTROLLED_EXPERIMENT_SPEC_DRAFT.md) and closure
preserve five historical baseline observations, seven SDK operations including two
Case 0001 failures, and five validated hosted outputs. All hosted actions were
`investigate`; semantic correctness was not evaluated. Restricted amount coverage
was 9 checked/matched of 17 baseline findings and 0 checked of 29 hosted findings,
with zero detected conflicts. Unchecked findings received no factual verification.

Relevant frozen local evidence remains **Git-ignored and local-only**:

- `outputs/experiments/W5-OPSMOKE-001-WHOLE-REVIEW-20261031T150256Z/`
- `outputs/experiments/W5-OPSMOKE-001-BOUNDED-CLOSURE-20261031T164640Z/`
- `outputs/evaluation/g02-paired-pilot-20261029/`
- `outputs/evaluation/g02-reconciliation-20261030/reconciliation_report.json`

These are evidence locations, not repository-accessible links or required new CI
fixtures. No historical run is retrospectively preregistered or relabeled held-out.
All previous live allowances remain consumed; this document grants zero new ones.

## 3. Proposed population, partition and provenance policy

All rules in this section are **proposals requiring owner approval**, extending the
accepted D-08 direction rather than establishing a new dataset today.

| Population | Established/proposed use | Independence and claim boundary |
| --- | --- | --- |
| G01-G05 [golden inputs and references](../../data/golden_cases/README.md) | Existing development/regression and exposed calibration material. All five reference files remain provisional. | Cannot support independent held-out claims; G02's separate owner rulings do not approve the other references. The duplicate-ID negative fixture is not a sixth labeled case. |
| Existing 50 [development investigations](../../data/generated/development/manifest.json) | Fifty unique, freshly hash-checked files; five families and 18 family/condition combinations. | Explicit development partition, shared templates, no independently authored cases or adjudicated labels. Remaining files are not held-out merely because they lack a recorded hosted run. |
| New draws from existing templates | Potential known-generator behavior study, if separately authorized. | New identifiers/amounts/seeds do not create new family independence. No claim of unseen-template generalization. |
| New synthetic families/templates | Candidate population for C, within current contract and approved fictional-policy scope. | Requires justified separation from all exposed template/source families. New wording or a renamed condition is insufficient. No cases selected or generated here. |
| Independently authored synthetic scenarios | Stronger authorial-separation alternative. | Requires actual authorship/access records and adjudication. Independent authorship alone does not establish expertise, realism or population representativeness. |

### 3.1 Independence unit and related-case handling

Use the **connected family/template lineage group** as the proposed primary partition
unit. Record individual cases, source-condition variants, counterfactual sibling
groups and authorship/source groups within that hierarchy. If two proposed families
share a material template, source case, sibling construction or authoring artifact,
record that edge and keep the connected group in one partition. Independent
authorship is an additional attribute, not a substitute for lineage separation.

All currently exposed golden/development groups remain development. A new template
derived materially from them must not be promoted to held-out on the strength of
a new name. Record conceptual commonalities and adjudicate uncertain lineage before
eligibility. Shared generic input schema and authorized rubric are not themselves
case-answer leakage; shared answer-bearing scenario structure can compromise the
intended family-independence claim.

Prepare a prospective partition manifest before candidate generation, with case
IDs, raw input hashes, family/template/source/author IDs, sibling membership,
source-condition descriptions, lineage edges, partition owner, freeze revision,
exposure events and eligibility reasons. Metadata stays outside model input. Source
conditions describe construction, not approved actions. Selection must follow a
fixed rule based on the declared population/conditions, never observed candidates.
Do not silently discard cases where the baseline has no implemented rule.

### 3.2 Freeze and exposure sequence

1. Approve question, population envelope, family-separation rule, source-reliance
   assumptions, role/access policy and intended measurements before authoring.
2. Prepare source records without candidate feedback. Record all author exposure
   to existing rules/examples. Source authoring and category-policy calibration on
   existing development material may proceed in parallel after separate approvals.
3. Validate sources, create a source-first inventory and resolve applicable case
   expectations before candidate review. Freeze input bytes, lineage/partition,
   references, unresolved items and reviewer provenance before candidate generation.
4. Freeze baseline/source revision, prompt and complete authorized instructions,
   schema, auditor/composer, dependency/runtime identities, model/settings and
   attempt/stop policy. No adaptation after opening held-out outcomes.
5. Generate only under a later execution release. Record exposure across operators,
   tools, history and feedback, not just final request text.
6. Keep case inventories separate from candidate-specific reviews. Correct genuine
   annotation errors through versioned amendments applied consistently to all affected
   outputs. Preserve the old versions and any resulting exposure; never silently
   improve the dataset or rerun a failed candidate under the same release.

If policy interpretation or source ambiguity cannot be resolved before generation,
record the limitation and exclude only the affected proposed semantic measurement
under an approved rule, not the case's execution/failure accounting. Unexpected
exposure means hold the independence claim and record contaminated, uncertain or
unaudited status; a replacement population requires a new decision.

### 3.3 Sample size and inference

No count or class quota is approved here. Justification needs the target population,
number of genuinely distinct family groups, condition coverage, approved action and
abstention eligibility distributions, reviewer capacity, intended precision and
cluster dependence, failure-accounting policy and any later paid budget. Claims
within a case and siblings within a family are not independent samples. Show case
and family counts alongside claim counts; verbosity must not create pseudo-replication.
Do not promise confidence intervals, significance or power before the design supports
them. A small diagnostic set may support bounded descriptions, not prevalence estimates.

## 4. Proposed policy/rubric and context access under D-06

| Information | Proposed generation access | Evaluation-side treatment |
| --- | --- | --- |
| Generic fictional action/rubric instructions | A retains current prompt and compiled baseline. B would allow only exact separately approved generic instruction text, uniformly applied. | Record exact authorized text/hash, version, differences and supported predicate scope. Policy ID alone does not supply content. |
| Case-specific policy facts legitimately in the investigation | Allowed as supplied data: instructions, registers, checks and timestamps. | Review what they actually establish. A recorded check outcome can be an outcome cue without constituting forbidden reference leakage. |
| Reference actions/rationales, inventories, adjudications and evaluation annotations | Forbidden. | Available only to assigned reviewers outside generation. Full policy files must not smuggle case outcomes into input. |
| Manifest family/condition metadata, baseline output and previous candidates | Forbidden to hosted generation. | Used only for provenance and evaluation; no optimization toward a presumed expected action. |
| Prior feedback or disagreement/adjudication notes | Forbidden for held-out generation. | Record any exposure and its effect on eligibility; do not restart the candidate with feedback. |
| Retrieval, tools and conversational history | No new channels proposed; preserve the current two-message hosted path. | Audit actual available context, operator use and any unexpected channels, not only prompt field names. |

The baseline legitimately embodies its published fixed rules; this is known
development exposure, not evidence of runtime reference access. Evaluator/reference
stores must remain outside producer loading paths. Review artifacts and model
outputs cannot instruct later held-out generation through an operator's history.
Where one person fills multiple roles, disclose knowledge transfer that technical
allowlists cannot prevent. Claims are limited to audited local controls; complete
provider pretraining or immutable hosted model internals are unavailable.

For A, record unequal REF-01 access conspicuously in every comparison. For B, approve
an information specification and a minimal new prompt version/test change first;
do not claim text equality makes the systems algorithmically equivalent. Current
[prompt tests](../../tests/test_openai_service.py) and request inspection can be
reused, but neither proves absence of every indirect cue or external exposure.

## 5. Proposed measurement contract

**No semantic scores are calculated or authorized.** The tables specify candidate
units, evidence, reporting populations and potential denominators for owner review.
Mechanical observations exist now; approval of this study and any aggregation/release
is separate. Existing auditor/service semantic statuses must not be overwritten by
an implication that the composer performed human semantic review.

### 5.1 Group A - mechanical observations available now

| Observation | Unit and required evidence | Population/reporting form | Potential denominator and exclusions | Approval/dependency |
| --- | --- | --- | --- | --- |
| Input structure | Unique frozen input plus original bytes, contract and validation entry point. | All planned inputs; stage counts, errors and missing inputs. | All inputs presented for validation; unavailable files remain missing/error, not valid. Do not multiply source validity by number of arms. | Existing check; study accounting/report form pending. |
| Output structure | Observed assessment attempt and original candidate or explicit absence. | Each arm; unconditional attempt outcomes plus a separately labeled conditional valid-input table. | All observed attempts expected to produce an assessment; disclose absent/unreadable candidates, invalid input and unevaluated stages. | Existing contract; plan must define attempt versus logical-slot populations. |
| Contextual references | Structurally valid input/candidate pair, root identities and typed citations. | Case-level passed/failed/not-evaluated/error counts with diagnostics. | Pairs meeting prerequisites, with blocked pairs retained in overall accounting. Permitted empty citations are not failures. No per-citation rate from fail-fast validation. | Existing validator; exhaustive occurrence reporting would need separate justification/implementation. |
| Generation outcome | Original service record, candidate availability and operator observations where actually supplied. | Attempt outcomes: completed, failed, refused, incomplete, unknown/publication uncertain. | Actual observed producer attempts, distinct from planned/authorized slots. Missing usage and CLI observations stay unknown. | Existing service records plus prospective ledger; no future attempts authorized. |
| Structural abstention and action pattern | Validated status/action pair, scope and review fields. | Counts of each submitted action and `unable_to_recommend`, separately from failure. | Valid outputs; show invalid/missing outputs against all attempts separately. No action correctness numerator. | Existing extraction; appropriateness requires Group B. |
| Restricted amount coverage/results | Original candidate, correct raw/canonical input binding and existing checker identity. | Findings total, checked, matched, conflicting and unchecked by case/arm. | All factual findings for coverage; checked findings for result counts. Preserve not-checked reasons and zero coverage; do not infer correctness. | Reuse exact existing grammar, no new parser. Not a semantic rate. |
| Literal preliminary/review compliance | Original candidate and contract diagnostics. | Exact field outcomes; never a completed-human-review count. | Candidate attempts expected to supply fields, retaining absent/invalid fields and unreadable outputs separately. | Existing models; prose compliance remains Group B. |
| Usage/latency, if supplied | Service usage/latency fields and attempt identity. | Per-attempt values and missing-metadata counts; disclose runtime/provider context. | Attempts with recorded measurements, alongside total attempts and unknowns. Baseline timing is not supplied by the current baseline CLI. | No new instrumentation required for the proposed primary dimensions. No billed-cost inference; estimates need separately verified assumptions. |

### 5.2 Group B - semantic judgments requiring approved review

The proposed initial semantic focus is **factual support and submitted-citation
adequacy**, with original whole-statement context and safety review mandatory to
avoid misleading atomic conclusions. Other dimensions remain separately reportable
review questions until their definitions and case evidence are approved.

| Proposed dimension | Unit and evidence | Applicable population/report form | Potential denominator and exclusions | Current status/dependency |
| --- | --- | --- | --- | --- |
| Factual support - initial primary | Factual proposition with candidate hash, exact occurrence/span, original full statement, source/opposing pointers and attribution/derivation basis. | All text locations, including question premises, rationale, interpretations and contradiction descriptions; category counts by case and location. | All reviewed applicable factual propositions for distribution; any assessable-only rate needs P03 approval. Preserve unreviewed, unassessable and fidelity-limited units separately. | D-04/P03 categories/precedence and D-07 review approval pending; G02 is case-specific calibration only. |
| Submitted-citation adequacy - initial primary | Same bound proposition and exact original citation list; approved sufficient source sets and applicability rule. | Applicable reviewed propositions; adequate/partial/inadequate/unassessable are proposed categories, not a released schema. | All reviewed citation-applicable propositions; separate empty-but-permitted lists from semantic citation requirements. Do not borrow uncited input evidence to repair the submitted set. | D-04/P03; multi-source conjunctions, absence inventories and uncited question premises need explicit treatment. |
| Whole-statement meaning/fidelity | Original statement occurrence, linked atoms, qualifiers, attribution, modality, scope and implications. | Every readable statement; separate qualifications and investigative-question relevance from factual passes. | Reviewed statement occurrences if category distributions approved; never add their failures to atomic failures as independent penalties. | Hybrid direction accepted; general classifications/eligibility pending. P01 protects original-wording fidelity. |
| Material completeness | Source-first adjudicated material-item inventory, pointers and acceptable equivalents. | Candidate-by-case coverage matrix, separate from number of asserted claims. | Applicable approved material items; repeated claims count once for an item. No inventory means no coverage score. | D-04 and case materiality decisions; G02 M01-M03 do not generalize. Defer new coverage rates initially. |
| Missing information/contradiction coverage | Adjudicated material missing/question/conflict items and both source sides. | Separate case-level coverage and misrepresentation reviews. | Applicable approved items by kind; no annotated conflict denominator does not mean no possible conflicts. | D-04 and source/materiality approval; deterministic null/difference detection alone is insufficient. |
| Recommendation quality | Adjudicated case action, alternatives, rubric clauses, rationale and source-reliance assumptions. | Descriptive actions now; future confusion counts/rationale judgments only after approval. | Assessable recommendations with approved actions, disclosing abstentions and failures against all attempts. No scores for provisional references. | D-01/D-02/D-03/D-05 as relevant, P03 and actual case adjudication. Deferred as an initial primary metric. |
| Abstention appropriateness | Candidate status/rationale and approved case answerability plus candidate-eligibility review. | Justified/unjustified abstention or unsupported commitment are proposed judgments. | Outputs with approved eligibility judgments; retain unreviewed/unassessable and failed generation separately. | D-03/P03 unresolved. Missing evidence does not automatically justify abstention or commitment. |
| Unsupported certainty/fabricated verification | Full prose, source authority, process/contract/run evidence when relevant and reviewed inference limits. | Concrete source-bound issue records and affected statements/cases, preserving uncertainty. | Reviewed applicable assertions/outputs only if later approved; no weighted severity score. | D-04/D-07/P03 authority/applicability; process claims cannot be judged solely from case citations. |
| Semantic preliminary scope | Whole prose plus literal fields and any claimed review/regulatory event evidence. | Reviewed inconsistencies/questions, distinct from literal field validity. | Readable, reviewed outputs; missing text stays disclosed, not compliant. | Human review and D-04/D-07/P03 before any semantic rate. A required-review flag is not performed review. |

Process/implementation statements require their appropriate code, contract or
execution authority. **Proposed initial treatment:** preserve them in a separate
authority-review section, outside case-factual denominators, until P03 approves
representation/applicability. No supplied authority means unresolved or unavailable
basis, not fabricated review metadata or automatic agreement with the statement.

Partial support receives no arbitrary fractional credit. Unreviewed means no
judgment; unassessable means a reviewed judgment could not be defensibly made;
not applicable means outside an explicitly approved category. A zero applicable
denominator yields no applicable rate, never a perfect result. Display excluded
counts and reasons. Category totals may overlap only where explicitly described
as different dimensions, not as independent error counts.

### 5.3 Group C - independent evaluation eligibility

| Proposed control observation | Unit/evidence | Population and report | Potential denominator/exclusions | Approval/dependency |
| --- | --- | --- | --- | --- |
| Family/partition isolation | Family-group lineage graph, sibling IDs and frozen partition assignments. | All proposed evaluation families; eligibility and violation/uncertainty records. | Audited family groups, with unaudited groups separate. Violating groups cannot support held-out claims but their observed attempts remain accounted for. | D-08 policy and owner-approved population absent. |
| Full candidate exposure | Attempt-level instruction/input/schema identities, operator/context/tool/history/feedback access record. | Every actual candidate attempt, including failed or uncertain attempts. | Audited contexts versus all observed attempts; uncertain/not-audited is not a clean exposure finding. | D-06 and role assignments; complete provider pretraining history unavailable. |
| Reference separation | Access roles, allowed producer paths, actual request/context evidence and exceptions. | All generation contexts; no-observed/confirmed/uncertain/not-audited exposure descriptions. | Audited contexts, not just successful candidates. A reserved-key scan is not a full leakage audit. | D-06 access policy and prospective evidence; no new access tests executed here. |
| Frozen provenance | Raw and canonical digest bases, source versions, immutable references, approval/revision records. | All planned sources and actual candidates; matched/missing/mismatched bindings. | Expected artifacts/bindings under an approved manifest; absent artifacts remain missing. | D-08/P04 release policy; raw-byte mismatch is not repaired by normalization. |
| Reviewer/authorship independence | Actual role IDs, overlap, qualifications, access and disagreement history. | All annotations/releases and relevant family groups; descriptive role/exposure statement. | Required review records, with absent records explicit; no automatic independent-review rate. | D-07/P05; ordinary owner-led synthetic review is not expert validation. |

## 6. Proposed human review and adjudication procedure

Use [protocol sections 4-6](../phase-2/EVALUATION_PROTOCOL_DRAFT.md), the existing
[annotation draft](../week-4/G02_ANNOTATION_FORMAT_DRAFT.md) and
[seven-bundle calibration plan](../week-4/G02_SEVEN_BUNDLE_CALIBRATION_PLAN_DRAFT.md)
as review aids, not approved general labels. Do not reapprove settled G02 findings.

| Minimum responsibility | Proposed assignment rule; no person assigned by this draft |
| --- | --- |
| Dataset author/source preparer | Records sources, lineage, ambiguities and all development exposure; supplies evidence, not hidden authorial intent as truth. |
| Candidate-generation operator | Uses only released input/instructions; records intent, settings and attempts. For any future hosted call, retain owner-only operation unless separately changed. |
| Synthetic-case reviewer/adjudicator | Reviews source sufficiency, material items, applicable rubric and acceptable alternatives before candidate inspection where feasible. Records unresolved questions. |
| Evaluation reviewer | Checks atomic fidelity, submitted citations, complete statements and coverage against frozen sources; records uncertainty and dissent. AI proposals remain proposals until actual review. |
| Release decision authority | Owner approves scope, amendments and which artifacts/results may be released under P04. A merge or file's existence alone does not establish semantic approval. |

One person may hold multiple responsibilities if disclosed. The strongest attainable
claim then reflects that overlap; do not invent blinding, independent adjudication or
an AML expert. A second reviewer is a useful option, not an already approved universal
requirement. Record whether candidate identity was visible and any unavoidable
baseline wording/style cues even if display order or producer labels are masked.

Proposed review records retain original judgments, reviewer/role as actually known,
review state, date when observed, source/candidate hashes, exact pointers/spans,
submitted citations, explanation, uncertainty, disagreements and the adjudicator's
reason. New fields may be proposed later; no annotation schema is released here.
Do not infer actual review from prose authority statements or fill missing IDs.

First inspect each full statement, then propose faithful atoms and review original
implications alongside them. Link repetitions and atoms to their containing
occurrences. Retain each occurrence for traceability while preventing duplicate
coverage credit or atomic-plus-statement penalties. Review both necessary source
conjunctions and possible alternative support sets. Preserve recorded facts,
customer claims, supplied check conclusions, interpretations and software claims
as distinct authorities. Questions can contain factual premises; a request itself
is not an asserted answer.

Disagreements retain separate interpretations and opposing pointers until resolved.
Provisional reference actions are not silently promoted. Approved alternatives must
be frozen consistently before action-quality evaluation. Later amendments identify
affected units/candidates and re-evaluate them consistently; no post hoc exception
for a favored system, silent citation repair or candidate rewrite is permitted.

## 7. Decision dependencies and preserved G02 rulings

### 7.1 D-01 through D-08: only applicable gates are prerequisites

| Decision | Existing accepted working direction | Required for this proposal; what may wait |
| --- | --- | --- |
| D-01 | Concern-specific corroboration with explicit source reliance; consistency is not authenticity. | Source-reliance assumptions needed for factual review. Specific closure-quality adjudication can wait while actions remain descriptive. |
| D-02 | Literal REF-01; senior review alone is no exception, bypass is not an invented prerequisite, same supplier account is not merely same counterparty. | Preserve in rubric/context review. Case-level referral-quality decisions are needed only for corresponding quality judgments, not action extraction. |
| D-03 | Specific material unanswered question; answerability differs from candidate inability. | Needed before recommendation/abstention appropriateness. Structural abstention can be reported without approving those judgments. |
| D-04 | Separate existence, support, submitted adequacy, completeness, conflict and review state; hybrid direction accepted. | Primary factual/citation/whole-statement applicability and faithful decomposition need owner approval before approved semantic reporting; rates additionally need denominators. Other coverage categories can be deferred. |
| D-05 | Version alternatives consistently, with no favored-candidate exceptions. | Before action-quality comparison, not a prerequisite for the initial descriptive action table. |
| D-06 | References separate; audit actual context/tools/retrieval/history/feedback and exact rubric access. | Before prospective generation and independent-context claims. Proposed A does not authorize adding policy text. |
| D-07 | Owner-led synthetic adjudication, disclosed limitations; absent intended facts are not evidence. | Assign roles and disagreement/release authority before annotation release. Draft review proposals may precede final approval. |
| D-08 | Separate random draws, new templates/combinations and independent authorship; isolate related families. | Population/partition policy before authoring and freeze/exposure release before held-out execution. |

### 7.2 P01/P02 remain approved, not generalized

The [G02 register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json)
records 75 units and 21 statement occurrences. Recorded distributions are 54
supported, 2 not established, 1 unassessable and 18 not applicable; whole statements
are 10 qualified factual passes, 3 qualified investigative questions and 8 reviewed
but not cleared for unconditional passes. These are recorded G02 dispositions, not
new scores, independent cases or a generally approved denominator.

- [P01 fidelity ruling](../phase-2/G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md):
  preserve H004/H034's original wording and existing judgments on the stronger
  drafted personal-authorship proposition. Do not automatically transfer its
  `not_established`/`inadequate` judgments into a candidate-level error. The original
  wording remains qualified, with no unconditional whole-statement pass.
- [P02 materiality ruling](../phase-2/G02_P02_MATERIALITY_DECISION_ADDENDUM_v0.1_2026-11-01.md):
  USD 48,500 versus recorded USD 25,000 is valid arithmetic and relevant profile
  context, not a hard transaction limit or automatic escalation rule. M04 remains
  contextual/nonmandatory for frozen G02, not inherently immaterial. M01-M03 remain
  the three mandatory items; M05 remains contextual. The qualified profile-fit
  question and limitations on `materially` remain.

Preserve corrected citation judgments, H047's narrow support, H049's ambiguity,
separate process authority and repeated M02 occurrences without duplicate coverage.
No existing judgment, annotation, reference or report is rewritten here. The
historical machine-readable pending markers remain; addenda record the later owner
decisions, and the existing reconciler does not ingest them. That is a versioned
release dependency, not an invitation to reopen the rulings.

### 7.3 P03/P04/P05: exact gates and bounded implications

| Gate: exact register description | Effect on proposed initial study |
| --- | --- |
| P03: `Sign off final report category applicability/denominators and external process-domain representation` | Still open. Approve factual-support and submitted-citation categories, whole-statement/fidelity treatment, authority-domain exclusions and review-state accounting for initial semantic reporting. Any rates need separate exact numerator/denominator, zero-denominator and exclusion decisions. Defer irrelevant action, abstention and material-coverage rate definitions. Scoring remains disabled. |
| P04: `Codex implementation approval and versioned repository adjudication release` | Existing non-scoring reconciliation already exists and is approved implementation evidence. Future formal annotation/report release needs explicit version, source/candidate bindings, authority, review metadata, amendments and release permission. Historical wording does not mean the code is absent. No register mutation or formal release is authorized here. |
| P05: `Independent held-out data and expert review` | Held-out claims require approved lineage/partition/exposure and actual reviewer-independence evidence. Qualified independent AML validation additionally requires a real suitably qualified independent reviewer and recorded review scope. These are distinct claims, not a declaration that all owner-led synthetic review requires an external expert. |

The register's status remains `CONSOLIDATED_DRAFT_NOT_REPOSITORY_RELEASE`, with
independent AML expert review `not_performed`. Its existing `blocking` descriptions
concern definitive semantic rates, controlled source/release changes and independent
performance/expert claims. Merged research files are not proof of approval for those
stronger claims. No missing structured metadata is inferred from approval prose.

## 8. Proposed safety and failure analysis

Each entry below is a **review taxonomy proposal**, not a newly approved label or
severity scale. Keep detection, suspicion, reviewed judgment and unresolved status
separate. A source limitation is not automatically a candidate failure.

| Review family | Deterministic evidence available | Human judgment / retained example |
| --- | --- | --- |
| Invalid, missing or failed output | Contract/context stages, original service failure/refusal/incomplete records and absent candidate. | Preserve phase, original errors and unknown publication/usage; do not turn failure into valid abstention. |
| Incorrect recognized amount | Existing restricted checker result and exact selected transaction values. | Retain candidate wording/citations and grammar scope. Unchecked text is neither matched nor correct. |
| Unsupported claim or misleading support | Citation identities and source pointers can be bound. | Review attribution, full statement and sufficiency; factual support elsewhere does not repair inadequate submitted citations. |
| Fabricated verification/process authority | Compare recorded wording with supplied checks, code/contract and actual run evidence where present. | Distinguish reported check conclusions, performed verification, required review and completed review. Do not assume a phrase detector resolves context. |
| Material omission | Approved source-first inventory can identify applicable items. | Review relevance/equivalent expression once per item. Absence of a candidate assertion cannot be found by claim scoring alone. |
| Unsupported recommendation/escalation or inappropriate abstention | Extract original action/status and record literal policy facts. | Applicable D-01-D-05 and case eligibility needed before labeling a quality failure; baseline disagreement alone is not evidence. |
| Source conflict/unqualified certainty | Bounded field differences and supplied contradictions may be traceable. | Review genuine conflict, scope and treatment; do not silently prefer a source or mistake unknown for false. |
| Non-preliminary or regulatory claims | Literal scope/human-review fields checked by contract. | Review prose implying final decisions, performed human review, SAR filing or wrongdoing. Correct flags do not excuse contrary prose. |
| Policy-access confounding | Frozen prompt/rules and approved access record. | Report unequal REF-01 access in A; never attribute its effects solely to model quality. |
| Leakage/contaminated evaluation | Manifest/context/access evidence and known forbidden paths. | Separate confirmed contamination, uncertain exposure and unaudited context. Do not certify provider training isolation. |

Proposed incident records bind exact input/candidate bytes or string digest,
statement pointer/span, submitted citations, source/authority pointers, diagnostic
version, reviewer/status and rationale. Preserve original and dissenting views,
related occurrences and unresolved questions. Retain concrete examples under a
later approved artifact/release policy; do not publish ignored evidence by default.
Use prespecified example-selection rules and disclose reviewed coverage, rather
than selecting only convenient anecdotes. Do not convert an example count into
a performance percentage, weighted severity score or model ranking.

No new safety probes, constructed responses or failure experiments were run for
this design. Existing engineering examples remain development fixtures.

## 9. Proposed evidence and reporting controls

Use existing service records wherever possible. A future ledger must distinguish
planned slots, not authorized, authorized but unexecuted, actual attempts, successful
responses, failures/refusals/incompleteness, missing/unpublished artifacts and unknown
outcomes. Record generation, validation and review failures separately. SDK attempt
counters are not provider billing receipts. A valid abstention remains an output,
not a network failure or a fourth AML disposition.

For each future frozen input, preserve original bytes and SHA-256 independently
of canonical validated-input JSON/hash. Preserve an accessible hosted candidate
string exactly and label its SHA-256 basis as UTF-8 of that supplied string, not
original HTTP envelope bytes. Serialize a newly authorized baseline output once
and freeze that candidate before audit/review. Never reconstruct unavailable
original bytes from a parsed model to satisfy an expected identity. An existing
hosted audit binds canonical input; a raw-input replay has a different input digest
basis even when applicable outcomes agree. Bind both accurately.

Freeze code/configuration/schema/dependency/runtime identities, instruction content,
model identifier and actual available provider metadata. A model identifier is
not an immutable provider snapshot. Record unavailable metadata explicitly; no
credential discovery is a requirement for offline review. Original-byte mismatches
mean hold, not LF/CRLF normalization or replacement of source evidence.

A future reproducible quantitative report should separate population/exposure
eligibility, all-attempt execution/mechanical counts, approved semantic category
distributions, per-case/family views, exclusions, concrete safety examples, provenance,
uncertainty and limitations. Semantic rates, per-class precision/recall, intervals
and action confusion reporting remain conditional on their relevant approvals and
data. No composite quality score, target threshold or statistical superiority claim
is proposed. Local absolute paths may aid tracing but do not make report bytes
portable between checkouts; distinguish source integrity from report-byte identity.

The [existing CI workflow](../../.github/workflows/foundation-tests.yml) and tracked
fixtures can validate future authorized code changes. Packet-dependent G02 research
tests intentionally skip without the ignored packet; green CI alone cannot prove
those tests ran. Reproducing a packet-dependent claim requires approved provisioning
and exact hashes, not changing the accepted skip behavior during study design.
No requirement is introduced to commit raw local evidence, secrets or a new framework.

Future hosted execution requires a separate owner release: exact model/settings,
case/attempt allowances, timeout, output ceiling, zero retries unless separately
changed, `store=False`, fresh non-overwriting destination, write-ahead intent,
operator and monetary authorization. Prior USD allowances do not roll over. Pricing,
model support and exposure must be verified at that later release; no estimate,
guaranteed billing cap or live command is supplied here. An uncertain request or
publication outcome must not cause an unapproved replacement.

## 10. Recommendation and owner decision register

### A. Recommended initial study - proposed, not approved

Choose the question in section 1A using a separately controlled family-isolated
synthetic population under 1C. Preserve existing systems and review factual support,
submitted-citation adequacy and complete-statement safety separately; report actions
descriptively. This provides a defined new question beyond the closed operational
smoke test without changing prompts to obtain preferred answers. New source/review
work is necessary, but no runtime redesign is demonstrated.

This initial scope is not a waiver of the charter's action-evaluation aims or a
Week 7 completion declaration. The owner must decide subsequent action-quality
evaluation and other required completion evidence once suitable adjudications exist.

### B. Required owner decisions

All items below are **pending**. They are study-specific choices, not amendments
to settled G02 decisions or a parallel replacement for D-01-D-08/P01-P05.

| ID | Decision to approve or revise | Blocks |
| --- | --- | --- |
| W7-S01 | Exact initial question, A-plus-C recommendation, permissible claims, action-quality deferral and relation to eventual Week 7/charter evidence. | Study authorization. |
| W7-S02 | Population envelope, family/lineage independence unit, fixed selection/partition rule, source preparer and sample-size justification process. | New dataset authoring; no actual case list/count approved here. |
| W7-S03 | A's unchanged unequal policy access, exact authorized context and exposure controls; B requires a separate prompt-treatment decision. | Prospective candidate generation and independence claims. |
| W7-S04 | Initial support/citation/whole-statement applicability, fidelity, process-authority exclusions and unreviewed/unassessable treatment; P03 remains open until explicitly resolved for the selected scope. | Approved semantic judgments/reporting; numerical rates require additional explicit eligibility/denominator and scoring permission. |
| W7-S05 | Actual role assignments, overlap disclosure, disagreement/adjudication and case/reference freeze procedure. | Approved annotation/reference release. |
| W7-S06 | Versioned artifact/review/report release controls under P04 and evidence supporting the exact independence claims under P05. | Formal evaluation release and related claims; no expert claim without actual expert evidence. |
| W7-S07 | Later execution-specific cases/settings, attempts, owner operator, budget, stop rules and evidence destination. | Any new producer execution, especially paid requests. Existing consumed allowances stay consumed. |

### C. Prerequisites in dependency order

1. Owner reviews this design and decides W7-S01-S03 and role/access requirements.
2. After separate authorization, source preparation under W7-S02 and development-only
   category/reviewer calibration under W7-S04-S05 may proceed in parallel. No held-out
   candidate feedback enters either source authoring or prompt tuning.
3. Review/freeze source sufficiency, inventories, lineage, partition, case expectations,
   source/reference identities and the system/access plan before generation. Resolve
   only decisions relevant to proposed quality measurements; preserve others as pending.
4. Separately approve bounded execution under W7-S07, with write-ahead accounting and
   immutable destinations. No study-design approval alone permits generation or spending.
5. Preserve outputs/failures; run unchanged mechanical mechanisms and separately
   authorized semantic review. Record disagreements and affected-unit eligibility.
6. Before numerical semantic scoring, approve precise P03 definitions and permission;
   authorize only a demonstrated minimal aggregation need. Before formal release,
   satisfy W7-S06/P04 and the actual P05 independence claims. No automatic milestone closure.

Draft proposals do not require all future scoring decisions. General recommendation
or abstention adjudication is not a blocker to mechanical counts or draft factual
review. Conversely, resolving G02 P03 alone would not create an independent population.

### D. Explicitly deferred work

- Equivalent-policy prompt changes, new baseline rules and multi-prompt optimization.
- General semantic scoring engines, weighted scores, automatic claim decomposition,
  LLM judges and numerical model rankings.
- New runner, CLI/publication framework, database, retrieval or agent architecture.
- Exhaustive citation diagnostics unless a chosen measurement requires them.
- Repeated hosted sampling, new model selection, additional paid experiments or
  action-quality metrics without a defined question and applicable approval.
- Independent AML expert validation unless an actual reviewer and authorized scope
  are established; independent authorship and owner-led review do not imply it.
- Public release/demo work and any Week 8 transition.

These are not automatic prerequisites for reviewing this draft. Current limitations
remain visible; deferral does not approve an otherwise unsupported claim.

### E. Proposed next bounded checkpoint - exactly one

**An owner decision checkpoint on this specification:** approve or revise the initial
question, population-independence/access policy and initial review scope, with actual
roles and explicit unresolved gates recorded. This would produce a bounded set of
accepted study decisions, not cases, assessments, scores or evaluator code. It should
precede dataset authoring or runtime work because eligibility and measurement rules
determine what those later artifacts must contain.

No implementation or feature branch is needed for that decision itself; any later
documentation/implementation branch is an owner-controlled Git choice. Do not begin
the next activity automatically. **STOP for owner review.**
