# Multi-display Contract

## Status

Phase 3 implementation contract. The current implementation is a deterministic, declarative display-topology model and planner; it does not mutate compositor, display-server, or host state.

## Responsibilities

- Represent validated display topology.
- Normalize display ordering deterministically.
- Maintain exactly one primary display for a non-empty topology.
- Validate display selections against the topology.
- Provide deterministic display selection for future runtime adapters.

## Invariants

- Display identifiers are non-empty and unique.
- Displays are ordered by display identifier.
- A non-empty topology has exactly one primary display.
- Display references must resolve to the normalized topology.
- Planning has no authorization semantics.
- Physical/display-server configuration remains outside this reference layer.

## Future runtime adapter

A production display adapter may translate a validated topology into COSMIC/display-server configuration. Any host mutation must remain behind the established desktop/system-service authorization boundary and require explicit verification evidence.
