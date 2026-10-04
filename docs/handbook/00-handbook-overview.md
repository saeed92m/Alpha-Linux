# Alpha Linux Master Handbook

**Handbook version:** 1.3.0  
**Handbook state:** Current / maintained  
**Repository release context:** Alpha 0.1.0a3  
**Current program phase:** Phase 7 — Alpha Releases  
**Last synchronized:** A3 direct publication, artifact transport hardening, and Ubuntu-based distro engineering review

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

The project is currently in **Phase 7 — Alpha Releases**, with **Alpha 0.1.0a3** as the active release context on `main`.

The immutable `v0.1.0a1` lineage remains historical and unchanged. Current `main` has a real amd64 OS-image build/evidence track with deterministic manifests, SHA-256/provenance, reproducibility validation, QEMU boot evidence, Live kernel/initramfs evidence, automated COSMIC graphical-runtime evidence, and release-safe ISO split assets.

These are engineering/CI evidence capabilities, not claims of physical installation readiness, complete hardware validation, production installer readiness, or Beta/Stable release.

PR #199 adds deterministic filesystem staging and a fail-closed post-install evidence contract. The implementation verifies the staged filesystem manifest before and after commit, while post-install success requires filesystem, boot-configuration and health evidence. This is fixture/runtime evidence and does not claim physical-disk installation or physical rollback.

The next release-scoped work closes the remaining boot/media matrix, Live product UX, installer implementation, physical installation, Windows coexistence, Secure Boot and post-install validation gates.

The Handbook remains educational and must not be treated as a substitute for normative requirements or architecture decisions.

### Phase 7 evidence model

**Requirement → Specification → Architecture → Implementation → Test → CI Evidence → Artifact → Runtime Validation → Gap Detection → Refinement → Verification → Release**

A capability is product-complete only when the applicable implementation and validation gates are satisfied. Physical installation, Secure Boot, Windows dual-boot, complete hardware compatibility and production installer readiness remain open gates.


## Lessons from Ubuntu-based distribution engineering

The comparative review of Ubuntu-based distribution projects is now part of Alpha's engineering guidance:

1. **One canonical image pipeline:** OS image creation has one authoritative build path. Duplicate builders are technical debt unless explicitly validation-only.
2. **Separate build, validation and publication:** publication consumes a specific successful validated run and never silently rebuilds or substitutes an image.
3. **Bound release transport size:** large provider transfers are avoided. Alpha's release transport uses ISO chunks of at most 900 MiB.
4. **Verify before publication:** provider artifact digests and the Alpha SHA-256 manifest/reassembly contract must pass before release publication.
5. **Installer is a separate subsystem:** Live ISO boot evidence does not prove physical installation, disk transactions, bootloader configuration, rollback/recovery, or post-install readiness.
6. **Hardware claims require hardware evidence:** QEMU validates software/virtual contracts; physical hardware, Secure Boot, Windows coexistence, touch/input, graphics, networking and suspend/resume require applicable physical tests.
7. **Document limitations explicitly:** unsupported hardware, Secure Boot state, online/offline assumptions and recovery procedures are release-visible.
8. **Prefer deterministic release paths:** remove complexity that does not improve evidence quality.

### A2 transport incident and resolution

A2 exposed unreliable GitHub artifact transfers when ISO parts approached multi-gigabyte sizes. The corrected contract is:

**ISO → ≤900 MiB parts → individual artifacts → provider digest verification → Alpha SHA-256 manifest → reassembly verification → GitHub Release**

This transport contract was implemented in PR #259. The A3 publication path goes further by publishing directly from the same validated OS-image workspace, eliminating the fragile cross-run publisher dependency.

### External engineering references reviewed

Public engineering patterns reviewed included Ubuntu image-build/livecd-rootfs, Universal Blue/image-template, Calamares, AnduinOS, Ubuntu Vanilla Build and TunaOS. These are learning inputs only; Alpha's own specification, architecture, implementation and CI evidence remain authoritative.

### Current release evidence

`v0.1.0a3` is a published prerelease from the validated A3 pipeline. It contains eight ISO parts, with parts 01–07 at 900 MiB and part 08 smaller, plus the SHA-256 manifest, parts metadata and reassembly instructions. The release is downloadable as a split ISO but remains an **Alpha/experimental** build; physical installation, production installer readiness, hardware matrix, Secure Boot and Windows coexistence are still separate gates.


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
