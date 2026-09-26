# Desktop Session Contract

## Status

Phase 3 reference contract. The current implementation models desktop/session
capabilities without changing the host or directly binding to COSMIC.

## Responsibilities

- Represent display geometry and scaling.
- Report touch, pen, HiDPI and multi-display capability state.
- Validate declarative desktop session configuration.
- Preserve deterministic display ordering.
- Expose theme metadata as declarative state.

## Invariants

- Capability discovery is read-only.
- Display identities are unique and deterministically ordered.
- Session plans may reference only discovered displays.
- Theme/session data cannot authorize privileged actions.
- Host display/input mutation remains outside the reference layer.

## COSMIC adapter boundary

A future COSMIC adapter may translate validated session plans into desktop
configuration, but privileged or host-mutating operations must cross the
existing system-service and authorization boundaries.
