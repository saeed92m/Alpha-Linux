# Alpha Linux — Subsystem Specification Matrix

**Status:** Phase 0 traceability baseline

This is the authoritative implementation-readiness index. Detailed behavior remains in the referenced normative specifications.

## State semantics

**Specified** means requirement intent is documented. **Ready** additionally requires an approved subsystem specification, architecture boundary, security/recovery treatment where applicable, test strategy, and dependency record.

| Subsystem | Requirement IDs | Specification / authority | Architecture | State |
|---|---|---|---|---|
| Alpha Core | AL-REQ-0001, AL-REQ-0002 | Master Specification | Dependency Boundaries | Specified |
| Package & Update | AL-REQ-0011, AL-PKG-* | Package Policy | Repository Architecture | Specified |
| COSMIC / Desktop | AL-REQ-0001, AL-UX-* | UI/UX Requirements | Dependency Boundaries | Specified |
| Design System | AL-UX-* | Design System | Experience Layer | Specified |
| AI Core | AL-AI-0001, AL-AI-0002 | AI Safety & Permissions | Intelligence Layer | Specified |
| Agent Runtime | AL-AI-0001–0004 | AI Safety & Permissions | Intelligence Layer | Specified |
| Orchestrator | AL-AI-0003–0004 | AI Safety & Permissions | Intelligence Layer | Specified |
| Memory / Learning | AL-AI-0005 | AI Safety & Permissions | Intelligence Layer | Specified |
| Knowledge Center | AL-REQ-0020 | specs/knowledge-center.md | Intelligence / Platform | Specified |
| Adaptive Resource Intelligence | AL-REQ-0002, AL-NFR-0008 | specs/adaptive-resource-intelligence.md | Alpha System Layer | Specified |
| Hardware / Firmware | AL-REQ-0010, AL-COMP-0002–0003 | Hardware Validation | Alpha System Layer | Specified |
| Installer / Boot | AL-REQ-0012, AL-COMP-0004 | Installer Architecture | Alpha System Layer | Specified |
| Recovery / Rollback | AL-REQ-0011, AL-REC-* | Recovery Architecture | Alpha System Layer | Specified |
| WSL Integration | AL-REQ-0013, AL-COMP-0005 | WSL Architecture | Alpha System Layer | Specified |
| Observability | AL-NFR-0006 | System Observability | Platform Services | Specified |
| Backup / DR | AL-REC-0001–0003 | Recovery Architecture | Platform Services | Specified |
| Security / Privacy | AL-SEC-* | Threat Model | Cross-cutting | Specified |
| CI/CD | AL-BLD-0003 | CI/CD Policy | Build/Release | Specified |
| ISO Build | AL-BLD-0001–0005 | ISO Build Architecture | Build/Release | Specified |
| Release / Provenance | AL-BLD-0002, AL-BLD-0004, AL-REL-* | Release Engineering | Build/Release | Specified |
| Developer Platform | AL-REQ-0020 | specs/developer-platform.md | Domain Platform | Specified |
| Astronomy / ZTF | AL-REQ-0020 | specs/astronomy-ztf-suite.md | Domain Platform | Specified |
| Engineering / CAE | AL-REQ-0020 | specs/engineering-cae-suite.md | Domain Platform | Specified |
| Motorsport | AL-REQ-0020 | specs/motorsport-suite.md | Domain Platform | Specified |
| Music & Audio | AL-REQ-0020 | specs/music-audio-suite.md | Domain Platform | Specified |
| Creator / Media | AL-REQ-0020 | specs/creator-media-suite.md | Domain Platform | Specified |
| Plugin / SDK | AL-SEC-0007 | specs/plugin-sdk.md | Platform Services | Specified |
| Domain Platform Contract | AL-REQ-0020 | specs/domain-platform-contract.md | Domain Platform | Specified |
| Localization / Accessibility | AL-NFR-0004 | UI/UX Requirements | Experience Layer | Specified |

## Readiness gate

A subsystem cannot enter **Ready** until:

1. all applicable P0 requirements have acceptance criteria;
2. the normative specification is identified;
3. architecture ownership and dependencies are explicit;
4. applicable threat controls are mapped;
5. recovery behavior is defined where state can be damaged;
6. test cases and validation evidence are identifiable;
7. unresolved contradictions are closed.

Wildcard families in this index are not requirements themselves; atomic IDs remain normative.

## Authority rule

This matrix is an index and readiness gate, not a second specification.
