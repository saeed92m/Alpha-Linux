# Hardware Validation Traceability

| Requirement | Implementation | Tests | Specification |
| --- | --- | --- | --- |
| Immutable hardware contracts | implementation/alpha_core/hardware_validation.py | implementation/tests/test_hardware_validation.py | specs/hardware-validation-contract.md |
| Deterministic normalization | HardwareValidationPlanner.normalize_* | test_normalization_is_deterministic | Semantics |
| Capability validation | HardwareValidationPlanner.evaluate | pass/fail tests | Semantics |
| Bounded planning | HardwareValidationPlanner.plan | test_plan_rejects_excess_capabilities | Semantics |
| Reference-only boundary | hardware validation planner | full CI + static security | Boundary |
