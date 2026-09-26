# Changelog

All notable Alpha Linux changes will be documented here.

The project follows a release-oriented change history. Unreleased work is kept under the `Unreleased` section until it is assigned to a release.

## Unreleased

### Added

- Alpha 0.1.0a1 release-publication foundation binding the verified package artifact to source commit, CI evidence, checksum, and deterministic tag intent without publication side effects.
- Alpha OS ISO/IMG artifact contract with deterministic naming, required metadata, provenance binding, format validation, checksum validation, and explicit no-release-before-evidence semantics.
- Executable OS image evidence validation and tests for deterministic filenames, file size, SHA-256 binding, and image-format boundaries.

### Changed

- Phase 6 security hardening is complete; privacy hardening is complete; recovery and backup are complete; compatibility is complete; performance is complete; hardware validation is complete; accessibility is complete; localization is complete; release QA is complete. Phase 6 Hardening is complete and Phase 7 — Alpha releases is active.
- Continued CI/CD, reproducibility, security, package, SBOM, artifact, and documentation validation as mandatory engineering evidence.
- Phase 7 release evidence includes machine-readable artifact SHA-256 binding through CI-REL-001.
- Phase 7 now contains a separate OS image artifact track; package release and OS image release remain independent.

### Notes

- The repository does not yet contain an installable Alpha Linux OS image release.
- No stable, beta, or alpha product release is claimed by this changelog until the relevant release artifact and required evidence exist.
- The Alpha OS image track currently provides the contract and executable evidence-validation foundation; it does not perform privileged host mutation, disk repartitioning, installation, or public release publication.
- Phase 3 completion refers to the deterministic reference/runtime foundation. Privileged host mutation, production COSMIC runtime integration, installer/ISO delivery, and release-scoped validation remain governed by their respective roadmap phases.
- Phase 4 reference-runtime implementation is complete. Production provider execution, persistent knowledge/memory backends, autonomous host actions, privileged integration, and release-scoped evidence remain outside these foundations and are governed by later implementation/release phases.
- Phase 5 and Phase 6 foundations remain reference contracts only unless their individual implementation evidence explicitly expands the boundary.
