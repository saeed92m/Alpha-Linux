# Hardware Manager Traceability

| Area | Contract | Implementation | Tests |
|---|---|---|---|
| Inventory model | specs/hardware-manager-contract.md | implementation/alpha_core/hardware_manager.py | implementation/tests/test_hardware_manager.py |
| Capability model | specs/hardware-manager-contract.md | implementation/alpha_core/hardware_manager.py | implementation/tests/test_hardware_manager.py |
| Degraded evidence | specs/hardware-manager-contract.md | implementation/alpha_core/hardware_manager.py | implementation/tests/test_hardware_manager.py |

## Security trace

Hardware Manager is read-only. Capability metadata is descriptive and cannot
authorize driver, firmware, power, or device mutation.
