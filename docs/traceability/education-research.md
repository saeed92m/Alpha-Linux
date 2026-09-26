# Education and Research Domain Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Immutable workspace contract | EducationWorkspace | workspace validation | Pure contract |
| Explicit research workflow roles | ResearchRole / EducationWorkflow | workflow tests | No workflow mutation |
| Capability modeling | EducationCapability | capability validation | No education-system execution |
| Planning requirements | EducationRequirement | requirement tests | Pure planning |
| Deterministic normalization | EducationResearchPlanner | normalization test | Pure transformation |
| Education-kind compatibility | EducationResearchPlanner.plan | scope test | No LMS/ERP execution |
| Capability compatibility | EducationResearchPlanner.plan | compatibility test | No I/O |
| Bounded planning | max_capabilities | bound test | No host mutation |
| Explicit rejection semantics | value objects and planner | invalid-contract tests | No network, subprocess, credentials |
