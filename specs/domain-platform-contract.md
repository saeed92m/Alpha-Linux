# Alpha Linux — Domain Platform Contract

**Status:** Phase 0 normative specification
**Scope:** Common contract for first-class domain suites.

## Purpose

Domain suites extend Alpha without redefining the Ubuntu foundation or bypassing Alpha security, packaging, recovery, observability, or UX contracts.

## Normative requirements

1. Every suite MUST declare owner, version, capability set, dependencies, supported environments, permissions, data locations, external services, and recovery behavior.
2. Domain applications MUST consume documented platform interfaces where available rather than creating parallel system-management mechanisms.
3. A suite MUST NOT silently install unrestricted repositories, modify boot state, weaken security policy, or acquire administrative privileges.
4. Long-running jobs MUST expose state, resource use, cancellation, logs, and failure evidence to System Observatory where technically possible.
5. User/project data MUST remain distinguishable from generated cache, temporary data, and reproducible build/runtime state.
6. Domain automation MUST use the same authorization model as Alpha agents.
7. Domain configuration MUST be exportable or reconstructable where practical.
8. Unsupported capabilities MUST be explicit rather than presented as working.

## Standard lifecycle

Discover → Validate Environment → Resolve Dependencies → Prepare Workspace → Execute → Observe → Verify → Persist Results → Recover/Clean Up.

## Integration points

- Alpha Project Manifest
- Alpha Environment Manager
- Alpha Command Bar
- Alpha AI/Agent Runtime
- Alpha Knowledge Center
- System Observatory
- Backup/Recovery
- Software/package policy
- Design System and localization

## Acceptance evidence

A domain suite is specification-ready only when its capability contract, dependency boundary, security treatment, recovery scenarios, test identifiers, and supported-state matrix are documented.
