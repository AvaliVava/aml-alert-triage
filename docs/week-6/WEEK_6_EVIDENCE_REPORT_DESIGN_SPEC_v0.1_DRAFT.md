# Week 6 evidence and narrative report design specification - v0.1 DRAFT

**DRAFT — NOT APPROVED FOR IMPLEMENTATION.**

**Checkpoint:** Specification only. In the current revision instruction, the owner accepted the offline source-first direction, E01-E06, one separate versioned JSON companion, content separation, conspicuously qualified deterministic conflicts, hard structure/identity/reference gates, explicit unknown optional provenance, and the first-slice/integration, conflict and provenance refinements below. This records design-level approval, not independent AML expert validation. The exact approval timestamp was not supplied. The detailed implementation contract, code, tests, experiments, hosted requests, scoring, commits and publication remain subject to separate authorization.

**Repository inspected:** `main` at `3435079aa7f33a33e3e1c9812fd7ebc43d1f1ed7` (PR #17). The tracked working tree and index were clean before drafting; the existing handoff ZIP was untracked. Inspection and this document do not change those historical artifacts.

**Decision convention:** The design-level choices expressly recorded above and in sections C-F/H-I are owner-approved constraints; they are not being submitted for reapproval. Exact schema fields/status spellings, template wording, interfaces, serialization details and executable tests remain implementation-contract proposals unless expressly identified as accepted design. Words such as "must" describe those design constraints, not authorization to implement them. Existing behavior is identified separately. The prominent draft status remains in force.

## Milestone and authoritative context

The [roadmap](../../ROADMAP.md) defines Week 6 as **"Evidence validation, narrative drafting and integration"**, with **"Full pipeline, integration tests, grounded report examples"** as required evidence. This first slice would contribute evidence assembly and bounded narrative/report composition; it would not complete Week 6 by itself.

Read alongside the [charter](../../PROJECT_CHARTER.md), [current status](../../PROJECT_STATUS.md), [worklog](../../WORKLOG.md), [decisions](../../DECISIONS.md), [evaluation protocol draft](../phase-2/EVALUATION_PROTOCOL_DRAFT.md), [Week 5 experiment specification](../week-5/CONTROLLED_EXPERIMENT_SPEC_DRAFT.md) and [owner-approved Week 5 closure](../week-5/WEEK_5_MILESTONE_CLOSURE_DECISION_v0.1_2026-11-01.md). Week 5's engineering comparison is closed; its outputs do not establish semantic correctness. Historical pre-implementation descriptions in the charter, roadmap progress notes and ADR-015 are not evidence that the now-implemented assessment/audit components are absent.

## A. Problem definition and assurance boundaries

| Distinction | What establishes it | What it does not establish |
| --- | --- | --- |
| Syntactically and structurally valid assessment | JSON parsing plus `InvestigationOutput.model_validate_json`, including custom consistency validators | A true claim, adequate rationale, authentic source or correct recommendation |
| Resolved citation | Exact typed identifier exists in the supplied investigation, checked by `validate_investigation_output_references` | That this source supports the cited sentence or that two cited records have the relationship asserted |
| Deterministic source-field check | A named, versioned predicate compares eligible supplied fields under explicit prerequisites | General statement meaning, commercial purpose, evidence authenticity or completeness |
| Substantively supported claim | Applicable evidence, attribution, scope, qualifications and complete-statement meaning justify the assertion under an approved review rule | Independent real-world verification merely because input records are internally consistent |
| Independently verified real-world fact | Suitable independent authority and an actual verification process outside this synthetic prototype | Nothing in this first slice supplies that authority or process |

The proposed slice would establish traceable transcription of allowlisted supplied fields, limited deterministic comparison results, candidate-content preservation and visible uncertainty. It would not judge arbitrary prose, authenticate documents, prove customer intent, choose an AML action, certify a recorded check, or establish that human review occurred. A correct template rendering is a software property; it is not independent AML validation.

Existing evidence makes this boundary necessary: `OpenAIAssessmentService._validate` uses the auditor's three mechanical stages for its `validated` service status. A restricted fact conflict does not change those stages. The [service tests](../../tests/test_openai_service.py) deliberately preserve this behavior for an incorrect amount and an unsupported authentication assertion. The proposed companion must inspect restricted results separately without changing legacy statuses or silently accepting them as substantive approval.

## B. Existing component reuse

| Existing interface | Reuse in the proposal | Relevant existing regression evidence and limit |
| --- | --- | --- |
| [InvestigationInput and InvestigationOutput](../../src/aml_triage/contracts.py) | Validate the same input/output contracts; preserve nulls, contextual evidence, permitted uncited questions and abstention | [test_contracts.py](../../tests/test_contracts.py): aggregate/reference tests; `test_abstention_accepts_null_action_and_uncited_rationale`, `test_human_review_requires_exact_boolean_true`, `test_recommendation_scope_requires_preliminary` |
| `validate_investigation_output_references` in the same module | Resolve exact case/alert and typed citations; reject invalid references without guessing | The contract reference tests also demonstrate that cited evidence and transactions need not link to one another; existence is not support |
| [audit_packet / audit_packet_files](../../src/aml_triage/auditor.py) | Reuse independent validation stages, diagnostics, artifact identities, restricted results and all nine semantic `not_evaluated` entries | [test_auditor.py](../../tests/test_auditor.py): `test_false_claim_with_real_citations_passes_only_mechanical_checks`, `test_recognized_amount_results_do_not_change_mechanical_or_semantic_stages`, file-preservation tests |
| [check_transaction_amounts](../../src/aml_triage/transaction_amount_checks.py) | Consume its results through the auditor; do not create a second amount-prose parser | [test_transaction_amount_checks.py](../../tests/test_transaction_amount_checks.py): exact Decimal/currency/direction predicates, ambiguous references, outside-grammar text and record-relative pointers |
| [assess_investigation](../../src/aml_triage/deterministic_baseline.py) | Existing baseline producer for a later integration test/caller | [test_deterministic_baseline.py](../../tests/test_deterministic_baseline.py): all 55 inputs, determinism, contextual validation and conflicting bank-side recipient evidence |
| [OpenAIAssessmentService.assess / AssessmentRun](../../src/aml_triage/openai_service.py) | Existing hosted boundary and execution bundle; later tests inject a mock client/transport | [test_openai_service.py](../../tests/test_openai_service.py): original-text preservation, SDK parse mismatch, unknown citations, refusal/incomplete output, disabled live guard and no retries |
| [build_assessment_prompt](../../src/aml_triage/openai_prompt.py) | Existing definition of validated-input canonical JSON, prompt version/hash and candidate exposure | `test_prompt_version_hash_and_exact_supplied_data`; no manifest, baseline, reference or review content is added to generation |
| [evaluate_evidence_relationships](../../src/aml_triage/evidence_relation_checks.py) | Preserve as a separate, optional future source of explicitly scoped results | [test_evidence_relation_checks.py](../../tests/test_evidence_relation_checks.py) separates true difference with insufficient citations from false equality with both citations. The implementation is G04/annotation-bound, not generic; first-slice operation would not require it or generate annotations |
| [generate_development_batch](../../src/aml_triage/synthetic_generator.py) and existing development fixtures | Existing tracked test inputs and lineage, not a new generation task | [test_synthetic_generator.py](../../tests/test_synthetic_generator.py): reproducibility, hashes, references and incomplete evidence. Generator metadata remains outside candidate generation |
| [hybrid_review_preview.verify / json_pointer](../../research/evaluation_calibration/hybrid_review_preview.py), [validate_register / build_reconciliation](../../research/evaluation_calibration/g02_reconciliation.py) | Reuse established integrity conventions and regression lessons; retain G02 tools unchanged | [test_g02_reconciliation.py](../../tests/test_g02_reconciliation.py) checks raw/canonical distinction, spans, citations and draft/scoring guards. These are case-specific research interfaces, not dependencies to import into the application report builder |

The existing [baseline CLI](../../scripts/run_baseline.py), [hosted CLI](../../scripts/run_openai_assessment.py) and [auditor CLI](../../scripts/audit_packet.py) already perform generation/auditing and non-overwriting publication in their respective scopes. No replacement service, new API client or experiment runner is proposed.

`InvestigationOutput` would remain unchanged. The companion would consume the original assessment and reference its fields; report metadata and narrative units would live in a separate artifact. It would not insert a `narrative`, score or provenance field into the existing output, or relabel/rewrite any producer field.

## C. Proposed minimal evidence-package contract

Proposed boundary: an offline composer consumes original investigation JSON bytes, original candidate JSON bytes/text when available, and explicitly supplied provenance/expected identities. It performs no assessment generation. A service bundle would supply its exact `candidate_json`, not its whole JSON envelope as an `InvestigationOutput`. No model object reserialization would replace original candidate text. Final function/module names are deferred to implementation approval.

### Proposed structured sections

| Section | Minimal proposed contents |
| --- | --- |
| `report_schema_version`, `composer_version`, `template_version` | Explicit report and transformation versions; values assigned only when implementation is authorized |
| `report_state` | `qualified_companion` or `rejected`; describes report eligibility only, never AML correctness or semantic pass |
| `case_identity` | Validated case/alert IDs are mandatory for an accepted companion; null is permitted only in rejected diagnostic results where validation could not establish them |
| `artifacts` | Mandatory exact supplied input and candidate identities/digest bases; original-byte digest/size where bytes were supplied, or exact candidate-string UTF-8 digest/size; separately labeled canonical validated-input digest when available; optional source-bundle digest; every supplied expected identity and its match outcome |
| `provenance` | Mandatory rule/check identities and audit-representation bindings as detailed below; available report/package/Pydantic/auditor/check versions. Producer identity, model, SDK execution metadata, prompt IDs, provider-side properties and other optional run metadata may be null with explicit availability/evidence status |
| `source_records` | Unique `(record_type, record_id)` entries, exact input-root pointers and faithful supplied record snapshots; all eight namespaces, including unflagged/contextual records. Account-reference strings inside evidence remain field values, not invented account records |
| `source_observations` | Allowlist rule/template ID, exact rendered text/value, source bindings and allowed transformation. No source-sufficiency or authenticity verdict |
| `candidate_content` | Exact assessment scalar fields, ordered statements and citations, complete contradiction descriptions/sides, original candidate JSON pointers and statement hashes; occurrence identities remain distinct |
| `validation` | Existing mechanical stages, reasons and diagnostics; complete restricted-check results/coverage with their own scope/status. New identity/pointer/composition gates remain separately named |
| `source_conditions` | Missing-member versus explicit-null versus unsupported value states for eligible inspected fields; paired source excerpts or existing check results where available; no universal absence or contradiction detector |
| `narrative_units` | Ordered template-generated or candidate-attributed units, each with provenance links as defined in section E |
| `limitations` | Unchecked text locations/reasons, unimplemented comparisons, unavailable metadata, restricted diagnostic coverage and all nine broad semantic states |

### Owner-approved provenance requirements; detailed encoding still proposed

For any accepted `qualified_companion`, the following bindings are mandatory:

- Exact supplied investigation payload identity and digest basis, and exact supplied candidate payload/text identity and digest basis.
- Validated case and alert identities.
- Actual typed source-record and field-pointer bindings for every generated source observation, including parent/key bindings for scoped missing-member observations.
- Explicit rule/check identity for every generated deterministic comparison; checker version, inspected fields and result remain traceable.
- Existing audit results bound to the exact input and candidate representation actually audited, with their digest bases.
- Candidate occurrence identity/location and unchanged original submitted citations, including permitted empty lists.

Any supplied expected hash or other expected identity must match the actual payload or applicable verified binding. A mismatch is a hard rejection, including when the metadata containing that expectation is optional. Unknown optional provenance cannot waive a mandatory binding. Rejected diagnostic results may retain unknown mandatory identities when the failure itself prevents establishing them; they are not accepted companions.

Producer identity, model, SDK execution metadata, prompt identifiers, provider-side properties and other optional run metadata may be absent. Preserve explicit null/unknown values with reasons rather than guessing or rejecting solely for their absence. For such metadata, distinguish **verified against supplied evidence**, **recorded but not independently verified**, and **not supplied or unavailable**. Exact JSON encoding of these evidence states remains proposed. Even the first state proves only the specified comparison/binding, not provider authenticity or real-world truth. Local Git, environment-variable, credential and network discovery are not prerequisites for the offline composer.

An existing audit would remain attributable to its actual input representation. Replaying it on original raw input can legitimately change its artifact digest/basis from a hosted audit on canonical input. Preserve both identities; do not claim identical audit bytes when only stage outcomes should agree. `audit_packet` identities are caller labels, not authenticated provenance.

### Proposed source binding

Each field binding would identify: input original-byte SHA-256, typed record ID, input-root record pointer (for example `/transactions/0`), record-relative field pointer (for example `/amount`), full input pointer, and exact decoded original JSON value. The record ID at that pointer must match. JSON Pointer escaping would follow `~0`/`~1`; pointer validity and exact values would be checked against the bound document. Typed/normalized values used in arithmetic would be recorded separately, with the transformation named. A model default for an omitted field would not be presented as a value actually supplied in the original JSON.

Proposed original-byte SHA-256 means exact file/payload bytes, including LF/CRLF, whitespace and serialization. For a service candidate available only as a string, record `utf8_encoded_candidate_text`, not a claim to possess HTTP-envelope bytes. The separately named canonical input digest would use the existing prompt builder's validated-model JSON definition. It must never substitute for a frozen original-byte identity. Unavailable original bytes would block a report claiming that binding; they would not be reconstructed from a model dump.

Report generation would not discover secret-bearing configuration, perform Git/network lookups or load references/adjudications. Source hashes identify content, not truthful authorship or authenticated execution. Expected hashes are supplied expectations; a newly computed hash alone is not verification against a previous identity.

## D. Proposed initial factual-content allowlist

**E01-E06 are owner-approved at design level, without expansion. Implementation is not authorized.** Their detailed schema/template encoding remains subject to the separate implementation contract. They deliberately avoid new AML decision rules, broad prose extraction and new beneficiary/policy evaluators. Other source fields can remain visible as exact record snapshots without becoming generated factual conclusions.

| Design-approved rule | Source fields and permitted transformation | Required provenance | Missing/null behavior, ambiguity and qualification |
| --- | --- | --- | --- |
| E01 - supplied investigation identity and alert scope | `/case/case_id`, `/case/primary_alert_id`, `/alert/alert_id`, `/alert/transaction_ids`. Transcribe identities/list membership as supplied | Case/alert typed records and exact pointers; resolve referenced transactions | Invalid explicit references already fail the contract. Alert membership does not establish suspiciousness or exclude contextual transactions from the package |
| E02 - individual transaction observation | Transaction ID, amount, currency, direction, type, aware timestamp, account ID and nullable counterparty ID. Format validated Decimal amount without rounding; retain original value and timestamp | Transaction record plus each used field; referenced account/counterparty only where actually supplied | Null counterparty means no counterparty reference supplied, not unknown payment recipient. Do not infer payment purpose, account ownership beyond explicit contract links, fund tracing or legitimacy. Do not silently convert timestamps or currencies |
| E03 - recorded profile interval | `/customer/expected_monthly_activity/{minimum,maximum,currency}` and optional paired daily cash bounds. Transcribe with their explicit monthly/daily labels | Customer record and exact field pointers | Say "the supplied profile records", not "the customer personally stated". Omitted optional bounds differ from explicit null. No single-payment limit, materiality judgment, profile-fit conclusion or monthly-versus-transaction threshold comparison is generated |
| E04 - attributed source excerpts | Exact `Evidence.source`, `evidence_type`, `verification_status`; selected original JSON facts: a `customer_explanation` string `/facts/claim`, or `supplier_invoice`/`wire_payment_record` `/facts/beneficiary_account_ref`; verification check `check_type`, `status`, `findings` and explicit evidence links | Exact evidence/check typed ID, input-root and field/list-item pointers; source/type metadata retained | Quote as a supplied record entry, never a new verification. A customer explanation remains a recorded claim. A supplied verification status does not establish that the composer independently executed verification. Unsupported fact shapes get no paraphrase. Preserve conflicting excerpts separately; do not pick a winner. A missing invoice reference and populated wire reference do not establish mismatch |
| E05 - scoped field availability | Inspect only E01-E04 eligible fields; identify missing JSON member, explicit null, empty/unsupported value or supplied usable value without conflating them | Parent record pointer and exact queried key; explicit-null pointer when it exists | A missing member has no resolvable child pointer: bind the parent/key and report non-membership. State the exact supplied-record scope. Do not infer missing documents globally, an unanswered request without a source, or a disposition from any gap |
| E06 - existing restricted transaction comparison | Reuse the existing checker through auditor `deterministic_fact_checks`, with its exact coverage/outcome names and two supported whole-statement amount grammars; no second amount parser or semantic generalization. Display exact claimed/recorded Decimal and currency values, and direction only when checked by that predicate | Candidate finding/citation location, transaction ID and each source field pointer, checker/predicate version and result | Ambiguous references, outside-grammar text or failed prerequisites stay `not_checked`/`not_evaluated` with existing reasons. A match validates only the listed fields. A conflict is prominent; neither outcome validates the whole assessment |

Illustrative proposed template, not a generated result: "Supplied transaction {ID} records {currency} {amount} as a {direction} at {original timestamp}." Each substituted field would have its own binding. Exact quoted source text remains untrusted content; punctuation inside a quote cannot authorize an instruction or become an unattributed composer claim.

Proposed initial exclusions: new multi-record totals, currency conversion, profile-deviation materiality, source authenticity, inferred purpose/intent, authorization/fraud findings, new general invoice/wire comparison logic, REF-01 reimplementation and automatic recommendation selection. Existing baseline observations about such matters would remain candidate-attributed. The annotation-bound G04 evaluator would not be generalized by substituting generated IDs. Future derivations require a specific approved predicate and tests, not an expanded regex or a rule inferred from a case label.

## E. Proposed narrative and report design

The proposed reviewer-facing rendering would have these fixed sections:

1. **Scope and identities:** supplied synthetic case, artifact identities, preliminary decision support and required human review; no evidence-authentication claim.
2. **Observations from supplied records:** E01-E05 templates only, clearly identified as supplied values or attributed source excerpts.
3. **Deterministic comparisons:** E06 outcomes, prerequisites, conflicting fields and checked/unchecked coverage. A source-field match is described at its exact scope.
4. **Producing system's assessment:** exact recommendation/abstention, rationale, every factual finding and interpretation, attributed to baseline/hosted producer where known. Unknown producer is stated as unknown. No "verified findings" heading for candidate content.
5. **Uncertainty and source differences:** all candidate missing-information statements, questions and contradictions; exact opposing source excerpts where available, without declaring candidate contradictions independently proven.
6. **Diagnostics and limits:** adverse checks, rejected/unchecked locations, unimplemented comparisons, incomplete provenance, no completed-human-review assertion and no semantic score.

Proposed sentence/unit provenance would contain a stable occurrence ID, origin (`source_template`, `restricted_check` or `candidate_quote`), exact text, applicable template/check ID, source bindings, and candidate JSON pointer/hash where applicable. Candidate statements would remain whole and verbatim; no atomic decomposition, strengthened normalization, meaning-changing connective or compression would be introduced. Original citations remain ordered under `submitted_citations`. Composer source bindings are separate: they never repair a candidate's inadequate or absent citations.

Every candidate statement occurrence would remain available, including repeated statements, contradiction descriptions and uncited questions. Rendering would not silently drop an adverse finding to improve readability. Exact candidate scalars, ordering and the original payload identity would remain accessible. Preserving an unchecked assertion as an attributed quote is not accepting it as a generated source observation. Generic statements about software execution, authenticity or completed human review would remain candidate assertions unless a separately authorized process-evidence review exists; case citations are not that authority.

Every recognized restricted conflict must appear conspicuously both in structured report diagnostics and in reviewer-facing narrative units. Each conflict unit must link the unchanged candidate occurrence and submitted citations, exact conflicting source values, and original checker outcome. A passing technical stage cannot suppress that unit or promote the conflicting assertion to a source-verified observation. A qualified companion is never an overall factual or semantic pass, and absent checker coverage is not agreement or correctness.

Human-readable text would escape/quote source content appropriately and render it inertly; no evaluation of embedded instructions, links, HTML or scripts is proposed. No broader semantic review can be inferred from this presentation safeguard.

## F. Proposed failure and qualification policy

`rejected` below would mean no eligible companion narrative, with a diagnostic result still available. `qualified_companion` would always disclose its bounded scope; it is never an unconditional support pass. The owner accepted the hard structure/identity/reference gates and qualified handling of restricted conflicts at design level; exact new report-state encoding remains proposed. Existing service/auditor statuses, outcome naming and CLI exits would remain unchanged.

All three existing mechanical stages (`input_structure`, `output_structure`, `contextual_references`) must pass before normal companion eligibility, together with the mandatory bindings in section C. A separate restricted-check failure remains explicitly retained even when those three stages pass. It cannot be overridden by the service's `validated` status or described as an overall factual/semantic pass. Zero checked findings or missing checker coverage do not imply agreement or correctness.

| Condition | Proposed result | Required handling |
| --- | --- | --- |
| Invalid investigation JSON/contract | Hard rejection | Preserve input identity and available independent audit diagnostics; no source narrative |
| Invalid assessment structure | Hard rejection | Retain original candidate identity and available diagnostics; do not fabricate fields or use a different parsed substitute |
| Wrong case/alert identity | Hard rejection | Existing contextual failure retained; no cross-case report |
| Missing cited ID or wrong namespace | Hard rejection | Preserve exact failing location; do not search another namespace or guess a near match |
| Expected original-byte/source/bundle/candidate identity mismatch, or stale pointer binding | Hard rejection | Stop report acceptance; no normalization, source substitution or frozen-evidence repair |
| Restricted deterministic fact conflict | Design-approved qualified companion if all three mechanical stages and mandatory bindings pass | Retain the restricted-check failure explicitly. Every recognized conflict must be conspicuous in structured diagnostics and narrative units, linked to the unchanged candidate statement/submitted citations, exact source values and checker outcome. Never promote the conflicting claim to source-verified observations or describe the report as an overall factual/semantic pass |
| Unsupported or unchecked candidate assertion | Qualified companion if other hard gates pass | Default to unchecked, not an invented unsupported judgment. The composer does not detect arbitrary unsupported prose. Preserve exact wording/citations and do not promote it. Any supplied prior reviewed judgment requires explicit authority and is outside initial ingestion |
| Missing member, explicit null or unsupported eligible source value | Qualified companion | Distinguish the states, scope to the queried supplied record and omit that factual template or render a scoped availability statement; never fill a gap |
| Optional provenance absent | Qualified companion if mandatory bindings and mechanical stages pass | Keep explicit null/unknown with availability reason; distinguish recorded/unverified metadata from metadata verified against supplied evidence. No Git, environment-variable, credential or network discovery is required; supplied expected identities must still match |
| Contradictory supplied records | Qualified companion | Retain both records/values and original candidate conflict descriptions. A detected conflict label requires an eligible existing predicate; otherwise show separate excerpts, not a fabricated semantic verdict |
| Valid abstention | Qualified companion | Preserve `unable_to_recommend`, null action and exact rationale, including allowed uncited rationale/empty findings. Do not turn it into `investigate` |
| Failed, refused or incomplete generation; absent candidate | Diagnostic rejection for that generation outcome | No accepted assessment/narrative and no manufactured abstention. Retain available service status and fragment identity. A fragment is not a completed assessment, even if parseable |
| Unexpected evaluator/composer exception | Hard rejection | Report safe error category and available identities; no success fallback or detailed secret-bearing exception dump |

A qualified report would expose a list of qualification reasons, never rely only on its single state field. Not every qualification can be automatically detected: unknown commercial meaning or a false arbitrary assertion can remain unchecked. The report would not claim complete error detection. Source lookup success, empty conflict lists and zero checked claims cannot erase this limitation.

## G. Proposed output format and reproducibility

| Representation | Advantages | Disadvantages |
| --- | --- | --- |
| Versioned JSON companion with structured narrative units | Explicit provenance/diagnostics, exact assertions, straightforward validation and deterministic tests | Less convenient for a reviewer without a renderer |
| Markdown-only narrative | Simple to read and diff | Weak machine enforcement of unit bindings, coverage and adverse-result preservation; easy to confuse prose with checked facts |
| JSON plus deterministic plain-text/Markdown rendering | One structured authority and a readable view | Two independently published files complicate atomicity and identity binding |

**Owner-approved design choice:** one versioned JSON companion, separate from `InvestigationOutput`, containing ordered source-derived and attributed narrative units. The first slice would compose/serialize this structure in memory; it would add no CLI or file-publication workflow. An optional separate human-readable rendering would be a later, separately authorized integration choice, derived deterministically from the same units. The earlier representation alternatives above are retained as tradeoff history, not authority to publish additional files. A new public HTML/UI or another model call is not proposed. Exact schema/type implementation remains subject to separate approval, using the standard library and existing dependencies.

Proposed stability properties: identical source/candidate payloads, explicit provenance, template/composer versions and configuration yield identical companion bytes. Specify UTF-8, sorted object keys, fixed indentation, LF terminator, no non-finite numbers, Decimal strings, original record/statement ordering and stable occurrence IDs based on identity/location rather than wall time. Preserve exact Unicode text and case; do not trim identifiers or rewrite candidate strings. Relocated copies with identical evidence and provenance labels should produce the same content. New report labels would be explicit repository-relative artifact identities, not discovered absolute machine paths. This proposal does not change existing G02 absolute paths or promise their report-byte portability.

Observed timestamps, machine locations or revision metadata would not be invented or discovered silently. If later required, supply them explicitly as provenance (thereby intentionally changing report bytes), or place them in a separate execution record outside the deterministic report digest. A report cannot include its own original-byte hash; compute that externally after serialization. Only at the later, separately authorized integration checkpoint, and if justified, a publication wrapper would validate complete bytes first and use an explicit, fresh destination with atomic non-overwrite semantics, following existing publication patterns. It would reject destinations that overwrite original input/candidate/frozen files; no cleanup of unrelated evidence is proposed.

## H. Proposed integration sequence

Future flow, not implemented here:

```text
original supplied input -> existing InvestigationInput validation
    -> existing baseline assessment OR existing guarded hosted assessment
    -> exact assessment payload + existing mechanical audit
    -> proposed evidence package and source/pointer checks
    -> proposed qualified narrative/report for human review
```

Existing stages already cover the input contract, both assessment producers, output/context validation and hosted audit execution. A saved candidate can enter after assessment generation without any new invocation. The diagram describes the later full flow, not the scope of the first implementation slice.

### First implementation slice - proposed, not yet authorized

- Offline evidence-package and report composer over supplied payloads; exact supplied input/candidate identities and source-pointer bindings.
- E01-E06 only, reusing existing contracts, contextual validation, auditor and restricted amount checker.
- One structured JSON companion with deterministic source-derived observations/narrative units, complete preservation and attribution of candidate content, and qualification/failure diagnostics.
- Focused composer unit tests using tracked or constructed fixtures, and reproducible in-memory report serialization/source preservation.

This slice introduces no new hosted request, producer orchestrator, CLI, file-publication workflow, semantic evaluator or general claim-understanding system. It would not coordinate batches or manage experiment allowances.

### Later Week 6 integration - separately authorized

- Baseline -> audit -> companion integration, and mocked hosted service -> audit -> companion integration.
- Full-flow failure propagation, integration tests and grounded/qualified report examples.
- Non-overwriting publication/CLI behavior only if justified by the integration requirements and separately approved.

The original Week 6 acceptance remains **full pipeline, integration tests, grounded report examples**. Completion of the first composer slice alone is not completion of Week 6. No live request is needed or authorized by either design description.

For later hosted integration, reuse `AssessmentRun` and exact `candidate_json`, assessment and audit. Do not reimplement `responses.parse`, guards, error classification, credentials or retries. Reuse a completed audit only after binding it to its exact payload representation; otherwise recompute through the existing auditor. Recorded embedded evidence and a fresh raw-input replay would remain distinct, with expected digest differences explained. An unsuccessful service run takes the diagnostic branch, not a successful narrative branch.

For later baseline integration, call the existing `assess_investigation` with a validated input, serialize the new candidate once, preserve those chosen bytes, then pass those exact bytes through the auditor/composer. This describes a future test/caller, not authorization to regenerate any frozen baseline.

Proposed integration tests would exercise baseline -> audit -> companion using tracked/constructed inputs, and mocked hosted service -> original candidate text -> audit -> companion with sockets/provider access blocked. Their assertions would test data flow and safeguards, not a correct AML winner. No new live call, revised prompt or expected-label input is needed to demonstrate this path.

## I. Proposed tests and acceptance design

The owner accepted the test-design intent and stage separation; every row remains an unimplemented, unexecuted test proposal. **A** means first-slice composer unit tests; **B** means later, separately authorized full-flow integration/publication tests. Keep all twelve test families, with the combined families split below. Neither label authorizes tests to run or implementation to begin. Reuse existing tracked [golden inputs](../../data/golden_cases/inputs/), [development investigations](../../data/generated/development/) and independently constructed candidate/mock responses. Do not load reference answers to generate assessments or copy ignored frozen candidates into Git without separate approval.

| Test family | Stage | Concrete proposed assertion |
| --- | --- | --- |
| T01 - valid source package | A - composer | Accept a valid input and candidate; every typed record/pointer/value resolves; preserve contextual/unflagged records, nullable counterparties and permitted empty citations |
| T02 - source-derived values | A - composer | E02 displays exact currency/Decimal amount and original timestamp; E03 preserves monthly/daily labels and does not invent personal authorship. Rendering does not round, combine currencies or infer a hard payment limit |
| T03 - recognized amount match and conflict | A - composer | Reuse exact supported statement grammar with one transaction citation. Correct amount matches; changing only amount produces the existing conflict. All three mechanical stages may still pass; the new report must visibly preserve the conflict and keep the false claim out of source observations |
| T04 - arbitrary unsupported text | A - composer | A structurally valid claim such as "This software authenticated every document" with an existing citation remains an unchecked attributed candidate quote. It cannot become a source-template claim or certify process execution |
| T05 - bad identities/references | A - composer | Wrong case/alert, unknown ID or same textual ID in the wrong namespace rejects; no guessed citation or fabricated evidence ID appears |
| T06 - byte and pointer binding | A - composer | Changing only LF/CRLF or JSON formatting changes original-byte identity even if canonical input is unchanged. A stale expected hash/value/pointer rejects; no normalization is used to rescue it. Preserve raw and canonical bases separately |
| T07 - missing/null and conflicting sources | A - composer | Distinguish absent key, explicit null, unsupported fact shape and nonempty value. Missing invoice account plus populated wire is not labeled disagreement. Two differing source excerpts are both retained, without fraud inference or automatic source precedence |
| T08 - complete candidate coverage | A - composer | Every rationale/finding/interpretation/question/missing-information/contradiction occurrence and both contradiction sides retain exact text, submitted citations, order and pointer. Repetitions stay separate. No new atomic normalization or citation repair |
| T09 - abstention and failed generation | A/B - split below | Valid abstention yields a qualified report with null action. Refusal, incompleteness, no parsed result or failed generation yields diagnostics, not invented abstention/assessment. Available fragments remain unaccepted |
| T10 - preliminary and review boundaries | A - composer | Existing contract rejects non-preliminary scope and false/nonboolean review values. Rendering preserves required review and never asserts that a person already reviewed the case |
| T11 - integration and no network | A/B - split below | Baseline and real-SDK mocked-transport service paths reach the same report interface; expected failures propagate. No credential lookup, live client construction or network access is allowed in offline report composition |
| T12 - reproducibility and preservation | A/B - split below | Same explicit inputs/versions/provenance produce identical bytes. Existing destination/frozen paths are refused; original source/candidate bytes and inputs remain unchanged on success/failure. Publication failure exposes no accepted partial report |

### Required split of combined families

- **T09-A (composer):** supplied valid abstention preserves null action; absent/invalid candidate or supplied failed/incomplete outcome cannot become a fabricated accepted assessment. Use constructed payloads/outcome metadata only, with no producer invocation. **T09-B (later integration):** mocked service refusal, incompleteness, missing parsed output and failure propagate from the real existing producer interface into diagnostic-only report handling.
- **T11-A (composer):** composing supplied payloads uses no producer coordination, credential lookup, Git/environment-variable discovery, live client construction or network access. **T11-B (later integration):** real baseline and real-SDK mocked-transport service paths connect through audit to companion, with network access blocked and expected full-flow failures preserved.
- **T12-A (composer):** identical explicit inputs/versions/provenance give identical serialized bytes; supplied source/candidate data remain unchanged on success/failure. Assert that no file-write/publication boundary is invoked and that source fixture hashes remain unchanged; the pure composer has no output-path/publication workflow that could overwrite frozen evidence. **T12-B (later integration, if publication/CLI is justified):** existing destinations and frozen paths are refused; publication failure never exposes an accepted partial report or triggers replacement generation.

T01/T06 would also cover accepted unknown optional provenance with explicit availability reasons, recorded-versus-verified metadata, a mandatory binding that cannot be established, mismatching supplied expected identities, and an exact candidate string hashed as UTF-8 text rather than an HTTP envelope. These are composer checks, with no discovery of missing metadata. T03 would assert both a structured conflict diagnostic and a reviewer-facing conflict unit, with unchanged candidate citations, exact source values and the original checker outcome.

**Proposed first-slice acceptance:** after separate implementation-contract/code authorization, pass the focused A tests and full existing suite with actual results; validate companion shape, mandatory bindings, E01-E06 output and deterministic serialization. Use tracked/constructed unit fixtures for match, unchecked text, missing/conflicting evidence, abstention and diagnostic rejection; no producer orchestration, CLI or publication acceptance is included. Those unit outputs are not completion of Week 6's later integration/examples requirement. Fresh-checkout CI must execute the new tests without ignored outputs. Existing optional research-packet skips remain unchanged and are not evidence that the new tests ran.

**Separate full Week 6 acceptance:** demonstrate the agreed full input -> assessment -> audit -> evidence/report flow, integration tests for both the baseline and mocked hosted path, grounded/qualified report examples and failure behavior, and owner review against the original roadmap. The first composer slice alone would not establish this milestone. Hosted re-execution, a broader factual allowlist, expert endorsement, semantic scores and held-out results are not inferred prerequisites; any new requirement or call needs separate scope approval.

Proposed implementation verification commands would use the existing project environment: focused new tests, `python -B -m unittest discover -s tests -v`, dependency checks, syntax checks and `git diff --check`, with the existing [CI Python 3.11-3.13 matrix](../../.github/workflows/foundation-tests.yml) and [constraints](../../constraints.txt). No dependency or workflow change is proposed. This document makes no fresh unit-suite or remote-CI success claim.

## J. Evaluation and release boundaries

- [P01](../phase-2/G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) remains owner-approved: stronger drafted personal-authorship propositions must not automatically become candidate errors; original attribution remains qualified. No rewriting of H004/H034, frozen wording or historical judgments.
- [P02](../phase-2/G02_P02_MATERIALITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) remains owner-approved: M04 is contextual/nonmandatory for frozen G02, not inherently immaterial. M01-M03 remain its mandatory items. This supplies no general threshold, whole-statement pass or new case labels.
- P03 remains under review. Proposed report-origin/qualification states are technical provenance controls, not approved semantic-support categories or denominator definitions. Numerical semantic scoring stays disabled; no rates, weighted scores, pass thresholds, accuracy, ranking or completeness percentage would be produced.
- P04 formal versioned adjudication/report release remains separately controlled. This companion is not a new G02 adjudication release, an addendum-ingestion implementation or permission to update the register/reconciler.
- P05 independent-evaluation/expert conditions remain separate; owner decisions and software checks are not independent AML expert validation. Human review required is not human review completed.
- The [G02 register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json), [reconciliation specification](../phase-2/G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md), original candidate/annotation packets and saved reports would remain unchanged. Historical pending fields in those records do not reopen P01/P02; the addenda remain the later decisions.
- All nine broad auditor semantic dimensions remain `not_evaluated`. Report generation is not a general semantic evaluator. Specific checked fields never imply completeness of claim support.
- Week 7 retains held-out evaluation and safety/failure analysis, with data/exposure/adjudication controls before quantitative claims. Current development templates, G02 and the five Week 5 cases cannot be redesignated held-out by rendering them in a report. Unequal baseline/hosted REF-01 access remains disclosed; a narrative does not equalize policy access or approve a disposition.

## K. Alternatives, blockers and owner decisions

| Alternative | Tradeoff and proposed disposition |
| --- | --- |
| Format candidate text alone | Lowest effort, but weak new evidence assembly and risk of apparent factual certification. Could be an explicitly attributed viewer; insufficient by itself for the proposed grounded-report slice |
| Source-first JSON companion with deterministic templates and candidate appendix | Owner-approved design direction and E01-E06 boundaries; bounded coverage is explicit. Exact implementation contract and coding remain separately authorized |
| Immediately build complete producer coordination or a second hosted narrative stage | More integration/state/error surface; assessment coordination already partly exists, and new free-form generation creates additional grounding/spend requirements. Defer unless a later approved need demonstrates value |

**Genuine current implementation blockers:** no missing dependency or need for architecture replacement was identified. The design direction, E01-E06, content separation, qualified-conflict handling, hard gates, optional unknown provenance and stage split are accepted; do not reopen those choices. The remaining approval gate is the detailed implementation contract and explicit coding authorization, which this draft does not supply. Particular future source/candidate identity failures would block those reports, not justify changing evidence. A requirement to certify arbitrary narrative truth would exceed existing checks and require separately approved semantic methodology.

**Accepted design choices, preserved for implementation-contract review:** E01-E06 only; one versioned JSON companion separate from `InvestigationOutput`; source/check/candidate/uncertainty separation; qualified reporting of recognized conflicts when all three mechanical stages and mandatory bindings pass; hard rejection for invalid structure, identity mismatches and unresolved contextual citations; explicit unknown optional metadata; first-slice A versus later-integration B separation. The conflict-handling alternative of rejecting every restricted conflict was considered previously; the owner selected conspicuous qualification instead. It is not an open choice in this revision.

**Remaining proposed implementation-contract choices and separate authorizations:**

1. Finalize exact JSON fields, validation types, status spellings and required/optional field encoding without weakening the mandatory bindings or accepted hard gates. No new assessment contract is needed.
2. Finalize deterministic template wording, occurrence identifiers, pointer encoding and serialization details within E01-E06; preserve exact candidate text/citations and conspicuous structured/narrative conflict links.
3. Select the tracked/constructed A fixtures and expected report structures, then explicitly authorize first-slice code and focused tests. No new derivation, general semantic verdict or human-review-ingestion authority is implied.
4. Separately authorize later baseline/mocked-hosted coordination, full-flow failure tests and grounded/qualified report examples. Assess whether a CLI or publication workflow is actually justified before adding it, including its non-overwrite contract and B tests.

No unresolved technical ambiguity was identified that requires reopening the accepted design. These remaining concrete contract choices need review before code, not another design direction or a new semantic adjudication. Any future human-review ingestion, broadened allowlist or different generation/evaluation scope requires its own authorization.

Optional improvements include richer approved cash/beneficiary predicates, additional presentation formats and narrow stale-status maintenance. None is a prerequisite for this proposed first slice. RAG, agents, databases, vector search, provider changes, new dependencies, scoring, prompt tuning and paid experiments have no demonstrated necessity here.

## Specification checkpoint verification and stopping boundary

The original specification-only checkpoint created this draft. The current checkpoint authorizes focused revision of this same untracked file to record owner-approved design decisions and the three refinements; it creates no replacement specification. Existing project/status/worklog/decision documents, code, tests, prompts, contracts, policy, datasets, G02 artifacts, Week 5 records, ignored evidence and the handoff ZIP are outside its write scope. No new allowance, experiment, backup, application implementation, semantic judgment or scoring permission is created.

Verification for this revision would check all repository-relative links, consistency of sections C/D/F/G/H/I/K and the retained eleven-section structure, preservation of unchanged sections/references and the focused edit diff, whitespace, modification of only this existing draft, all unrelated pre-existing project-file identities and the Git index. Unit tests are not run for a specification-only change; their future requirements are listed above, not presented as executed results. The final engineering response records actual preservation and Git results without modifying other documentation.

**Stop for owner review. Application implementation and full Week 6 acceptance remain separately authorized decisions.**
