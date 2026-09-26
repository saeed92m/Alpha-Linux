# Alpha OS ISO/IMG Artifact Contract

## Purpose

Define the release-scoped contract for an installable Alpha Linux OS image artifact without claiming that an installable image exists before CI produces and validates one.

## Artifact boundary

The OS image track is separate from the Python package track.

- Package release target: `0.1.0a1`
- OS image channel: Alpha
- Candidate image formats: ISO and IMG, selected by the implemented build target
- No OS release is considered publishable without an actual image artifact and independent CI evidence.

## Required metadata

Every produced image candidate must have machine-readable evidence containing:

- release identifier
- product version
- channel
- artifact filename
- artifact format
- artifact byte size
- SHA-256 digest
- source commit
- CI run identifier
- deterministic artifact name
- build environment identifier
- reproducibility result
- SHA-256 digest of the reproducibility comparison build
- fixed `SOURCE_DATE_EPOCH` used by the reproducible build

## Deterministic naming

The image filename must encode product, version, channel, architecture and format.

Reference pattern:

`alpha-linux-{version}-{channel}-{arch}.{format}`

Examples:

- `alpha-linux-0.1.0a1-alpha-amd64.iso`
- `alpha-linux-0.1.0a1-alpha-amd64.img`

The exact filename is part of the release evidence and must not be silently changed after evidence generation.

## Reproducibility

The Alpha ISO build uses a fixed `SOURCE_DATE_EPOCH` and performs a second build from the same verified Ubuntu base image and the same generated provenance input during the same CI run.

The reproducibility gate passes only when the SHA-256 digest of the final artifact exactly matches the SHA-256 digest of the comparison build.

The evidence records:

- `reproducibility_result`: `passed`, `failed`, or `not-run`;
- `reproducibility_reference_sha256`: digest of the comparison build;
- `source_date_epoch`: fixed timestamp input.

This is a same-run deterministic reproducibility check. It does not by itself establish reproducibility across different xorriso versions, runner images, operating systems, or independently reconstructed environments.

## Validation gates

An OS image candidate must pass:

1. format validation;
2. non-zero and internally consistent byte-size validation;
3. SHA-256 generation and verification;
4. source-commit binding;
5. CI-run binding;
6. deterministic filename validation;
7. metadata completeness validation;
8. executable two-build reproducibility validation;
9. package-path regression validation.

## Non-goals

This contract does not itself provide:

- privileged host installation;
- bootloader mutation;
- disk repartitioning;
- unattended host modification;
- public release publication;
- a claim that an ISO/IMG is installable merely because the artifact was generated.

## Release rule

No OS image tag, GitHub Release, download claim, or installability claim may be made until an actual image artifact and all required evidence are present and green.
