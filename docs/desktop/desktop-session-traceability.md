# Desktop Session Traceability

| Area | Contract | Implementation | Tests |
|---|---|---|---|
| Display model | specs/desktop-session-contract.md | implementation/alpha_core/desktop.py | implementation/tests/test_desktop.py |
| Interaction capabilities | specs/desktop-session-contract.md | implementation/alpha_core/desktop.py | implementation/tests/test_desktop.py |
| Session planning | specs/desktop-session-contract.md | implementation/alpha_core/desktop.py | implementation/tests/test_desktop.py |

## Security trace

The reference desktop layer is read/plan only. It does not install COSMIC,
change display/input state, or grant authorization.
