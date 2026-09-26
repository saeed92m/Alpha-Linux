# Software Center Contract

## Status

Phase 2 implementation contract. The current implementation is a deterministic,
read-only catalog and transaction-planning reference; it does not mutate host
package state.

## Responsibilities

- Discover structured local software catalog manifests.
- Validate package identifiers and required metadata.
- Expose deterministic catalog ordering and lookup.
- Produce deterministic install/remove transaction plans.
- Preserve explicit privilege and dry-run metadata.

## Invariants

- Catalog entries are sorted by stable package identifier.
- Duplicate package identifiers resolve deterministically.
- Invalid or inaccessible manifests are skipped rather than converted into fabricated data.
- Transaction plans have stable identities derived from normalized action inputs.
- Transaction planning never performs package installation or removal.
- Authorization remains outside Software Center.

## Future package-manager adapter

A future Ubuntu package-manager adapter may resolve and execute transactions,
but execution must remain behind the existing Policy Engine/System Service
boundary, with explicit authorization, verification, audit evidence, and
recovery semantics.
