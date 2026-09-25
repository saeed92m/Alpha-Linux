from .core import AlphaCore
from .models import ActionRequest, PermissionLevel
from .policy import PolicyEngine
from .registry import ServiceDispatcher, ServiceRegistry
from .system_service import SystemService


def build_core() -> AlphaCore:
    registry = ServiceRegistry()
    service = SystemService(PolicyEngine())
    return AlphaCore(ServiceDispatcher(registry, service))


def main() -> int:
    core = build_core()
    health = core.health()
    print("alpha-core: " + ("healthy" if health.healthy else "unhealthy"))
    return 0 if health.healthy else 1
