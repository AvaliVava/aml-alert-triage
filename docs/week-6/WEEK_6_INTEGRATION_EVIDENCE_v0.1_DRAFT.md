# Week 6 bounded pipeline integration evidence - v0.1 DRAFT

**DRAFT - engineering evidence for owner review; not a Week 6 closure decision.**

Prepared on November 1, 2026, on `feature/week-6-pipeline-integration` from
`6d851fc8c9556cc24aa35eacfa657f75dbca8aa1` (PR #18). The owner authorized only
[integration tests](../../tests/test_week6_pipeline_integration.py) and this document.
No runtime module, orchestrator, CLI, publication workflow, dependency or existing file is changed.
Progress-document reconciliation and milestone acceptance remain separately reviewed.

## Scope and existing interfaces exercised

The [roadmap](../../ROADMAP.md) requires evidence validation, narrative drafting and integration:
full pipeline, integration tests and grounded report examples. This checkpoint demonstrates
bounded library composition, using the unchanged [implementation contract](EVIDENCE_REPORT_IMPLEMENTATION_CONTRACT_v0.1.md)
and [design](WEEK_6_EVIDENCE_REPORT_DESIGN_SPEC_v0.1_DRAFT.md). It does not certify arbitrary prose.

- Baseline: original input bytes -> `InvestigationInput.model_validate_json` ->
  [assess_investigation](../../src/aml_triage/deterministic_baseline.py) -> serialize the
  new assessment once -> [compose_evidence_report](../../src/aml_triage/evidence_report.py)
  -> `serialize_evidence_report`. The composer invokes the unchanged
  [audit_packet](../../src/aml_triage/auditor.py).
- Mocked hosted: validated original input -> [OpenAIAssessmentService.assess](../../src/aml_triage/openai_service.py)
  -> `AssessmentRun.candidate_json` unchanged -> explicit outcome mapping -> composer -> serializer.
  The SDK client uses `httpx2.MockTransport`, `https://mock.invalid/v1`, an explicit synthetic
  credential, and an injected client. Default application client construction and socket/DNS
  access are blocked. Tests replace environment getters with null-returning mocks; real
  credentials/environment values are not discovered. Report publication and path write methods
  are blocked. No report file or historical assessment is generated or replaced.

The three baseline inputs are tracked G03, G05 and development case 0002. New in-memory
assessments preserve the baseline's existing `escalate`, `investigate` and null actions respectively.
These assertions are behavior regressions, not correctness labels. The last input is reused
only as a tracked fixture; no ignored Week 5 baseline is opened or regenerated.

## Reproduction and construction

Run from the repository root in the existing constrained environment; no installation or key is needed:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_week6_pipeline_integration.py -v
```

All examples below are computed in memory by that test module. `constructed_candidate`
uses case/alert IDs and the first transaction from the validated supplied input. The default
rationale and sole factual finding are separate occurrences of:
`Transaction {transaction_id} amount was {currency} {amount:,.2f}.`, each with the exact
typed transaction citation. Other statement lists are empty, action is the constructed
`investigate`, scope is `preliminary`, and `human_review_required` is true. This action is
a mechanical fixture choice, not an approved disposition.

`candidate_text` is exactly one space plus LF, followed by
`json.dumps(value, indent=3, ensure_ascii=False, allow_nan=False)`, followed by LF plus one space.
Outer whitespace is deliberate. The hosted parsed model never replaces this exact text.
`baseline_bytes` follows the existing [baseline CLI](../../scripts/run_baseline.py):
`(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")`.
Every newly produced baseline candidate is serialized once per pipeline execution; repeated
executions test determinism, not regeneration of any frozen historical output.

| Example | Exact change from the default construction | Reproducing test (in the linked module) |
| --- | --- | --- |
| A | Original tracked G02; default constructed candidate | `test_example_a_sdk_pipeline_preserves_text_and_separate_audit_representations` |
| B | G02; replace both rationale/finding text with `The incoming transaction was USD 99,999.00.` | `test_example_b_service_validated_amount_conflict_stays_conspicuously_qualified` |
| C | G02; replace both texts with `This software authenticated all supplier documents.` | `test_example_c_unchecked_authentication_assertion_remains_candidate_attributed` |
| D | Original G04; additionally test two in-memory copies, deleting `/evidence/3/facts/beneficiary_account_ref` or setting it to JSON null. Encode modified inputs with `baseline_bytes`; leave the rest of the supplied records unchanged | `test_example_d_differing_excerpts_and_missing_null_variants_preserve_scope` |
| E-hosted | G02; `action=None` sets status `unable_to_recommend`, null action, no factual findings and an uncited rationale `No recommendation is supplied in this test response.` | `test_example_e_sdk_abstention_remains_null_and_preliminary` |
| E-baseline | Actual baseline on tracked development case 0002; no constructed hosted response | `test_real_baseline_pipeline_preserves_once_serialized_candidate_and_audit` |
| F-incomplete | Same exact candidate text as A, but synthetic response status `incomplete` and `incomplete_details.reason=max_output_tokens` | `test_example_f_parseable_incomplete_response_is_diagnostic_only` |
| F-missing-parsed | Same text as A and completed response; fault-inject `None` from SDK `parse_text` while preserving the actual SDK/MockTransport call | `test_valid_text_without_sdk_parsed_output_cannot_become_completed` |

F-missing-parsed deliberately simulates an unavailable parser result; it is not a claim that
an unmodified SDK spontaneously drops valid parsed output. The test targets the existing
service's defensive handling. The SDK-private patch is confined to this fault test and
the currently pinned SDK version.

## Input identities and digest bases

All digests here are SHA-256 from actual local execution. Original hashes cover exact supplied
bytes (`supplied_bytes`); canonical hashes cover the existing prompt builder's validated-input
UTF-8 JSON (`validated_input_canonical_json_utf8`). Canonical data never replaces original bytes.

| Supplied input | Original/supplied SHA-256 | Canonical validated-input SHA-256 |
| --- | --- | --- |
| [G02](../../data/golden_cases/inputs/G02.json) | `60cbf66dbbb24b59f0ae0a86e03a92d6f0dac0e68511ec05cd1953b96763326f` | `7f077f89d97f17fac644273d0a53c5b108b519d00adcddba0c21a9122f6a58da` |
| [G03](../../data/golden_cases/inputs/G03.json) | `151f108c7df2998f8f417b03e6a1b44a6c3528120fcf24ae27287b4b6007ecb0` | `745a8dae61a86a388f065b0e4e32630b35dea7dd0b475378a62d63d254f6901e` |
| [G04](../../data/golden_cases/inputs/G04.json) | `df2769ace061cb69f587d78dbc6b1b010c820563a0085b60c9ddb5be8a73bc02` | `71deff8de669d74c938acc7a3454d3547168ffeef6748a8cf4e01d5d3fb0f0a4` |
| D missing variant (memory only) | `6ba2f3386ae72fa27ec553f5b9fc003b72a4dfa0b852a936a4b32e420fbf1019` | `3ab9a7a780592b2b7e4453e71c6df793684eb3c9020bfaafd2933c3067e77fd0` |
| D null variant (memory only) | `7593d0b302c3091759435eda71437159bee913a3d7a208b6705eadaab80e978e` | `0c135ff650d686f9c50f5b03a023655ba237701eaf3830f9999eb5ec03cdcf80` |
| [G05](../../data/golden_cases/inputs/G05.json) | `e05078620366578697a9d821d7fbd08829786d44f53d0548741d36ccc245fe09` | `ede847d9bd8d87e7f9e909626bfeb181a786feb41dfb8f8d9b428ebe220ab70e` |
| [Development case 0002](../../data/generated/development/CASE-DEV-S20261027-0002.json) | `11370ba0cd8338fc6d4884c9fc1427e7de1d7d1213d7dc7efbab899f1de5b1d2` | `efc2f9e4066854aaa74feb5e13d266a505fb4dfffd60d6549ac2d31b9575db64` |

The original G04 file is never edited. Its missing/null variants retain the original recorded
check conclusions as supplied entries, even though those entries can be stale relative to
the constructed variant. They are robustness fixtures, not newly adjudicated investigations.
The composer quotes those check conclusions as recorded data and does not rerun their alleged verification.

Golden-input line endings can differ across checkouts; the generated development JSON is protected
by the existing [Git attributes](../../.gitattributes). These are local exact-byte identities,
not promises of platform-independent report hashes. CI derives hashes from its actual fixture
bytes; it never normalizes a file to match this table. A raw-byte change changes the report
identity even if canonical input is unchanged. Identical payloads, metadata and component
versions reproduce the same companion bytes.

## Candidate and serialized companion identities

Hosted candidate digests cover the UTF-8 encoding of the exact returned string
(`utf8_encoded_candidate_text`), not HTTP-envelope bytes. Baseline candidate digests cover
the once-serialized bytes (`supplied_bytes`). Companion hashes cover the unchanged serializer's
complete UTF-8 output, including its single LF terminator. Full reports remain in memory.

| Example | Candidate SHA-256 | Serialized companion SHA-256 | Companion bytes |
| --- | --- | --- | ---: |
| A | `99b129e12bcec3b6a8dea2d6f6144083aad05bc261ebdea34a3b5fe05df09295` | `0c52efb89fdf447a021a32cc105d12a69787ca1681c21c26975556e228119057` | 95879 |
| B | `2c46f051a97ca17d3a18c80ba6857d6f622b2d937a714a29c24e3c3b008bfa31` | `796a5ef31d13483f089c4731424611dcadaad5a6c23a813a6f1268eb98d05223` | 97420 |
| C | `a1ec7366b3977ab76cf0979daa56e68e56bf044976b1d1e0690f836e764d7840` | `80b2f9ffc20dbecf94ebb5848f4d08364667d594828a34145755b55a74a71084` | 93018 |
| D-available | `ee45da1e64ca9d4278c23aa13e3cabf69ecbfb492f855f4cf55905b1071ac886` | `f1cb89ebd686a99f2aed68d5c850905448ed5087e432aec10bda3105e87097b5` | 193279 |
| D-missing | `ee45da1e64ca9d4278c23aa13e3cabf69ecbfb492f855f4cf55905b1071ac886` | `7f2308e35952745b3cc891638d34fdf5fc6a5d96de1d3ac157430445487328ae` | 190356 |
| D-explicit_null | `ee45da1e64ca9d4278c23aa13e3cabf69ecbfb492f855f4cf55905b1071ac886` | `734338c2903f560da81bd32bc80a8b6ff4c5b52659e2cb5d1eec6e57e1132f87` | 190341 |
| E-hosted | `5c596c1548a11c3fd25ea73d1009cec8c9209a5d57f34f5c8235177b9396b5be` | `babfe5425e50836d50ace37dbed9eb2776650962864ba81a69927f1c07436da3` | 89951 |
| F-incomplete | `99b129e12bcec3b6a8dea2d6f6144083aad05bc261ebdea34a3b5fe05df09295` | `a67dfcb3e4bd6c52e80e4f1cad608ff1d7f46c743b21f04915f2d8acf7a97f84` | 12210 |
| F-missing-parsed | `99b129e12bcec3b6a8dea2d6f6144083aad05bc261ebdea34a3b5fe05df09295` | `7d3f3532e00e2aa4b5be9e80be59f6527cd8444c46908d61031765f812d2fc29` | 12206 |
| A-baseline | `382cd2ff8f6678b276660cafb0452caca836fe7bf9eca36946f14064ebe636ee` | `c4e7358d3363f47ab94d3cbb55d5d44fb832269f69a38a329a3ec6887db83fcf` | 119175 |
| baseline-G05 | `e07db29cc9ae08f12d8c38db5111e898489c2ff9ed89f7e613f963d0dee36494` | `7f32ca2e671c3982bc04ced220930ce4db48fba4262f80aad0231dc8061414fc` | 86674 |
| E-baseline | `dc88009b4e1de78fa2af5c38e2405219581b6725ff3b5f1eab50a2a19780f82e` | `19f7bccd31fca21271d9ca96a0dda9abd90c9a3dba89bb2376a935ba45a8aa3a` | 159276 |

## Actual report excerpts

### A - bounded source observation and attributed assessment

`report_state=qualified_companion`; all three mechanical stages passed. One factual finding
was checked and matched; there were no conflicts or unchecked findings in this constructed
candidate. This field match does not validate the recommendation or rationale semantically.

Actual E02 source observation:

> Supplied transaction "TX-G02-01" records USD 48500.00 as "credit" ("domestic_transfer") at "2026-10-13T11:00:00Z"; account reference "ACC-G02", counterparty reference "CP-G02-01". No payment purpose or legitimacy is inferred.

Actual amount binding (excerpt; source values remain JSON text snapshots):

```json
{
  "input_sha256": "60cbf66dbbb24b59f0ae0a86e03a92d6f0dac0e68511ec05cd1953b96763326f",
  "record_type": "transaction",
  "record_id": "TX-G02-01",
  "record_pointer": "/transactions/0",
  "field_pointer": "/amount",
  "input_pointer": "/transactions/0/amount",
  "value_json": "\"48500.00\"",
  "missing_member": null,
  "evidence_state": "verified_against_supplied_evidence"
}
```

The submitted candidate text is `Transaction TX-G02-01 amount was USD 48,500.00.` at
`/factual_findings/0/statement`; its submitted citation is
`{"record_type":"transaction","record_id":"TX-G02-01"}`. The rationale repeats it as a
separate occurrence. Original ordered citations and whole statements are preserved.

### B - restricted deterministic conflict

Service status is still `validated` under its existing mechanical-stage semantics.
The companion is qualified, with `restricted_conflict` in both qualification reasons and
structured diagnostics at `/factual_findings/0/statement`.

Actual reviewer-facing conflict unit:

> RESTRICTED FIELD CONFLICT: conflicts_with_record; candidate "The incoming transaction was USD 99,999.00."; compared fields=[{"claimed":"99999.00","field":"amount","matches":false,"recorded":"48500.00","source":{"field_pointer":"/amount","record_id":"TX-G02-01","record_type":"transaction"}},{"claimed":"USD","field":"currency","matches":true,"recorded":"USD","source":{"field_pointer":"/currency","record_id":"TX-G02-01","record_type":"transaction"}},{"claimed":"credit","field":"direction","matches":true,"recorded":"credit","source":{"field_pointer":"/direction","record_id":"TX-G02-01","record_type":"transaction"}}]. Checked fields conflict with the cited record. No whole-statement semantic approval.

Its bindings include `/transactions/0/amount`, `/transactions/0/currency` and
`/transactions/0/direction`; its check pointer is
`/validation/audit/deterministic_fact_checks/findings/0`. Claimed amount is `99999.00`,
recorded amount is `48500.00`; the original claim and citation remain unchanged.
The conflicting claim does not appear in `source_observations`.

### C - unchecked process assertion

Actual attributed candidate unit:

> The supplied candidate (recorded producer "OpenAIAssessmentService") states "This software authenticated all supplier documents.". Semantic support is not evaluated.

The occurrence at `/factual_findings/0/statement` has `semantic_review=not_evaluated`.
The restricted checker reports zero checked and one `not_checked` finding; its status is
`not_evaluated`. There is no source observation claiming authentication. Neither the
resolved transaction citation nor the service's `validated` status supplies process authority.

### D - differing source excerpts and field absence

The original G04 report preserves these separate E04 excerpts:

> Supplied evidence "EV-004" records beneficiary_account_ref="SUPPLIER-ACC-A". This is a recorded reference, not proof of recipient legitimacy.

> Supplied evidence "EV-005" records beneficiary_account_ref="BENEFICIARY-ACC-B". This is a recorded reference, not proof of recipient legitimacy.

No new beneficiary-comparison predicate, source precedence or fraud verdict is generated.
The existing supplied check's stated comparison remains attributed to that supplied check.

| In-memory condition | Actual binding pointer | `missing_member` | Observed state |
| --- | --- | --- | --- |
| Original populated invoice field | `/evidence/3/facts/beneficiary_account_ref` | null | `available` |
| Deleted invoice field | `/evidence/3/facts` | `beneficiary_account_ref` | `missing` |
| Invoice field set to JSON null | `/evidence/3/facts/beneficiary_account_ref` | null | `explicit_null` |

All three reports remain qualified and retain the wire reference. The missing/null invoice
field is not described as a demonstrated account mismatch. No original G04 bytes are changed.

### E - valid abstention

Actual mocked candidate scalar/rationale excerpt:

```json
{
  "assessment_status": "unable_to_recommend",
  "recommended_action": null,
  "rationale": {
    "statement": "No recommendation is supplied in this test response.",
    "citations": []
  },
  "recommendation_scope": "preliminary",
  "human_review_required": true
}
```

The real baseline on development case 0002 independently returns `unable_to_recommend`
with null action, preliminary scope and human review required. Its actual rationale is:

> [BASE-01] Unable to recommend: no supported decision rule supplies sufficient justification in this limited baseline. Arithmetic agreement does not justify closure; closure corroboration remains under review.

Abstention can retain factual findings: this baseline has eight findings, three restricted
matches and five unchecked findings. The constructed hosted abstention has no findings.
Neither is transformed into an `investigate` recommendation.

### F - failed generation despite parseable text

Both the incomplete response and missing-parsed-output fault retain the exact A candidate
text and digest. Its structure, references and one restricted amount match can be replayed,
but that does not convert failed generation to a successful assessment.

Actual diagnostic excerpt for the incomplete response:

```json
{
  "service_status": "failed",
  "generation_status": {
    "value": "incomplete",
    "evidence_state": "recorded_not_independently_verified",
    "reason": "Recorded caller metadata; not independently verified."
  },
  "report_state": "rejected",
  "candidate_content": null,
  "narrative_units": [],
  "diagnostics": [
    {
      "severity": "rejection",
      "code": "generation_not_completed",
      "location": null,
      "message": "Supplied generation outcome is not a completed assessment."
    }
  ]
}
```

The missing-parsed-output fault instead retains service category `missing_output`, maps to
`generation_status=failed`, and returns the same `generation_not_completed` diagnostic.
Original producer records, accessible fragments and hashes remain unchanged. Separately
tested malformed/contract-invalid SDK responses demonstrate the existing limitation:
SDK parsing can fail before original candidate text becomes accessible; unavailable bytes
remain unavailable and no parsed substitute or fabricated abstention is introduced.

## Outcome handoff and audit representation

`companion_for_run` is test-local integration logic, not a public runtime component.

| Actual/supplied service state | Composer generation status | Result requirement |
| --- | --- | --- |
| `validated`, with accepted assessment and exact text | `completed` | Eligible only after composer gates; still qualified |
| `failed`, error category `refusal` | `refused` | Rejected diagnostic |
| `failed`, error category `incomplete` | `incomplete` | Rejected diagnostic, including parseable text |
| Other `failed` | `failed` | Rejected diagnostic |
| `dry_run`, unknown/absent status, or validated label without assessment/text | `failed` in this test-local diagnostic branch | Never accepted; original producer status is preserved |

Only the real default dry run is an observed service outcome. Unknown/absent status and
validated-without-assessment cases are deliberately altered copies of a synthetic run,
used to challenge the handoff. They do not describe a newly observed service defect.

The service's audit is bound to canonical input text (`utf8_encoded_string` in the auditor).
The companion's audit is bound to original input bytes (`supplied_bytes`). Candidate text
has the same UTF-8 digest in both audits. Example A has different raw/canonical input hashes
as recorded above; its validation stages and restricted-check outcomes agree exactly.
Complete audit objects are not required to be identical. The test checks the companion's
canonical input digest against the service's recorded canonical digest.

Changed source content after assessment is rejected through the canonical identity binding.
A composer failure leaves the original producer `validated` record intact while rejecting
the companion. No second generation, replacement candidate or successful fallback occurs.

## Verification results and limits

- Focused integration tests: **16 passed, 0 failures/errors/skips**.
- Complete discovery: **499 tests; 499 passed, 0 failures, 0 errors, 0 skips**.
  The discovery method used by existing CI found all 16 new tests.
- `pip check`: **No broken requirements found**.
- In-memory syntax compilation: **36 Python files passed**, without writing bytecode.
- Local runtime: **Python 3.11.9**, Pydantic **2.14.1**, OpenAI **3.40.0**, httpx2 **2.16.0**.
- Existing report schema/composer/template: **1.0 / 0.1.0 / 1.0**; baseline **0.1.0**;
  auditor **0.2.0**, restricted amount checker **1.0**.
- All broader audit semantic dimensions remain `not_evaluated`; the companion retains
  `{"status":"not_evaluated","scoring_authorized":false}`.

Full-suite command actually used locally (an SDK-only empty environment facade prevents
existing SDK tests from discovering real optional credentials; the real environment is unchanged):

```powershell
@'
import sys, unittest
from types import SimpleNamespace
from unittest.mock import patch
with patch('openai._client.os', SimpleNamespace(environ={})):
    suite = unittest.defaultTestLoader.discover('tests')
    result = unittest.TextTestRunner(verbosity=1).run(suite)
sys.exit(not result.wasSuccessful())
'@ | .\.venv\Scripts\python.exe -B -
```

The existing [CI workflow](../../.github/workflows/foundation-tests.yml) runs
`python -m unittest discover -s tests -v` with constrained dependencies on Python
3.11, 3.12 and 3.13. No workflow/dependency change is made. Linux and Python 3.12/3.13
execution and remote CI have **not** been freshly verified here. Existing optional research
packet skips remain unchanged; the new integration tests require no ignored outputs.

Other actual local checks:

```powershell
.\.venv\Scripts\python.exe -B -m pip check
.\.venv\Scripts\python.exe -B scripts/check_setup.py
git diff --check
```

Syntax was checked by compiling every Python source under the existing source, script,
test and research directories in memory. New untracked files also receive explicit
Git whitespace checks; ordinary `git diff --check` alone does not inspect them.
The foundation smoke check passed its file/CLI checks, but its status payload still
contains historical Week 1 `false` implementation flags. That payload is not current
pipeline-capability evidence. Updating that existing runtime status is outside this scope.

## Preservation and remaining acceptance work

The starting preservation snapshot covered 353 pre-existing project/evidence files
(205 under local ignored outputs), excluding Git internals, the virtual environment
and rebuildable caches. Final verification matched all 353 original file sizes and SHA-256
digests, with no changed or removed original and exactly the two authorized additions.
The separately hashed Git index and handoff ZIP are unchanged. All 34 distinct documented
input/canonical/candidate/report hashes match the actual in-memory example records;
the quoted source observation, binding, conflict unit, unchecked quote and baseline
abstention rationale also match those records. All 16 relative links resolve and all
three JSON excerpts parse. Git whitespace checks are clean after removing one extra
EOF blank line. For untracked additions, `git diff --no-index --check -- NUL <file>`
returns the expected difference status 1 with no whitespace diagnostics; Git's LF/CRLF
conversion warnings are not permission to normalize frozen evidence. No existing
status, worklog or decision entry is edited.
The new evidence is reviewed documentation and in-memory tests, not a newly frozen experiment packet.

This checkpoint demonstrates both producer-to-report paths, bounded source bindings,
explicitly qualified conflicts, attributed unchecked content and safe failure/abstention
handling. It does not establish semantic correctness, classification accuracy, policy
equivalence, model superiority, evidence authenticity or independent AML expert validation.
The model, request IDs and usage values in mock responses are synthetic test metadata,
not provider receipts. The SDK version is read from installed package metadata.
No held-out example, numerical semantic score or new experimental result is produced.

E01-E06 and existing contracts remain unchanged. P01/P02 remain approved; P03 remains open
with scoring disabled; P04/P05 controls remain separate. G02 case-specific adjudications
are not generalized. Week 5 artifacts remain frozen; Week 7 evaluation independence is preserved.

Owner review must decide whether this library integration and these bounded/qualified
examples satisfy the original Week 6 completion evidence. Progress-document reconciliation
and any formal Week 6 acceptance are later authorized work. CLI/publication, broader
predicates, extra renderers, hosted calls and semantic evaluation are not automatic next steps.
