# Installer Safety POC

This module is a **non-destructive planning layer**, not a disk writer.

It converts a normalized storage observation plus an installation intent into a proposed change set with an explicit safety level.

## Safety boundary

The POC must never:
- open or mutate a real block device;
- repartition a host;
- remove a Windows partition implicitly;
- bypass BitLocker/recovery state;
- execute a proposed operation.

CI tests use synthetic storage observations only.

## Supported decisions

- Alpha-only: destructive operations are represented as a proposal and require explicit confirmation.
- Alongside Windows: requires detected NTFS + ESP and blocks BitLocker state.
- Second disk: requires explicit target confirmation.
- Manual partitioning: requires explicit confirmation.
- Unsupported or read-only storage: blocked.

The next implementation layer can bind these decisions to a disposable virtual disk fixture. A physical-disk adapter remains a separate, privileged integration boundary and is not part of this POC.
