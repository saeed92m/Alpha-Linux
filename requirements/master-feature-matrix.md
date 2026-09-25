# Alpha Linux — Master Feature Matrix

This document is the authoritative traceability index for project capabilities.

## State model

| State | Meaning |
|---|---|
| Planned | Identified as desired scope |
| Specified | Requirements are defined |
| Designed | Architecture/design exists |
| Ready | Implementation prerequisites are satisfied |
| Implementing | Work is actively underway |
| Implemented | Functionality exists |
| Tested | Automated/manual tests pass |
| Validated | Requirement demonstrated on target environment |
| Released | Included in an official release |

## Phase 0 traceability matrix

| Area | State | Requirement family | Authoritative specification / architecture |
|---|---|---|---|
| Product / Core | Specified | AL-REQ | Master Specification; Dependency Boundaries |
| COSMIC / Desktop | Specified | AL-REQ, AL-UX | UI/UX Requirements; Dependency Boundaries |
| Themes / Design System | Specified | AL-UX | Design System; UX Requirements |
| AI Core / Assistant | Specified | AL-AI | AI Safety & Permissions |
| Agents / Orchestrator | Specified | AL-AI | AI Safety & Permissions; Dependency Boundaries |
| Memory / Continuous Learning | Specified | AL-AI, AL-SEC | AI Safety & Permissions; Threat Model |
| Adaptive Resource Intelligence | Specified | AL-REQ, AL-NFR | System Architecture; Dependency Boundaries |
| Installer / Boot | Specified | AL-REQ, AL-REC | Installer Architecture |
| Recovery / Rollback | Specified | AL-REC | Recovery Architecture |
| Windows Dual Boot | Specified | AL-COMP, AL-REC | Compatibility Requirements; Installer Architecture |
| WSL | Specified | AL-COMP | WSL Architecture |
| Hardware / Firmware | Specified | AL-HW | Hardware/Firmware Requirements; Hardware Validation |
| Security / Privacy | Specified | AL-SEC | Security Requirements; Threat Model |
| Packaging | Specified | AL-PKG | Package/Repository Requirements; Repository Architecture; Package Policy |
| Build / Reproducibility | Specified | AL-BLD | Build System Architecture; Reproducible Builds |
| CI/CD | Specified | AL-BLD, AL-REL | CI/CD Policy; Test Strategy |
| ISO | Specified | AL-BLD, AL-REL | ISO Build Architecture |
| Developer Platform | Specified | AL-REQ | Master Specification |
| AI/ML/HPC | Specified | AL-REQ | Master Specification |
| Astronomy / ZTF integration | Specified | AL-REQ | Master Specification |
| Aerospace | Specified | AL-REQ | Master Specification |
| Engineering | Specified | AL-REQ | Master Specification |
| Motorsport | Specified | AL-REQ | Master Specification |
| Electronics / Embedded | Specified | AL-REQ | Master Specification |
| SDR / Radio | Specified | AL-REQ | Master Specification |
| Office / PDF | Specified | AL-REQ | Master Specification |
| Creator / Media | Specified | AL-REQ | Master Specification |
| Music & Audio | Specified | AL-REQ | Master Specification |
| Gaming / Simulation | Specified | AL-REQ | Master Specification |
| Data / GIS | Specified | AL-REQ | Master Specification |
| Cloud / DevOps | Specified | AL-REQ | Master Specification |
| Business | Specified | AL-REQ | Master Specification |
| Accessibility / Localization | Specified | AL-UX, AL-NFR | UX/Accessibility Requirements; Design System |
| Backup / Disaster Recovery | Specified | AL-REC | Recovery Architecture |
| Plugin / SDK | Specified | AL-SEC, AL-REQ | Master Specification; Threat Model |
| Observability / Diagnostics | Specified | AL-NFR | System Observability |
| QA / Release Engineering | Specified | AL-TEST, AL-REL | Test Requirements; Test Strategy; Release Engineering |

## Requirement-family coverage

Atomic Phase 0 requirement families now include:

- AL-REQ — functional
- AL-NFR — non-functional
- AL-SEC — security/privacy
- AL-HW — hardware/firmware
- AL-UX — UI/UX/accessibility
- AL-COMP — compatibility
- AL-PKG — packaging/repository
- AL-BLD — build/reproducibility
- AL-REL — release/lifecycle
- AL-REC — recovery/rollback
- AL-AI — AI/agent
- AL-TEST — test/validation

## Readiness rule

No area is implementation-ready merely because its row says **Specified**. The subsystem specification matrix is the authoritative readiness gate.

## Release traceability

Every released capability must map:

**Requirement → Specification → Architecture → Implementation → Test → Validation Evidence → Release**
