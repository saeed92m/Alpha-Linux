# Motorsport Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Immutable vehicle capability contract | MotorsportVehicle | vehicle validation | No vehicle probing |
| Component capability contract | MotorsportComponent | compatibility tests | No hardware access |
| Explicit setup requirements | SetupRequirement | requirement validation | Pure contract |
| Deterministic component selection | normalize_components / plan | normalization/planning tests | Pure transformation |
| Vehicle compatibility | MotorsportPlanner.plan | vehicle capability test | No ECU/CAN execution |
| Component compatibility | MotorsportPlanner.plan | kind/capability tests | No telemetry I/O |
| Bounded setup planning | max_components | component-limit test | No scheduler/actuator mutation |
| Explicit rejection semantics | value objects and planner | rejection tests | No network, subprocess, credentials, or host mutation |
