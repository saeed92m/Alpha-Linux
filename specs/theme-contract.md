# Theme System Contract

## Status

Phase 3 implementation contract. The current implementation is immutable, deterministic, declarative, and read-only.

## Responsibilities

- Represent validated theme identity and tokens.
- Normalize token ordering deterministically.
- Derive a stable content identity.
- Apply deterministic token overlays.
- Keep host mutation outside the reference layer.

## Invariants

- Theme identifiers are non-empty.
- Token names and values are non-empty.
- Token names are unique and ordered.
- Theme identity is derived from canonical theme content.
- Overlay output is deterministic.
- Planning has no authorization semantics.

## Runtime boundary

A production desktop adapter may translate a validated theme into COSMIC configuration. Any host mutation must remain behind the established authorization/system-service boundary and require explicit verification.
