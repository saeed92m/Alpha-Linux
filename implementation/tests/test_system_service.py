import pytest

from alpha_core.models import ActionRequest, PermissionLevel
from alpha_core.policy import PolicyEngine
from alpha_core.system_service import SystemService


def req():
    return ActionRequest(
        action_id="system.safe",
        actor="agent",
        description="safe operation",
        permission=PermissionLevel.EXECUTE_SAFE,
        target="system",
        required_capability="system.safe",
        capabilities=frozenset({"system.safe"}),
    )


def test_service_executes_only_after_policy_allows():
    result = SystemService(PolicyEngine()).execute(
        req(), handler=lambda _: {"verified": True}
    )
    assert result.success
    assert result.evidence["verified"]


def test_service_rejects_unauthorized_request():
    denied = req()
    denied = ActionRequest(
        action_id=denied.action_id,
        actor=denied.actor,
        description=denied.description,
        permission=denied.permission,
        target=denied.target,
        required_capability=denied.required_capability,
        capabilities=frozenset(),
    )
    with pytest.raises(PermissionError):
        SystemService(PolicyEngine()).execute(denied, handler=lambda _: {})


def test_health_reports_authorization_boundary():
    assert SystemService(PolicyEngine()).health().healthy
