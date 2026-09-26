import pytest

from alpha_core.recovery import RecoveryEngine, RecoveryPlanner, RecoveryState, ReferenceRecoveryBackend


def test_recovery_engine_keeps_verified_plan():
    planner = RecoveryPlanner()
    checkpoint = planner.checkpoint("phase-2-baseline")
    plan = planner.plan(checkpoint)

    result = RecoveryEngine(ReferenceRecoveryBackend()).execute(checkpoint, plan)

    assert result.state is RecoveryState.KEEP
    assert result.history == (
        RecoveryState.CHECKPOINT,
        RecoveryState.PREPARE,
        RecoveryState.RESTORE,
        RecoveryState.VERIFY,
        RecoveryState.KEEP,
    )
    assert result.dry_run
    assert result.evidence["restore"]["restored"] is False


def test_recovery_engine_fails_when_verification_fails():
    planner = RecoveryPlanner()
    checkpoint = planner.checkpoint("phase-2-baseline")
    plan = planner.plan(checkpoint)

    result = RecoveryEngine(
        ReferenceRecoveryBackend(verification_ok=False)
    ).execute(checkpoint, plan)

    assert result.state is RecoveryState.FAIL
    assert result.history[-2:] == (RecoveryState.VERIFY, RecoveryState.FAIL)


def test_checkpoint_identity_is_stable():
    planner = RecoveryPlanner()
    assert planner.checkpoint("same").checkpoint_id == planner.checkpoint("same").checkpoint_id


def test_plan_rejects_mismatched_checkpoint():
    planner = RecoveryPlanner()
    first = planner.checkpoint("first")
    second = planner.checkpoint("second")

    with pytest.raises(ValueError):
        RecoveryEngine(ReferenceRecoveryBackend()).execute(
            first, planner.plan(second)
        )
