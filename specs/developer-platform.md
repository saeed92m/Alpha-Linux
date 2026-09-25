# Alpha Linux — Developer Platform Specification

**Status:** Phase 0 normative specification
**Requirement:** AL-REQ-0020

## Purpose

Provide a coherent development environment spanning native Linux, containers, WSL, Git/GitHub, IDEs, Python/ML, build systems and remote/HPC workflows.

## Capabilities

- Project manifests and reproducible environments.
- Git/GitHub integration.
- Python and common language toolchains through controlled environment management.
- Docker/Podman integration.
- KVM/QEMU/libvirt integration where supported.
- SSH, remote development, Jupyter, MPI/Slurm integration points.
- WSL project synchronization without conflating WSL and bare-metal state.

## Rules

Developer tooling MUST NOT silently modify unrelated projects or system security policy. Environment changes MUST be inspectable and attributable. Secrets MUST use the system secret boundary and MUST NOT be written to project manifests by default.

## Recovery

Corrupt environment → recreate from manifest/lock data.
Failed toolchain update → restore prior environment or rebuild from known-good inputs.
Project data remains outside disposable environment state unless explicitly included.

## Acceptance evidence

Fresh-environment bootstrap, reproducibility, Git isolation, secret handling, container integration, WSL separation, remote execution, and recovery tests.
