# Phase 2 Evaluation Protocol — DRAFT

> **DRAFT / NOT YET AN APPROVED EVALUATION STANDARD.** Scoring methods, semantic annotations and adjudication proposals in this document require human review. The five golden-case labels remain provisional. No numerical pass thresholds are assigned.

## 1. Purpose, repository basis and status

This draft proposes how to evaluate preliminary assessments of synthetic AML investigations. It separates structural acceptance, reference integrity, factual support, material coverage and recommendation quality so that success in one dimension cannot conceal failure in another.

The repository basis is `ee03f08` on `feature/phase-2-evaluation-protocol`. Git history records input contracts merged through PR #3 (`327e600`) and output contracts merged through PR #4 (`ee03f08`). The preceding read-only audit confirmed 144 passing local unit tests. That result establishes regression-test behavior, not assessment accuracy, semantic grounding or remote CI success. This documentation task does not rerun the suite.

Existing interfaces and decisions are documented in:

- [contracts.py](../../src/aml_triage/contracts.py): individual records, `InvestigationInput`, the four output models and contextual reference validation.
- [Contract tests](../../tests/test_contracts.py) and [golden-fixture tests](../../tests/test_golden_fixtures.py): existing acceptance and regression behavior.
- [DECISIONS.md](../../DECISIONS.md), especially ADR-009 through ADR-014: incomplete inputs, reference separation and output-validation boundaries.
- [Fictional labeling policy](../../specs/labeling_policy_v1.json) and [golden-case guidance](../../data/golden_cases/README.md): current provisional dispositions and synthetic-data limitations.
- [Project charter](../../PROJECT_CHARTER.md), [workflow research](../../specs/aml_workflow.md), [candidate domain requirements](../phase-1/DOMAIN_REQUIREMENTS.md) and [investigation workflow](../phase-1/INVESTIGATION_WORKFLOW.md): project direction and human-review boundaries.

The contracts and approved ADRs describe existing behavior. Evaluation categories, annotation fields, reporting conventions, dataset controls and implementation steps below are proposals unless explicitly identified as existing behavior. Earlier project-stage wording in other documents may predate PR #4; this draft does not modify those documents or historical decisions.

No recommendation generator, AML classifier, LLM investigation agent, automated verification system or complete triage pipeline is implemented by this draft. It asserts no production AML policy, SAR determination or regulatory compliance result. It does not finalize Phase 2, the labeling vocabulary or the five reference answers.

## 2. Existing contract and policy boundaries

### 2.1 Existing validation behavior

`InvestigationInput` checks the supplied record structure and explicit relationships. `InvestigationOutput` checks submitted structure and internal consistency. The separate [validate_investigation_output_references](../../src/aml_triage/contracts.py) function accepts already-validated models, checks exact case/alert identities and resolves typed citations without mutating either model.

The eight citation namespaces are `case`, `customer`, `account`, `counterparty`, `transaction`, `alert`, `evidence` and `verification_check`. Identifier matching is exact. An account reference appearing inside evidence facts is not automatically a supplied `account` record.

Preserve these existing allowances in any evaluator:

- Supplied transactions outside the alert subset may be cited, including G04's `TX-105`.
- Contextual evidence may have no transaction references. Counterparty collections may be empty and transaction counterparty IDs may be null.
- Questions and missing-information statements may have no citations. Abstention may have an uncited rationale and no factual findings.
- Factual findings, interpretations and both contradiction sides require citations. A provided recommendation also requires a cited rationale and at least one cited factual finding.
- References may recur across statements. Not every supplied record must be cited, and separately cited evidence and transactions need not reference one another.

Successful ID resolution establishes record existence only. It does not establish that a statement is true, that a citation supports it, or that a recorded verification was independently performed. Existing validation does not load reference answers, resolve a policy registry or interpret the fictional policy. The contract tests deliberately preserve this semantic boundary.

### 2.2 Existing fictional dispositions and provenance distinctions

The current fictional policy defines:

| Action | Existing rubric distinction |
| --- | --- |
| `close` | Adequate corroboration resolves the flagged concern, with no material unresolved question in the supplied review scope. |
| `investigate` | A material unanswered question remains without an established fictional referral condition. |
| `escalate` | An established fictional referral condition is met, regardless of other questions. |

REF-01 concerns at least two outgoing payments to the same supplier account after a documented instruction requiring senior review, together with a supplied independent register recording that the payee is not approved and no authorized change is recorded. Its current wording does not explicitly require proof that senior review was bypassed. Interpretation remains pending in decision D-02 below.

The output contract represents inability to recommend using `assessment_status="unable_to_recommend"` and explicit `recommended_action=null`. This is an assessment status, not a fourth disposition. All outputs require `recommendation_scope="preliminary"` and exact boolean `human_review_required=True`. The fictional policy does not yet define semantic abstention eligibility.

For semantic review, preserve the difference between a customer statement, a supplied ledger or document, a supplied check result and a reproducible derivation. Reporting that a customer claims a commercial purpose does not establish that purpose. Reporting a check's status does not establish that this software executed the check. Arithmetic agreement establishes agreement among supplied values, not document authenticity.

## 3. G01–G05 provisional-label audit

The input-supported observations below summarize the preceding input-and-policy review. The final column records proposed adjudication work, not new mandatory findings or approved label changes. All existing expected actions remain unchanged and provisional.

| Case and artifacts | Current provisional action | Input-supported observations | Uncertainty and pending adjudication proposals |
| --- | --- | --- | --- |
| G01 — [input](../../data/golden_cases/inputs/G01.json), [reference](../../data/golden_cases/references/G01_reference.json) | `close` | Four deposits total USD 34,150; each exceeds the supplied typical daily maximum. POS and bank reconciliation records agree, including a recorded zero unmatched amount. Supplied checks are resolved. A received promotion notice covers the flagged dates. | **D-01:** Decide whether this supplied corroboration is adequate for preliminary closure within the limited scope. The promotion notice is not independently authenticated merely because dates agree. The daily-range comparison requires customer-profile support as well as transaction support; the existing reference finding has no customer citation field. Consider whether promotion context is material to the closure explanation. Do not turn scoped closure into a claim that all suspicious activity is absent. |
| G02 — [input](../../data/golden_cases/inputs/G02.json), [reference](../../data/golden_cases/references/G02_reference.json) | `investigate` | A USD 48,500 incoming payment is flagged. The wholesale-goods purpose is a customer claim, its invoice reference is null, and the supplied commercial-purpose check records absent corroboration. Counterparty relationships are unverified. | Commercial records and the sender relationship remain unresolved. Bound absence claims to supplied records. The payment identifies a sender; an unverified relationship does not mean the sender is unidentified. The reference is consistent with these gaps, and no supplied REF-01 condition is established. Materiality and acceptable supporting citations remain for annotation review. |
| G03 — [input](../../data/golden_cases/inputs/G03.json), [reference](../../data/golden_cases/references/G03_reference.json) | `escalate` | Two outgoing payments total USD 35,500. Both follow the instruction timestamp. Register and payment evidence identify the same non-approved receiving account and no recorded authorized change. A supplied check has status `escalation_condition_met`. | **D-02:** Confirm REF-01's intended reading and the evidentiary role of supplied statuses. That status is a recorded result, not independent proof or new verification by this system. Examine the underlying register, instruction and payments. The instruction requires review before release; the input does not establish whether review occurred. The reference's question about payments proceeding "despite" the instruction must not become a finding that review was bypassed or fraud occurred. |
| G04 — [input](../../data/golden_cases/inputs/G04.json), [reference](../../data/golden_cases/references/G04_reference.json) | `investigate` | Four deposits total USD 37,300 and individually exceed the supplied daily maximum. Sales records are partial and not independently reconciled. The separate USD 32,000 wire has different invoice and recorded payment beneficiary accounts, with no verified relationship supplied. | The daily comparison requires customer-profile support. Explain that each deposit exceeds the daily range; do not compare a multi-day total directly with a daily bound. Reconciliation and recipient-relationship questions remain material. **There is no supported inference that the deposits funded the outgoing wire.** The reference preserves that limitation. Account mismatch alone is not REF-01, and a request to verify supplier instructions does not establish that instructions were supplied. |
| G05 — [input](../../data/golden_cases/inputs/G05.json), [reference](../../data/golden_cases/references/G05_reference.json) | `investigate` | A USD 27,000 outgoing payment has null counterparty and beneficiary-account references. An information request records `not_received`; the supplied beneficiary-information check is unresolved. The investigation is structurally valid. | **D-03:** Missing beneficiary information supports investigation but does not automatically justify abstention. Details and relationship records remain unresolved. No received response in the snapshot does not establish refusal or permanent nonresponse. "Supplier remittance" is a supplied description, not a verified relationship. No defined referral condition is established. |

G01 and G04 expose a reference-format limitation: their daily-range findings depend on customer-profile fields, while existing required-finding references list only transactions, evidence and checks. Proposing richer evaluation annotations does not change those reference files or impose new fields on the investigation contracts.

## 4. Proposed reporting conventions

All conventions in this section await approval under D-04.

1. Report each dimension separately, with category counts, numerator, denominator, skipped cases and reasons. Do not create a weighted overall score or numerical acceptance threshold.
2. Count every submitted candidate attempt in the attempt inventory, including missing or malformed output. Report structural failures before conditional downstream results; never discard them from the report.
3. Distinguish an invalid input from a poor assessment of a valid input. Where a stage lacks its prerequisites, report `not_run` and the reason rather than success. Execution failures are not semantic abstentions.
4. For conditional rates, identify the eligible population explicitly: structurally valid pairs, citation-resolved outputs, assessable claims or cases with approved annotations. Also disclose how many attempts were excluded at each stage.
5. Report no applicable items as `not_applicable`, with a zero denominator, rather than assigning a perfect score. Report unresolved annotations as unassessable and include their counts.
6. Split compound statements into atomic claims for review. Inspect assertions in rationale, findings, interpretations, questions, missing-information statements and contradiction descriptions, not only the factual-findings list.
7. Count each annotated material item once for completeness. Repetition and citation volume do not earn additional coverage; submitted text itself is not rewritten or deduplicated.
8. Preserve incorrect, unsupported and unassessable results separately. A plausible action does not erase fabricated verification or a material omission.
9. Report case-level results alongside claim/item counts so verbose outputs cannot hide failures through aggregation. Keep contaminated results visibly separate from independent evaluation evidence.

## 5. Proposed evaluation dimensions

These dimensions define proposed measurements, not approved release criteria. Each requires the reporting conventions above and the pending decisions in section 9.

### 5.1 Input and output structural validity

- **Data required:** Original input payload, submitted candidate payload or missing-output record, and contract version. Record whether validation uses the Python or JSON entry point.
- **Scoring categories:** Input accepted/rejected; candidate present/missing; output accepted/rejected; stage not run. Preserve validation errors and field paths. For negative-input regression cases, record whether expected rejection occurred.
- **Denominators:** Input results over all input-validation attempts; output acceptance over all candidate attempts expected to provide output. Report missing outputs separately within that population. Also report conditional output validity for valid-input attempts.
- **Failure examples:** Unsupported schema version, missing field, malformed list, duplicate input IDs or an incompatible assessment-status/action combination. The intentionally invalid duplicate fixture is a structural negative, not a sixth AML-labeled case.
- **Automation limits:** Existing Pydantic contracts reliably apply their declared rules. Passing them does not establish valid policy reasoning or true facts.
- **Human review:** Needed for contract changes and disputed requirements, not routine application of existing validators.

### 5.2 Citation identity and existence

- **Data required:** Structurally validated input/output pair and exact typed citations at every statement location.
- **Scoring categories:** Case/alert match or mismatch; citation resolved or unresolved in its declared namespace; contextual validation passed/failed/not run. Preserve error paths.
- **Denominators:** Case-level contextual outcomes over structurally valid pairs; resolved citation occurrences over all citation occurrences examined in those pairs. Empty permitted lists have no citation denominator and are not citation failures. Root identities still require checking for abstentions.
- **Failure examples:** Unknown ID, wrong namespace, root case mismatch or normalized identifier substituted for the submitted value.
- **Automation limits:** The existing function reliably checks identities and existence, stopping at the first mismatch. Complete occurrence-level reporting would need a separately approved evaluator diagnostic traversal; it must not alter contract behavior. Existence does not measure relevance or support.
- **Human review:** Normally unnecessary for exact lookup. Relevant support is reviewed under grounding. Preserve all eight namespaces and valid incomplete-input allowances.

### 5.3 Claim-level factual grounding

- **Data required:** Atomic candidate claims, text locations, exact supporting and opposing record/field pointers, attribution expectations and any reproducible derivation.
- **Scoring categories:** `supported`, `partly_supported`, `contradicted`, `not_established` or `unassessable`, as defined in section 6. Review the supplied citation set as well as whether the claim is supported elsewhere in the input.
- **Denominators:** Category counts over all reviewed atomic factual claims; supported claims over assessable reviewed claims, with unassessable and unreviewed counts disclosed. Report claims by output location and case. Report interpretive reasoning separately from factual support.
- **Failure examples:** A real transaction cited with the wrong amount; an uncited source elsewhere being used to excuse irrelevant submitted citations; a customer claim presented as confirmed purpose.
- **Automation limits:** Approved selected-field, Decimal arithmetic and timestamp checks can be deterministic. General prose entailment, compound-claim decomposition, attribution and source sufficiency cannot be assumed reliable automatically.
- **Human review:** Initially required for semantic judgments, acceptable supporting sets, the distinction between inference and fact, and assertions embedded in questions or contradiction descriptions.

### 5.4 Material finding completeness

- **Data required:** An adjudicated case-level inventory of material findings, materiality reasons, supporting pointers and acceptable equivalent expressions.
- **Scoring categories:** Covered with adequate support, partly covered, omitted, not applicable or unassessable. A fact mentioned with materially wrong content is not adequately covered.
- **Denominators:** Adequately covered findings over applicable, adjudicated material findings for each evaluated candidate. Report partial coverage and omissions separately. Disclose candidates that could not be reviewed; no findings inventory is inferred from every available record.
- **Failure examples:** Omitting G03's instruction when explaining REF-01, or omitting G04's beneficiary mismatch while discussing only cash deposits.
- **Automation limits:** Selected predicates can assist. Keyword presence, copied reference phrasing and citation count do not establish semantic coverage.
- **Human review:** Required to settle materiality, equivalent expressions and whether missing support changes the assessment. The current references are seeds for review, not exhaustive approved inventories.

### 5.5 Missing information and contradiction coverage

- **Data required:** Adjudicated material unresolved questions, missing-information items and contradictions, including the records on both sides and their relevance.
- **Scoring categories:** Adequately represented, partly represented, omitted, misrepresented, not applicable or unassessable. Track questions, missing information and contradictions separately.
- **Denominators:** Adequately represented items over applicable adjudicated items in each category, plus affected-output counts. No annotated contradictions means no contradiction-coverage denominator, not proof that every possible conflict was excluded.
- **Failure examples:** Hiding G04's account discrepancy, presenting unavailable beneficiary data as confirmed, or describing a received explanation as a resolved question.
- **Automation limits:** Exact field differences and nulls can be detected selectively. Their materiality, genuine contradiction, resolution and treatment in prose require review. Empty permitted citation lists are not automatically semantic failures.
- **Human review:** Required for uncertainty scope and material conflict interpretation. A structurally valid contradiction with two cited sides is not proof that the sides conflict semantically.

### 5.6 Preliminary recommendation quality

- **Data required:** Applicable fictional rubric version, an adjudicated action and reasoning, clause-level policy basis and any explicitly approved alternatives.
- **Scoring categories:** Agreement with the adjudicated action, approved alternative, disagreement or unassessable; separately assess rationale adequacy and policy-condition support. Report recommendation and abstention status separately.
- **Denominators:** Action comparisons over assessable submitted recommendations with adjudicated actions; disclose abstentions, invalid outputs and unadjudicated cases separately against all attempts. Report class confusion counts and rationale judgments independently. Any later per-class precision/recall must disclose sample counts and small-sample limitations.
- **Failure examples:** Closing G02 without addressing the commercial gap; escalating G04 solely for a mismatch; treating G03's status string as a complete REF-01 argument.
- **Automation limits:** Action comparison is deterministic after adjudication. Approved checks may examine explicit policy predicates, but adequate corroboration, materiality and persuasive reasoning remain semantic judgments.
- **Human review:** Required for rubric interpretation and annotation approval. Correct action alone does not establish adequate reasoning. Alternatives require explicit adjudication, not automatic tolerance of every action.

### 5.7 Appropriate abstention

- **Data required:** Adjudicated recommendation eligibility, acceptable abstention reasons, applicable policy and the candidate's status, action and rationale.
- **Scoring categories:** Supported recommendation, justified abstention, unjustified abstention, unsupported commitment or unassessable. Structural status/null consistency remains a separate existing check.
- **Denominators:** Recommendation and abstention counts over structurally valid assessment outputs; judged appropriateness over outputs with approved eligibility annotations. Also report invalid/missing output counts over all attempts and recommendation errors alongside recommendation coverage.
- **Failure examples:** Automatically abstaining whenever information is missing, or asserting a recommendation without an adjudicated sufficient basis. G05's missing beneficiary information does not automatically justify abstention.
- **Automation limits:** Structural consistency can be checked reliably. Semantic eligibility is not yet defined by the fictional policy. Invalid input or an execution failure must not be counted as a valid assessment abstention.
- **Human review:** Required under D-03 before any eligibility rule or abstention-quality score is implemented. No fourth AML disposition is proposed.

### 5.8 Fabricated verification and unsupported certainty

- **Data required:** Claims across all output text, source/provenance annotations, forbidden inferences and the supplied record scope.
- **Scoring categories:** No identified issue, fabricated verification, attribution overstatement, invented financial relationship, unsupported intent/legal assertion, other unsupported certainty or unassessable. "No identified issue" describes review scope, not a guarantee of truth.
- **Denominators:** Issue counts over reviewed applicable assertions and affected outputs over semantically reviewed outputs. Disclose unreviewed text and structural failures separately. Preserve concrete examples rather than combining severity into a weighted score.
- **Failure examples:** "We contacted the supplier," "the deposits funded the wire," or "the customer committed fraud" when the supplied records establish none of those claims.
- **Automation limits:** Selected contradictions or phrases can be flagged for review. Phrase matching cannot reliably distinguish an assertion from a quotation, hypothetical or explicit warning.
- **Human review:** Required to assess context, attribution and certainty. A supplied `verified` or `escalation_condition_met` value is not new verification by this system.

### 5.9 Preliminary scope and human-review compliance

- **Data required:** Candidate scope/review fields and all output prose.
- **Scoring categories:** Exact field compliance/noncompliance; prose consistent/inconsistent with preliminary human review; unassessable text. Record these separately.
- **Denominators:** Field outcomes over all candidate attempts, including missing/invalid fields; prose outcomes over candidates whose text was reviewed. Disclose unreadable or missing candidates. A review-required flag does not prove review occurred.
- **Failure examples:** Boolean `False` or numeric `1` in place of exact `True`; final scope; prose asserting final closure, completed regulatory filing or an institution's final SAR decision despite correct flags.
- **Automation limits:** Existing models reliably enforce the literal scope and boolean. They do not detect every conflicting statement or execute human review.
- **Human review:** Required for semantic scope and any assertion of actual human or regulatory action. No production regulatory requirement is derived from the fictional rubric.

### 5.10 Reference-answer leakage and dataset independence

- **Data required:** Dataset partitions and lineage, input/candidate hashes, authorized instruction manifest, generation-context records, annotation/reference access records and exposure history.
- **Scoring categories:** No observed unauthorized exposure, confirmed contamination, uncertain exposure or not audited; separately record development/held-out eligibility and family-partition violations.
- **Denominators:** Audited candidate contexts over all candidate attempts; exposure findings over audited contexts; partition violations over audited families. Report unaudited attempts explicitly. Exposed or contaminated cases cannot be counted as independent held-out evidence.
- **Failure examples:** A reference rationale in a generation prompt; a held-out counterfactual sibling used for tuning; evaluation annotations supplied as evidence.
- **Automation limits:** Allowlisted loading, hashes, manifest comparisons and access tests can enforce known boundaries. The four existing reserved evidence-fact keys are not a general prose-leak detector. Lexical overlap alone does not prove leakage.
- **Human review:** Required for indirect answer cues, ambiguous context exposure and dataset provenance. Ordinary disposition words in legitimate evidence are not forbidden merely because labels use them.

## 6. Proposed evaluation-only semantic annotation format

This is a format sketch for review, not an implemented schema or a populated annotation set. No case annotations, reference edits or new output fields are created by this document. Keep case-level expectations separate from candidate-specific claim reviews, with both outside `InvestigationInput`, `InvestigationOutput` and future candidate prompts.

| Record group | Proposed fields and types | Purpose and pending review |
| --- | --- | --- |
| Version and identity | String format/dataset/rubric/contract versions; case ID; input digest; candidate ID/output digest when reviewing a candidate | Tie every judgment to immutable artifacts. Candidate-specific records must not be mistaken for case-level expectations. |
| Typed field pointer | `record_type` from the existing eight namespaces; exact string `record_id`; record-relative JSON Pointer string; original input digest | Identify both a supplied record and a precise field. Resolve the typed ID first, then the pointer within that record; do not use mutable collection position as its identity. |
| Atomic candidate claim | Claim ID; output field path; exact text span and offsets tied to the output digest; atomic proposition; claim kind | Review each assertion without rewriting candidate text. Compound statements need multiple review entries. Distinguish factual propositions from interpretations and questions. |
| Support and attribution | Lists of acceptable supporting-pointer sets and opposing pointers; source kind; required attribution; derivation/selection description where applicable | Express conjunctions of sources and distinguish customer statements, supplied records, supplied checks and derived calculations. Preserve currency, time window and record-selection assumptions. |
| Claim judgment | One proposed grounding category; reviewer explanation; submitted-citation sufficiency; supporting-input judgment | Distinguish a claim supported elsewhere from one supported by its submitted citations. Exact category policy awaits D-04. |
| Material finding | Finding ID; proposition; materiality rationale; supporting sets; applicability; candidate coverage judgment | Track material findings and omissions once each; allow approved equivalent wording. |
| Uncertainty or contradiction | Item ID; question/missing-information/contradiction kind; materiality rationale; relevant pointers; opposing sides where applicable; coverage judgment | Preserve unresolved issues without claiming that the evaluator performed an investigation. |
| Recommendation and policy basis | Provisional or adjudicated state; action; explicitly approved alternatives; criterion IDs; clause-level basis and unknowns; adjudication rationale | Compare against reviewed reasoning rather than copying reference prose. An empty alternatives list does not finalize the current labels. |
| Abstention eligibility | Pending or adjudicated state; eligibility judgment; reasons and required limitations | Remain unset/pending until D-03 is resolved. Eligibility is separate from structural permission to abstain. |
| Forbidden inference | Inference ID; proposition or inference type; scope; source-based explanation | Record prohibited extrapolations such as unsupported fund tracing or software-executed verification. These records are evaluation material, not model inputs. |
| Review and disagreement | Reviewer identity or stable role ID; role/qualifications as actually known; review state; separate judgments; disagreement reason; adjudicator identity/role and rationale; revision history | Preserve dissent and accountability. Do not invent a qualified AML reviewer, approval or adjudication event. |

Proposed grounding categories:

- **Supported:** The submitted citation set supports the whole atomic factual claim with appropriate attribution and scope, including a reproducible approved derivation where needed.
- **Partly supported:** Some content or a necessary qualifier is supported, but the complete claim is not. Split avoidable compound claims before using this category; do not award an arbitrary fractional score.
- **Contradicted:** Supplied material directly conflicts with the claim. Record both sides and any unresolved source conflict rather than silently choosing a convenient source.
- **Not established:** The claim goes beyond what the supplied support establishes. This does not necessarily mean the claim is false outside the investigation snapshot.
- **Unassessable:** The evaluator cannot make a defensible judgment because the annotation, interpretation rule or review basis is unresolved. Do not use this category to hide an assessably unsupported claim merely because input information is missing.

These definitions and category precedence remain proposals under D-04. Attribution and source sufficiency need adjudication: a check can support the statement that a result was recorded without proving independent execution or establishing every underlying proposition on its own.

## 7. Proposed dataset isolation and leakage controls

### 7.1 Development, held-out data and limitations

Treat G01–G05 as development/regression examples. Their inputs, references and labels have already been reviewed; they cannot now be redesignated independent held-out cases. Five selected synthetic cases can expose particular failures and exercise regression behavior. They cannot establish real-world AML effectiveness, generalization, calibrated abstention, analyst time savings or reliable class-level performance.

Proposed future partition rules, pending D-08:

- Define case-family membership and development/held-out assignments before prompt or rule tuning.
- Keep a base case and all related counterfactual variants in the same partition. Renaming IDs or paraphrasing a development example does not create independent held-out evidence.
- Freeze input snapshots and adjudicated annotations for a held-out release. Version changes to facts, labels, policy interpretation, family membership and annotations; preserve lineage and old results.
- Record which examples, references and failure analyses were exposed to developers or candidate-generation context. Once a held-out case is used for tuning, disclose the exposure and treat subsequent use accordingly.
- Report case and family counts, label distribution, unadjudicated items and reviewed population. Do not imply that a larger count of related variants creates equivalent independent coverage.

Future scenario proposals include additional corroborated closure cases, individually absent or unknown REF-01 conditions, conflicts between checks and underlying records, and cases with adjudicated abstention eligibility. No additional fixtures are generated here.

For counterfactual sensitivity, change one meaningful condition at a time and keep dependent records consistent unless contradiction is intentional. Examples for later approval include G03 payment timing or authorized-change variants; G04 removing a beneficiary mismatch while leaving reconciliation unresolved; and G01 losing corroboration while retaining a promotion claim. Removing one concern does not automatically imply closure. Consistent identifier renaming and order changes should not change substantive judgments.

### 7.2 Generic instructions versus prohibited answers

Candidate access to generic rubric definitions remains pending under D-06. An approved generic instruction would explain the fictional actions and applicable referral criteria uniformly, without a case-specific expected action, rationale or annotation. The input's policy ID alone does not supply policy content, and existing validators do not perform policy lookup.

Prohibited candidate context includes case-specific reference answers, expected outcomes, reference rationales, adjudication notes, semantic scoring annotations and held-out examples used as demonstrations. Approval of generic policy instructions must not be treated as permission to supply those artifacts.

Proposed controls:

1. Use separate, explicit loading boundaries for candidate inputs/instructions and evaluator-only references/annotations. Construct and audit the actual candidate request from an allowlist.
2. Freeze or record the candidate before the scoring side loads its case-specific answers. Keep evaluation diagnostics and feedback out of later held-out candidate context.
3. Version and identify the authorized generic instructions separately from the fictional policy and reference files. Record their exact content and digest for each future run.
4. Test known forbidden access and request-content paths. Audit prose for indirect answer information; do not rely only on reserved key names or ban ordinary disposition words.
5. Mark confirmed contamination and uncertain exposure explicitly. Do not present contaminated results as independent performance evidence.

G03's supplied `escalation_condition_met` status is a legitimate current input record but an outcome-revealing cue. Other supplied check findings also simplify the task. Record this limitation when interpreting results. A future task without such cues would need a separately approved dataset design; do not silently remove or rewrite existing checks.

## 8. Proposed evaluator stages and automation scope

No evaluator is implemented by this document. Preserve the separation between contract validation and semantic evaluation.

| Stage | Proposed behavior | Result and boundary |
| --- | --- | --- |
| 1. Load versioned artifacts | Load the frozen input and candidate output with dataset, contract, rubric and evaluator versions and artifact identities. Record authorized instruction and exposure information when candidate generation exists. | Reproducible evaluation packet. Inputs, outputs, references and annotations remain separate artifacts. |
| 2. Structural validation | Apply existing `InvestigationInput` and `InvestigationOutput` validation; retain original payloads and errors. | Separate input/output outcomes. Invalid input is not an AML disposition; a malformed candidate is not repaired. |
| 3. Contextual citation validation | Invoke the existing reference-validation function on validated models. Check exact root identities and every typed citation location. | Contextual pass/failure and useful paths. Preserve current incomplete-input allowances and fail-fast behavior. Additional exhaustive diagnostics require an evaluator-only implementation decision. |
| 4. Approved deterministic factual checks | Apply only reviewed explicit predicates with recorded source selection, arithmetic, currency and timestamp assumptions. Unsupported evidence shapes remain outside that check's scope. | Predicate results and limitations. Do not add universal facts schemas, financial reconciliation requirements or production decision logic to contracts. |
| 5. Human-reviewed semantic annotations | Apply approved claim, completeness, uncertainty, contradiction, recommendation and abstention annotations; record disagreements and unresolved review. | Separate semantic categories and explanations. Never infer that supplied verification labels prove software execution or independent truth. |
| 6. Transparent reporting | Report each dimension, its numerator/denominator, exclusions, errors, review scope, contamination and versions. Retain concrete failures. | Evaluation diagnostics and annotation records stay outside `InvestigationOutput`; no new output fields, weighted composite or invented pass threshold. |

The proposed initial approach combines deterministic structural/reference checks with human semantic review. Selected factual checks can be added after their assertions are approved. Human review effort is a real cost; two independent reviewers would improve disagreement visibility where feasible, but a qualified AML reviewer is not assumed to exist. D-07 must assign actual responsibilities and disclose single-reviewer limitations where necessary.

An LLM judge is optional future work, not a prerequisite or approved implementation. It would require a bounded budget, human-calibrated examples and tests for evaluator bias, prompt injection, instability and correlated candidate/judge mistakes. It must not substitute for adjudication or create unsupported accuracy claims. No model calls or new dependencies are authorized by this draft.

## 9. Decision register — pending human adjudication

Every item below is **pending human adjudication**. The audit table does not resolve these decisions or authorize evaluator coding.

| ID | Decision required | Evidence or question to resolve | State |
| --- | --- | --- | --- |
| D-01 | G01 closure corroboration | Is the supplied POS/deposit agreement adequate within the review scope? Is promotion context material, and what attribution and profile support must the closure explanation preserve? | Pending human adjudication |
| D-02 | REF-01 interpretation and supplied verification statuses | Does REF-01 apply to the recorded post-instruction payments regardless of whether senior review occurred? Define how underlying records and recorded statuses support the fictional criterion without inventing bypass, intent or new verification. | Pending human adjudication |
| D-03 | Abstention eligibility | Define when a valid investigation supports a preliminary action versus inability to recommend. Preserve G05's current provisional investigation label; missing information alone is not an approved abstention rule. | Pending human adjudication |
| D-04 | Grounding judgments and completeness criteria | Approve atomic-claim categories, attribution, acceptable support sets, material inventories, partial/unknown handling, reporting denominators and the evaluation-only annotation format. Include customer-profile support for G01/G04 daily comparisons. | Pending human adjudication |
| D-05 | Acceptable alternative preliminary actions | Decide whether any case admits an alternative and document why. Do not silently accept every action, replace an expected action or finalize current provisional labels. | Pending human adjudication |
| D-06 | Candidate access to generic rubric definitions | Approve the exact generic policy instructions and exposure boundary, distinguishing them from prohibited case-specific answers and evaluation notes. No policy registry lookup is introduced. | Pending human adjudication |
| D-07 | Human adjudication responsibilities | Assign reviewer/adjudicator identities or roles, independent-review procedure, disagreement handling and approval authority. Disclose qualifications and availability as actually known. | Pending human adjudication |
| D-08 | Future held-out evaluation data | Approve scenario families, partition ownership, counterfactual isolation, annotation/version freeze and exposure handling. Existing G01–G05 remain development/regression material. | Pending human adjudication |

## 10. Proposed next steps and checkpoint limits

1. Independently review this draft and resolve or explicitly defer the decision-register items with reasons.
2. Separately authorize creation and adjudication of evaluation-only annotations; preserve original reference artifacts and their history.
3. Approve a small evaluator implementation that reuses existing contract checks and adds independent reporting, without changing investigation contracts.
4. Add reviewed factual and semantic regression examples covering wrong amounts, irrelevant citations, material omissions, contradictory sources and fabricated verification. Preserve existing tests and input fixtures.
5. Separately authorize future scenario creation and held-out partitioning before evaluating recommendation-generation capability.

This checkpoint creates only this draft document. It creates no annotation records, evaluator code, candidate assessments or synthetic fixtures and changes no existing labels, policy, contracts, tests or project records. No evaluation accuracy, model performance, finalized labels, successful remote CI or recommendation-generation capability is claimed.

**DRAFT / NOT YET AN APPROVED EVALUATION STANDARD. Stop for independent human review before implementation.**
