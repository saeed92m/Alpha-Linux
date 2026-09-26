# Performance Traceability

| Requirement | Implementation | Tests | Specification |
| --- | --- | --- | --- |
| Immutable performance contracts | implementation/alpha_core/performance.py | implementation/tests/test_performance.py | specs/performance-contract.md |
| Deterministic normalization | PerformancePlanner.normalize_* | test_normalization_is_deterministic | Semantics |
| Threshold evaluation | PerformancePlanner.evaluate | latency/throughput/budget/workload tests | Semantics |
| Bounded planning | PerformancePlanner.plan | test_plan_rejects_excess_targets | Semantics |
| Reference-only boundary | performance planner | full CI + static security | Boundary |
