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
- Persistent Portable execution from removable media
- Updates and rollback
- WSL and Windows integration
- Storage, filesystems, swap/ZRAM/hibernate
- Persistent Portable storage, optional encryption and removable-media lifecycle
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


## 6. Product deployment model

Alpha Linux is one product with a shared Ubuntu 26.04 LTS + COSMIC base and three deployment modes:

1. **Persistent Portable:** full desktop execution from removable media with persistent user state, installed applications, updates, configuration and user data.
2. **Live/Recovery:** disposable execution for evaluation, diagnostics and recovery.
3. **Installed:** native installation of the same Alpha base to internal storage.

Persistent Portable must not be treated as a conventional non-persistent Live ISO. It has a separate artifact contract, storage layout, persistence tests and release gates.

## 7. Modular software policy

The release-critical Base remains minimal. Applications are independently installable through Ubuntu/Debian-compatible package mechanisms and Alpha's software catalog/UX. Bundles are convenience manifests; installing one application must not require installing an entire domain bundle. Large datasets and heavy optional stacks are not mandatory Base/ISO payload.

## 8. Change control

The Portable Persistent and modular per-application direction is introduced through Change Request #290. The Phase 0 freeze remains intact; this additive scope must satisfy the existing security, compatibility, recovery, reproducibility and evidence rules before release promotion.
