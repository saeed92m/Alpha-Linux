# Alpha Linux Risk Register

| ID | Risk | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|
| R-001 | Scope grows faster than engineering capacity. | High | Master Feature Matrix + Change Requests + phased releases. | Project | Open |
| R-002 | Ubuntu/COSMIC upstream changes cause regressions. | High | Compatibility matrix, pinned build inputs, CI and upgrade testing. | Foundation | Open |
| R-003 | Hardware variability creates inconsistent behavior. | High | Hardware Compatibility Database and validation matrix. | Foundation | Open |
| R-004 | AI actions create security or privacy exposure. | Critical | Explicit permissions, sandboxing, approval and auditability. | Security/AI | Open |
| R-005 | Non-reproducible builds weaken release confidence. | High | Reproducible build policy, manifests, checksums and provenance. | Release | Open |
| R-006 | Recovery/rollback is insufficient during failed updates. | Critical | Snapshots, staged updates, health checks and rollback testing. | Recovery | Open |
| R-007 | Documentation diverges from implementation. | High | Traceability and documentation as release gates. | Documentation | Open |
