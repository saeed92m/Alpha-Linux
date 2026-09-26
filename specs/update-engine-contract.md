# Update Engine Contract

## Status

Phase 2 implementation contract. The current implementation is a deterministic reference engine and does not mutate the host package state.

## Purpose

The Update Engine provides the transaction boundary for future Alpha system updates:

CHECK -> RESOLVE -> SNAPSHOT -> APPLY -> HEALTH_CHECK -> KEEP/ROLLBACK

## Invariants

- A plan has a stable identity derived from its normalized actions.
- The engine executes the lifecycle in the declared order.
- Snapshot creation precedes any apply stage.
- Health verification is mandatory before a successful KEEP state.
- Failed health verification selects ROLLBACK.
- The reference backend is non-mutating.
- Privileged package operations remain behind an explicit OS-backed service boundary.
- Model, UI, event subscription, or plan metadata never grants authorization.
- Evidence is structured and suitable for later observability integration.

## Future privileged adapter

A production Ubuntu adapter may implement package transactions, snapshots, boot health checks, and rollback, but must remain subject to the existing policy and System Service authorization boundary.
