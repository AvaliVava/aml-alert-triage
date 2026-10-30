# G02 calibration research tools - unreviewed draft

This integrates compatible files from the owner's
`G02_Codex_Calibration_Implementation.zip` handoff. These standard-library tools
organize seven calibration bundles, 38 selected review units, H-00 through H-07
rule hypotheses and 13 conceptual counterfactuals. They check mechanical
traceability and prepare human review. They do not evaluate general semantic
truth, approve labels or rules, assign scores, or rank candidates.

See the [draft calibration plan](../../docs/week-4/G02_SEVEN_BUNDLE_CALIBRATION_PLAN_DRAFT.md),
[original integration handoff](../../docs/week-4/CODEX_REPOSITORY_INTEGRATION_TASK.md),
[paired pilot](../../docs/week-4/G02_PAIRED_EVALUATION_PILOT_DRAFT.md) and
[annotation proposal](../../docs/week-4/G02_ANNOTATION_FORMAT_DRAFT.md).

## Source and conflict handling

- The repository's root README was preserved. This file replaces the archive's
  standalone README instructions for use inside this repository.
- The archive's nested packet contains the same nine file bytes as the existing
  ignored [local pilot packet](../../outputs/evaluation/g02-paired-pilot-20261029/).
  That existing directory remains the default and is never modified by these tools.
  No duplicate ZIP or extracted candidate is introduced into Git.
- The [catalog](calibration_cases.draft.json) preserves the supplied unit text,
  proposed judgments, bundle order and conceptual tests. Integration adds exact
  SHA-256 bindings for all nine existing packet files. Bundle order and wording
  remain proposals; importing them is not adjudication.
- The catalog's `frozen_packet_sha256` identifies the original ZIP container.
  Directory-mode reports verify individual artifact bytes and explicitly report
  `zip_bytes_verified=false`; they do not pretend to verify ZIP bytes from a directory.
  An explicitly supplied original packet ZIP is also supported and its bytes checked.
- The supplied HTML and inspection report were not imported as current results.
  Generate fresh views from verified local artifacts instead. The outer handoff ZIP
  is preserved unchanged; its SHA-256 is
  `da48d846bfa772f972b94f4ef79c24aa4821c730643477f7ad9e9009aea80f0b`.

## Offline use

Run from the repository root using the existing environment. No installation,
API key, network access or model request is needed for these research tools.

```powershell
.\.venv\Scripts\python.exe -B research\evaluation_calibration\hybrid_calibration.py
.\.venv\Scripts\python.exe -B research\evaluation_calibration\hybrid_review_preview.py
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p "test_hybrid*.py" -v
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

To save new, ignored local review artifacts, choose destinations that do not exist:

```powershell
.\.venv\Scripts\python.exe -B research\evaluation_calibration\hybrid_calibration.py --output outputs\evaluation\my-calibration\inspection.json --blank-review outputs\evaluation\my-calibration\worksheet.json
.\.venv\Scripts\python.exe -B research\evaluation_calibration\hybrid_review_preview.py --output outputs\evaluation\my-calibration\preview.json
.\.venv\Scripts\python.exe -B research\evaluation_calibration\build_calibration_review_ui.py --output outputs\evaluation\my-calibration\review.html
```

All output paths refuse existing files. Outputs are individual files, not an atomic
multi-file publication; an earlier newly created output can remain if a later output
fails. The HTML builder requires an explicit destination. It embeds exact source
fields and proposed annotation links, performs no remote requests, and exports
unreviewed notes only. Notes are held in the browser tab until exported; they are
not automatically saved or treated as human approval.
The HTML is a generated snapshot; rerun integrity checks and build a new view if
any source artifact changes.

`--packet` selects an explicit directory or packet ZIP; `--catalog` selects the
catalog. Missing or mismatching artifacts are errors, with no automatic recovery
or reconstruction. The tools are intentionally specific to this frozen G02 draft.

## Tests, review and limitations

The supplied tests check integrity, draft-state guards, citation membership,
numeric-comparison preconditions and repeated occurrences. Added integration tests
exercise directory/ZIP loading, artifact bindings, source-preserving views,
finite Decimal comparisons, no-network/no-extra-file access, HTML escaping and CLI
overwrite refusal. They do not execute the proposed semantic counterfactuals.

On a fresh checkout without the ignored local packet, the two packet-dependent
test classes explicitly skip with a reason. The portable directory/ZIP adapter
tests still run. A skipped packet test is not evidence that the G02 calibration
packet was verified; local artifacts must be supplied explicitly to exercise it.

The [blank worksheet](blank_review_worksheet.json) binds the input, candidates and
packet files. Reviewer/adjudicator identities and semantic judgments remain unset.
The tools reject unexpected approvals in this unreviewed draft format; they are
not an adjudication-release system. Those original draft tools do not consume the
later owner register described below. Remaining fidelity, source-sufficiency,
materiality, reviewer-responsibility and denominator decisions are governed by the
[evaluation protocol](../../docs/phase-2/EVALUATION_PROTOCOL_DRAFT.md) and the
register's explicit limitations.

No application contract, baseline, auditor, prompt, hosted behavior, dataset,
dependency or policy is changed. G02 remains exposed synthetic development data,
with unequal policy access between the two configured candidates. Neither the
AI-authored draft nor this integration constitutes independent AML expert review.

## G02 owner-register reconciliation — non-scoring research

[g02_reconciliation.py](g02_reconciliation.py) consumes the separate
[draft adjudication register](../../data/evaluation/G02_Adjudication_Register_v0.1_DRAFT.json)
under the [reporting specification](../../docs/phase-2/G02_Reconciliation_Audit_and_Reporting_Spec_v0.1_DRAFT.md).
It reuses the packet verifier, catalog integrity checks and application mechanical
auditor. It verifies all 75 original units and 21 statement occurrences, exact
text, offsets, JSON pointers, submitted citations, source-pointer bindings,
artifact hashes and declared populations. It does not generate semantic judgments.

Run from the repository root, choosing a new report destination:

```powershell
.\.venv\Scripts\python.exe -B research\evaluation_calibration\g02_reconciliation.py --output outputs\evaluation\my-reconciliation\report.json
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_g02_reconciliation.py -v
```

Without `--output`, the complete report is printed as JSON. Explicit `--register`,
`--packet`, `--input` and `--catalog` paths select the bound sources. Missing or
altered artifacts cause rejection, not reconstruction. The output refuses
existing files and destinations inside the frozen packet directory. Exit codes
are 0 for successful non-scoring reconciliation, 1 for expected validation or
release-gate rejection, and 2 for I/O or unexpected execution errors. Success
does not mean an assessment passed semantic evaluation.

The Python interface is `build_reconciliation(register_path=..., packet_path=...,
input_path=..., catalog_path=...)`. Import it with this research directory on
`sys.path`, following the existing research tests. `load_register(path)` loads and
checks root fields; `validate_register(register, raw, docs, input_json)` checks
the detailed frozen bindings. The complete builder also enforces catalog hashes
and existing mechanical validation. It never changes source artifacts.

Reports preserve each original AI-draft annotation beside its recorded owner
decision, with separate factual support, citation applicability/adequacy,
whole-statement, process-authority and material-coverage sections. Counts reproduce
the register's 10 qualified factual passes, 3 qualified investigative questions
and 8 reviewed but not cleared statements. M01–M03 are the mandatory G02 items;
M04 and M05 remain contextual. Repeated baseline M02 occurrences remain visible
without additional coverage credit. The registered action and alternative-action
restriction are reported without changing the provisional reference.

Raw-file SHA-256 digests bind the original input and candidate bytes. Canonical
digests identify separately serialized validated models and never replace raw
bindings. Directory-mode verification does not authenticate historical ZIP bytes.
Register identity and provenance are recorded declarations, not independently
authenticated approval events. Missing structured review states, reviewer/event
IDs, dated revision history and rubric version are reported as missing, not
inferred from prose. Original context pointers remain available alongside copied
support/opposing pointers; mechanical pointer validity does not certify source
sufficiency.

All numerical rates and scoring are disabled; `build_reconciliation(scoring=True)`
raises `ReconciliationError`. H004/H034 fidelity exclusions, H047's narrow scope,
H049's ambiguity and the register's P01–P05 gates remain explicit. Process-domain
observations do not certify independent runtime execution or completed human
review. The original draft-state guards and all nine broad auditor semantic
`not_evaluated` results remain unchanged. This is one exposed synthetic
development case, with no held-out, independent expert or model-ranking claim.

The 30 packet-dependent reconciliation tests explicitly skip if the ignored local
packet is absent; the five register-parser tests still run. Supplying the original
bound packet is necessary to reproduce the complete local verification.
