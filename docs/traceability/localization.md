# Localization Traceability

| Requirement | Implementation | Tests | Specification |
| --- | --- | --- | --- |
| Immutable localization contracts | implementation/alpha_core/localization.py | implementation/tests/test_localization.py | specs/localization-contract.md |
| Deterministic normalization | LocalizationPlanner.normalize_* | test_locale_normalization_is_deterministic | Semantics |
| Locale/fallback planning | LocalizationPlanner.plan | requested/fallback tests | Semantics |
| Missing bundle reporting | LocalizationPlanner.plan | test_missing_bundle_is_reported | Semantics |
| Bounded planning | LocalizationPlanner.plan | test_plan_rejects_excess_locales | Semantics |
| Reference-only boundary | localization planner | full CI + static security | Boundary |
