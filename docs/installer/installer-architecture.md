# Alpha Linux Installer Architecture

The installer is a release-critical system component.

## Supported installation intents

- Alpha-only installation
- Alpha alongside Windows
- second-disk installation
- manual partitioning
- encrypted installation
- advanced storage configurations where supported

## Safety requirements

The installer must inspect disk state before mutation and must never blindly modify an encrypted Windows installation.

For Windows dual boot, it must recognize UEFI/GPT, ESP, NTFS and BitLocker-related states and provide explicit warnings and recovery guidance.

## Architecture

```
Hardware Discovery
→ Boot/Storage Inspection
→ User Intent
→ Validation
→ Proposed Changes
→ Explicit Confirmation
→ Transactional Disk Changes
→ OS Installation
→ Boot Configuration
→ Post-install Health Check
→ Recovery Path
```

## Failure principle

Disk mutation must be designed as a recoverable transaction wherever technically feasible.

## Live environment

The Live environment must support hardware validation, network setup, diagnostics, recovery and installation from the same environment.
