# Recovery and Backup Contract

Phase 6 recovery/backup is a deterministic reference planning foundation. It models recovery intent, backup scope, verification, and retention without performing recovery or backup operations.

## Contracts

RecoveryPolicy defines recovery kind, backup scope, retention bound, and verification requirement. RecoveryRequest describes requested recovery state. RecoveryDecision explicitly returns allow/deny. RecoveryPlan provides bounded deterministic policy and denied-request identifiers.

## Determinism and validation

Policies normalize by policy_id; duplicate IDs are rejected. Requests evaluate in request_id order. Plans enforce a positive max_policies bound.

## Boundary

No filesystem, network, subprocess, credential, archive, encryption, upload, download, restore, deletion, or host mutation is performed.
