# Hardware Manager Contract

## Status

Phase 2 implementation contract. Hardware Manager is a read-only normalization
layer over hardware evidence; it does not authorize or mutate hardware.

## Responsibilities

- Normalize Hardware Discovery evidence into stable records.
- Report availability explicitly.
- Expose deterministic capability metadata for consumers such as Control Center,
  diagnostics, and future AI services.
- Preserve source evidence without inventing unavailable hardware state.

## Invariants

- Inventory ordering is deterministic.
- Missing evidence produces unavailable records, not guessed values.
- Capabilities describe observed/read-only capabilities and never grant permission.
- Driver, firmware, power, or device mutation remains outside this component.
- Privileged operations must cross the existing Policy Engine / System Service boundary.

## Future extensions

GPU, PCI, USB, storage, display, audio, network, thermal, sensor, and firmware
adapters may extend the inventory while preserving provenance, privacy,
deterministic ordering, and read-only semantics.
