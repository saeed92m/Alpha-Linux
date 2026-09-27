# Alpha Linux Master Roadmap

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

### Release 0.1.0a1

- Package artifact verified.
- `v0.1.0a1` published.
- OS image built, reproducibility checked and release-safe assets published.
- ISO reassembly, checksum, size and manifest QA automated and passing.
- QEMU pre-install boot smoke verified.
- Installer safety model verified.
- Disposable installer transaction execution verified.

**Status:** Active Alpha release program.

### Phase 7A — Boot and media compatibility

- Preserve a single release ISO containing UEFI and Legacy BIOS boot paths where supported by the base image.
- Validate UEFI boot in QEMU.
- Validate Legacy BIOS boot in QEMU.
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

## Continuous improvement

**Requirement → Specification → Architecture → Implementation → Automated Test → CI Evidence → Artifact → Runtime Validation → Gap Detection → Requirement/Architecture refinement → Implementation → Verification → Release → Observe**

Completed phase foundations may be refined when later runtime evidence identifies a real gap; such refinement does not retroactively claim an unverified product capability.
