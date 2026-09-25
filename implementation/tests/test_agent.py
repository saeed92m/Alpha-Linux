import pytest

from alpha_core.agent import AgentRuntime
from alpha_core.models import ActionRequest, PermissionLevel


def test_denied_action_cannot_enter_execution():
    request = ActionRequest(
        action_id="system.update",
        actor="agent",
        description="update",
        permission=PermissionLevel.RESTRICTED_ADMIN,
        target="system",
        required_capability="system.admin",
        capabilities=frozenset({"system.admin"}),
    )
    with pytest.raises(PermissionError):
        AgentRuntime().authorize(
            request,
            type("Decision", (), {"allowed": False, "reason": "approval required"})(),
        )


def test_read_action_does_not_require_verification():
    request = ActionRequest(
        action_id="system.inspect",
        actor="agent",
        description="inspect",
        permission=PermissionLevel.READ,
        target="system",
    )
    assert not AgentRuntime().requires_verification(request)
