from alpha_core.hardware_validation import (
    HardwareCapability,
    HardwareRequirement,
    HardwareValidationDisposition,
    HardwareValidationPlanner,
)


def capability(capability_id="c1", attrs=("gpu", "vulkan")):
    return HardwareCapability(capability_id, "graphics", attrs)


def requirement(requirement_id="r1", attrs=("gpu",)):
    return HardwareRequirement(requirement_id, "graphics", attrs)


def test_normalization_is_deterministic():
    result = HardwareValidationPlanner().normalize_capabilities((capability("b"), capability("a")))
    assert tuple(item.capability_id for item in result) == ("a", "b")


def test_requirement_passes():
    decision = HardwareValidationPlanner().evaluate(requirement(), (capability(),))
    assert decision.disposition == HardwareValidationDisposition.PASS
    assert decision.capability_id == "c1"


def test_missing_attribute_fails():
    decision = HardwareValidationPlanner().evaluate(requirement(attrs=("npu",)), (capability(),))
    assert decision.disposition == HardwareValidationDisposition.FAIL


def test_device_class_mismatch_fails():
    value = HardwareCapability("c1", "audio", ("gpu",))
    decision = HardwareValidationPlanner().evaluate(requirement(), (value,))
    assert decision.disposition == HardwareValidationDisposition.FAIL


def test_duplicate_capability_ids_rejected():
    try:
        HardwareValidationPlanner().normalize_capabilities((capability("a"), capability("a")))
    except ValueError as exc:
        assert str(exc) == "capability IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_duplicate_requirement_ids_rejected():
    try:
        HardwareValidationPlanner().normalize_requirements((requirement("a"), requirement("a")))
    except ValueError as exc:
        assert str(exc) == "requirement IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_plan_is_bounded_and_sorted():
    result = HardwareValidationPlanner().plan((capability("b"), capability("a")), (requirement("r2"), requirement("r1")))
    assert result.capability_ids == ("a", "b")
    assert result.failed_requirement_ids == ()


def test_plan_rejects_excess_capabilities():
    try:
        HardwareValidationPlanner().plan((capability("a"), capability("b")), (), max_capabilities=1)
    except ValueError as exc:
        assert str(exc) == "hardware validation plan exceeds capability limit"
    else:
        raise AssertionError("expected bound rejection")
