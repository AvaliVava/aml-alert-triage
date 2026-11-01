# Offline evidence report implementation contract - v0.1

**Scope:** Owner-authorized first Week 6 implementation slice, on
`feature/week-6-evidence-report` from `3435079aa7f33a33e3e1c9812fd7ebc43d1f1ed7`.
This concrete contract follows the accepted design-level choices in the unchanged
[design specification](WEEK_6_EVIDENCE_REPORT_DESIGN_SPEC_v0.1_DRAFT.md).
That document's historical implementation restriction is superseded only for this
explicitly authorized slice. Later integration and full Week 6 completion are not authorized.

## Public interface

The new [evidence_report.py](../../src/aml_triage/evidence_report.py) exports:

```python
compose_evidence_report(
    investigation_json: bytes,
    candidate_json: bytes | str | None,
    *,
    expected_identities: dict[str, str] | None = None,
    provenance: dict[str, str | None] | None = None,
    generation_status: str | None = None,
) -> dict

serialize_evidence_report(report: dict) -> bytes
```

The composer reads only its arguments, invokes the existing contracts/auditor and
canonical-input helper, and returns a new JSON-compatible dictionary. It never
reads/writes files, discovers Git/environment variables/credentials, invokes a producer,
constructs a client, or makes a network request. Input must be actual supplied bytes;
parsed models/dictionaries and reconstructed input serialization are not accepted.
Candidate strings are accepted exactly, without trimming or reserialization. `None`
means no candidate, not abstention. A whole hosted execution bundle is not a candidate.

`generation_status` accepts `None`, `completed`, `failed`, `refused` or `incomplete`.
Non-completed supplied outcomes are rejected even if a fragment happens to validate.
`None` is explicitly unavailable generation provenance, not an inferred success.
The composer cannot discover a failure the caller does not supply.

`expected_identities` accepts only `input_sha256`, `candidate_sha256`,
`canonical_input_sha256`, `case_id`, `alert_id`. Values must be strings; digest
expectations must be 64 lowercase hexadecimal characters. Every supplied expectation
must equal the actual value. An unavailable expected binding is not a match.

Optional `provenance` accepts only `producer`, `model`, `sdk_version`, `prompt_version`,
`prompt_sha256`, `request_id`, each a nonempty string or null. These are recorded but
not independently verified, even if they look like a known model/prompt/request.
Absent/null entries stay explicitly unavailable. Unknown keys, invalid argument types
or unsupported generation states produce rejection, without echoing their values.
No actual credential, raw exception message or hidden configuration is collected.

## JSON companion schema 1.0

All listed fields are required unless expressly nullable; objects described below
reject extra fields. Lists retain deterministic source/statement order.

| Root field | Type and meaning |
| --- | --- |
| `report_schema_version` | literal `"1.0"` |
| `composer_version` | literal `"0.1.0"` |
| `template_version` | literal `"1.0"` |
| `report_state` | `qualified_companion` or `rejected`, never a factual/semantic pass |
| `case_identity` | `{case_id: string, alert_id: string}` or null if unavailable |
| `artifacts` | exactly `input`, `candidate`, `canonical_validated_input`, each an artifact descriptor |
| `provenance` | exactly the six optional metadata names above plus `generation_status`, each a metadata descriptor |
| `component_versions` | string map of composer/template/auditor/amount-check versions and available audit contract versions |
| `source_records` | list of supplied-record snapshots |
| `source_observations` | list of E01-E05 source-template units; no candidate claims |
| `source_conditions` | list of inspected field conditions |
| `candidate_content` | complete unchanged validated candidate JSON object, or null on rejection |
| `candidate_occurrences` | list of exact statement/description occurrences |
| `restricted_checks` | unchanged existing auditor `deterministic_fact_checks`, or null without audit |
| `validation` | `{audit: existing audit object or null, diagnostics: list of diagnostics, expected_identity_checks: list of identity checks}` |
| `qualification_reasons` | ordered distinct reason-code strings; empty on rejection |
| `narrative_units` | ordered scope, source-template, restricted-check, candidate-quote and diagnostic units; empty on rejection |
| `semantic_evaluation` | `{status: "not_evaluated", scoring_authorized: false}` |
| `limitations` | fixed scope/authority limitation strings |

An artifact descriptor has `sha256: string|null`, `bytes: integer|null`,
`digest_basis: string`, `unavailable_reason: string|null`. Bases are `supplied_bytes`,
`utf8_encoded_candidate_text`, and `validated_input_canonical_json_utf8`.
Unknown artifacts have null digest/size and a reason; no unavailable bytes are fabricated.
Original-byte identities retain LF/CRLF/whitespace differences. Canonical input uses
the existing [build_assessment_prompt](../../src/aml_triage/openai_prompt.py) definition;
its digest never substitutes for supplied input bytes. Candidate-string hashes cover
the exact string's UTF-8 encoding, not an HTTP envelope.

A metadata descriptor has `value: string|null`, `evidence_state` equal to
`recorded_not_independently_verified` or `not_supplied_or_unavailable`, and
`reason: string`. Field bindings below have `verified_against_supplied_evidence`:
this means exact lookup/value consistency, not authenticated evidence or execution.

A source-record snapshot has `input_sha256`, `record_type`, `record_id`,
`record_pointer`, `record_json`, all strings. All eight existing typed namespaces
are included. Same textual IDs in different namespaces are separate records.
Snapshots include supplied contextual/unflagged records without implying relevance.

A binding has `input_sha256`, `record_type`, `record_id`, `record_pointer`,
`field_pointer`, `input_pointer`, `value_json`, `evidence_state` (strings) and
`missing_member: string|null`. Record-relative and input-root JSON pointers use
standard `~0`/`~1` escaping. Record identity, pointer and value are checked before
acceptance. For a missing field the binding resolves its real parent and records
the missing member separately; no nonexistent child is represented as resolved.

`record_json` and `value_json` are lossless JSON **text** snapshots of decoded source
values, not strings substituted for source numbers. Parsing uses Decimal for JSON
fractional numbers; snapshots encode numbers as numbers without binary-float rounding.
For example source number `1.20` gives `value_json="1.20"`, whereas source string
`"1.20"` gives `value_json="\"1.20\""`. Snapshot whitespace is deterministic, not
original-fragment whitespace; the supplied-payload digest binds original bytes.
Typed Decimal formatting and source snapshots remain distinguishable. If the existing
contract's JSON-number normalization changes a transaction amount relative to the exact
supplied value, reject with `source_numeric_normalization` at that amount's input pointer.
Do not repair the input, change the contract/checker, or present a rounded typed amount
as a supplied source observation. This guard compares scalar representations; it is
not another candidate-statement parser. Large exact Decimal strings remain supported.

A source condition has `record_type`, `record_id`, `queried_field_pointer`, `state`
(`missing`, `explicit_null`, `unsupported_or_unusable`, `available`) and `binding`.
This is field availability only, never a general missing-document finding.

An occurrence has `occurrence_id`, `candidate_sha256`, `json_pointer`,
`statement_sha256`, `text`, `section`, `kind` (`statement` or `contradiction_description`),
`citation_pointer: string|null`, `submitted_citations: list[RecordCitation]|null`,
and `semantic_review: "not_evaluated"`. Occurrence ID hashes candidate digest plus
exact JSON pointer; identical repeated text at different locations stays distinct.
Contradiction descriptions have null citation pointer/list because that field has no
submitted citations. All actual cited statements preserve their exact ordered lists,
including permitted empty lists. No normalization or atomic decomposition is performed.

A narrative/source unit has `unit_id`, `origin` (`source_template`, `restricted_check`,
`candidate_quote`, `diagnostic`), `rule_id: string|null`, `text`, `bindings: list[binding]`,
`candidate_occurrence_id: string|null`, `check_pointer: string|null`,
`check_outcome: string|null`, `diagnostic_code: string|null`.
Source-unit IDs bind input digest/rule/location; check and candidate units bind the
candidate occurrence. Text safely quotes supplied strings as data; no renderer or
execution of embedded text is implemented. Candidate quotes are attributed to a
recorded producer when supplied, without certifying that producer identity.

A diagnostic has `severity` (`rejection` or `qualification`), `code`, `location: string|null`,
and a fixed safe `message`. Existing audit diagnostics/outcome names are retained
unchanged inside `validation.audit`; unexpected exception details are not copied.

An identity check has `name` (one of the five allowed expectation names), `expected`
(string), `actual` (string or null), and `outcome` (`matched`, `mismatch`, `unavailable`
or `not_evaluated`). Every supplied expectation is retained in name-sorted order.
Checks remain `not_evaluated` when failed prerequisites prevent establishing identities.
Accepted companions require every supplied expectation to be `matched`; unavailable
values never match, and rejected diagnostics preserve available comparison records.

## E01-E06 and acceptance gates

Only the approved [E01-E06 allowlist](WEEK_6_EVIDENCE_REPORT_DESIGN_SPEC_v0.1_DRAFT.md#d-proposed-initial-factual-content-allowlist)
is implemented. E01 transcribes case/alert IDs and flagged transaction references.
E02 formats individual typed Decimal amounts without rounding and retains original
timestamps/account/counterparty references. Null counterparty is not missing payee proof.
E03 transcribes monthly/daily profile intervals with their actual labels, without
personal authorship, materiality or per-transfer-limit inference.
E04 quotes evidence metadata, the specified explanation/beneficiary fact fields,
and supplied check fields; no new verification or source precedence is inferred.
E05 records field states for inspected E01-E04 fields, with a scoped gap unit where
appropriate. E06 consumes only existing auditor results, including exact coverage.
No parser, beneficiary predicate, aggregate total, policy rule or disposition is added.

Normal eligibility requires all three existing mechanical stages to pass, all supplied
expectations to match, every generated mandatory binding to validate, and no failed
generation outcome. Invalid/missing payloads, invalid configuration, malformed structures,
wrong case/alert, unresolved citations, unavailable expected identities and unexpected
audit/composition errors return `rejected`. Rejected reports preserve available artifact,
case and audit diagnostics but clear companion content/observations/units. No invalid
candidate is repaired or promoted. Serializer misuse can raise Pydantic/encoding errors;
serialization is not a replacement for composition against supplied source evidence.

Every eligible report remains qualified. Reason codes include `bounded_scope`,
`unchecked_candidate_content`, `source_field_gaps`, `restricted_conflict`,
`restricted_coverage_incomplete`, and `generation_status_unavailable` as applicable.
A restricted conflict is **not** rejection: every recognized conflict has a structured
qualification diagnostic and prominent narrative unit linked to the original occurrence,
unchanged citations, exact source values, check pointer and unchanged checker outcome.
It cannot be overridden by mechanical pass/service `validated` or promoted into
`source_observations`. Unchecked text remains attributed, never judged supported.
Even matched fields do not clear complete statements, rationale or recommendations.
Valid abstention stays null; failed generation never becomes fabricated abstention.

The audit always runs against the supplied input representation and exact candidate
bytes/string; no caller-provided stale audit is trusted. Its SHA/basis are cross-checked
against those actual arguments. This slice does not ingest hosted bundles or reproduce
their canonical-input embedded audit interface. All nine existing semantic entries stay
`not_evaluated`; P01/P02 remain approved, P03 open/scoring disabled, P04/P05 separate.

## Determinism, verification and deferred work

The serializer validates the companion's declared structural model, then emits sorted
keys, two-space indentation, UTF-8, one LF terminator, no NaN/Infinity and no timestamps
or machine paths discovered by the composer. Same supplied payloads/provenance/component
versions yield identical bytes. Returned data never aliases caller dictionaries.
Structural serialization validation alone does not re-establish source truth after
someone edits a returned report; compose again against supplied evidence for that.

Focused A tests use tracked inputs and constructed candidates, with network/credential
and write boundaries blocked where relevant. Test original string/bytes identity,
Decimal values, pointers, citations, optional metadata, missing/null fields, explicit
conflicts, abstention/failure, negative binding/error cases and deterministic output.
Later T09-B/T11-B/T12-B producer coordination, CLI/publication and integration examples
are deferred. No ignored packet, new dependency, hosted request, scorer or overall
factual-pass result is introduced. This implementation does not complete Week 6.
