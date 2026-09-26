# Theme System Contract

## Status

Phase 3 implementation contract. The current implementation is a deterministic, declarative theme model and resolver; it does not mutate desktop or compositor state.

## Responsibilities

- Represent validated theme identity, metadata, and visual tokens.
- Resolve ordered declarative overlays deterministically.
- Provide stable theme identity for normalized inputs.
- Preserve theme state as descriptive configuration only.

## Invariants

- Theme identifiers follow a stable machine-readable format.
- Theme color tokens use explicit six-digit hexadecimal values.
- Overlay order is deterministic; later overlays override earlier values.
- Unknown tokens are rejected rather than silently ignored.
- Theme resolution has no authorization semantics.
- Theme application to COSMIC or the host remains outside this reference layer.

## Future runtime adapter

A production theme adapter may translate resolved themes into COSMIC configuration, but any host mutation must remain behind the existing desktop/system-service authorization boundary and require verification evidence.
