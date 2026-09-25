# Alpha Linux Release Engineering

## Release lifecycle

```
Development
→ Nightly
→ Alpha
→ Beta
→ Stable
→ Maintenance
→ EOL
```

## Release gates

A release candidate requires:

- source state identified by immutable Git commit;
- version metadata;
- successful build;
- automated test suite;
- integration/system tests;
- security checks;
- package validation;
- dependency/SBOM data;
- artifact checksums;
- artifact signatures;
- upgrade validation;
- rollback validation;
- documentation and release notes;
- known-issues record.

## Git tags

Release tags must be immutable annotated tags following the project's versioning policy.

Examples:

- `v0.1.0`
- `v0.2.0-alpha.1`
- `v0.2.0-beta.1`
- `v1.0.0`

## Release artifacts

Artifacts must be traceable to source, build inputs and build environment. The release process must publish checksums and signatures for distributable artifacts.
