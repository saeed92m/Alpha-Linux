# Alpha WSL Architecture

Alpha Linux integrates with official WSL rather than attempting to replace it.

## Scope

Alpha WSL support covers:

- distribution/environment management;
- import/export/backup/restore;
- resource configuration;
- systemd;
- WSLg;
- Windows/Linux filesystem interoperability;
- development tooling;
- Git/GitHub;
- containers;
- supported GPU/ML workflows;
- SSH and remote development;
- scientific workloads.

## Boundary

WSL and bare-metal Alpha remain independent environments.

Integration must be explicit and must not assume that WSL has identical hardware, device or kernel semantics to bare-metal Linux.

## Portability

Alpha Project Manifests should allow projects to declare dependencies and environment requirements so that supported projects can move between Windows+WSL and bare-metal Alpha with documented limitations.
