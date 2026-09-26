# Recovery Foundation Contract

## Status

Phase 2 implementation contract. The reference implementation is deterministic
and non-mutating; it does not restore the host.

## Lifecycle

CHECKPOINT -> PREPARE -> RESTORE -> VERIFY -> KEEP/FAIL

## Invariants

- Checkpoint identity is stable for the same normalized label.
- Restore plans identify exactly one checkpoint.
- Verification is mandatory before KEEP.
- Failed verification produces FAIL evidence.
- The reference backend performs no destructive host mutation.
- Recovery orchestration does not depend on the Control Center UI.
- Authorization remains outside the recovery engine.
- Future filesystem, package, boot and snapshot adapters must preserve explicit
  authorization, audit, verification and recovery boundaries.
