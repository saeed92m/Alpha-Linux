# SDR/RF Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Immutable RF frequency contract | RFFrequencyBand | band validation | No RF probing |
| Immutable SDR capability contract | SDRDevice | device validation | No hardware access |
| Explicit acquisition requirement | RFRequirement | requirement validation | Pure contract |
| Deterministic device normalization | normalize_devices | normalization test | Pure transformation |
| Frequency compatibility | SDRRFPlanner.plan | frequency test | No tuner control |
| Sample-rate compatibility | SDRRFPlanner.plan | sample-rate test | No capture |
| Mode compatibility | SDRRFPlanner.plan | mode test | No DSP execution |
| Bounded device planning | max_devices | device-limit test | No host mutation |
| Explicit rejection semantics | value objects and planner | rejection tests | No network, subprocess, or credentials |
