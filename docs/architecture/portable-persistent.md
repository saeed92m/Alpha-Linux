# Alpha Linux Portable Persistent Architecture

**Status:** Proposed/implementing under Change Request #290.  
**Scope:** Persistent removable-media execution, separate from disposable Live semantics and native installation.

## Product model

Alpha Linux is one product with one Ubuntu 26.04 LTS + COSMIC base and three deployment modes:

1. **Portable Persistent** — a complete Alpha desktop runs from removable media and persists the user's system state on that media.
2. **Live/Recovery** — disposable execution intended for testing, diagnostics and recovery; changes are not part of the persistent product state.
3. **Installed** — the same Alpha base is installed to internal storage by the graphical installer.

The modes share the product/base contracts. They are not separate distributions.

## Portable boot contract

Insert Alpha USB → power on/restart → firmware Boot Menu (or configured USB-first boot) → Alpha bootloader → Alpha Persistent system → login → COSMIC desktop.

No host-OS installation, internal-disk partitioning, bootloader installation, or host package installation is required for Portable Persistent mode.

The portable system uses the host machine's RAM and detected hardware. zram is the preferred memory-pressure mechanism. USB-backed swap is optional.

## Reference 64-GB layout

| Area | Initial target | Purpose |
|---|---:|---|
| EFI System Partition | 512 MiB | UEFI boot |
| Boot | 1 GiB | kernel/initramfs/boot support |
| Alpha system | 20–24 GiB | base OS + selected applications |
| Optional swap | 0–4 GiB | only when explicitly enabled |
| Persistent home/data | remainder | user files, settings and persistent application state |

The implementation must calculate actual usable capacity and reserve space rather than assuming decimal vendor capacity.

## Persistence contract

Persistent state includes, subject to the selected security policy: user account and password hash; installed packages and package configuration; Alpha configuration; desktop settings; user home directory; user projects and documents; and explicitly enabled application state.

Regeneratable data should remain outside the persistent contract where practical: temporary files, caches, transient runtime state, unnecessary logs, and rebuildable package caches. The design must minimize unnecessary writes to removable media.

## Security

Portable persistence must support an encrypted-storage profile. The encryption boundary, recovery-key handling and password/key lifecycle must be explicit before the feature is promoted to a release claim.

## Hardware portability

The image must not be tied to one laptop model. Boot-time discovery and generic Ubuntu-compatible hardware support are the baseline. CI/QEMU can establish software/runtime contracts but cannot prove physical USB, firmware or hardware compatibility.

## Update semantics

A persistent portable system is a normal writable Alpha system from the user's perspective: package updates are persistent; installed applications are persistent; configuration changes are persistent. The implementation must protect against interrupted updates and filesystem corruption and provide recovery guidance.

## Relationship to the existing ISO

The current release ISO remains the disposable/installation artifact until a dedicated persistent image is implemented and validated. A Live ISO must not be described as Persistent Portable merely because it can be written to USB.

Portable Persistent should be released as a separately identified artifact/image contract, even when produced from the same Alpha base.

## Release gates

Portable Persistent is not release-complete until boot, login, reboot persistence, package/update persistence, file persistence, optional swap policy, encryption profile (if advertised), filesystem integrity/recovery and physical USB validation have evidence. QEMU, CI fixtures and ISO metadata do not close physical-media gates.
