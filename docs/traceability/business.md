# Business Domain Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Immutable workspace contract | BusinessWorkspace | workspace validation | Pure contract |
| Explicit workflow lifecycle roles | WorkflowRole / BusinessWorkflow | workflow tests | No workflow mutation |
| Capability modeling | BusinessCapability | capability validation | No business-system execution |
| Planning requirements | BusinessRequirement | requirement tests | Pure planning |
| Deterministic normalization | BusinessPlanner | normalization test | Pure transformation |
| Business-kind compatibility | BusinessPlanner.plan | scope test | No transaction execution |
| Capability compatibility | BusinessPlanner.plan | compatibility test | No I/O |
| Bounded planning | max_capabilities | bound test | No host mutation |
| Explicit rejection semantics | value objects and planner | invalid-contract tests | No network, subprocess, credentials |
