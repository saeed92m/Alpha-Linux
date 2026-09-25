# Alpha Linux ISO Build Architecture

## Target artifacts

- Live ISO
- Installer-capable ISO
- checksums
- signatures
- release metadata
- SBOM/provenance where applicable

## Build stages

```
Pinned Inputs
→ Root Filesystem Assembly
→ Alpha Integration
→ Package Validation
→ Boot Configuration
→ ISO Assembly
→ Boot/Install Tests
→ Security Checks
→ Reproducibility Check
→ Sign
→ Publish
```

## Validation

Every release candidate ISO must be tested for:

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

The exact implementation technology will be selected after architecture comparison and proof-of-concept evaluation.
