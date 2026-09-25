# Alpha Linux — System Observatory

**Status:** Phase 2 reference implementation

The System Observatory is a read-only aggregation surface for system state and health evidence. It does not execute remediation, authorize actions, or expose secrets.

## Contract
- collect system discovery evidence;
- aggregate component health;
- expose immutable snapshots to Control Center and AI consumers;
- preserve the distinction between observed state and inferred diagnosis;
- never treat telemetry as authorization.

The current implementation is intentionally host-safe and non-privileged.
