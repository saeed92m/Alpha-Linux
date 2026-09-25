# Alpha Linux — System Integration Contract

**Status:** normative Phase 2 contract

## Purpose
Define the non-privileged integration boundary between Alpha Core and the host operating system.

## Required capabilities
- configuration/state access with explicit schemas;
- read-only system discovery;
- structured diagnostics;
- package/update inspection and planning;
- aggregated health reporting.

## Security boundary
This layer MUST NOT infer authorization from model output, UI state, service registration, or event subscriptions. Privileged mutation remains behind the existing policy/system-service boundary and OS-enforced authorization.

## Lifecycle
Discover → Validate → Prepare → Execute → Observe → Verify → Persist → Recover.

For this implementation phase, mutation-capable operations are represented as plans/dry-runs; no privileged host mutation is performed.

## Failure semantics
- malformed input is rejected deterministically;
- unavailable host information is reported as degraded evidence, not fabricated;
- diagnostics preserve structured identifiers and severity;
- health aggregation must distinguish healthy, degraded, and failed components.

## Testability
Every adapter must be usable with deterministic in-memory/reference backends so CI does not require privileged host access.
