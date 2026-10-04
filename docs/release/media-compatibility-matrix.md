# Alpha Linux Media Compatibility Matrix

## Purpose

This matrix is the release-gate record for physical USB/media validation. It deliberately distinguishes declared targets from observed evidence.

A row is **not validated** until a concrete test record identifies the ISO, USB-writing method, firmware mode, media layout, hardware, result, and evidence artifact.

| Firmware | USB layout | Target layout | Current status | Evidence required |
|---|---|---|---|---|
| UEFI | GPT | GPT | unverified | Physical boot record |
| UEFI | MBR | GPT | unverified | Physical boot record + tool mode |
| Legacy BIOS | MBR | MBR | unverified | Physical boot record |
| Legacy BIOS | GPT | MBR | unverified | Physical boot record + firmware support |

## Required evidence fields

- Alpha Linux release/tag and exact ISO SHA-256.
- USB-writing tool and version (for example, Rufus version and selected image mode).
- USB device model/capacity.
- Firmware mode and firmware version.
- USB partition layout actually created.
- Target-disk partition layout where installation is tested.
- Boot result and timestamp.
- Hardware model and relevant storage/display/network details.
- Evidence artifact: photo, firmware screenshot, console log, or structured test record.
- Known limitations or deviations from the declared target.

## Evidence rules

- QEMU evidence closes only the virtual-boot rows it explicitly tests; it does not close physical rows.
- A successful USB write does not prove firmware compatibility.
- A UEFI/GPT result does not imply UEFI/MBR, BIOS/MBR, or BIOS/GPT compatibility.
- Missing evidence keeps the row **unverified**.
- Secure Boot is a separate gate and must not be inferred from ordinary UEFI boot.

## Current state

The repository has automated contracts for the matrix, but no physical validation is claimed here. The next release-gate action is direct testing with the published Alpha ISO on representative hardware.
