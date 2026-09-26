# Theme System Traceability

| Area | Contract | Implementation | Tests |
|---|---|---|---|
| Theme model | specs/theme-system-contract.md | implementation/alpha_core/theme.py | implementation/tests/test_theme.py |
| Token validation | specs/theme-system-contract.md | implementation/alpha_core/theme.py | implementation/tests/test_theme.py |
| Overlay resolution | specs/theme-system-contract.md | implementation/alpha_core/theme.py | implementation/tests/test_theme.py |
| Stable identity | specs/theme-system-contract.md | implementation/alpha_core/theme.py | implementation/tests/test_theme.py |

## Security trace

Theme data is declarative configuration. It cannot grant authorization and the reference resolver performs no desktop, compositor, package, display, or input mutation.
