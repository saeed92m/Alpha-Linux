# COSMIC Integration Contract

## Status

Phase 3 implementation contract. The current implementation is a deterministic,
non-mutating reference boundary for future COSMIC runtime integration.

## Responsibilities

- Describe supported COSMIC session/compositor integration metadata.
- Bind a validated desktop session configuration to a deterministic integration identity.
- Report explicit supported, degraded, or unavailable compatibility state.
- Preserve display and theme intent without applying it to the host.

## Invariants

- Binding identity is deterministic for identical normalized inputs.
- Missing requested displays result in unavailable state.
- Unsupported requested HiDPI behavior results in degraded state.
- The reference adapter never installs packages, starts/replaces a compositor, or mutates display/input configuration.
- Integration metadata cannot grant authorization.

## Future runtime adapter

A production COSMIC adapter may interact with the actual desktop session and compositor,
but privileged operations must remain behind the existing OS/service authorization boundary.
Session health and rollback evidence must be explicit before a runtime change is considered successful.
