# Compatibility Contract

## Purpose

Define the Phase 6 compatibility foundation as immutable, deterministic planning contracts.

## Contracts

- CompatibilityTarget describes a reference platform/version and declared capabilities.
- CompatibilityRequirement declares a platform, minimum version, and required capabilities.
- CompatibilityDecision records a compatible/incompatible planning result.
- CompatibilityPlan records normalized targets and incompatible requirements.
- CompatibilityPlanner performs deterministic normalization, compatibility evaluation, and bounded planning.

## Semantics

1. Target and requirement identifiers must be non-empty and unique within their collections.
2. Normalization is deterministic by identifier.
3. Platform names must match exactly.
4. Target version must meet or exceed the requirement minimum version using deterministic dotted-version token comparison.
5. Every required capability must be declared by the target.
6. Unmatched requirements are incompatible and have no selected target.
7. Planning is bounded by max_targets.

## Boundary

This is reference-only planning. It does not probe the host, inspect installed packages, access the network or filesystem, execute subprocesses, install software, or mutate system state.
