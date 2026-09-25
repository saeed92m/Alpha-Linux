from alpha_core.models import ActionRequest, PermissionLevel
from alpha_core.policy import PolicyEngine


def test_model_output_cannot_authorize_admin_action():
    request = ActionRequest(
        action_id="system.update",
        actor="agent",
        description="update system",
        permission=PermissionLevel.RESTRICTED_ADMIN,
        parameters={},
    )
    result = PolicyEngine().decide(request, approved=False)
    assert result.allowed is False
    assert result.policy_id == "POL-APPROVAL-001"


def test_safe_action_can_be_authorized_by_policy():
    request = ActionRequest(
        action_id="system.inspect",
        actor="agent",
        description="inspect system",
        permission=PermissionLevel.READ,
        parameters={},
    )
    assert PolicyEngine().decide(request).allowed is True
