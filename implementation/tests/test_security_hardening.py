from alpha_core.security_hardening import (
    SecurityAuditEvent,
    SecurityClassification,
    SecurityControl,
    SecurityControlKind,
    SecurityDisposition,
    SecurityHardeningPlanner,
)


def control(control_id: str, action: str) -> SecurityControl:
    return SecurityControl(
        control_id,
        SecurityControlKind.AUTHORIZATION,
        SecurityClassification.INTERNAL,
        (action,),
    )


def test_controls_are_normalized_deterministically() -> None:
    planner = SecurityHardeningPlanner()
    result = planner.normalize_controls((control("b", "write"), control("a", "read")))
    assert tuple(item.control_id for item in result) == ("a", "b")


def test_plan_selects_first_compatible_control_and_denies_unknown_actions() -> None:
    plan = SecurityHardeningPlanner().plan(
        ("write", "unknown", "write"),
        (control("z", "write"), control("a", "write")),
    )
    assert plan.controls == ("a",)
    assert plan.events == ("deny:unknown",)


def test_duplicate_control_ids_are_rejected() -> None:
    planner = SecurityHardeningPlanner()
    try:
        planner.normalize_controls((control("a", "read"), control("a", "write")))
    except ValueError as exc:
        assert str(exc) == "control IDs must be unique"
    else:
        raise AssertionError("expected duplicate control rejection")


def test_duplicate_event_ids_are_rejected() -> None:
    planner = SecurityHardeningPlanner()
    event = SecurityAuditEvent(
        "e1", "read", SecurityClassification.INTERNAL, SecurityDisposition.ALLOW
    )
    try:
        planner.normalize_events((event, event))
    except ValueError as exc:
        assert str(exc) == "event IDs must be unique"
    else:
        raise AssertionError("expected duplicate event rejection")


def test_control_rejects_empty_actions() -> None:
    try:
        SecurityControl(
            "c1",
            SecurityControlKind.INTEGRITY,
            SecurityClassification.SENSITIVE,
            (),
        )
    except ValueError as exc:
        assert str(exc) == "actions must be non-empty"
    else:
        raise AssertionError("expected empty action rejection")


def test_invalid_control_bound_is_rejected() -> None:
    try:
        SecurityHardeningPlanner().plan((), (), max_controls=0)
    except ValueError as exc:
        assert str(exc) == "max_controls must be positive"
    else:
        raise AssertionError("expected bound rejection")


def test_audit_event_requires_nonempty_action() -> None:
    try:
        SecurityAuditEvent(
            "e1", "", SecurityClassification.PUBLIC, SecurityDisposition.DENY
        )
    except ValueError as exc:
        assert str(exc) == "action is required"
    else:
        raise AssertionError("expected action rejection")
