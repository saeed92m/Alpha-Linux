# Alpha Linux Boot, Live and Installer Requirements

## Scope

This requirement set makes boot compatibility, Live USB usability and installer UX explicit release-scoped requirements.

### BOOT-001 — UEFI
Alpha Linux shall provide a UEFI boot path in the release ISO.

### BOOT-002 — Legacy BIOS
Alpha Linux shall provide a Legacy BIOS boot path where supported by the selected base-image/tooling stack.

### BOOT-003 — Single ISO
The preferred product model is one ISO containing both supported firmware boot paths rather than separate UEFI and BIOS downloads.

### BOOT-004 — USB writer compatibility
The ISO shall support common USB creation workflows, including Rufus, subject to the validated firmware/media matrix.

### BOOT-005 — GPT and MBR
The installer shall support GPT targets for UEFI installations and MBR targets for Legacy BIOS installations. Additional firmware/layout combinations may be supported when validated.

### LIVE-001 — Live boot
The release USB shall provide a usable Live environment without requiring installation to internal storage.

### LIVE-002 — Graphical experience
The Live environment shall provide a polished graphical Alpha-branded experience based on the selected COSMIC desktop integration.

### LIVE-003 — Diagnostics
The Live environment shall expose hardware, display, network and storage diagnostics appropriate to the supported release.

### LIVE-004 — Installer entry
The Live environment shall provide a graphical entry point to the installer.

### LIVE-005 — Recovery
The Live environment shall expose recovery/diagnostic capabilities appropriate to the release.

### INST-001 — Storage discovery
The installer shall inspect firmware mode and storage state before proposing changes.

### INST-002 — Explicit confirmation
Destructive or potentially destructive storage changes shall require explicit confirmation.

### INST-003 — Transaction boundary
Disk mutation shall occur through a transaction layer separate from UI concerns.

### INST-004 — Rollback
Installer failures shall have a defined rollback/recovery path, validated first on disposable media.

### INST-005 — Windows safety
The installer shall detect Windows/NTFS/ESP and BitLocker-related states and shall not silently bypass protection.

### INST-006 — Post-install verification
Installation shall verify filesystem, boot configuration and essential system health before reporting success.

## Evidence rule

These requirements are not claims of completion. Each requires implementation plus appropriate automated, virtualized or physical evidence before being marked complete.
