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

**Status:** Completed reference-runtime foundation. All listed desktop and interaction slices are implemented, tested, CI-validated, and merged. Production privileged host mutation, production COSMIC runtime integration, and release-scoped validation remain governed by later phases.

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

**Status:** Completed hardening foundation. Security, privacy, recovery/backup, compatibility, performance, hardware validation, accessibility, localization, and release QA foundations are implemented, tested, CI-validated, and merged. Phase 6 — Hardening is complete; Phase 7 — Alpha releases is now the active program. No product release is claimed without actual release artifacts and evidence.

## Phase 7 — Alpha releases

- Alpha 0.x
- Alpha 1.0
- Beta
- Stable release

### Alpha 0.1.0a1 package track

- Package artifact verified in CI.
- Release-publication foundation complete.
- Release evidence bound to source commit, CI run and artifact SHA-256.
- Publication/tag remain separately gated.

### Alpha OS image track

- ISO/IMG artifact contract defined.
- Deterministic naming and evidence model implemented.
- Executable image-file validation and tests added.
- Actual OS image build, boot/install validation and image release evidence remain required before any OS image release claim.

Dates are intentionally not fixed until the relevant implementation and release evidence is available.
