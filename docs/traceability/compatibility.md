# Compatibility Traceability

| Requirement | Implementation | Tests | Specification |
| --- | --- | --- | --- |
| Immutable compatibility contracts | implementation/alpha_core/compatibility.py | implementation/tests/test_compatibility.py | specs/compatibility-contract.md |
| Deterministic normalization | CompatibilityPlanner.normalize_* | test_normalization_is_deterministic | Semantics 1-2 |
| Platform/version/capability evaluation | CompatibilityPlanner.evaluate | compatibility and mismatch tests | Semantics 3-6 |
| Bounded planning | CompatibilityPlanner.plan | test_plan_rejects_excess_targets | Semantics 7 |
| Reference-only boundary | compatibility planner | full CI suite + static security | Boundary |
