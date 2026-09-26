from alpha_core.accessibility import (
    AccessibilityCapability,
    AccessibilityDisposition,
    AccessibilityPlanner,
    AccessibilityRequirement,
)


def capability(capability_id="c1", features=("keyboard", "screen-reader")):
    return AccessibilityCapability(capability_id, "interaction", features)


def requirement(requirement_id="r1", features=("keyboard",)):
    return AccessibilityRequirement(requirement_id, "interaction", features)


def test_normalization_is_deterministic():
    result = AccessibilityPlanner().normalize_capabilities((capability("b"), capability("a")))
    assert tuple(item.capability_id for item in result) == ("a", "b")


def test_requirement_passes():
    decision = AccessibilityPlanner().evaluate(requirement(), (capability(),))
    assert decision.disposition == AccessibilityDisposition.PASS
    assert decision.capability_id == "c1"


def test_missing_feature_fails():
    decision = AccessibilityPlanner().evaluate(requirement(features=("braille",)), (capability(),))
    assert decision.disposition == AccessibilityDisposition.FAIL


def test_category_mismatch_fails():
    value = AccessibilityCapability("c1", "visual", ("keyboard",))
    decision = AccessibilityPlanner().evaluate(requirement(), (value,))
    assert decision.disposition == AccessibilityDisposition.FAIL


def test_duplicate_capability_ids_rejected():
    try:
        AccessibilityPlanner().normalize_capabilities((capability("a"), capability("a")))
    except ValueError as exc:
        assert str(exc) == "capability IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_duplicate_requirement_ids_rejected():
    try:
        AccessibilityPlanner().normalize_requirements((requirement("a"), requirement("a")))
    except ValueError as exc:
        assert str(exc) == "requirement IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_plan_is_bounded_and_sorted():
    result = AccessibilityPlanner().plan((capability("b"), capability("a")), (requirement("r2"), requirement("r1")))
    assert result.capability_ids == ("a", "b")
    assert result.failed_requirement_ids == ()


def test_plan_rejects_excess_capabilities():
    try:
        AccessibilityPlanner().plan((capability("a"), capability("b")), (), max_capabilities=1)
    except ValueError as exc:
        assert str(exc) == "accessibility plan exceeds capability limit"
    else:
        raise AssertionError("expected bound rejection")
