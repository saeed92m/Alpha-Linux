# Performance Contract

## Purpose

Define deterministic, reference-only performance planning for Phase 6.

## Semantics

- Targets and requirements are immutable and identified uniquely.
- Normalization is deterministic by identifier.
- A target meets a requirement only when workload matches, latency is at or below the maximum, throughput is at or above the minimum, and resource budget is at or below the maximum.
- Unmatched requirements are reported as misses.
- Planning is bounded by max_targets.

## Boundary

The planner does not benchmark, execute workloads, probe hosts, inspect processes, access filesystem/network resources, or mutate system state.
