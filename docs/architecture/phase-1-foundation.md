# Alpha Linux — Phase 1 Foundation

Phase 1 converts the frozen Phase 0 contracts into the smallest executable foundation.

## Initial vertical slice

`request → policy boundary → decision → health evidence`

The model/agent layer is not an authorization authority. Privileged execution remains outside this package and must be implemented behind explicit service boundaries.

## Foundation components

- versioned Python contracts;
- authorization decision model;
- health/evidence model;
- automated unit tests;
- CI validation entry point;
- traceability from implementation to Phase 0 requirements.

## Non-goals

This slice does not implement the installer, ISO, package repository, privileged daemon, desktop shell, AI runtime, firmware manager, or recovery engine.

Those systems will consume these contracts only after their own implementation gates are satisfied.
