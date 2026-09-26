# Recovery and Backup Traceability

| Requirement | Implementation | Test | Specification |
| --- | --- | --- | --- |
| Recovery/backup contracts | implementation/alpha_core/recovery.py | implementation/tests/test_recovery.py | specs/recovery-backup-contract.md |
| Deterministic normalization | RecoveryPlanner.normalize | test_normalization_is_deterministic | Determinism and validation |
| Verification/retention denial | RecoveryPlanner.evaluate | test_unverified_backup_is_denied; test_expired_backup_is_denied | Contracts |
| Bounded planning | RecoveryPlanner.plan | test_plan_is_bounded_and_sorted; test_plan_rejects_excess_policy_count | Determinism and validation |
| Reference-only boundary | RecoveryPlanner | full test module | Boundary |
