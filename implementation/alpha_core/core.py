from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .models import ActionRequest, HealthResult
from .policy import PolicyEngine
from .registry import ServiceDispatcher


@dataclass(frozen=True)
class CoreHealth:
    healthy: bool
    components: Mapping[str, HealthResult]


class AlphaCore:
    """Orchestrates policy-authorized service dispatch without owning OS privilege."""

    def __init__(self, policy: PolicyEngine, dispatcher: ServiceDispatcher) -> None:
        self.policy = policy
        self.dispatcher = dispatcher

    def execute(self, service_id: str, request: ActionRequest, *, approved: bool = False):
        return self.dispatcher.dispatch(service_id, request, approved=approved)

    def health(self) -> CoreHealth:
        service = self.dispatcher.health()
        return CoreHealth(healthy=service.healthy, components={"system-service": service})
