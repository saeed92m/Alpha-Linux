# Alpha Linux — Roadmap Traceability

**Status:** Active delivery control — Phase 7: Alpha Releases

This document is the release traceability view of the current master roadmap. The master roadmap is normative for phase names and program state; this document maps each phase to its required evidence and delivery gates.

## Delivery gates

| Phase | Entry condition | Exit evidence |
|---|---|---|
| Phase 0 — Product and specification | Product scope and architecture defined | Frozen requirements/specification/architecture baseline |
| Phase 1 — Foundation | Phase 0 frozen | Reproducible build, package policy, CI/CD, baseline QA and artifact evidence |
| Phase 2 — Alpha Core | Foundation validated | System-integration and reference-runtime evidence for core platform surfaces |
| Phase 3 — Desktop and interaction | Alpha Core baseline available | Desktop/interaction reference-runtime evidence and CI validation |
| Phase 4 — AI Platform | Core platform contracts available | AI/agent runtime, permissions and verification foundation evidence |
| Phase 5 — Domain platform | Core and AI platform foundations available | Domain foundation evidence across supported technical and creative domains |
| Phase 6 — Hardening | Domain/platform foundations available | Security, privacy, recovery, compatibility, performance, hardware-validation, accessibility, localization and release-QA evidence |
| Phase 7 — Alpha releases | Hardening baseline and release contracts validated | Versioned release artifacts, provenance, traceability, publication and release-readiness evidence |

## Current Phase 7 release gates

### Alpha 0.1.0a1 package track

- Package artifact verified in CI.
- Release publication completed as `v0.1.0a1`.
- Tag and GitHub Release are bound to verified source/CI evidence.
- Artifact provenance and SHA-256 evidence are retained.

### Alpha OS image track

- ISO/IMG artifact contract defined.
- Deterministic naming and evidence model implemented.
- Executable image-file validation and tests are present.
- Actual amd64 OS image build is implemented and CI-verified.
- The verified image is distributed through release-safe split assets.
- Part checksums, reassembly instructions, full ISO checksum, size and manifest are automatically validated.
- Physical installation/boot validation across target hardware remains a future gate.
- Installer UX and production installer readiness remain future gates.
- Beta/Stable promotion remains gated by their respective implementation and validation evidence.

## Mandatory sequencing

- No implementation may silently redefine frozen normative scope; material scope changes follow the Change Request process.
- No release claim is made without the corresponding artifact and retained evidence.
- Domain capabilities consume stable platform contracts rather than bypassing core boundaries.
- AI capabilities remain subject to explicit permission, security and verification boundaries.
- Privileged host integration and production application execution remain separately gated from reference-runtime foundations.
- Every phase exit requires retained, machine-checkable or otherwise auditable evidence.

## Continuous improvement loop

**Build → Test → Observe → Measure → Gap → Requirement/Spec/Architecture update → Implement → Verify → Release → Observe**

This loop is cumulative rather than strictly linear: later evidence can trigger a requirement, architecture, implementation or validation update in an earlier subsystem without reopening completed phase gates unnecessarily.

## Evidence principle

A roadmap item is considered implemented only when the repository contains the corresponding implementation or executable contract, automated/manual validation evidence appropriate to the item, and traceability to the applicable requirement or release gate.

Dates are not treated as completion evidence; artifact and validation evidence are.

## Phase 7 boot/live/installer traceability

| Area | Requirement / architecture | Current evidence | Remaining gate |
|---|---|---|---|
| Boot | `docs/requirements/boot-live-installer-requirements.md`, BOOT-001..005 | ISO boot metadata preserved; QEMU pre-install boot smoke verified | UEFI/BIOS matrix validation, Rufus validation, Secure Boot |
| Live | LIVE-001..005 | ISO artifact exists; Live runtime not yet claimed | COSMIC Live startup, diagnostics, installer launch, recovery validation |
| Installer safety | INST-001..005 | Safety model + disposable transaction evidence | Full installation transaction, failure injection, rollback, physical adapter |
| Post-install | INST-006 | Not yet claimed | Filesystem, boot configuration and health verification after installation |
| Physical installation | Phase 7D | Not yet claimed | UEFI/Legacy hardware, Windows coexistence, recovery and Secure Boot |

The boot/media architecture intentionally separates ISO firmware boot paths from target-disk partition-table selection. GPT/UEFI and MBR/Legacy are target installation modes; no unsupported firmware/media combination is claimed without evidence.
