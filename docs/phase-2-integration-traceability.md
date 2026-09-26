# Phase 2 Integration Traceability

| Surface | Contract | Implementation | Tests |
|---|---|---|---|
| Control Center aggregation | specs/control-center-contract.md | implementation/alpha_core/control_center.py | implementation/tests/test_control_center.py |
| Software Center | specs/software-center-contract.md | implementation/alpha_core/software_center.py | implementation/tests/test_software_center.py |
| Profiles | specs/profiles-contract.md | implementation/alpha_core/profiles.py | implementation/tests/test_profiles.py |
| Update Engine | specs/update-engine-contract.md | implementation/alpha_core/update_engine.py | implementation/tests/test_update_engine.py |
| Recovery | specs/recovery-foundation-contract.md | implementation/alpha_core/recovery.py | implementation/tests/test_recovery.py |
| Unified Phase 2 surface | specs/phase-2-integration-contract.md | implementation/alpha_core/phase2.py | implementation/tests/test_phase2.py |

## Security trace

The facade is read/plan only. No registration, profile, catalog entry, plan,
or snapshot grants authorization or privileged execution.
