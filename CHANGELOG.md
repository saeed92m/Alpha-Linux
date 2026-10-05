# Changelog

**Current documentation/release context:** Alpha 0.4.0  
**Handbook:** v1.1.0

All notable Alpha Linux changes will be documented here.

The project follows a release-oriented change history. Unreleased work is kept under the `Unreleased` section until it is assigned to a release.

## Alpha 0.4.0 — Modular Core & Online Software

### Added

- First-login graphical Software Setup selector for optional workstation capability bundles.
- AI & Automation / ML, Development, Engineering & CAD, Science & Astronomy, Aerospace, Networking & Security, Media & Creative, and Office package groups.
- Reusable Software Setup launcher for installing additional capabilities later.
- Repository availability filtering before optional package installation.

### Changed

- Alpha 0.4.0 keeps Core + COSMIC as the release-critical ISO payload while moving heavy optional applications online.
- The 0.4.0 image path preserves the stable installable COSMIC/Ubuntu foundation and does not require optional branding assets.

## Unreleased

### Documentation synchronization

- Synchronized README, Master Handbook, roadmap and release traceability with the actual Phase 7 / Alpha 0.1.0a2 state.
- Recorded the distinction between CI/runtime evidence and physical product validation.
- Recorded PR #193 as the release-asset metadata interpolation correction merged to `main`.
- Recorded the final A2 publication-gate hardening: publication is fail-closed and bound to the exact `main` commit after both package CI and OS-image evidence succeed.

### Added

- Alpha 0.1.0a1 release-publication foundation binding the verified package artifact to source commit, CI evidence, checksum, and deterministic tag intent without publication side effects.
- Alpha OS ISO/IMG artifact contract with deterministic naming, required metadata, provenance binding, format validation, checksum validation, and explicit no-release-before-evidence semantics.
- Executable OS image evidence validation and tests for deterministic filenames, file size, SHA-256 binding, and image-format boundaries.

### Changed

- Phase 6 security hardening is complete; privacy hardening is complete; recovery and backup are complete; compatibility is complete; performance is complete; hardware validation is complete; accessibility is complete; localization is complete; release QA is complete. Phase 6 Hardening is complete and Phase 7 — Alpha releases is active.
- Continued CI/CD, reproducibility, security, package, SBOM, artifact, and documentation validation as mandatory engineering evidence.
- Phase 7 release evidence includes machine-readable artifact SHA-256 binding through CI-REL-001.
- Phase 7 now contains a separate OS image artifact track; package release and OS image release remain independent.
- A2 publication is now fail-closed: the publisher will not download, upload, or publish release assets unless the exact target SHA has successful Alpha OS Image and Alpha Linux CI/CD runs.

### Notes

- The current `main` lineage has a verified amd64 OS image release candidate with SHA-256 and machine-readable evidence. This is not a retroactive modification of the immutable `v0.1.0a1` tag and is not a claim of production installer readiness.
- `v0.1.0a1` is an Alpha release candidate with verified package and OS-image evidence. Beta/Stable promotion remains gated by the remaining release criteria.
- The Alpha OS image track now includes a real CI build path that repacks the verified Ubuntu 26.04.1 amd64 desktop image while preserving boot metadata and emits deterministic image/provenance evidence. OS-image publication remains a separate release decision from the Python package release. It does not perform privileged host mutation, disk repartitioning, installation, or public release publication.
- Phase 3 completion refers to the deterministic reference/runtime foundation. Privileged host mutation, production COSMIC runtime integration, installer/ISO delivery, and release-scoped validation remain governed by their respective roadmap phases.
- Phase 4 reference-runtime implementation is complete. Production provider execution, persistent knowledge/memory backends, autonomous host actions, privileged integration, and release-scoped evidence remain outside these foundations and are governed by later implementation/release phases.
- Phase 5 and Phase 6 foundations remain reference contracts only unless their individual implementation evidence explicitly expands the boundary.
