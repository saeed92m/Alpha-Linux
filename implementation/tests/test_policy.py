from alpha_core.models import ActionRequest, PermissionLevel, RiskLevel
from alpha_core.policy import PolicyEngine


def request(**kwargs):
    values = dict(
        action_id="system.update",
        actor="agent",
        description="update",
        permission=PermissionLevel.EXECUTE_SAFE,
        target="system",
        required_capability="system.update",
        capabilities=frozenset({"system.update"}),
    )
    values.update(kwargs)
    return ActionRequest(**values)


def test_safe_action_requires_capability():
    decision = PolicyEngine().decide(request())
    assert decision.allowed


def test_missing_capability_is_denied():
    decision = PolicyEngine().decide(request(capabilities=frozenset()))
    assert not decision.allowed
    assert decision.policy_id == "POL-CAPABILITY-002"


def test_admin_requires_explicit_approval():
    decision = PolicyEngine().decide(
        request(permission=PermissionLevel.RESTRICTED_ADMIN, approved=False)
    )
    assert not decision.allowed
    assert decision.requires_approval


def test_high_risk_requires_approval():
    decision = PolicyEngine().decide(request(risk=RiskLevel.HIGH))
    assert not decision.allowed
    assert decision.requires_approval
