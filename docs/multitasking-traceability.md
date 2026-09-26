# Multitasking Traceability

| Area | Contract | Implementation | Tests |
|---|---|---|---|
| Workspace model | specs/multitasking-contract.md | implementation/alpha_core/multitasking.py | implementation/tests/test_multitasking.py |
| Window model | specs/multitasking-contract.md | implementation/alpha_core/multitasking.py | implementation/tests/test_multitasking.py |
| Deterministic normalization | specs/multitasking-contract.md | implementation/alpha_core/multitasking.py | implementation/tests/test_multitasking.py |
| Workspace selection | specs/multitasking-contract.md | implementation/alpha_core/multitasking.py | implementation/tests/test_multitasking.py |

## Security trace

Multitasking state is declarative configuration. The reference planner has no
permission to mutate windows, workspaces, the compositor, input devices, or
the host system.
