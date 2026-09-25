# Package Lifecycle

Alpha-maintained packages follow:

```
Source
→ Package Definition
→ Build
→ Static/Dependency Checks
→ Unit/Integration Tests
→ Repository Publication Candidate
→ Signing
→ Repository Publication
→ Release
→ Monitoring
→ Update/Rollback
→ Retirement
```

## Package metadata

Each maintained package must define its version, architecture, dependencies, source, license information, maintainer and changelog.

## Repository promotion

Packages should not move directly from source to a stable repository without passing the applicable validation gates.
