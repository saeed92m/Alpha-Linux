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

## Deterministic naming

The image filename must encode product, version, channel, architecture and format.

Reference pattern:

`alpha-linux-{version}-{channel}-{arch}.{format}`

Examples:

- `alpha-linux-0.1.0a1-alpha-amd64.iso`
- `alpha-linux-0.1.0a1-alpha-amd64.img`

The exact filename is part of the release evidence and must not be silently changed after evidence generation.

## Build implementation

The first Alpha image build target uses the verified Ubuntu 26.04.1 LTS amd64 desktop ISO as its immutable base, injects machine-readable Alpha provenance, and preserves the source image boot metadata through the xorriso replay mechanism. The build workflow must publish the resulting ISO and its evidence separately from the package release path.

## Validation gates

An OS image candidate must pass:

1. format validation;
2. non-zero and internally consistent byte-size validation;
3. SHA-256 generation and verification;
4. source-commit binding;
5. CI-run binding;
6. deterministic filename validation;
7. metadata completeness validation;
8. reproducibility validation when the build target supports a second independent build;
9. package-path regression validation.

## Non-goals

This contract does not itself provide:

- privileged host installation;
- bootloader mutation;
- disk repartitioning;
- unattended host modification;
- public release publication;
- a claim that an ISO/IMG already exists.

## Release rule

No OS image tag, GitHub Release, download claim, or installability claim may be made until an actual image artifact and all required evidence are present and green.
