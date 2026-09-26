# Phase 2 Integration Contract

## Status

Phase 2 integration reference contract. The facade aggregates read-only state
and deterministic plans from the system surfaces implemented in Phase 2.

## Invariants

- The integration snapshot is immutable.
- Catalog, hardware, observatory, and configuration evidence remains read-only.
- Profile resolution is declarative and cannot grant authorization.
- Update, Software Center, and Recovery plans remain dry-run and deterministic.
- The facade does not execute privileged operations.
- Authorization remains owned by the existing Policy Engine / System Service boundary.
