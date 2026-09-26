# Contributing to Alpha Linux

Alpha Linux is developed documentation-first and specification-first.

## Current phase

The repository has completed the **Phase 2 reference-runtime baseline** and is entering **Phase 3 — Desktop and Interaction**. Phase 0 specification and Phase 1 foundation baselines remain established; all implementation work must remain traceable to the frozen specification.

## Workflow

1. Identify or create the requirement.
2. Confirm the relevant specification and architecture boundary.
3. Create an issue or approved change request for non-trivial work.
4. Use a focused branch.
5. Implement the smallest coherent change.
6. Add or update unit/integration tests and traceability.
7. Run applicable automated checks.
8. Submit a pull request.
9. Complete review and resolve findings.
10. Merge only when the change is traceable, tested and documented.

## Commit convention

Use clear Conventional Commit-style messages:

- feat
- fix
- docs
- build
- ci
- test
- refactor
- perf
- security
- chore

Example: `docs: define package repository policy`

## Quality principle

A change is not complete until its requirements, documentation, tests and release implications are addressed.
