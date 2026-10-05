# Alpha Linux Portable Persistent Requirements

**Change Request:** #290  
**Status:** Proposed/implementing; no physical support claim until evidence exists.

## PP-001 — Full desktop execution
Portable Persistent shall provide the complete Alpha desktop environment, including COSMIC, terminal, file management, networking and core system controls.

## PP-002 — No host installation
Portable Persistent shall boot and operate without installing Alpha Linux to the host internal disk or installing host-side packages.

## PP-003 — Persistent user state
A successful shutdown/reboot shall preserve the documented user account, password configuration, desktop settings, files and installed application state.

## PP-004 — Persistent package state
Packages explicitly installed by the user shall remain installed after reboot.

## PP-005 — Host RAM
The running Alpha system shall use the RAM of the machine on which it is booted. Portable media capacity shall not substitute for host RAM.

## PP-006 — Memory pressure
zram shall be the preferred default mechanism for compressed swap-like memory pressure. USB-backed swap shall be optional and must not be mandatory.

## PP-007 — Minimal base
The release-critical base shall contain only software required for a functional Alpha workstation. Heavy domain applications, large datasets and optional development stacks shall not be mandatory ISO payload.

## PP-008 — Individual applications
Each supported application shall be independently installable. A domain bundle is a convenience manifest and shall not be a dependency of an individual application.

## PP-009 — Dependency resolution
Installing one application shall install only its required dependencies and shared runtime components. Removing one application shall not remove dependencies still required by another installed application.

## PP-010 — Bundle semantics
Optional bundles such as Astronomy or Engineering shall be selectable sets of individual applications. Users shall be able to install any application without installing the whole bundle.

## PP-011 — Persistence boundary
Temporary/cache data should not be persisted when it can be regenerated. Persistent storage design shall minimize unnecessary writes to removable media.

## PP-012 — Capacity
The first reference target shall support a 64-GB-class device. The build must calculate available capacity and fail closed if the selected persistent layout cannot fit.

## PP-013 — Encryption
Portable persistence shall have a supported encryption design before the feature is promoted as suitable for sensitive personal data.

## PP-014 — Recovery
The system shall provide a documented recovery path for filesystem errors, failed updates and an unusable persistent state without requiring the host OS to be modified.

## PP-015 — Firmware
UEFI shall be supported first. Legacy BIOS support remains subject to the existing media compatibility contract and direct evidence.

## PP-016 — Physical evidence
Physical USB/media/hardware validation shall remain separate from CI, QEMU and fixture evidence.

## PP-017 — Existing-path non-regression
Adding Portable Persistent shall not weaken or bypass existing Alpha build, installer, security, provenance or release gates.

## PP-018 — Artifact identity
Portable Persistent images shall have an explicit artifact type and versioned manifest. A disposable Live ISO shall not be relabeled as a persistent image.

## Definition of done
A Portable Persistent release candidate requires implementation, automated tests, artifact/provenance evidence, runtime persistence evidence and applicable physical-media evidence. Missing evidence leaves the gate open.
