# Alpha Linux — Architecture Dependency Boundaries

**Status:** Phase 0 normative architecture boundary model

## 1. Architectural rule

Alpha integrates Ubuntu and COSMIC rather than replacing their foundations. Alpha-owned components shall depend on stable platform interfaces where practical.

The dependency direction is:

**Foundation → Alpha System Layer → Experience / Intelligence / Platform / Domain Layers**

Higher layers may consume lower-layer contracts; lower layers must not depend on higher-level product behavior.

## 2. Logical layers

| Layer | Responsibility | Examples |
|---|---|---|
| L0 Foundation | OS and hardware interfaces | Linux kernel, Ubuntu base, systemd, firmware, drivers |
| L1 Alpha System | Alpha-owned system integration | Alpha Core, package/update, hardware, power, network |
| L2 Experience | Human interaction | COSMIC integration, Control Center, Command Bar, Profiles |
| L3 Intelligence | AI and agent behavior | AI Core, Memory, Knowledge, Agent Runtime, Orchestrator |
| L4 Platform Services | Cross-cutting services | Security, observability, backup/recovery, sync, plugin/SDK |
| L5 Domain Suites | Specialized workflows | Astronomy, Engineering, Motorsport, Creator, Music, Developer |

## 3. Dependency rules

1. L0 shall not depend on Alpha UI, agents, or domain suites.
2. L1 may consume L0 interfaces and expose stable Alpha contracts upward.
3. L2 may consume L1 and selected L4 contracts; it must not own privileged authorization.
4. L3 may request actions through the Tool/Policy boundary but cannot grant itself authorization.
5. L4 security/policy controls may mediate L1–L5 operations.
6. L5 suites shall consume published Alpha contracts and shall not redefine the OS foundation.
7. Shared contracts must be versioned and documented.
8. Cross-layer calls must have an explicit owner, timeout/failure behavior, and recovery behavior where applicable.

## 4. Prohibited coupling

Unless explicitly approved by an Architecture Decision Record:

- AI model code directly invokes unrestricted privileged interfaces.
- Domain code changes package/repository policy.
- UI code becomes the authorization authority.
- Plugin code receives implicit full-system privileges.
- Recovery depends on the unavailable normal-session UI.
- Observability collects unrestricted sensitive data for convenience.
- Core, AI, UI and domain layers form circular dependencies.
- Alpha relies on uncontrolled arbitrary Debian repositories.

## 5. Trust boundaries

Critical boundaries are:

- User ↔ Alpha UI
- AI model ↔ Tool/Policy enforcement
- Alpha ↔ privileged system services
- Alpha ↔ external package repositories
- Alpha ↔ plugins/agents
- Alpha ↔ cloud services
- Alpha ↔ recovery environment
- Alpha ↔ removable/external storage
- Build system ↔ release artifacts

Authorization, integrity and validation must be enforced at the boundary.

## 6. Contract ownership

| Contract | Owner |
|---|---|
| OS/system integration | Alpha System Layer |
| Privileged authorization | Security / Policy Layer |
| User interaction | Experience Layer |
| AI planning/inference | Intelligence Layer |
| Agent execution | Agent Runtime + Policy Layer |
| Memory persistence | Memory subsystem |
| Knowledge retrieval | Knowledge Center |
| Package/update state | Package/Update subsystem |
| Recovery state | Recovery subsystem |
| Diagnostics | Observability subsystem |
| Domain APIs | Domain Platform |
| External integrations | Integration boundary |

## 7. Architecture-readiness gate

A subsystem is **architecture-ready** only when owner, inputs, outputs, dependencies, trust boundaries, failure states, recovery path, and test hooks are documented.

**Traceability:** Requirement → Specification → Boundary → Contract → Implementation → Test → Evidence
