# Touch and Pen Interaction Contract

## Status

Phase 3 reference contract. The current implementation models touch and pen
devices as immutable declarative state and produces read-only capability plans.

## Responsibilities

- Represent touch and pen devices with stable identifiers.
- Preserve explicit device kind and capability metadata.
- Normalize device ordering deterministically.
- Validate unique device identities and capability lists.
- Validate declarative input profiles against discovered devices.

## Invariants

- Device identifiers are unique.
- Device ordering is deterministic by kind and identifier.
- Device kind is explicitly typed as touch or pen.
- Device capabilities are unique and deterministically ordered.
- Input profiles may reference only discovered devices.
- Planning does not mutate input devices, desktop state, compositor state, or
  the host.

## Runtime boundary

A future desktop/input adapter may translate validated profiles into actual
input configuration. Any host mutation or privileged operation must remain
behind the existing authorization and system-service boundaries and must
provide explicit verification evidence.
