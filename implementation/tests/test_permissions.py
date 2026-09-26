from alpha_core.permissions import (
    PermissionEffect,
    PermissionPlanner,
    PermissionRequest,
    PermissionRule,
)


def rules() -> tuple[PermissionRule, ...]:
    return (
        PermissionRule("rule-b", "network.read", PermissionEffect.DENY),
        PermissionRule("rule-a", "filesystem.read", PermissionEffect.ALLOW),
    )


def test_rule_normalization_is_deterministic() -> None:
    normalized = PermissionPlanner().normalize(rules())
    assert [rule.rule_id for rule in normalized] == ["rule-a", "rule-b"]


def test_explicit_allow_is_returned() -> None:
    decision = PermissionPlanner().evaluate(
        rules(), PermissionRequest("filesystem.read")
    )
    assert decision.effect is PermissionEffect.ALLOW
    assert decision.rule_id == "rule-a"


def test_explicit_deny_is_returned() -> None:
    decision = PermissionPlanner().evaluate(
        rules(), PermissionRequest("network.read")
    )
    assert decision.effect is PermissionEffect.DENY
    assert decision.rule_id == "rule-b"


def test_unknown_capability_is_default_denied() -> None:
    decision = PermissionPlanner().evaluate(
        rules(), PermissionRequest("host.shutdown")
    )
    assert decision.effect is PermissionEffect.DENY
    assert decision.rule_id is None


def test_duplicate_rule_ids_are_rejected() -> None:
    duplicate = (
        PermissionRule("same", "a", PermissionEffect.ALLOW),
        PermissionRule("same", "b", PermissionEffect.DENY),
    )
    try:
        PermissionPlanner().evaluate(duplicate, PermissionRequest("a"))
    except ValueError as exc:
        assert str(exc) == "rule IDs must be unique"
    else:
        raise AssertionError("expected rejection")


def test_invalid_request_is_rejected() -> None:
    try:
        PermissionRequest(" ")
    except ValueError as exc:
        assert str(exc) == "capability is required"
    else:
        raise AssertionError("expected rejection")
