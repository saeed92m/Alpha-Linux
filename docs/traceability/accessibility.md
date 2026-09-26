# Accessibility Traceability

| Requirement | Implementation | Tests | Specification |
| --- | --- | --- | --- |
| Immutable accessibility contracts | implementation/alpha_core/accessibility.py | implementation/tests/test_accessibility.py | specs/accessibility-contract.md |
| Deterministic normalization | AccessibilityPlanner.normalize_* | test_normalization_is_deterministic | Semantics |
| Capability validation | AccessibilityPlanner.evaluate | pass/fail tests | Semantics |
| Bounded planning | AccessibilityPlanner.plan | test_plan_rejects_excess_capabilities | Semantics |
| Reference-only boundary | accessibility planner | full CI + static security | Boundary |
