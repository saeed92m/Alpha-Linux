# Release QA Contract

## Purpose

Define deterministic, reference-only release QA evidence aggregation for Phase 6.

## Semantics

- QA gates and evidence are immutable and uniquely identified.
- Normalization is deterministic by gate identifier.
- Required gates must have passing evidence.
- Missing required evidence and failed required evidence fail the QA result.
- Missing optional gates do not fail the result.
- Passing evidence must carry an evidence identifier.

## Boundary

The planner does not publish releases, create tags, upload artifacts, access filesystem/network resources, execute subprocesses, or mutate host/repository state.
