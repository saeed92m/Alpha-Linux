# Custom Linux Distribution Engineering References

**Status:** Curated Alpha Linux engineering reference
**Updated:** 2026-10-05

## Purpose

This document records external projects and techniques that are useful to Alpha Linux without making them dependencies of the product.

## Reference: penguins-eggs

Project: https://github.com/infowanderer/penguins-eggs

Useful patterns observed:

- remaster an existing Debian/Ubuntu-family installation into a bootable Live ISO;
- hybrid BIOS/UEFI bootable media;
- selectable compression strategies;
- USB/VM-oriented Live image generation;
- installer integration through Calamares;
- backup/clone/recovery-oriented image workflows;
- separation between the base distribution and the customization layer.

Alpha decision:

- **Use as a reference, not as the Alpha build engine.**
- Keep Alpha's current Ubuntu base + COSMIC + Alpha customization architecture.
- Keep Alpha's own deterministic build inputs, provenance manifest, SHA-256 evidence, reproducibility gate, QEMU validation and release transport contract.
- Revisit selected ideas later for installer UX, offline recovery and optional remaster/backup workflows.

## General rules extracted for Alpha

1. A custom distribution does not need to fork its base distribution. A controlled product layer on top of Ubuntu/Debian is a valid architecture.
2. The Live image, installer, package repository and recovery system should be treated as related but separately testable subsystems.
3. BIOS/UEFI compatibility must be validated from the produced image, not inferred from the build command.
4. Compression and image size are release-engineering concerns because they affect CI transport, USB creation and download reliability.
5. Product identity must be coherent across OS metadata, boot menus, Live filesystem, installer UI and desktop session.
6. Release publication must consume the exact validated artifact; it must not silently rebuild a different image.
7. External projects provide engineering patterns only. Alpha adopts a pattern only after checking reproducibility, security, licensing, maintenance, and compatibility with Alpha's contracts.

## Current Alpha-specific lesson

The A4 runtime failure demonstrated a concrete identity-boundary bug: the Live filesystem used UID 1000 user alpha, while the generated greetd configuration attempted to start the graphical session as ubuntu. The COSMIC packages and boot stack were valid, but greetd repeatedly failed PAM account lookup.

Therefore:

- define one canonical Live session user;
- use that identity consistently in greetd, session validation and runtime evidence;
- avoid inherited Ubuntu username assumptions after product branding changes;
- make the CI gate fail closed if the configured session user does not exist.

This reference is intentionally implementation-neutral; the Alpha repository's specification and CI evidence remain authoritative.