from alpha_core.models import ActionRequest, PermissionLevel
from alpha_core.service import AlphaService


def test_service_never_executes_denied_action():
    called = False

    def handler():
        nonlocal called
        called = True

    request = ActionRequest(
        action_id="system.update",
        actor="agent",
        description="update",
        permission=PermissionLevel.RESTRICTED_ADMIN,
        target="system",
        capabilities=frozenset({"system.admin"}),
    )
    result = AlphaService().execute(request, handler)
    assert not result.executed
    assert not called


def test_service_verifies_successful_action():
    request = ActionRequest(
        action_id="system.inspect",
        actor="agent",
        description="inspect",
        permission=PermissionLevel.READ,
        target="system",
    )
    result = AlphaService().execute(
        request,
        lambda: {"status": "ok"},
        verifier=lambda value: value["status"] == "ok",
    )
    assert result.executed
    assert result.verified
