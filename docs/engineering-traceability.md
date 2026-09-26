# Engineering Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Explicit engineering value/unit contract | EngineeringValue | unit validation test | No unit conversion side effects |
| Immutable project/analysis contract | EngineeringProject | duplicate/empty validation | Pure value objects |
| Compute capability contract | EngineeringResource | resource validation/planning tests | No hardware probing |
| Deterministic resource normalization | EngineeringPlanner.normalize_resources | normalization test | Pure transformation |
| Analysis/resource compatibility | EngineeringPlanner.plan | capability/size tests | No solver execution |
| Bounded resource planning | max_resources | resource-limit test | No scheduler mutation |
| Explicit rejection | Planner/value objects | rejection tests | No network, subprocess, credentials, or host mutation |
