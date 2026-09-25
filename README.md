# Alpha Linux

Alpha Linux is an Ubuntu 26.04 LTS–based, AI-native universal workstation platform built around COSMIC Desktop.

## Vision

> Own the experience, integrate the ecosystem, don’t reinvent the foundation.

Alpha Linux preserves Ubuntu compatibility while providing an integrated platform for AI, scientific computing, engineering, astronomy, aerospace, motorsport, development, creator workflows, music and audio, education, business, and advanced desktop computing.

## Project Status

**Current phase: Phase 1 Foundation**

Phase 0 specification and architecture are frozen. Phase 1 implementation is active. The repository is moving from normative contracts to executable foundation components, automated tests and CI evidence.

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
- `.github/workflows/` — executable CI gates

## Documentation hierarchy

**Handbook** explains concepts and teaches the system.

**Specification** defines what Alpha must provide.

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
- [Phase 0 Freeze Decision](docs/audits/phase-0-freeze-decision.md)
- [Decision Log](planning/decision-log.md)
- [Roadmap](roadmap/master-roadmap.md)
