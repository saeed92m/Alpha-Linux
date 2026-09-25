import pytest

from alpha_core.core import AlphaCore
from alpha_core.models import ActionRequest, PermissionLevel
from alpha_core.policy import PolicyEngine
from alpha_core.registry import ServiceDispatcher, ServiceRegistration, ServiceRegistry
from alpha_core.system_service import SystemService


def make_core():
    registry = ServiceRegistry()
    registry.register(ServiceRegistration("echo", "system.echo", lambda request: {"target": request.target}))
    service = SystemService(PolicyEngine())
    return AlphaCore(PolicyEngine(), ServiceDispatcher(registry, service))


def test_core_dispatch_requires_capability():
    core = make_core()
    request = ActionRequest("a1", "test", "echo", PermissionLevel.EXECUTE_SAFE, "system")
    with pytest.raises(PermissionError):
        core.execute("echo", request)


def test_core_dispatches_authorized_request():
    core = make_core()
    request = ActionRequest(
        "a1", "test", "echo", PermissionLevel.EXECUTE_SAFE, "system",
        required_capability="system.echo", capabilities=frozenset({"system.echo"}),
    )
    result = core.execute("echo", request)
    assert result.result.success
    assert result.service_id == "echo"


def test_duplicate_service_registration_is_rejected():
    registry = ServiceRegistry()
    registration = ServiceRegistration("echo", "system.echo", lambda request: {})
    registry.register(registration)
    with pytest.raises(ValueError):
        registry.register(registration)
