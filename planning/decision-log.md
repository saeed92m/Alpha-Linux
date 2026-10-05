# Alpha Linux — Decision Log

## Purpose

Record architectural and product decisions so the project remains understandable and reproducible.

## Decision format

- Decision
- Context
- Alternatives
- Chosen approach
- Reason
- Trade-offs
- Consequences
- Date
- Status

## D-001 — Product name

**Decision:** The product is named **Alpha Linux**.

**Status:** Accepted

## D-002 — Base distribution

**Decision:** Use **Ubuntu 26.04 LTS** as the foundation, targeting the latest supported 26.04 point release during implementation.

**Status:** Accepted

## D-003 — Desktop

**Decision:** Use **COSMIC Desktop** as the primary desktop environment.

**Status:** Accepted

## D-004 — Architectural philosophy

**Decision:** Own the experience, integrate the ecosystem, and avoid reinventing foundational components when mature upstream solutions are appropriate.

**Status:** Accepted

## D-005 — AI architecture

**Decision:** AI is a first-class system layer rather than a standalone chatbot application.

**Status:** Accepted

## D-006 — Multi-agent architecture

**Decision:** Alpha includes a dedicated multi-agent orchestration layer with specialized agents, tool permissions, verification and user approval for sensitive actions.

**Status:** Accepted

## D-007 — Continuous learning

**Decision:** Continuous learning and personalization are core capabilities and must remain user-controlled, inspectable and reversible.

**Status:** Accepted

## D-008 — Themes

**Decision:** Light, Dark, System/Auto and extensible custom themes are first-class requirements.

**Status:** Accepted

## D-009 — Product branding

**Decision:** The project owner's supplied logo is the product-logo reference for Alpha Linux. The reference palette includes `#003C91` and `#8A8A8A`.

**Status:** Accepted

## D-010 — Documentation-first development

**Decision:** Implementation begins only after the specification and architecture baseline are reviewed and frozen.

**Status:** Accepted

## D-011 — Single ISO with dual firmware boot targets

**Decision:** The preferred Alpha Linux release model is one bootable ISO carrying both UEFI and Legacy BIOS boot paths where supported by the selected Ubuntu base-image/tooling stack.

**Context:** The product must support Live USB use and installation across modern UEFI systems and compatible legacy BIOS systems without forcing users to download separate firmware-specific images.

**Trade-offs:** Dual-path media increases boot-validation scope and compatibility testing. Some firmware/media combinations may remain unsupported and must be documented rather than assumed.

**Status:** Accepted; Phase 7 validation required.

## D-012 — GPT/MBR installation compatibility

**Decision:** Alpha Linux targets GPT installation for UEFI systems and MBR installation for Legacy BIOS systems. Additional combinations are allowed only when validated.

**Context:** Firmware mode and target partition table are distinct concerns and must be detected before installation.

**Status:** Accepted; Phase 7 validation required.

## D-013 — Live environment as a first-class product surface

**Decision:** The Live USB environment is a product surface with graphical Alpha/COSMIC experience, diagnostics, recovery entry points and graphical installer access.

**Context:** Users must be able to evaluate and repair the system without installing it first.

**Status:** Accepted; implementation and runtime validation required.

## D-014 — Installer safety and transaction boundary

**Decision:** The graphical installer must remain separated from privileged storage mutation. Storage discovery, safety planning, explicit confirmation, transactional execution, verification and rollback/recovery form distinct boundaries.

**Context:** Installer correctness and user safety require testable separation between intent/UI and disk mutation.

**Status:** Accepted; disposable transaction evidence exists; physical adapter remains future work.


## D-015 — Persistent Portable as a first-class deployment mode

**Decision:** Alpha Linux will support a Persistent Portable deployment mode in addition to disposable Live/Recovery and native Installed modes.

**Context:** A complete Ubuntu + COSMIC desktop can run from removable media while persisting user state, applications, updates and files. The host internal disk should not need to be modified.

**Chosen approach:** Keep one shared Alpha Base and implement Portable Persistent as a distinct artifact/storage contract. Do not turn the existing disposable Live ISO into a misleading persistent product.

**Trade-offs:** Removable-media I/O, filesystem integrity, recovery, encryption, capacity and physical hardware validation become additional release gates.

**Status:** Accepted as additive product direction; implementation under CR #290.

## D-016 — Minimal Base and independent applications

**Decision:** The Alpha Base remains minimal. Individual applications are independently installable; bundles are convenience manifests only.

**Context:** Users must be able to install one astronomy, engineering, AI or development application without pulling an entire domain stack.

**Chosen approach:** Keep Ubuntu/Debian package mechanisms as the foundation and layer Alpha catalog/grouping/UX/provenance over them.

**Trade-offs:** Software catalog and dependency presentation require more metadata and testing, but the ISO and Portable device remain significantly lighter.

**Status:** Accepted; implementation under CR #290.

## D-017 — zram-first optional USB swap

**Decision:** zram is the default memory-pressure mechanism for Portable Persistent. USB-backed swap is optional.

**Context:** The portable device should use the host machine's RAM and avoid unnecessary write amplification on removable media.

**Status:** Accepted; implementation and runtime validation required.
