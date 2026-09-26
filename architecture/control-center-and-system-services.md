# Control Center and System Services Architecture

## Layering

Alpha Core
  |
Control Center
  +-- System Observatory
  +-- Hardware Discovery
  +-- Configuration Store
  +-- Update Planner / Update Engine
  |
Policy / System Service
  |
OS-backed privileged adapters (future)

## Boundary rules

1. Control Center aggregates state and plans; it is not an authorization authority.
2. System Observatory remains read-only.
3. Hardware Discovery remains read-only.
4. Configuration Store is state, not a secret store or policy engine.
5. Update Planner creates deterministic plans.
6. Update Engine owns transaction sequencing and verification, not privilege.
7. Privileged package/driver/firmware operations require the existing policy and System Service boundary plus OS authorization.
8. Recovery must be able to operate independently of the normal Control Center UI.

## Current implementation status

The reference implementation is host-safe: update application is a no-op backend and hardware discovery reads standard Linux pseudo-filesystems only.

## Software Center boundary

Software Center sits beside the Control Center as a read/plan service. It may expose catalog state and deterministic install/remove plans, but it does not authorize or execute privileged package operations. Future package-manager adapters must cross the existing Policy / System Service boundary and provide verification and recovery evidence.
