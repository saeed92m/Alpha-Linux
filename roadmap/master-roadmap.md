# Alpha Linux Master Roadmap

**Roadmap state:** Active delivery control  
**Current phase:** Phase 7 — Alpha Releases  
**Current release context:** Alpha 0.3.0a (published prerelease)  
**Last synchronized:** PR #273 Phase 7A media-matrix contract; physical USB/media evidence is now the active release gate

## Phase 0 — Product and specification

- Repository foundation
- Master Specification
- Master Handbook
- Requirements
- Architecture
- Design System
- Feature Matrix
- Decision Log
- Compatibility Matrix
- Risk register
- Specification audit
- Specification freeze

**Status:** Completed baseline; frozen specification is maintained through Change Requests.

## Phase 1 — Foundation

- Reproducible build system
- Ubuntu 26.04 LTS integration
- package policy
- CI/CD
- baseline QA
- artifact pipeline

**Status:** Completed foundation baseline; release/ISO-scoped evidence remains conditional on applicable artifacts.

## Phase 2 — Alpha Core

- system integration
- Control Center
- Software Center
- Hardware Manager
- Observatory
- Profiles
- update/recovery foundations

**Status:** Completed reference-runtime baseline. Integrated system surfaces are implemented, tested, validated by CI, and merged. Privileged OS adapters, desktop integration and release-scoped evidence remain in later phases.

## Phase 3 — Desktop and interaction

- COSMIC integration
- multitasking
- touch
- pen
- HiDPI
- multi-display
- theme system

**Status:** Completed reference-runtime foundation. Production privileged host mutation, production COSMIC runtime integration, and release-scoped validation remain governed by later phases.

## Phase 4 — AI Platform

- Alpha AI Core
- Assistant
- Memory
- Knowledge Center
- Command Bar
- Agent Runtime
- Orchestrator
- permissions
- verification

**Status:** Completed reference-runtime foundation. Alpha AI Core, AI Execution Runtime, Assistant, Memory, Knowledge Center, Command Bar, Agent Runtime, Orchestrator, Permissions, and Verification foundations are implemented, tested, CI-validated, and merged.

## Phase 5 — Domain platform

- Developer
- AI/ML/HPC
- Astronomy
- Aerospace
- Engineering
- Motorsport
- Electronics
- SDR/RF
- Creator
- Music & Audio
- Data/GIS
- Business
- Cloud/DevOps
- Education and research

**Status:** Completed domain foundation. All listed reference foundations are implemented, tested, CI-validated, and merged.

## Phase 6 — Hardening

- security
- privacy
- recovery
- backup
- compatibility
- performance
- hardware validation
- accessibility
- localization
- release QA

**Status:** Completed hardening foundation. Phase 6 is complete; its reference foundations are not equivalent to physical product validation.

## Phase 7 — Alpha releases

### Historical release context — Alpha 0.1.0a2 / 0.1.0a3

The immutable `v0.1.0a1` package release remains historical. The current published OS release candidate is `v0.3.0a`; its release assets are bound to the verified tag commit and remain separate from the historical package tag.

### Verified engineering/release evidence

- Real amd64 OS image build and CI verification.
- BIOS + UEFI El Torito boot metadata validation and independent QEMU boot-smoke evidence.
- Deterministic image manifest, SHA-256 and provenance.
- Reproducibility validation.
- QEMU pre-install boot smoke.
- Live kernel/initramfs runtime evidence.
- Automated COSMIC graphical-runtime evidence.
- Package/OS release-candidate evidence binding.
- Release-safe ISO split assets with checksums and reassembly instructions.
- PR #193 release-asset metadata interpolation correction merged to `main`.

### Newly verified in PR #199

- Deterministic filesystem install staging with content manifest and SHA-256 verification before and after commit.
- Fail-closed post-install verification contract requiring filesystem, boot-configuration, and health evidence.
- Automated tests for staging integrity, target safety, and post-install evidence requirements.
- PR #199 merged to `main` as `35c1ff79033f7105b32e45cf1437b0191b06a5f3`; CI run `36757368104` completed successfully across all reported gates.
- This remains fixture/runtime contract evidence; it does **not** constitute physical-disk installation or physical rollback validation.

### Current v0.3.0a product boundary

The published `v0.3.0a` release is a real downloadable Alpha OS image with reproducibility, provenance, BIOS/UEFI metadata, QEMU smoke and split/reassembly verification. It is not yet a Beta/Stable installer release.

The current installer entrypoint is a destructive UEFI + Alpha-only prototype that requires a dedicated empty disk. Disposable-fixture transaction tests cover confirmation, commit, failure injection and rollback; physical-disk installation remains a hardware gate.

### Explicitly not yet product-complete

- Complete UEFI/Legacy media matrix.
- Rufus validation.
- Secure Boot.
- Complete Live UX/diagnostics/recovery.
- Production installer UX and full real-disk transaction.
- Physical installation and hardware validation.
- Windows dual-boot validation.
- Post-install boot/health validation.
- Beta/Stable promotion.

### Release 0.1.0a1 (historical)

- Package artifact verified.
- `v0.1.0a1` package release published; its tag remains immutable.

**Status:** Historical package/release lineage. The current OS release context is `v0.3.0a`.

### Phase 7A evidence contract

- Added a fail-closed media compatibility matrix contract covering UEFI/Legacy BIOS × GPT/MBR declarations.
- A matrix entry is not accepted as evidence unless it is explicitly declared bootable and carries an evidence reference.
- Missing matrix cases remain open rather than being inferred from other firmware/partition combinations.
- This contract does **not** claim Rufus, physical USB, firmware, or hardware validation; those require direct validation evidence.

### Phase 7A — Boot and media compatibility

- Preserve a single release ISO containing UEFI and Legacy BIOS boot paths where supported by the base image. **Verified in CI.**
- Validate UEFI boot in QEMU. **Verified in CI with OVMF.**
- Validate Legacy BIOS boot in QEMU. **Verified in CI.**
- Validate Rufus USB creation workflows.
- Validate GPT and MBR media/firmware combinations that are technically supported.
- Record the tested compatibility matrix.
- Add Secure Boot validation as a separate gate.

### Phase 7B — Live environment

- Boot into Live environment without internal-disk installation.
- Validate COSMIC graphical startup.
- Establish Alpha-branded boot/loading experience.
- Validate display/input/network/storage initialization.
- Provide diagnostics and recovery entry points.
- Validate graphical installer launch from Live.

### Phase 7C — Installer

- Storage discovery.
- Firmware/partition-mode detection.
- Graphical installation plan.
- Alpha-only installation.
- Alongside-Windows safety path.
- Second-disk installation.
- Manual partitioning.
- GPT/UEFI installation.
- MBR/Legacy installation.
- Explicit confirmation boundary.
- Transaction execution.
- Failure injection.
- Rollback/recovery.
- Post-install verification.
- Boot configuration.

### Phase 7D — Physical validation

- Physical UEFI installation.
- Legacy BIOS installation where applicable.
- Windows dual-boot validation.
- Hardware compatibility validation.
- Recovery after interrupted installation.
- Secure Boot validation.
- Release-ready installer evidence.

### Promotion

- Alpha 1.0
- Beta
- Stable release

Dates are intentionally not fixed until the relevant implementation and evidence exist.

## Current priority order

1. Complete physical USB/media validation (Rufus + declared GPT/MBR matrix).
2. Close remaining Live UX/diagnostics/recovery evidence gaps.
3. Validate the UEFI Alpha-only installer on disposable physical hardware.
4. Add physical recovery/interrupted-install evidence.
5. Implement and validate Windows coexistence only after safe disk-state detection is proven on real hardware.
6. Add Secure Boot evidence.
7. Promote only after all release gates are independently evidenced.

## Completion and evidence protocol

A Phase 7 item is not complete merely because code exists or a pull request is mergeable. The project uses this fail-closed sequence:

1. Implement the smallest verifiable contract.
2. Add deterministic automated tests for the normal path and relevant failure paths.
3. Run real repository CI and wait for terminal conclusions; queued, running, missing, or unknown evidence is not success.
4. Inspect the actual failed job/log when any gate fails; do not infer the cause from a summary.
5. Merge only after required CI gates are successful.
6. Verify the PR after merge with `merged=true`, `state=closed`, and the actual merge commit; never treat `merge_commit_sha` alone as proof.
7. Re-check the target `main` commit and its CI after merge before using the change as release evidence.
8. Bind release claims to concrete evidence: commit SHA, workflow run, artifact/provenance, and applicable runtime or physical validation record.
9. Keep virtual/fixture/QEMU evidence separate from physical hardware evidence. QEMU cannot satisfy a physical installation or hardware gate.
10. Before advancing phases, re-audit open PRs/issues and current `main` so stale evidence cannot silently drive the roadmap.

### Definition-of-done matrix

| Evidence layer | What it proves | What it cannot prove |
|---|---|---|
| Unit/contract tests | Deterministic software behavior | Real hardware behavior |
| CI gates | Repository-level quality and build contracts | Physical installation |
| Artifact/provenance | Exact produced output and lineage | Hardware compatibility |
| QEMU/runtime validation | Boot/runtime behavior in the declared virtual environment | Physical firmware/device matrix |
| Physical validation | Actual device/firmware/install behavior | Broader untested hardware populations |
| Release gate | Required evidence is bound and present | Evidence outside its declared scope |

### Evidence truth rules

- Never claim success from a pending or partial workflow.
- Never use an old run ID as evidence for a newer commit unless the binding is explicit and verified.
- Never infer physical validation from CI, fixtures, or QEMU.
- Never mark a roadmap item complete without identifying the evidence that closes its gate.
- If required evidence is missing or ambiguous, the gate remains open.

## Continuous improvement

**Requirement → Specification → Architecture → Implementation → Automated Test → CI Evidence → Artifact → Runtime Validation → Gap Detection → Requirement/Architecture refinement → Implementation → Verification → Release → Observe**

Completed phase foundations may be refined when later runtime evidence identifies a real gap; such refinement does not retroactively claim an unverified product capability.
