from alpha_core.compatibility import (
    CompatibilityDisposition,
    CompatibilityPlanner,
    CompatibilityRequirement,
    CompatibilityTarget,
)


def target(target_id="t1", version="26.04", capabilities=("touch", "gpu")):
    return CompatibilityTarget(target_id, "ubuntu", version, capabilities)


def requirement(requirement_id="r1", minimum_version="24.04", capabilities=("touch",)):
    return CompatibilityRequirement(requirement_id, "ubuntu", minimum_version, capabilities)


def test_normalization_is_deterministic():
    result = CompatibilityPlanner().normalize_targets((target("b"), target("a")))
    assert tuple(item.target_id for item in result) == ("a", "b")


def test_valid_target_is_compatible():
    decision = CompatibilityPlanner().evaluate(requirement(), (target(),))
    assert decision.disposition == CompatibilityDisposition.COMPATIBLE
    assert decision.target_id == "t1"


def test_platform_mismatch_is_incompatible():
    value = requirement()
    target_value = CompatibilityTarget("t1", "debian", "26.04", ("touch",))
    decision = CompatibilityPlanner().evaluate(value, (target_value,))
    assert decision.disposition == CompatibilityDisposition.INCOMPATIBLE
    assert decision.target_id is None


def test_version_mismatch_is_incompatible():
    decision = CompatibilityPlanner().evaluate(requirement(minimum_version="26.10"), (target(),))
    assert decision.disposition == CompatibilityDisposition.INCOMPATIBLE


def test_missing_capability_is_incompatible():
    decision = CompatibilityPlanner().evaluate(requirement(capabilities=("npu",)), (target(),))
    assert decision.disposition == CompatibilityDisposition.INCOMPATIBLE


def test_duplicate_target_ids_are_rejected():
    try:
        CompatibilityPlanner().normalize_targets((target("a"), target("a")))
    except ValueError as exc:
        assert str(exc) == "target IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_duplicate_requirement_ids_are_rejected():
    try:
        CompatibilityPlanner().normalize_requirements((requirement("a"), requirement("a")))
    except ValueError as exc:
        assert str(exc) == "requirement IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_plan_is_bounded_and_sorted():
    result = CompatibilityPlanner().plan(
        (target("b"), target("a")), (requirement("r2"), requirement("r1"))
    )
    assert result.target_ids == ("a", "b")
    assert result.incompatible_requirement_ids == ()


def test_plan_rejects_excess_targets():
    try:
        CompatibilityPlanner().plan((target("a"), target("b")), (), max_targets=1)
    except ValueError as exc:
        assert str(exc) == "compatibility plan exceeds target limit"
    else:
        raise AssertionError("expected bound rejection")
