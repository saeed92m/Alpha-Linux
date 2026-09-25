# Versioning Policy

Alpha Linux uses Semantic Versioning for product releases:

`MAJOR.MINOR.PATCH`

Pre-release identifiers may be appended for development channels, for example:

- `1.0.0-alpha.1`
- `1.0.0-beta.1`
- `1.0.0-rc.1`

## Rules

- MAJOR: incompatible public product/API changes after stable release.
- MINOR: backward-compatible capabilities.
- PATCH: backward-compatible fixes.
- Pre-release versions are not stable releases.

Git release tags use the exact release version with a `v` prefix, such as `v1.0.0`.

Version numbers are never reused for different release artifacts.
