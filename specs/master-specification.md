# Alpha Linux — Master Specification

**Status:** Phase 2 reference-runtime baseline completed; Phase 3 desktop and interaction implementation is the active next phase.

## 1. Product definition

Alpha Linux is an Ubuntu 26.04 LTS–based universal workstation platform using COSMIC Desktop and an Alpha-specific integration layer.

The platform must provide a coherent experience across desktop, laptop, tablet, 2-in-1 and multi-display systems while remaining compatible with the Ubuntu ecosystem.

## 2. Scope

The master scope includes:

- Alpha Core and system integration
- COSMIC desktop experience
- Design System and theming
- AI Core, Assistant, Memory and Knowledge Center
- Multi-Agent Intelligence and orchestration
- Continuous Learning and personalization
- Adaptive Resource Intelligence
- Hardware and Firmware management
- Installer, Live environment, Boot and Recovery
- Updates and rollback
- WSL and Windows integration
- Storage, filesystems, swap/ZRAM/hibernate
- Networking, identity, privacy and secrets
- Virtualization, containers and distributed computing
- Developer platform
- AI/ML/HPC
- Astronomy and ZTF workflows
- Aerospace
- Mechanical engineering and CAE/CFD/FEA
- Motorsport and automotive
- Electronics, embedded systems, robotics
- SDR, RF and radio astronomy
- Office, PDF and research workflows
- Creator, graphics, photography, video and VFX
- Music and audio production
- Gaming and simulation
- Data engineering and GIS
- Cloud, DevOps and home-lab workflows
- Business/ERP/CRM workflows
- Education and learning workflows
- Laboratory/scientific instrumentation
- Accessibility and localization
- Security, privacy, backup and disaster recovery
- Plugin/SDK ecosystem
- Cross-device synchronization
- Observability, diagnostics, benchmarking and QA

## 3. Non-goals

Alpha Linux will not:

- blindly fork or rewrite Ubuntu foundations;
- mix Debian/Ubuntu repositories without controlled compatibility policy;
- bundle proprietary commercial software without appropriate licensing;
- replace the Linux kernel merely for branding;
- replace WSL with a proprietary clone;
- make destructive/admin changes without appropriate authorization;
- make user-controlled learning opaque or irreversible.

## 4. Release principle

No major subsystem is considered complete merely because it exists. Requirements must progress through the project state model:

Planned → Specified → Designed → Ready → Implementing → Implemented → Tested → Validated → Released.

## 5. Specification freeze

The Phase 0 specification baseline has been frozen. New scope is introduced through the Change Request process.

Implementation work in later phases must continue to trace back to the frozen specification and preserve its security, compatibility, recovery, testability and release constraints.
