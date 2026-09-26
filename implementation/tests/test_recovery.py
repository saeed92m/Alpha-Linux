from alpha_core.recovery import (
    BackupScope,
    RecoveryBackupDisposition,
    RecoveryBackupPlanner,
    RecoveryBackupPolicy,
    RecoveryBackupRequest,
    RecoveryPlanner,
    RecoveryState,
)


def policy(policy_id="p1", retention_days=30, requires_verified_backup=True):
    return RecoveryBackupPolicy(
        policy_id, RecoveryState.RESTORE, BackupScope.STATE,
        retention_days, requires_verified_backup
    )


def request(request_id="r1", backup_verified=True, backup_age_days=1):
    return RecoveryBackupRequest(
        request_id, RecoveryState.RESTORE, BackupScope.STATE,
        backup_verified, backup_age_days
    )


def test_existing_recovery_contract_remains_available():
    checkpoint = RecoveryPlanner().checkpoint("system")
    plan = RecoveryPlanner().plan(checkpoint)
    assert plan.checkpoint_id == checkpoint.checkpoint_id


def test_backup_normalization_is_deterministic():
    result = RecoveryBackupPlanner().normalize((policy("b"), policy("a")))
    assert tuple(item.policy_id for item in result) == ("a", "b")


def test_unverified_backup_is_denied():
    decision = RecoveryBackupPlanner().evaluate((policy(),), request(backup_verified=False))
    assert decision.disposition == RecoveryBackupDisposition.DENY
    assert decision.policy_id == "p1"


def test_expired_backup_is_denied():
    decision = RecoveryBackupPlanner().evaluate(
        (policy(retention_days=3),), request(backup_age_days=4)
    )
    assert decision.disposition == RecoveryBackupDisposition.DENY


def test_missing_policy_match_is_denied():
    value = RecoveryBackupRequest(
        "r1", RecoveryState.FAIL, BackupScope.STATE, True, 1
    )
    decision = RecoveryBackupPlanner().evaluate((policy(),), value)
    assert decision.disposition == RecoveryBackupDisposition.DENY
    assert decision.policy_id is None


def test_valid_recovery_is_allowed():
    decision = RecoveryBackupPlanner().evaluate((policy(),), request())
    assert decision.disposition == RecoveryBackupDisposition.ALLOW


def test_duplicate_policy_ids_are_rejected():
    try:
        RecoveryBackupPlanner().normalize((policy("a"), policy("a")))
    except ValueError as exc:
        assert str(exc) == "policy IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_negative_retention_is_rejected():
    try:
        policy(retention_days=-1)
    except ValueError as exc:
        assert str(exc) == "retention_days must be non-negative"
    else:
        raise AssertionError("expected retention rejection")


def test_plan_is_bounded_and_sorted():
    result = RecoveryBackupPlanner().plan(
        (policy("b"), policy("a")), (request("r2"), request("r1"))
    )
    assert result.policy_ids == ("a", "b")
    assert result.denied_request_ids == ()


def test_plan_rejects_excess_policy_count():
    try:
        RecoveryBackupPlanner().plan((policy("a"), policy("b")), (), max_policies=1)
    except ValueError as exc:
        assert str(exc) == "recovery plan exceeds policy limit"
    else:
        raise AssertionError("expected bound rejection")
