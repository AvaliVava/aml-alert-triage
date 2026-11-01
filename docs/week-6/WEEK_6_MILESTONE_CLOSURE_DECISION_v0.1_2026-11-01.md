# Week 6 milestone closure decision - v0.1

**Decision ID:** W6-MILESTONE-CLOSURE-2026-11-01-v0.1

**Owner approval date:** November 1, 2026. The exact approval time was not supplied.

**Status:** Formally accepted by the project owner. Week 6 — Evidence Validation,
Narrative Drafting and Integration — is closed on its bounded engineering objective.
Week 7 has not started and is not authorized.

## 1. Authority and original objective

The owner's instruction, "CODEX — FORMALLY RECORD OWNER-APPROVED WEEK 6 MILESTONE CLOSURE",
explicitly accepts the completed work and limitations. This document records that decision;
it does not reconsider it. Conversation approval is not an independently authenticated
approval receipt, independent AML expert validation, Git publication or an evaluation release.

The unchanged [roadmap](../../ROADMAP.md) specifies:

> Objective: Evidence validation, narrative drafting and integration
>
> Evidence required: Full pipeline, integration tests, grounded report examples

The accepted interpretation is an executable **library-level full pipeline** through
the existing baseline or mocked hosted assessment service, auditing and qualified evidence
report composition. It satisfies the owner's bounded engineering interpretation without
claiming a standalone operational CLI, deployment or new orchestrator. The
[charter](../../PROJECT_CHARTER.md) retains its broader research and evaluation objectives.

## 2. Verified implementation history

Local Git history at starting HEAD `fd63925e365c88732df84778f8a30140ca942e8d` verifies
both source commits, merge commits, parent relationships and added-file populations.

| Change | Source commit | Merge commit | Added files |
| --- | --- | --- | ---: |
| [PR #18](https://github.com/AvaliVava/aml-alert-triage/pull/18) | `3ea402bcfd0456fa915196c32d65402eb2e3dc7e` | `6d851fc8c9556cc24aa35eacfa657f75dbca8aa1` | 4 |
| [PR #19](https://github.com/AvaliVava/aml-alert-triage/pull/19) | `82559e73d4dac76ebfe5976747ceed634bc9fb68` | `fd63925e365c88732df84778f8a30140ca942e8d` | 2 |

PR #18 added the [design specification](WEEK_6_EVIDENCE_REPORT_DESIGN_SPEC_v0.1_DRAFT.md),
[implementation contract](EVIDENCE_REPORT_IMPLEMENTATION_CONTRACT_v0.1.md),
[evidence composer](../../src/aml_triage/evidence_report.py) and
[focused tests](../../tests/test_evidence_report.py). It implements E01–E06 source observations,
pointer/digest bindings, deterministic narrative units, preserved candidate occurrences,
qualified conflicts and diagnostic rejection in a separate JSON companion.

PR #19 added [integration tests](../../tests/test_week6_pipeline_integration.py) and
[integration evidence](WEEK_6_INTEGRATION_EVIDENCE_v0.1_DRAFT.md), covering six evidence
scenario families and 16 integration tests. Test-local handoff logic connects existing
interfaces; it is not a new public production interface.

These are local original-byte SHA-256 bindings of the six merged artifacts inspected for
this decision. They are distinct from Git object identities and canonical input hashes.

| Existing artifact | Local original-byte SHA-256 |
| --- | --- |
| [WEEK_6_EVIDENCE_REPORT_DESIGN_SPEC_v0.1_DRAFT.md](WEEK_6_EVIDENCE_REPORT_DESIGN_SPEC_v0.1_DRAFT.md) | `36dbc0b4a162a44e2b5e36772e09829a7db5f77bf4161ed982277f0d61c4992c` |
| [EVIDENCE_REPORT_IMPLEMENTATION_CONTRACT_v0.1.md](EVIDENCE_REPORT_IMPLEMENTATION_CONTRACT_v0.1.md) | `0979f6eab9767cf1c9596113349467eeac5c685a5d20c06a0a6aeab1afd52aa0` |
| [evidence_report.py](../../src/aml_triage/evidence_report.py) | `793aedd14c7cee9a7d475e1bd94aeba3f02a0f232caa9b07c0870ea981400de4` |
| [test_evidence_report.py](../../tests/test_evidence_report.py) | `164f77f18a12750ce095ecb389f04d6a790241547cb0f2fc4e6d3d85af3a56c7` |
| [test_week6_pipeline_integration.py](../../tests/test_week6_pipeline_integration.py) | `83bf00d562424134fa82c1096dd6f19e82e17c180bbf05da5f42b6d2fbe8a3f1` |
| [WEEK_6_INTEGRATION_EVIDENCE_v0.1_DRAFT.md](WEEK_6_INTEGRATION_EVIDENCE_v0.1_DRAFT.md) | `cf2108044d7eaf10976bed9d47b2d27bdd0d750f01f631ce0393df09f9f38e61` |

## 3. Owner-accepted Week 6 evidence matrix

| Requirement | Existing evidence and established behavior | Boundary retained |
| --- | --- | --- |
| Source evidence validation | Composer and contract: exact input/candidate identities; typed record IDs and field pointers; existing input/output/contextual validation; mandatory binding gates | Source lookup is not substantive support or source authenticity |
| Deterministic narrative composition | E01–E06, versioned JSON companion, source-derived units and unchanged candidate occurrences in composer tests | No arbitrary prose understanding, new AML policy or general factual certification |
| Baseline-to-report integration | `test_real_baseline_pipeline_preserves_once_serialized_candidate_and_audit`: validated input -> real baseline -> once-serialized candidate -> composer/audit -> serialization | Newly constructed in-memory test assessments do not replace frozen baselines; actions are not truth labels |
| Mocked-hosted-to-report integration | `test_example_a_sdk_pipeline_preserves_text_and_separate_audit_representations`: real SDK/MockTransport, exact candidate text and canonical/raw identities | Synthetic test responses, no hosted execution; distinct audits need not have identical bytes |
| Integration tests | PR #19 test module: 16 integration tests discovered by the existing unittest command | Historical local pass evidence; no fresh test replay in this documentation checkpoint |
| Grounded and qualified examples | Integration evidence A–F: bounded field observation, recognized amount conflict, unchecked assertion, missing/null/differing sources, abstention and failed generation | Grounded means traceable eligible supplied fields; no overall semantic pass |
| Failure propagation and abstention | Parseable incomplete and missing SDK-parsed outputs rejected; refusal/other failure/dry-run/unknown states cannot become accepted companions; null action retained | No repaired candidate, fabricated abstention or successful fallback; report failure does not rewrite the producer record |
| Reproducibility and CI | Deterministic serialization, representation-specific hashes, tracked/constructed fixtures, reported local checks and owner-reported successful PR #19 matrix | Same explicit payloads/provenance/versions required; CI workflow definition alone is not proof of a run's success |

All rows are accepted by the owner as sufficient bounded engineering evidence. No
semantic-quality category, score, denominator or AML disposition is approved by this matrix.

## 4. Verification evidence and its provenance

| Evidence | Result accepted with the owner decision | Provenance and verification limit |
| --- | --- | --- |
| Composer checkpoint | 45 focused tests reported passing locally | Prior Codex local report cited by owner approval; current source contains 45 test methods, but definition count alone is not pass evidence |
| Integration checkpoint | 16 focused tests reported passing locally | Merged integration evidence and earlier Codex execution report |
| Complete integration-checkpoint suite | 499 local tests reported passing, zero failures/errors/skips | Merged integration evidence; no claim of 499 tests independently rerun here or of identical CI counts |
| Local engineering checks | Dependency consistency, foundation smoke, syntax and whitespace checks reported successful | Historical integration checkpoint, as documented in its evidence record |
| GitHub Actions, PR #19 | Successful Python 3.11, 3.12 and 3.13 jobs, including dependency, foundation smoke and unit checks | Owner-supplied observation of GitHub CI, separate from Codex's local report; CI logs were not independently retrieved by Codex in this checkpoint |

The local [workflow](../../.github/workflows/foundation-tests.yml) independently confirms
the three-version matrix and commands: constrained installation, `python -m pip check`,
`python scripts/check_setup.py`, and `python -m unittest discover -s tests -v`.
The owner's reported result is associated with [PR #19 checks](https://github.com/AvaliVava/aml-alert-triage/pull/19/checks).
No run/job identifier, remote log, terminal receipt or CI test count is invented.

The earlier integration record correctly says remote CI had not been freshly verified
at that checkpoint. The owner's later CI observation and milestone approval are recorded
here without rewriting that historical statement. The foundation status payload's old
Week 1 flags remain a disclosed limitation, not a capability detector or closure blocker.

This documentation checkpoint verifies history, artifact identities, source/test interfaces,
links, document consistency, preservation and Git whitespace. It does **not** execute
the runtime test suite, regenerate assessments, call a live API or inspect credentials.

## 5. Accepted limitations and tradeoffs

- No general semantic correctness or full factual verification is established. Only
  restricted deterministic checks and bounded E01–E06 source observations are claimed.
- No classification accuracy, recall, precision, model superiority or held-out generalization
  is established. Matching a restricted amount predicate does not validate a full statement.
- Unsupported or unchecked candidate assertions remain attributed and unevaluated.
  Citation existence and supplied-record bindings do not authenticate sources or corroborate
  every assertion. Recorded verification conclusions are not new verification by this software.
- There is no independent AML subject-matter validation, production banking integration
  or regulatory compliance claim. Preliminary scope and mandatory human review remain;
  required review is not completed review.
- There is no standalone operational end-to-end CLI, deployment or new orchestrator.
  Existing individual CLIs remain separate. Producer-outcome handoff is demonstrated
  through test-local integration logic rather than a new public production interface.
- Mocked hosted responses are synthetic test responses, not new provider receipts.
  SDK parsing can prevent access to invalid original text; unavailable bytes are not reconstructed.
- Exact original bytes, canonical input and candidate-string UTF-8 retain separate
  digest bases. Line endings and supplied optional metadata can change report bytes.
- Existing optional research-packet test behavior remains unchanged. New integration
  tests use tracked/constructed fixtures and do not require ignored experiment outputs.

Further runtime development is not required merely to satisfy this owner-approved
bounded milestone. A CLI/publication layer would add operational responsibilities beyond
the accepted library demonstration; it requires evidence of need and separate authorization.
Additional prose predicates, renderers, model calls and semantic evaluators are not implied.

## 6. Evaluation, release and preservation controls

- [P01](../phase-2/G02_P01_FIDELITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) and
  [P02](../phase-2/G02_P02_MATERIALITY_DECISION_ADDENDUM_v0.1_2026-11-01.md) remain approved,
  case-specific owner rulings. They are not generalized or reopened.
- P03 remains under review; numerical semantic scoring remains disabled. No ranking,
  metric, denominator release or overall factual pass is authorized.
- P04 formal adjudication/report release and P05 independence/expert-review conditions
  remain separately controlled. This milestone decision does not release G02 semantic evaluation.
- All nine broader audit semantic dimensions remain `not_evaluated`.
- [Week 5 closure](../week-5/WEEK_5_MILESTONE_CLOSURE_DECISION_v0.1_2026-11-01.md), frozen
  experiments, original candidates/baselines, G02 annotations/reports and all consumed live
  allowances remain unchanged. No allowance reset, hosted request or new spending is authorized.
- Week 7 held-out evaluation independence remains required. Development fixtures do not
  become independent evaluation data through report composition or milestone acceptance.

Before editing, a size/SHA-256 snapshot covered **355 pre-existing project/evidence files**,
including **205 ignored local output files**, plus a separate Git-index digest and Git ref
snapshot. Git internals other than the separately checked index/refs, virtual environments
and rebuildable caches are outside that file snapshot. No secret-bearing file was inspected.
The authorized changes are one new closure document and additive updates to current status,
worklog, decisions and current roadmap progress. Original historical content remains intact.
Post-edit verification matched all 351 pre-existing files outside the four authorized
existing documents, including all 205 local output files and the handoff ZIP. Removing
only the new additions from each modified document recovers its exact original SHA-256;
the roadmap table and historical entries therefore remain byte-for-byte intact.
The closure document is the sole new file; the Git index and ref set are unchanged.
All 40 new relative links/anchors resolve, artifact hashes and commit identities match,
and whitespace checks pass. No runtime tests were rerun. No backup or cloud operation
is performed.

Earlier design/contract/evidence statements limiting implementation or leaving milestone
acceptance pending describe their historical checkpoints. The successive owner authorizations
and this formal bounded closure supersede those timing statements only. Draft provenance,
semantic restrictions and frozen records remain intact. Older status/worklog/ADR statements
that Week 6 was unauthorized remain historical; the new current notice and ADR-017 govern.

## 7. Completion and next authorization boundary

**Week 6's original bounded engineering objective is formally closed by owner approval
on November 1, 2026.** The full library flow, integration tests and grounded/qualified examples
are accepted within the limits above. This is not completion of the entire Phase 2 research program.

The decision is also recorded in [current status](../../PROJECT_STATUS.md),
[ADR-017](../../DECISIONS.md#adr-017--close-week-6-on-bounded-evidence-report-and-library-integration-evidence),
[worklog](../../WORKLOG.md) and [current roadmap progress](../../ROADMAP.md#current-roadmap-progress).
Historical content and the original eight-week table remain unchanged.

**Week 7 has not started and is not authorized.** It requires a separate readiness review,
applicable evaluation-protocol decisions and explicit owner authorization before work begins.
No hosted execution, scoring, Git publication or further implementation follows automatically.
