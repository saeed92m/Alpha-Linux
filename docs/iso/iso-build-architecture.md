# Alpha Linux ISO Build Architecture

## Target artifacts
- Live ISO
- Installer-capable ISO
- checksums
- signatures
- release metadata
- SBOM/provenance where applicable

## Build stages

Pinned Inputs → Root Filesystem Assembly → Alpha Integration → Package Validation → Boot Configuration → ISO Assembly → Automated Boot Smoke → Live/Install Tests → Security Checks → Reproducibility Check → Sign → Publish

## Current automated validation

The CI OS-image workflow now performs an automated QEMU boot-smoke test against the produced amd64 ISO. This is an executable pre-install boot check: it verifies that the generated image can start under QEMU long enough for a basic guest-liveness check and fails on detected fatal/kernel-panic signatures.

This test does **not** constitute physical hardware validation, a complete live-session test, installer validation, disk mutation validation, Windows dual-boot validation, or recovery validation.

## Release-candidate validation

Every release candidate ISO is intended to be tested for:
- UEFI boot;
- Live session;
- network;
- storage detection;
- graphics;
- audio;
- input;
- installation;
- dual boot where supported;
- recovery path;
- checksum/signature verification.

The exact implementation technology for full live/install validation will be selected after architecture comparison and proof-of-concept evaluation.

## Validation boundary

Automated CI evidence and physical/manual hardware evidence are tracked separately. A CI boot-smoke pass must not be promoted into a claim of physical installability.