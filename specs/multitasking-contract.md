# Multitasking Contract

## Status

Phase 3 reference contract. The current implementation models workspaces and
windows as immutable declarative state and produces read-only plans.

## Responsibilities

- Represent workspaces and windows with stable identifiers.
- Validate window-to-workspace assignments.
- Normalize workspace and window ordering deterministically.
- Provide deterministic window selection per workspace.
- Preserve window state and metadata without granting authorization.

## Invariants

- Workspace identifiers are unique.
- Workspace order is deterministic by index and identifier.
- Window identifiers are unique.
- Every window references an existing workspace.
- Window state is explicitly typed.
- Planning does not mutate compositor, desktop, or host state.

## Runtime boundary

A future desktop runtime adapter may translate validated plans into COSMIC
operations. Any host mutation must remain behind the existing authorization
and system-service boundaries and must provide verification evidence.
