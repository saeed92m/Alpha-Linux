# AI/ML/HPC Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Immutable workload contract | implementation/alpha_core/ai_ml_hpc.py | test_ai_ml_hpc.py | Frozen dataclass |
| Compute capacity contract | implementation/alpha_core/ai_ml_hpc.py | normalization and selection tests | No device probing |
| Deterministic planning | MLHPCPlanner | normalization test | Pure planning |
| Explicit incompatibility rejection | MLHPCPlanner.plan | disabled/insufficient tests | No fallback execution |
| Bounded resource selection | max_resources | resource-limit test | No scheduler mutation |
| No runtime side effects | Domain contract | Full CI suite | No subprocess, network, credentials, package install, or host mutation |
