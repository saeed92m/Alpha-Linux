# Alpha Linux — Executable CI/CD Gate Definitions

**Status:** Phase 0 normative gate contract

The following gate IDs are the minimum machine-oriented contract for the CI implementation.

| Gate ID | Stage | Required outcome | Blocks |
|---|---|---|---|
| CI-VAL-001 | Validate | repository structure and required metadata are valid | merge |
| CI-DOC-001 | Documentation | internal references and required documents resolve | merge |
| CI-LINT-001 | Lint | configured source/documentation lint passes | merge |
| CI-TEST-001 | Unit | applicable unit tests pass | merge |
| CI-TEST-002 | Integration | applicable integration tests pass | merge/release |
| CI-PKG-001 | Package | package metadata/dependencies/policy checks pass | merge/release |
| CI-SEC-001 | Security | secret/dependency/policy scans pass or are dispositioned | merge/release |
| CI-BLD-001 | Build | declared artifact builds successfully | release |
| CI-ART-001 | Artifact | artifact structure, manifest and digest validate | release |
| CI-REP-001 | Reproducibility | declared reproducibility target is satisfied | stable release |
| CI-ISO-001 | ISO | boot/live/install validation passes for release candidate | stable release |
| CI-REL-001 | Release | provenance, signatures, notes and compatibility records are complete | stable release |

## Current executable ISO evidence

The OS-image workflow now includes an automated QEMU boot-smoke check after ISO creation. This is supporting evidence for CI-ISO-001, not completion of the full gate.

The boot-smoke check:
- boots the generated amd64 ISO with QEMU;
- keeps the guest running for a bounded liveness interval;
- captures serial/stderr evidence;
- fails when fatal/kernel-panic signatures are detected.

The current OS-image workflow now independently exercises both BIOS and UEFI firmware boot paths under QEMU and records separate logs. This closes the automated virtualized firmware-boot evidence portion of BOOT-001/BOOT-002; it does not claim physical hardware compatibility.

The following remain separate validation requirements before CI-ISO-001 can be considered fully satisfied for a release candidate:
- UEFI/Legacy boot validation on target physical hardware;
- live-session functional validation;
- network, graphics, audio and input validation;
- actual installation;
- supported dual-boot scenarios;
- recovery path;
- checksum/signature verification at the installation boundary.

## Gate execution policy

1. A gate must have deterministic pass/fail criteria.
2. A skipped gate must have a documented applicability rule; it cannot be silently skipped.
3. Release-critical failures block promotion.
4. Manual approvals are explicit evidence, not substitutes for automated checks where automation is required.
5. Gate results identify source commit, artifact/version, environment and timestamp.
6. Gate definitions are versioned with the project.

## Implementation mapping

CI configuration maps each gate ID to concrete jobs/steps. The mapping becomes part of release evidence and must not silently rename or remove a gate.