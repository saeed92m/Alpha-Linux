# Touch and Pen Traceability

| Area | Contract | Implementation | Tests |
|---|---|---|---|
| Device model | specs/touch-pen-contract.md | implementation/alpha_core/input.py | implementation/tests/test_input.py |
| Deterministic ordering | specs/touch-pen-contract.md | implementation/alpha_core/input.py | implementation/tests/test_input.py |
| Device selection | specs/touch-pen-contract.md | implementation/alpha_core/input.py | implementation/tests/test_input.py |
| Input profile validation | specs/touch-pen-contract.md | implementation/alpha_core/input.py | implementation/tests/test_input.py |

## Security trace

The reference input planner is declarative and read-only. It has no permission
to mutate input devices, the compositor, desktop configuration, or the host
system.
