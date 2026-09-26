# Accessibility Contract

## Purpose

Define deterministic, reference-only accessibility planning for Phase 6.

## Semantics

- Accessibility capabilities and requirements are immutable and uniquely identified.
- Normalization is deterministic by identifier.
- A requirement passes only when category matches and every required feature is declared by a capability.
- Unmatched requirements fail.
- Planning is bounded by max_capabilities.

## Boundary

The planner does not probe UI state, query assistive technologies, access filesystem/network resources, execute subprocesses, or mutate host state.
