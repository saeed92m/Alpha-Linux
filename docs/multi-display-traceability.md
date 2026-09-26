# Multi-display Traceability

| Contract requirement | Implementation | Test evidence |
|---|---|---|
| Immutable display topology | implementation/alpha_core/multidisplay.py — DisplayNode/DisplayTopology | topology validation tests |
| Deterministic ordering | MultiDisplayPlanner.normalize | test_normalize_orders_displays_and_selects_primary |
| Exactly one primary display | DisplayTopology | test_multiple_primary_displays_are_rejected |
| Display reference validation | MultiDisplayPlanner.select | test_unknown_display_selection_is_rejected |
| Deterministic selection | MultiDisplayPlanner.select | test_selection_is_deterministic |

## Security trace

The implementation is declarative and read-only. It has no capability to mutate compositor state, display-server configuration, desktop settings, physical displays, or the host. Future privileged/runtime integration remains behind the established authorization and system-service boundary.
