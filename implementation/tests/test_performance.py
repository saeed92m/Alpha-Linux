from alpha_core.performance import (
    PerformanceDisposition,
    PerformancePlanner,
    PerformanceRequirement,
    PerformanceTarget,
)


def target(target_id="t1", latency=10, throughput=100, budget=50):
    return PerformanceTarget(target_id, "build", latency, throughput, budget)


def requirement(requirement_id="r1", latency=20, throughput=80, budget=60):
    return PerformanceRequirement(requirement_id, "build", latency, throughput, budget)


def test_normalization_is_deterministic():
    result = PerformancePlanner().normalize_targets((target("b"), target("a")))
    assert tuple(item.target_id for item in result) == ("a", "b")


def test_target_meets_requirement():
    decision = PerformancePlanner().evaluate(requirement(), (target(),))
    assert decision.disposition == PerformanceDisposition.MEETS_TARGET
    assert decision.target_id == "t1"


def test_latency_miss():
    decision = PerformancePlanner().evaluate(requirement(latency=5), (target(),))
    assert decision.disposition == PerformanceDisposition.MISSES_TARGET


def test_throughput_miss():
    decision = PerformancePlanner().evaluate(requirement(throughput=101), (target(),))
    assert decision.disposition == PerformanceDisposition.MISSES_TARGET


def test_resource_budget_miss():
    decision = PerformancePlanner().evaluate(requirement(budget=40), (target(),))
    assert decision.disposition == PerformanceDisposition.MISSES_TARGET


def test_workload_mismatch():
    value = PerformanceRequirement("r1", "test", 20, 80, 60)
    decision = PerformancePlanner().evaluate(value, (target(),))
    assert decision.disposition == PerformanceDisposition.MISSES_TARGET


def test_duplicate_target_ids_rejected():
    try:
        PerformancePlanner().normalize_targets((target("a"), target("a")))
    except ValueError as exc:
        assert str(exc) == "target IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_plan_is_bounded_and_sorted():
    result = PerformancePlanner().plan((target("b"), target("a")), (requirement("r2"), requirement("r1")))
    assert result.target_ids == ("a", "b")
    assert result.missed_requirement_ids == ()


def test_plan_rejects_excess_targets():
    try:
        PerformancePlanner().plan((target("a"), target("b")), (), max_targets=1)
    except ValueError as exc:
        assert str(exc) == "performance plan exceeds target limit"
    else:
        raise AssertionError("expected bound rejection")
