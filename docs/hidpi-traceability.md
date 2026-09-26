# HiDPI Traceability

| Contract requirement | Implementation | Test evidence |
|---|---|---|
| Immutable display scaling model | implementation/alpha_core/hidpi.py — DisplayScaleDescriptor | test_unsupported_scale_is_rejected |
| Deterministic display ordering | HiDPIPlanner.normalize | test_normalize_is_deterministic |
| Unique display identifiers | HiDPISnapshot | test_duplicate_display_ids_are_rejected |
| Policy/display reference validation | HiDPIPlanner.validate_policy | test_policy_accepts_available_displays, test_unknown_display_is_rejected |
| Deterministic display selection | HiDPIPlanner.scales_for_displays | test_scales_for_displays_are_deterministic |

## Security trace

The implementation is declarative and read-only. It has no capability to mutate compositor state, display-server configuration, desktop settings, or the host. Future privileged/runtime integration remains behind the established authorization and system-service boundary.
