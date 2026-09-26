from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EnvironmentKind(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    LAB = "lab"


class ServiceKind(str, Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    DATABASE = "database"
    NETWORK = "network"


class DeploymentRole(str, Enum):
    SOURCE = "source"
    PROCESS = "process"
    OUTPUT = "output"


class CloudCapabilityKind(str, Enum):
    PROVISIONING = "provisioning"
    OBSERVABILITY = "observability"
    SECURITY = "security"
    DELIVERY = "delivery"


@dataclass(frozen=True)
class CloudService:
    service_id: str
    kind: ServiceKind
    environment_kinds: tuple[EnvironmentKind, ...]
    capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.service_id.strip():
            raise ValueError("service_id is required")
        if not self.environment_kinds:
            raise ValueError("environment_kinds must be non-empty")
        if len(set(self.environment_kinds)) != len(self.environment_kinds):
            raise ValueError("environment_kinds must be unique")
        if not self.capabilities:
            raise ValueError("capabilities must be non-empty")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")
        if any(not item.strip() for item in self.capabilities):
            raise ValueError("capabilities must be non-empty")


@dataclass(frozen=True)
class CloudEnvironment:
    environment_id: str
    name: str
    environment_kinds: tuple[EnvironmentKind, ...]
    services: tuple[CloudService, ...] = ()

    def __post_init__(self) -> None:
        if not self.environment_id.strip():
            raise ValueError("environment_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.environment_kinds:
            raise ValueError("environment_kinds must be non-empty")
        if len(set(self.environment_kinds)) != len(self.environment_kinds):
            raise ValueError("environment_kinds must be unique")
        service_ids = [service.service_id for service in self.services]
        if len(set(service_ids)) != len(service_ids):
            raise ValueError("service IDs must be unique")
        scope = set(self.environment_kinds)
        if any(
            not scope.intersection(service.environment_kinds)
            for service in self.services
        ):
            raise ValueError("service environment kind is outside environment scope")


@dataclass(frozen=True)
class CloudRequirement:
    requirement_id: str
    capability_kind: CloudCapabilityKind
    environment_kind: EnvironmentKind
    required_capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.required_capabilities:
            raise ValueError("required_capabilities must be non-empty")
        if len(set(self.required_capabilities)) != len(self.required_capabilities):
            raise ValueError("required_capabilities must be unique")
        if any(not item.strip() for item in self.required_capabilities):
            raise ValueError("required_capabilities must be non-empty")


@dataclass(frozen=True)
class CloudPlan:
    environment_id: str
    service_ids: tuple[str, ...]
    requirement_ids: tuple[str, ...]


class CloudDevOpsPlanner:
    def normalize_services(
        self, services: tuple[CloudService, ...]
    ) -> tuple[CloudService, ...]:
        ids = [service.service_id for service in services]
        if len(set(ids)) != len(ids):
            raise ValueError("service IDs must be unique")
        return tuple(sorted(services, key=lambda item: item.service_id))

    def normalize_requirements(
        self, requirements: tuple[CloudRequirement, ...]
    ) -> tuple[CloudRequirement, ...]:
        ids = [requirement.requirement_id for requirement in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def plan(
        self,
        environment: CloudEnvironment,
        requirements: tuple[CloudRequirement, ...],
        max_services: int = 8,
    ) -> CloudPlan:
        if max_services <= 0:
            raise ValueError("max_services must be positive")

        services = self.normalize_services(environment.services)
        normalized_requirements = self.normalize_requirements(requirements)
        scope = set(environment.environment_kinds)
        selected: list[CloudService] = []

        for requirement in normalized_requirements:
            if requirement.environment_kind not in scope:
                raise ValueError("environment lacks required environment kind")
            compatible = [
                service
                for service in services
                if requirement.environment_kind in service.environment_kinds
                and set(requirement.required_capabilities).issubset(
                    set(service.capabilities)
                )
            ]
            if not compatible:
                raise ValueError("no compatible cloud service")
            selected.append(compatible[0])

        service_ids = tuple(service.service_id for service in selected)
        if len(set(service_ids)) > max_services:
            raise ValueError("cloud plan exceeds service limit")

        return CloudPlan(
            environment_id=environment.environment_id,
            service_ids=service_ids,
            requirement_ids=tuple(
                requirement.requirement_id
                for requirement in normalized_requirements
            ),
        )
