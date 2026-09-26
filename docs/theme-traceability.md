# Theme System Traceability

| Contract requirement | Implementation | Test evidence |
|---|---|---|
| Immutable theme model | ThemeToken / ThemeDescriptor | constructor validation tests |
| Deterministic ordering | ThemePlanner.normalize | test_normalize_orders_tokens |
| Unique tokens | ThemeDescriptor | test_duplicate_tokens_are_rejected |
| Stable identity | ThemePlanner.identity | test_identity_is_stable |
| Deterministic overlays | ThemePlanner.overlay | test_overlay_is_deterministic |

## Security trace

The implementation is declarative and read-only. It cannot mutate compositor state, display-server configuration, desktop settings, installed assets, or the host. Runtime mutation remains behind the established authorization and system-service boundary.
