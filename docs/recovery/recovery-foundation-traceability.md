# Recovery Foundation Traceability

| Area | Contract | Implementation | Tests |
|---|---|---|---|
| Checkpoint identity | specs/recovery-foundation-contract.md | implementation/alpha_core/recovery.py | implementation/tests/test_recovery.py |
| Restore planning | specs/recovery-foundation-contract.md | implementation/alpha_core/recovery.py | implementation/tests/test_recovery.py |
| Restore verification | specs/recovery-foundation-contract.md | implementation/alpha_core/recovery.py | implementation/tests/test_recovery.py |

## Security trace

The recovery engine is an orchestration boundary, not an authorization authority.
The reference backend is non-mutating. Future privileged restore adapters must
cross the existing Policy Engine / System Service boundary.
