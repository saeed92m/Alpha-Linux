from alpha_core.recovery import (
    BackupScope,
    RecoveryDisposition,
    RecoveryKind,
    RecoveryPlanner,
    RecoveryPolicy,
    RecoveryRequest,
)


def policy(policy_id="p1", retention_days=30, requires_verified_backup=True):
    return RecoveryPolicy(
        policy_id, RecoveryKind.RESTORE, BackupScope.STATE,
        retention_days, requires_verified_backup
    )


def request(request_id="r1", backup_verified=True, backup_age_days=1):
    return RecoveryRequest(
        request_id, RecoveryKind.RESTORE, BackupScope.STATE,
        backup_verified, backup_age_days
    )


def test_normalization_is_deterministic():
    result = RecoveryPlanner().normalize((policy("b"), policy("a")))
    assert tuple(item.policy_id for item in result) == ("a", "b")


def test_unverified_backup_is_denied():
    decision = RecoveryPlanner().evaluate((policy(),), request(backup_verified=False))
    assert decision.disposition == RecoveryDisposition.DENY
    assert decision.policy_id == "p1"


def test_expired_backup_is_denied():
    decision = RecoveryPlanner().evaluate((policy(retention_days=3),), request(backup_age_days=4))
    assert decision.disposition == RecoveryDisposition.DENY


def test_missing_policy_match_is_denied():
    value = RecoveryRequest("r1", RecoveryKind.ROLLBACK, BackupScope.STATE, True, 1)
    decision = RecoveryPlanner().evaluate((policy(),), value)
    assert decision.disposition == RecoveryDisposition.DENY
    assert decision.policy_id is None


def test_valid_recovery_is_allowed():
    decision = RecoveryPlanner().evaluate((policy(),), request())
    assert decision.disposition == RecoveryDisposition.ALLOW


def test_duplicate_policy_ids_are_rejected():
    try:
        RecoveryPlanner().normalize((policy("a"), policy("a")))
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
    plan = RecoveryPlanner().plan(
        (policy("b"), policy("a")), (request("r2"), request("r1"))
    )
    assert plan.policy_ids == ("a", "b")
    assert plan.denied_request_ids == ()


def test_plan_rejects_excess_policy_count():
    try:
        RecoveryPlanner().plan((policy("a"), policy("b")), (), max_policies=1)
    except ValueError as exc:
        assert str(exc) == "recovery plan exceeds policy limit"
    else:
        raise AssertionError("expected bound rejection")
