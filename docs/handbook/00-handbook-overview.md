# Alpha Linux Master Handbook

**Handbook version:** 1.1.0  
**Handbook state:** Current / maintained  
**Repository release context:** Alpha 0.1.0a2  
**Current program phase:** Phase 7 — Alpha Releases  
**Last synchronized:** after PR #193 release-asset metadata correction (#193)

## Purpose

The Master Handbook is the learning and operational guide for understanding Alpha Linux from first principles through distribution engineering, AI integration, implementation, testing, release engineering and maintenance.

It is deliberately separate from the normative specification.

## Learning path

1. Computer and operating-system fundamentals
2. Linux fundamentals
3. Ubuntu/Debian foundation
4. Kernel, boot, storage, memory and services
5. Hardware, drivers, networking and security
6. Desktop Linux and COSMIC
7. Distribution engineering
8. Bootable media and Live environments
9. Installation, partitioning, boot configuration and recovery
10. Alpha architecture
11. AI, LLMs, memory and agents
12. Alpha implementation
13. Testing and QA
14. Release engineering
15. Maintenance and evolution

## Chapter method

Each chapter should contain:

- Concept
- Why it matters
- How Linux/Ubuntu implements it
- How Alpha uses it
- Architecture
- Practical examples
- Tools and commands
- Configuration
- Common failures
- Troubleshooting
- Security considerations
- Alpha-specific decisions
- Testing
- Exercises

Each chapter should end with:

> بعد از این فصل باید چه چیزی بلد باشم؟

## Handbook vs specification

The Handbook teaches **what, why and how the underlying concepts work**.

Release evidence establishes which implementation claims are currently verified; the Handbook must not turn an unverified capability into a completion claim.

The Specification defines **exactly what Alpha Linux must provide**.

The Architecture describes **how Alpha is intended to provide it**.

The Implementation is the actual system.

Testing demonstrates that the system satisfies its requirements.

## Current phase

The project is currently in **Phase 7 — Alpha Releases**, with **Alpha 0.1.0a2** as the active release context on `main`.

The immutable `v0.1.0a1` lineage remains historical and unchanged. Current `main` has a real amd64 OS-image build/evidence track with deterministic manifests, SHA-256/provenance, reproducibility validation, QEMU boot evidence, Live kernel/initramfs evidence, automated COSMIC graphical-runtime evidence, and release-safe ISO split assets.

These are engineering/CI evidence capabilities, not claims of physical installation readiness, complete hardware validation, production installer readiness, or Beta/Stable release.

The next release-scoped work closes the remaining boot/media matrix, Live product UX, installer implementation, physical installation, Windows coexistence, Secure Boot and post-install validation gates.

The Handbook remains educational and must not be treated as a substitute for normative requirements or architecture decisions.

### Phase 7 evidence model

**Requirement → Specification → Architecture → Implementation → Test → CI Evidence → Artifact → Runtime Validation → Gap Detection → Refinement → Verification → Release**

A capability is product-complete only when the applicable implementation and validation gates are satisfied. Physical installation, Secure Boot, Windows dual-boot, complete hardware compatibility and production installer readiness remain open gates.
