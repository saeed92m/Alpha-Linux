# Cloud/DevOps Domain Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Immutable environment contract | CloudEnvironment | environment validation | Pure contract |
| Service modeling | CloudService | service validation | No cloud execution |
| Requirement modeling | CloudRequirement | requirement tests | Pure planning |
| Deterministic normalization | CloudDevOpsPlanner | normalization test | Pure transformation |
| Environment compatibility | CloudDevOpsPlanner.plan | scope test | No deployment |
| Service compatibility | CloudDevOpsPlanner.plan | compatibility test | No I/O |
| Bounded planning | max_services | bound test | No host mutation |
| Explicit rejection semantics | value objects and planner | invalid-contract tests | No network, credentials, subprocesses |
