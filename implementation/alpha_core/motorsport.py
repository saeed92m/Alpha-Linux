from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MotorsportComponentKind(str, Enum):
    POWERTRAIN = "powertrain"
    DRIVETRAIN = "drivetrain"
    CHASSIS = "chassis"
    DATA = "data"


@dataclass(frozen=True)
class MotorsportVehicle:
    vehicle_id: str
    name: str
    capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.vehicle_id.strip():
            raise ValueError("vehicle_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")
        if any(not capability.strip() for capability in self.capabilities):
            raise ValueError("capabilities must be non-empty")


@dataclass(frozen=True)
class MotorsportComponent:
    component_id: str
    name: str
    kind: MotorsportComponentKind
    capabilities: tuple[str, ...]
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.component_id.strip():
            raise ValueError("component_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")
        if any(not capability.strip() for capability in self.capabilities):
            raise ValueError("capabilities must be non-empty")


@dataclass(frozen=True)
class SetupRequirement:
    requirement_id: str
    component_kind: MotorsportComponentKind
    required_capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.required_capabilities:
            raise ValueError("required_capabilities must be non-empty")
        if len(set(self.required_capabilities)) != len(self.required_capabilities):
            raise ValueError("required_capabilities must be unique")


@dataclass(frozen=True)
class MotorsportSetupPlan:
    vehicle_id: str
    component_ids: tuple[str, ...]
    requirement_ids: tuple[str, ...]


class MotorsportPlanner:
    """Deterministic motorsport setup planning only."""

    def normalize_components(
        self, components: tuple[MotorsportComponent, ...]
    ) -> tuple[MotorsportComponent, ...]:
        ids = [component.component_id for component in components]
        if len(set(ids)) != len(ids):
            raise ValueError("component IDs must be unique")
        return tuple(sorted(components, key=lambda item: item.component_id))

    def normalize_requirements(
        self, requirements: tuple[SetupRequirement, ...]
    ) -> tuple[SetupRequirement, ...]:
        ids = [requirement.requirement_id for requirement in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def plan(
        self,
        vehicle: MotorsportVehicle,
        components: tuple[MotorsportComponent, ...],
        requirements: tuple[SetupRequirement, ...],
        max_components: int = 4,
    ) -> MotorsportSetupPlan:
        if max_components <= 0:
            raise ValueError("max_components must be positive")

        normalized_components = self.normalize_components(components)
        normalized_requirements = self.normalize_requirements(requirements)
        vehicle_capabilities = set(vehicle.capabilities)
        selected: list[MotorsportComponent] = []

        for requirement in normalized_requirements:
            if not set(requirement.required_capabilities).issubset(vehicle_capabilities):
                raise ValueError("vehicle lacks required setup capabilities")
            compatible = [
                component
                for component in normalized_components
                if component.enabled
                and component.kind == requirement.component_kind
                and set(requirement.required_capabilities).issubset(
                    set(component.capabilities)
                )
            ]
            if not compatible:
                raise ValueError("no compatible motorsport component")
            selected.append(compatible[0])

        selected_ids = tuple(component.component_id for component in selected)
        if len(set(selected_ids)) > max_components:
            raise ValueError("setup exceeds component limit")

        return MotorsportSetupPlan(
            vehicle_id=vehicle.vehicle_id,
            component_ids=selected_ids,
            requirement_ids=tuple(
                requirement.requirement_id for requirement in normalized_requirements
            ),
        )
