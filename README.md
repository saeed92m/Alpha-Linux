# Alpha Linux

Alpha Linux is an Ubuntu 26.04 LTS–based, AI-native universal workstation platform built around COSMIC Desktop.

## Vision

> **Own the experience, integrate the ecosystem, don’t reinvent the foundation.**

Alpha Linux preserves Ubuntu compatibility while providing an integrated platform for AI, scientific computing, engineering, astronomy, aerospace, motorsport, development, creator workflows, music and audio, education, business, and advanced desktop computing.

The product vision includes a polished end-to-end experience from **boot media → Live environment → installation → first boot → desktop → AI and domain workflows**, while keeping privileged system operations behind explicit safety and verification boundaries.

## Project Status

**Current phase: Phase 7 — Alpha Releases**

Phase 0 specification/architecture work is frozen as the normative foundation. Phases 1–6 established the executable engineering, Alpha Core, desktop/interaction, AI platform, domain platform, and hardening reference foundations. Phase 7 is implementing release-scoped artifact, boot, Live-environment, installer, traceability, readiness, and publication foundations with deterministic contracts, executable tests, CI evidence, and explicit non-goal boundaries.

Alpha **0.1.0a1** is the current verified Alpha release candidate. The `v0.1.0a1` tag and GitHub Release are bound to verified source/CI evidence. The OS image track publishes the verified amd64 image as four release-safe parts with checksums and a reassembly manifest.

## Boot and installation product goals

Alpha Linux targets a single ISO that can provide, where supported and validated:

- UEFI boot;
- Legacy BIOS boot;
- Live USB operation;
- Rufus-compatible USB creation;
- GPT/UEFI installation;
- MBR/Legacy installation;
- graphical COSMIC-based Live environment;
- Alpha-branded boot/loading experience;
- graphical installer;
- storage diagnostics;
- recovery entry points;
- explicit confirmation before destructive disk changes;
- transactional installation with verification and rollback/recovery.

These are **product requirements and roadmap targets**, not blanket claims of current completion. Each capability requires corresponding implementation and evidence.

## Core principles

- Ubuntu-compatible by design, not Ubuntu-limited by design
- COSMIC Desktop as the primary desktop environment
- Modular capabilities with a lightweight core
- AI-native architecture with explicit permissions
- Multi-agent orchestration
- User-controlled memory and continuous learning
- Strong recovery, rollback, backup and observability
- First-class touch, pen, HiDPI and multi-display support
- Light, Dark, System/Auto and extensible custom themes
- Offline-first wherever practical
- Reproducible builds and release engineering
- Documentation-first development
- Safety-first privileged system boundaries
- Runtime evidence over assumption

## Repository map

- `docs/` — project documentation
- `docs/handbook/` — Master Handbook and learning path
- `specs/` — normative specifications
- `architecture/` — architecture documentation
- `requirements/` — functional and non-functional requirements
- `planning/` — decisions, assumptions, risks and open questions
- `roadmap/` — milestones and delivery planning
- `integrations/` — external software and project integrations
- `implementation/` — executable implementation boundary
- `.github/workflows/` — executable CI/CD gates

## CI/CD gates

The CI/CD workflow covers:

- repository and documentation validation;
- linting and unit/contract tests;
- Python 3.11/3.12/3.13 compatibility;
- static type checking;
- coverage reporting;
- package build, metadata and installation validation;
- artifact provenance;
- reproducible builds;
- security auditing;
- secret scanning;
- CycloneDX SBOM generation;
- machine-readable gate evidence;
- Alpha OS ISO build, base-image verification, boot-metadata preservation, artifact hashing, provenance and evidence publication on the OS image track;
- QEMU pre-install boot smoke;
- installer safety and disposable transaction validation.

The OS image artifact and release evidence have been verified for `v0.1.0a1`. Physical installation/boot validation, full Live desktop validation, installer UX, and promotion to Beta/Stable remain future gates.

## Documentation hierarchy

**Handbook** explains concepts and teaches the system.

**Specification / Requirements** define what Alpha must provide.

**Architecture** defines how the system is intended to provide it.

**Implementation** contains the actual system.

**Testing** demonstrates that requirements are satisfied.

## Branding

Product name: **Alpha Linux**

Reference brand colors:
- Alpha Blue: `#003C91`
- Alpha Gray: `#8A8A8A`

## Repository governance

Phase 0 is frozen. Material changes to normative scope follow the Change Request process. Implementation changes remain subordinate to requirements, specifications, architecture, security and recovery boundaries.

See:
- [Master Specification](specs/master-specification.md)
- [Master Handbook](docs/handbook/00-handbook-overview.md)
- [Boot, Live and Installer Architecture](docs/architecture/boot-live-installer.md)
- [Boot, Live and Installer Requirements](docs/requirements/boot-live-installer-requirements.md)
- [Phase 0 Freeze Decision](docs/audits/phase-0-freeze-decision.md)
- [Decision Log](planning/decision-log.md)
- [Roadmap](roadmap/master-roadmap.md)