# HiDPI Contract

## Status

Phase 3 implementation contract. The current implementation is a deterministic, declarative HiDPI model and planner; it does not mutate desktop, compositor, display-server, or host state.

## Responsibilities

- Represent validated per-display scale factors.
- Normalize display scaling state deterministically.
- Validate declarative scaling policies against known displays.
- Provide deterministic display selection for future runtime adapters.

## Invariants

- Display identifiers are non-empty and unique.
- Display state is ordered by display identifier.
- Scale factors use an explicit supported set.
- Policy display references must resolve to the normalized snapshot.
- Planning has no authorization semantics.
- Host display configuration remains outside this reference layer.

## Future runtime adapter

A production display adapter may translate a validated plan into COSMIC/display-server configuration. Any host mutation must remain behind the existing desktop/system-service authorization boundary and require explicit verification evidence.
