# Alpha Linux Boot, Live Environment and Installer Architecture

## Status

Active Phase 7 architecture baseline. This document records the intended release architecture for boot compatibility, Live USB operation and the graphical installation experience. It does not claim physical-hardware validation that has not yet been performed.

## Product goals

Alpha Linux shall target a single release ISO that can provide:

- UEFI boot;
- Legacy BIOS boot where the platform permits it;
- Live USB operation;
- graphical Live desktop;
- graphical installer entry;
- recovery and diagnostics entry points;
- installation from the Live environment;
- GPT installation for UEFI systems;
- MBR installation for Legacy BIOS systems;
- compatibility with common USB-writing tools such as Rufus.

The boot media format and the target-disk partition table are separate concerns. The ISO provides firmware-specific boot paths; the installer selects the target-disk layout from detected firmware mode, existing storage state and explicit user intent.

## Boot architecture

```
USB media
  |
  +-- UEFI firmware --> EFI boot path --+
  |                                     |
  +-- Legacy BIOS ----> BIOS boot path -+
                                        |
                                  Linux kernel
                                        |
                                  initramfs
                                        |
                               Live filesystem
                                        |
                                Alpha Live UI
```

The release ISO should retain both UEFI and BIOS boot metadata where the selected Ubuntu base and image tooling support it. Validation must test each path independently.

## USB creation

Rufus is an intended supported USB-writing workflow. Alpha Linux does not require the USB itself to use one universal partition-table choice. The supported creation/boot matrix shall be validated for:

| Firmware | USB layout | Target layout | Status |
|---|---|---|---|
| UEFI | GPT | GPT | Target |
| UEFI | MBR | GPT | Target where firmware/tooling permits |
| Legacy BIOS | MBR | MBR | Target |
| Legacy BIOS | GPT | MBR | Compatibility target where firmware permits |

The exact Rufus mode and firmware behavior must be validated empirically rather than assumed.

## Live environment

The Live environment is a first-class product surface, not merely a rescue shell.

Required experience:

1. Alpha-branded boot/loading sequence.
2. Clear boot mode and recovery choices where practical.
3. Graphical COSMIC-based Live desktop.
4. Hardware, display, network and storage diagnostics.
5. Graphical installer launch.
6. Recovery/diagnostic entry point.
7. Read-only inspection before destructive operations.

The Live environment must remain usable without installing to the internal disk.

## Installer boundary

```
Live UI
  |
User intent
  |
Storage discovery
  |
Safety engine
  |
Installation plan
  |
Explicit confirmation
  |
Transaction engine
  |
Post-install verification
  |
Boot configuration
  |
Recovery/reporting
```

The UI must not directly mutate disks. Privileged physical-device access remains behind a separately controlled adapter boundary.

## Target installation modes

- Alpha-only installation;
- alongside Windows;
- second-disk installation;
- manual partitioning;
- encrypted installation where the required recovery/key handling is supported.

The installer must detect firmware mode, partition table, ESP presence, Windows/NTFS state, encryption/BitLocker indicators and writable state before proposing mutations.

## Safety requirements

- No implicit destructive operation.
- Explicit confirmation before disk mutation.
- BitLocker-protected Windows layouts are not silently modified.
- Proposed operations are reviewable before execution.
- Transaction failure must produce rollback/recovery evidence.
- Physical-device access is separately privileged and tested.
- Disposable virtual-disk validation precedes physical installation claims.

## Validation gates

### Current evidence

- ISO build and reproducibility evidence: verified.
- QEMU pre-install boot smoke: verified.
- Non-destructive installer safety model: verified.
- Disposable regular-file transaction execution: verified on the merged PR path.

### Required future evidence

- UEFI QEMU boot validation.
- Legacy BIOS QEMU boot validation.
- Live desktop startup validation.
- Installer graphical UX validation.
- Disposable full-install transaction and post-install verification.
- Failure injection and rollback validation.
- Physical UEFI installation.
- Legacy BIOS installation where hardware supports it.
- Windows alongside-installation validation.
- Secure Boot validation.
- Recovery after interrupted installation.

No future item is considered complete until its corresponding evidence exists.
