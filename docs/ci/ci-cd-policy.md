# CI/CD Policy

CI is a quality system, not merely an automation convenience.

## Required pipeline stages

```
Validate
→ Lint
→ Unit Tests
→ Integration Tests
→ Package Checks
→ Security Checks
→ Build
→ Artifact Validation
→ Reproducibility Checks
→ Release Candidate
```

## Pull request gates

A pull request must not merge when a required gate fails.

Documentation-only changes may use an appropriately reduced pipeline, but policy and architecture changes still require consistency checks.

## Release pipeline

Production promotion must use immutable source identification and produce traceable artifacts, checksums, signatures and provenance.

## Secrets

Signing keys and production credentials must never be stored in source control. CI should use short-lived credentials or protected secret storage where available.

## Failure handling

Failed release jobs are investigated and rerun only after determining whether the failure is transient, environmental or caused by the change.
