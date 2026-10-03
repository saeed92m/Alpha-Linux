# Alpha Linux Master Handbook

**Handbook version:** 1.3.0  
**Handbook state:** Current / maintained  
**Repository release context:** Alpha 0.1.0a2  
**Current program phase:** Phase 7 — Alpha Releases  
**Last synchronized:** PR #259 A2 ISO artifact-transport hardening and Ubuntu-based distro comparative review

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

PR #199 adds deterministic filesystem staging and a fail-closed post-install evidence contract. The implementation verifies the staged filesystem manifest before and after commit, while post-install success requires filesystem, boot-configuration and health evidence. This is fixture/runtime evidence and does not claim physical-disk installation or physical rollback.

The next release-scoped work closes the remaining boot/media matrix, Live product UX, installer implementation, physical installation, Windows coexistence, Secure Boot and post-install validation gates.

The Handbook remains educational and must not be treated as a substitute for normative requirements or architecture decisions.

### Phase 7 evidence model

**Requirement → Specification → Architecture → Implementation → Test → CI Evidence → Artifact → Runtime Validation → Gap Detection → Refinement → Verification → Release**

A capability is product-complete only when the applicable implementation and validation gates are satisfied. Physical installation, Secure Boot, Windows dual-boot, complete hardware compatibility and production installer readiness remain open gates.



## Lessons from Ubuntu-based distribution engineering

The comparative review of Ubuntu-based distributions and image-building projects identified several practices that are now part of Alpha's engineering rules:

1. **One canonical image pipeline:** OS image creation must have one authoritative build path. Duplicate image workflows that produce the same release artifact are technical debt and must be removed or explicitly classified as validation-only.
2. **Separate build, validation and publication:** building an ISO, validating it, and publishing release assets are separate gates. Publication must consume a specific successful upstream run and must never silently rebuild or substitute an unverified image.
3. **Keep transport artifacts below provider limits:** release transport must not depend on near-limit multi-gigabyte artifact transfers. Alpha A2 therefore uses ISO chunks of at most 900 MiB, with explicit part manifests and SHA-256 verification.
4. **Integrity before publication:** every release asset is verified by provider artifact digest and/or the Alpha release checksum contract before it can enter a GitHub Release.
5. **Installer is a product subsystem:** installer UX, disk transaction, boot configuration, rollback/recovery and post-install health are separate release gates. A bootable Live ISO is not evidence of physical installation readiness.
6. **Hardware claims require hardware evidence:** QEMU/fixture evidence proves software contracts only. Physical installation, Secure Boot, Windows coexistence, touch/input, graphics, networking and suspend/resume require applicable physical validation.
7. **Document limitations explicitly:** known unsupported hardware, Secure Boot state, offline/online assumptions and recovery procedures must be release-visible rather than inferred.
8. **Prefer simple deterministic release paths:** complexity that does not improve evidence quality is removed. The goal is a short, observable path from verified image to release.

### A2 release-transport incident and resolution

The A2 release path exposed a concrete failure: ISO parts near 1.9 GiB were unreliable through the GitHub artifact transfer path. A publisher that downloaded an artifact archive successfully at the HTTP level could still receive a non-valid ZIP stream after the large transfer failed/truncated. Retrying the same transfer did not solve the architectural problem.

The corrective contract is:

**ISO → ≤900 MiB parts → individual artifacts → provider digest verification → Alpha SHA-256 manifest → reassembly verification → release publication**

This is now the preferred Alpha release-asset transport model. It is deliberately independent from the logical ISO size.

PR #259 implements the transport hardening and updates the release documentation. The release must still be rebuilt and revalidated under the new artifact contract before A2 is considered published.

### External engineering references reviewed

The comparative review used public engineering patterns from:

- Ubuntu image-build/livecd-rootfs architecture
- Universal Blue / image-template
- Calamares installer architecture
- AnduinOS build/release documentation
- Ubuntu Vanilla Build
- TunaOS documentation

These references are learning inputs, not dependencies or product requirements. Alpha's source of truth remains its own specification, architecture, implementation and CI evidence.

## Project completion protocol

Alpha Linux is completed by evidence, not by code volume. The operational loop is:

**Requirement → Specification → Architecture → Implementation → Test → CI → Artifact/Provenance → Runtime Validation → Physical Validation where applicable → Gap Detection → Refinement → Verification → Release**

### Non-negotiable evidence rules

1. **CI truth:** only terminal successful jobs count as successful. Queued, running, skipped, cancelled, missing or unknown results do not close a required gate.
2. **Failure truth:** when CI fails, inspect the actual failing job/log and correct the concrete failure. Do not guess from workflow names or previous runs.
3. **Merge truth:** a PR is merged only when GitHub reports `merged=true` and `state=closed`; a returned `merge_commit_sha` by itself is not proof.
4. **Main truth:** after merge, verify the target `main` commit and its current CI before treating the change as integrated release evidence.
5. **Evidence binding:** every release-critical claim must identify its commit, workflow run and relevant artifact/provenance or runtime/physical evidence.
6. **Scope separation:** unit tests, fixtures and QEMU validate declared software/virtual contracts. They do not satisfy physical hardware, physical installation, Secure Boot, or Windows dual-boot gates.
7. **Fail closed:** missing or ambiguous evidence keeps the gate open.
8. **Re-audit before phase advancement:** inspect current `main`, open PRs/issues and applicable workflows before moving to the next phase.

### How we finish a feature

For every release-critical feature, record four things: **implementation**, **automated evidence**, **runtime/physical evidence when applicable**, and **release-gate status**. A feature advances only when all applicable fields are satisfied. If later validation exposes a gap, update the requirement/architecture and implementation rather than retroactively treating earlier evidence as sufficient.

### Current Phase 7 completion gates

The remaining gates are tracked explicitly in the roadmap: boot/media compatibility matrix, Live UX/diagnostics/recovery, production installer UX and real-disk transaction, physical installation/hardware validation, Windows coexistence, Secure Boot, post-install boot/health validation, and Beta/Stable promotion.
