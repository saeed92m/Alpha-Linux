from alpha_core.hidpi import (
    DisplayScaleDescriptor,
    HiDPIPlanner,
    HiDPIPolicy,
    HiDPISnapshot,
)


def test_normalize_is_deterministic() -> None:
    planner = HiDPIPlanner()
    snapshot = planner.normalize(
        (
            DisplayScaleDescriptor("display-b", 1.5),
            DisplayScaleDescriptor("display-a", 2.0),
        )
    )
    assert tuple(display.display_id for display in snapshot.displays) == (
        "display-a",
        "display-b",
    )


def test_policy_accepts_available_displays() -> None:
    planner = HiDPIPlanner()
    snapshot = HiDPISnapshot((DisplayScaleDescriptor("display-a", 2.0),))
    policy = HiDPIPolicy(default_scale=2.0, display_ids=("display-a",))
    assert planner.validate_policy(policy, snapshot) == policy


def test_unknown_display_is_rejected() -> None:
    planner = HiDPIPlanner()
    snapshot = HiDPISnapshot((DisplayScaleDescriptor("display-a", 2.0),))
    policy = HiDPIPolicy(display_ids=("display-b",))
    try:
        planner.validate_policy(policy, snapshot)
    except ValueError as exc:
        assert str(exc) == "policy references unavailable display"
    else:
        raise AssertionError("expected unavailable display rejection")


def test_duplicate_display_ids_are_rejected() -> None:
    try:
        HiDPISnapshot(
            (
                DisplayScaleDescriptor("display-a", 2.0),
                DisplayScaleDescriptor("display-a", 1.5),
            )
        )
    except ValueError as exc:
        assert str(exc) == "display identifiers must be unique"
    else:
        raise AssertionError("expected duplicate display rejection")


def test_unsupported_scale_is_rejected() -> None:
    try:
        DisplayScaleDescriptor("display-a", 1.33)
    except ValueError as exc:
        assert str(exc) == "scale_factor must use a supported deterministic value"
    else:
        raise AssertionError("expected unsupported scale rejection")


def test_scales_for_displays_are_deterministic() -> None:
    planner = HiDPIPlanner()
    snapshot = HiDPISnapshot(
        (
            DisplayScaleDescriptor("display-a", 2.0),
            DisplayScaleDescriptor("display-b", 1.5),
        )
    )
    result = planner.scales_for_displays(("display-b", "display-a"), snapshot)
    assert tuple(display.display_id for display in result) == (
        "display-a",
        "display-b",
    )
