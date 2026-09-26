# Hardware Validation Contract

## Purpose

Define deterministic, reference-only hardware validation planning for Phase 6.

## Semantics

- Hardware capabilities and requirements are immutable and uniquely identified.
- Normalization is deterministic by identifier.
- A requirement passes only when device class matches and every required attribute is declared by a capability.
- Unmatched requirements fail.
- Planning is bounded by max_capabilities.

## Boundary

The planner does not probe hardware, open device handles, execute subprocesses, access filesystem/network resources, or mutate host state.
