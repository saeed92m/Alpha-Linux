# Alpha Release Candidate Evidence Contract

## Purpose

Bind the verified Python package artifact and verified Alpha OS image artifact into one release candidate without publishing either artifact.

## Candidate identity

A candidate is valid only when:

- package and OS release IDs match;
- package and OS versions match;
- package and OS source commits match;
- the deterministic tag is `v<version>`;
- both artifact SHA-256 values are valid;
- package and OS CI run IDs remain independently recorded.

## Gate semantics

Candidate readiness requires every required gate to be explicitly present in `passing_gate_ids`.

A candidate is not ready when:

- a required gate is missing;
- a required gate is failed;
- package/OS identity binding fails;
- either artifact digest is invalid.

The candidate evidence model performs planning only. It does not create tags, GitHub Releases, uploads, downloads, or repository mutations.

## Artifact tracks

The package and OS tracks remain independently evidenced:

- package artifact: Python wheel, package CI run and SHA-256;
- OS artifact: Alpha ISO/IMG, OS CI run and SHA-256.

Combining them into candidate evidence does not imply that the OS image has been installation-validated or publicly released.

## Release boundary

This contract establishes **release-candidate readiness evidence**, not publication.

An actual Alpha release still requires an explicit publication operation after all release gates have been independently reviewed.
