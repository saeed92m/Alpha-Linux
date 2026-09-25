# Alpha Linux — Recovery Acceptance Matrix

**Status:** Phase 0 normative verification matrix

| Scenario | Detection | Recovery entry | Expected safe state | Evidence |
|---|---|---|---|---|
| Failed package transaction | Transaction error / health failure | Recovery/update rollback | Last validated package state | Automated fault test |
| Failed system update | Post-update health/boot failure | Previous system / snapshot restore | Bootable validated state | Integration + boot test |
| Bootloader failure | Boot failure | Boot Recovery | Bootable installed system or documented recovery state | VM/device test |
| Driver regression | Device/desktop health failure | Driver Recovery / previous system | Known-good driver state | Hardware validation |
| Broken package metadata | Package manager failure | Package Repair | Consistent package database | Package repair test |
| Filesystem/storage issue | SMART/filesystem diagnostics | System Repair / data recovery | Data preserved where possible | Storage fault test |
| Desktop failure | Session/startup failure | Safe Mode / emergency terminal | Diagnostic access without normal UI | Recovery test |
| Network unavailable | Connectivity failure | Network Recovery | Offline-capable recovery path | Recovery test |
| User-data corruption | Integrity/restore failure | User Data Recovery | Recoverable versioned data | Restore test |
| Full system corruption | System unrecoverable | Reinstall / migration path | Reinstallable system with preserved recoverable data | DR exercise |

## Safety invariants

1. Recovery must not silently destroy user data.
2. Recovery actions must identify the affected scope before mutation.
3. Encryption/authentication boundaries must remain enforced.
4. Recovery must remain usable when the normal desktop is unavailable.
5. A rollback is successful only after post-rollback health validation.
6. Recovery evidence must identify the tested artifact/version and environment.

## Traceability

Maps to AL-REQ-0011, AL-REQ-0012, AL-REC-0001 through AL-REC-0006, AL-SEC-0009 and AL-NFR-0003/0009.
