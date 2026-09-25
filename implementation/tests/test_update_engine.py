from alpha_core.system_integration import UpdatePlanner
from alpha_core.update_engine import ReferenceUpdateBackend, UpdateEngine, UpdateState


def test_update_engine_keeps_healthy_plan():
    plan = UpdatePlanner().plan(("install:example",))
    result = UpdateEngine(ReferenceUpdateBackend()).execute(plan)
    assert result.state is UpdateState.KEEP
    assert result.history == (
        UpdateState.CHECK,
        UpdateState.RESOLVE,
        UpdateState.SNAPSHOT,
        UpdateState.APPLY,
        UpdateState.HEALTH_CHECK,
        UpdateState.KEEP,
    )
    assert result.dry_run


def test_update_engine_rolls_back_when_health_check_fails():
    plan = UpdatePlanner().plan(("upgrade:example",))
    result = UpdateEngine(ReferenceUpdateBackend(health_ok=False)).execute(plan)
    assert result.state is UpdateState.ROLLBACK
    assert result.history[-2:] == (UpdateState.HEALTH_CHECK, UpdateState.ROLLBACK)
    assert "rollback" in result.evidence


def test_update_plan_identity_is_stable_for_same_actions():
    planner = UpdatePlanner()
    first = planner.plan(("install:example", "remove:old"))
    second = planner.plan(("install:example", "remove:old"))
    assert first.plan_id == second.plan_id
