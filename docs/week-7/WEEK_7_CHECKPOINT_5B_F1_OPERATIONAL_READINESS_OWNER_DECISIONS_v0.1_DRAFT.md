# Week 7 Checkpoint 5B — F1 Operational Readiness Owner Decisions (v0.1 DRAFT)

**Status:** Owner-approved procedural and role decisions, consolidated for repository consistency review. **Not an actual F1 freeze, authorization, or verified preservation event.**

**Discussion date:** 2026-11-02 (owner responses in conversation; exact independent event timestamps not authenticated).

**Repository reference (reported Checkpoint 5A):** `main` at `383845b742b7d3ec0fe2d9133fbca6186a5a065d`; independently reverify before subsequent operational work. Earlier provisional OP02 reference: `807de6e39ca0cc8730f61372e2c43402060ccd84` (Checkpoint 3C). The Checkpoint 4C merge is documentation-only according to the 5A audit. **No component freeze is claimed.**

## 1. Governing context and scope

This record implements, but does not replace or reopen, Week 7 W7-S01–S07, W7-PF01–PF14, W7-OP01–OP08 and applicable historical P01–P05 controls. Original baseline and original hosted candidates are the initial measurement artifacts; composer-generated reports remain outside initial semantic presentation unless separately authorized. Keep baseline/hosted policy-access differences explicit. P03 numerical semantic scoring remains unresolved, P04 formal report release and P05 held-out independence/expert-validation claims remain separately controlled.

Checkpoint 5A was a read-only evidence inspection. It found no unexplained producer-component differences, identified hashes of the current checkout/Git representations, instruction and schema digests, a matching pinned dependency environment and a passing `pip check`. It did not generate cases, run assessments, access the provider, perform preservation or freeze the system. Its technical inventory is **supporting inspection evidence**, not a completed F1 manifest or an authorization.

## 2. Owner decisions

### W7-5B-01 — F1 custodian and release authority — APPROVED

The project owner accepts both actual F1 freeze-custodian responsibility and F1 release-authority responsibility. Role overlap and prior development exposure must be disclosed. Codex may assist with preparation or mechanical checks only under specifically authorized task scope; ChatGPT may assist with analysis and review. No AI role is presented as an independent human reviewer. **Role assignment does not authorize the actual freeze.** For release records, identify the actual owner actor and approval provenance; do not invent a personal identifier or timestamp.

### W7-5B-02 — Historical exposure declaration — APPROVED PROCEDURE

Use an evidence-backed, non-exhaustive declaration distinguishing (1) documented exposure linked to actual artifacts, (2) exposure personally confirmed by the owner, and (3) unknown or incomplete exposure. Preserve relevant knowledge of golden/development cases, G02 input/reference/candidate and adjudication materials, family construction recipes, historical baseline/hosted behavior, and AI-assisted contexts as supported by records; do not infer an individual's viewing of every file from general repository access. Record actors, roles, materials, version/context where known, source of claim, uncertainty and potential influence. Future discoveries require versioned amendments, not silent rewrites. **Actual person-specific owner declaration is still pending.** No claim of blinding, independent authorship or independent AML validation follows from this procedure.

### W7-5B-03 — Versioned F1 evidence and approval record design — APPROVED PROCEDURE

Four separately identifiable logical records, implementable as compact versioned JSON without a database:

1. **F1 manifest:** study/record/schema version, source revision, exact included/conditional components, original checkout byte sizes and SHA-256, Git representation/blob identities and their distinct digest basis, exact instruction-string identity, generated schema identities and serialization basis, runtime/dependency observations, intended OP03 settings, excluded components, permitted changes and limitations.
2. **Custody and exposure record:** actual roles, source-backed exposure, personal declarations, AI context and unresolved uncertainties.
3. **Preservation evidence record:** approved primary/independent destinations, access and fault boundary, scope, integrity checks, recovery procedure and actual verification evidence when performed.
4. **F1 owner approval record:** actual actor and separate approval event, exact completed manifest-byte SHA-256, prerequisite evidence identities, authorized scope, conditions, stop rules and distinct status.

The manifest must be finalized and checked before any approval is bound to its exact hash. The approval record must not be embedded in the manifest being hashed. Prepared or `verified_pending_approval` records are not a freeze. Corrections are new versions retaining superseded bytes. Every replacement manifest has a distinct byte identity; an earlier approval remains bound to its original manifest digest. Before use, a replacement manifest requires a new explicit owner approval binding its exact digest. Material changes additionally require substantive review. Later verification records may be appended separately without rewriting the approved manifest. The design approval **does not authorize record creation, preservation operations or F1 release**.

### W7-5B-04 — Independent preservation and recovery — APPROVED POLICY

W7-5B-04 approves a stronger F1 preservation approach than the earlier OP07 minimum: a local working evidence copy and a separately retained **off-device preservation copy are required**. An additional independent local physical-disk copy is optional. Encryption is preferred, subject to an owner-approved method. Any alternative preservation arrangement requires an explicit owner amendment. Document specific artifact scope, local primary and off-device destinations, failure separation, actor permissions, access and retrieval, checksum integrity and recovery verification. Use versioned, non-overwriting preservation records and retain superseded versions. Do not assume two drive letters indicate independent failure boundaries or that a synchronized cloud folder alone gives immutable preservation. Actual destinations, platform, archive/encryption/retention method and recovery-test steps remain pending; no destination, method or successful preservation event is established as verified by this record. **No copying, uploading, backups or recovery testing were authorized by this policy approval.**

### W7-5B-05 — F1 readiness, release and completion sequence — APPROVED PROCEDURE

Required sequence:

1. Complete actual evidence-backed owner exposure and custody declarations.
2. Finalize exact F1 manifest, record formats, inventory, representation identities and permissible-change limits; refresh applicable identity checks at the real release.
3. Verify primary and independent storage locations, access, failure separation, artifact scope, integrity and recovery-verification procedures.
4. Run a bounded **offline readiness audit** with evidence-referenced PASS/HOLD findings and limitations.
5. Seek **separate, explicit owner authorization** binding the final manifest SHA-256 and exact operational/preservation scope; then, only within any granted release permission, distinguish `authorized_for_F1_release` from `F1_completed_and_verified` based on actual evidence and copy/recovery checks.

HOLD on unexplained source/manifest mismatch, missing custodian/exposure evidence, unverified independent preservation, ambiguous authorization, undocumented relevant changes or failed release preservation/integrity checks. Provider access/availability remains unverified and must not be tested during offline readiness; it can block later dispatch without silently changing the treatment. The procedure approval **does not release F1**.

## 3. Remaining blockers and explicit next stage

| Requirement | Status after 5B owner decisions | Evidence needed next |
|---|---|---|
| Owner custodian and release-authority role | Assigned by owner, but actual authorization event absent | Record owner actor/role and provenance |
| Owner-specific exposure declaration | **Pending** | Source-supported exposure register and owner confirmation of actual exposure and unknowns |
| Versioned F1 manifest and records | **Design approved; artifacts not created** | Exact formats and evidence-bound draft identities, separate authorization for writing |
| Actual local primary/independent off-device destinations | **Not verified** | Owner-provided destination details, fault separation, access and recovery plan |
| Off-device backup, checksums and recovery evidence | **Not performed** | Separately authorized copy and verification events |
| Offline readiness audit | **Not performed for a completed release packet** | Final package with evidence-specific PASS/HOLD |
| Actual F1 authorization | **Not granted** | Separate owner approval of completed manifest digest and permitted operation |
| Gate A/source authoring, F2/F3 adjudication/population, F4/F5 execution, scoring and publication | **Not authorized** | Separate downstream prerequisite evidence and specific owner releases |

**Next proposed checkpoint: 5C — F1 Evidence Completion Preparation.** First assemble a non-destructive, read-only *owner exposure declaration worksheet* from cited repository evidence, explicitly identify facts that only the owner can confirm, and propose (not perform) the exact format and verification questions for the off-device preservation plan. No access to unrelated drives, credentials, external storage or provider API, and no file writes, Git actions, backup, freeze or generation without further permission.

## 4. Publication and verification status

This is a **conversation-derived consolidation draft**, not yet checked by Codex against repository references, staged, committed or merged. Owner's approval of the five decision recommendations does not itself approve every phrasing in this synthesized document. Obtain read-only consistency review, address findings, and inspect exact staged scope before publication. Do not describe a committed decision document as an operational release.
