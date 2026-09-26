# Electronics Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Immutable interface capability contract | ElectronicsInterface | interface validation | No hardware probing |
| Board capability contract | ElectronicsBoard | board planning tests | No device access |
| Component capability contract | ElectronicsComponent | compatibility tests | No flashing/programming |
| Explicit circuit requirements | CircuitRequirement | requirement validation | Pure contract |
| Deterministic component selection | normalize_components / plan | normalization/planning tests | Pure transformation |
| Board compatibility | ElectronicsPlanner.plan | board capability test | No GPIO/I2C/SPI/serial I/O |
| Component compatibility | ElectronicsPlanner.plan | component compatibility test | No instrument control |
| Bounded component planning | max_components | component-limit test | No host mutation |
| Explicit rejection semantics | value objects and planner | rejection tests | No network, subprocess, or credentials |
