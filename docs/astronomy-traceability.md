# Astronomy Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Immutable sky-position contract | implementation/alpha_core/astronomy.py | coordinate validation tests | No coordinate-service I/O |
| Photometry validation | Photometry | non-finite magnitude test | Pure value object |
| Observation contract | AstronomyObservation | construction and planning tests | No archive/FITS access |
| Deterministic normalization | AstronomyPlanner.normalize | normalization test | Pure transformation |
| Bounded object-specific selection | AstronomyPlanner.plan | bounded planning test | No scheduler or data acquisition |
| Explicit rejection | Planner and value objects | duplicate/missing/invalid tests | No fallback side effects |
