# Alpha Release Contract

## Purpose

Define Phase 7 release-engineering contracts without performing publication.

## Semantics

- Release manifests are immutable and require a release ID, version, channel, and at least one artifact identifier.
- Release evidence is immutable and uniquely identified.
- Required gate IDs must be unique.
- A release is ready only when every required gate has evidence and every required evidence item passes.
- Missing or failed required evidence makes the release not ready.

## Boundary

The planner does not publish releases, create Git tags, upload artifacts, access filesystem/network resources, execute subprocesses, or mutate repository/host state.
