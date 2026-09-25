from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from .models import ActionRequest
from .system_service import ServiceResult


@dataclass(frozen=True)
class ServiceRegistration:
    service_id: str
    capability: str
    handler: Callable[[ActionRequest], Mapping[str, object]]


class ServiceRegistry:
    """Explicit service registry; registrations do not grant authorization."""

    def __init__(self) -> None:
        self._services: dict[str, ServiceRegistration] = {}

    def register(self, registration: ServiceRegistration) -> None:
        if not registration.service_id.strip() or not registration.capability.strip():
            raise ValueError("service identity and capability are required")
        if registration.service_id in self._services:
            raise ValueError(f"service already registered: {registration.service_id}")
        self._services[registration.service_id] = registration

    def resolve(self, service_id: str) -> ServiceRegistration:
        try:
            return self._services[service_id]
        except KeyError as exc:
            raise KeyError(f"unknown service: {service_id}") from exc

    def health(self) -> bool:
        return True

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._services))


@dataclass(frozen=True)
class DispatchResult:
    service_id: str
    result: ServiceResult


class ServiceDispatcher:
    def __init__(self, registry: ServiceRegistry, system_service) -> None:
        self._registry = registry
        self._system_service = system_service

    def dispatch(self, service_id: str, request: ActionRequest, *, approved: bool = False) -> DispatchResult:
        registration = self._registry.resolve(service_id)
        if registration.capability not in request.capabilities:
            raise PermissionError("service capability was not granted")
        result = self._system_service.execute(
            request, approved=approved, handler=registration.handler
        )
        return DispatchResult(service_id, result)
