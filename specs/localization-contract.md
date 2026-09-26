# Localization Contract

## Purpose

Define deterministic, reference-only localization planning for Phase 6.

## Semantics

- Locale and translation-bundle contracts are immutable and uniquely identified.
- Locale and bundle normalization is deterministic by identifier.
- The requested locale is selected when supported; otherwise the configured default locale is selected.
- The default locale must be supported.
- Supported locales without a translation bundle are reported explicitly.
- Planning is bounded by max_locales.

## Boundary

The planner does not call translation services, access filesystem/network resources, execute subprocesses, or mutate application state.
