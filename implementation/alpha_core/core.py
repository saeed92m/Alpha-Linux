from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .models import ActionRequest, HealthResult
from .registry import DispatchResult, ServiceDispatcher


@dataclass(frozen=True)
class CoreHealth:
    healthy: bool
    components: Mapping[str, HealthResult]


class AlphaCore:
    """Orchestrates service dispatch; authorization remains owned by the policy boundary."""

    def __init__(self, dispatcher: ServiceDispatcher) -> None:
        self.dispatcher = dispatcher

    def execute(
        self,
        service_id: str,
        request: ActionRequest,
        *,
        approved: bool = False,
    ) -> DispatchResult:
        return self.dispatcher.dispatch(service_id, request, approved=approved)

    def health(self) -> CoreHealth:
        service = self.dispatcher.health()
        return CoreHealth(healthy=service.healthy, components={"system-service": service})
