# Profiles Traceability

| Area | Contract | Implementation | Tests |
|---|---|---|---|
| Profile model | specs/profiles-contract.md | implementation/alpha_core/profiles.py | implementation/tests/test_profiles.py |
| Registry | specs/profiles-contract.md | implementation/alpha_core/profiles.py | implementation/tests/test_profiles.py |
| Overlay resolution | specs/profiles-contract.md | implementation/alpha_core/profiles.py | implementation/tests/test_profiles.py |

## Security trace

Profiles are declarative data only. They cannot authorize operations or cross
the Policy Engine / System Service boundary.
