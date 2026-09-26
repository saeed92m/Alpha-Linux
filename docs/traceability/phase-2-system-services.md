# Phase 2 System Services Traceability

| Area | Contract | Architecture | Implementation | Tests |
|---|---|---|---|---|
| Update lifecycle | specs/update-engine-contract.md | architecture/control-center-and-system-services.md | implementation/alpha_core/update_engine.py | implementation/tests/test_update_engine.py |
| Hardware evidence | specs/hardware-discovery-contract.md | architecture/control-center-and-system-services.md | implementation/alpha_core/hardware.py | implementation/tests/test_hardware.py |
| Control Center | existing Observatory/System Integration contracts | architecture/control-center-and-system-services.md | implementation/alpha_core/control_center.py | implementation/tests/test_control_center.py |
| Update planning | System Integration contract | architecture/control-center-and-system-services.md | implementation/alpha_core/system_integration.py | implementation/tests/test_system_integration.py |
| Event privacy | Observability contract | Core event boundary | implementation/alpha_core/events.py | implementation/tests/test_lifecycle.py |

## Security trace

No new component becomes an authorization authority. Update mutation remains behind the pre-existing Policy Engine/System Service boundary. Hardware discovery is read-only. Control Center is aggregation-only.
