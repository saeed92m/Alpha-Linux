# Recovery and Backup Contract

## Scope

Phase 6 recovery and backup is a deterministic reference-planning foundation. It models recovery intent, backup scope, verification, and retention without performing recovery or backup operations.

## Contracts

- RecoveryPolicy defines recovery kind, backup scope, retention bound, and verification requirement.
- RecoveryRequest describes a requested recovery and the age/verification state of its backup.
- RecoveryDecision explicitly returns allow/deny and the matched policy when present.
- RecoveryPlan provides bounded, deterministic policy IDs and denied request IDs.

## Determinism

Policies normalize by policy_id; duplicate IDs are rejected. Requests are evaluated by request_id order. Plans enforce a positive max_policies bound.

## Boundary

No filesystem or network access, subprocess execution, credential handling, archive/encryption operation, upload/download, restore/delete operation, or host mutation is performed.
