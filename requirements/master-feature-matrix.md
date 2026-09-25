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

| Area | State | Requirement family | Architecture / specification |
|---|---|---|---|
| Product / Core | Specified | AL-REQ | Master Specification |
| COSMIC / Desktop | Specified | AL-REQ, AL-UX | UI/UX requirements |
| Themes / Design System | Specified | AL-UX | Design System |
| AI Core / Assistant | Specified | AL-AI | AI specifications |
| Agents / Orchestrator | Specified | AL-AI | Agent architecture |
| Memory / Continuous Learning | Specified | AL-AI, AL-SEC | AI specifications |
| Adaptive Resource Intelligence | Specified | AL-REQ, AL-NFR | Resource architecture |
| Installer / Boot | Specified | AL-REQ, AL-REC | Installer architecture |
| Recovery / Rollback | Specified | AL-REC | Recovery architecture |
| Windows Dual Boot | Specified | AL-COMP, AL-REC | Compatibility + installer |
| WSL | Specified | AL-COMP | WSL architecture |
| Hardware / Firmware | Specified | AL-HW | Hardware specification |
| Security / Privacy | Specified | AL-SEC | Threat model |
| Packaging | Specified | AL-PKG | Package policy + repository architecture |
| Build / Reproducibility | Specified | AL-BLD | Build architecture |
| CI/CD | Specified | AL-BLD, AL-REL | CI/CD policy |
| ISO | Specified | AL-BLD, AL-REL | ISO architecture |
| Developer Platform | Specified | AL-REQ | Developer requirements |
| AI/ML/HPC | Specified | AL-REQ | Scientific requirements |
| Astronomy / ZTF integration | Specified | AL-REQ | Astronomy specification |
| Aerospace | Specified | AL-REQ | Aerospace specification |
| Engineering | Specified | AL-REQ | Engineering specification |
| Motorsport | Specified | AL-REQ | Motorsport specification |
| Electronics / Embedded | Specified | AL-REQ | Lab specification |
| SDR / Radio | Specified | AL-REQ | RF specification |
| Office / PDF | Specified | AL-REQ | Productivity specification |
| Creator / Media | Specified | AL-REQ | Creator specification |
| Music & Audio | Specified | AL-REQ | Music specification |
| Gaming / Simulation | Specified | AL-REQ | Gaming specification |
| Data / GIS | Specified | AL-REQ | Data specification |
| Cloud / DevOps | Specified | AL-REQ | Infrastructure specification |
| Business | Specified | AL-REQ | Business specification |
| Accessibility / Localization | Specified | AL-UX | Accessibility specification |
| Backup / Disaster Recovery | Specified | AL-REC | Recovery specification |
| Plugin / SDK | Specified | AL-REQ, AL-SEC | Platform specification |
| Observability / Diagnostics | Specified | AL-NFR | Observability specification |
| QA / Release Engineering | Specified | AL-TEST, AL-REL | Test + release strategy |

## Requirement ID rule

Stable IDs are defined by `requirements/requirement-id-policy.md`. The next Phase 0 task is to decompose each high-level area into atomic IDs with explicit acceptance criteria and validation evidence.

No area is considered implementation-ready merely because its row says **Specified**.

## Release traceability

Every released capability must eventually map:

`Requirement → Specification → Architecture → Implementation → Test → Validation Evidence → Release`
