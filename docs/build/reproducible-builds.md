# Alpha Linux Reproducible Build Policy

Builds must be designed so that release artifacts can be independently traced and, where technically feasible, reproduced from documented inputs.

## Required build metadata

- source commit
- version
- package set
- repository snapshot/policy
- build environment
- build configuration
- toolchain versions
- generated artifacts
- checksums
- signatures

## Goals

- deterministic inputs
- isolated build environments
- pinned dependencies where practical
- artifact provenance
- repeatable CI builds
- documented exceptions when bit-for-bit reproducibility is not achievable
