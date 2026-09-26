from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ElectronicsInterfaceKind(str, Enum):
    POWER = "power"
    DIGITAL = "digital"
    ANALOG = "analog"
    BUS = "bus"


@dataclass(frozen=True)
class ElectronicsInterface:
    interface_id: str
    kind: ElectronicsInterfaceKind
    capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.interface_id.strip():
            raise ValueError("interface_id is required")
        if not self.capabilities:
            raise ValueError("capabilities must be non-empty")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")
        if any(not capability.strip() for capability in self.capabilities):
            raise ValueError("capabilities must be non-empty")


@dataclass(frozen=True)
class ElectronicsBoard:
    board_id: str
    name: str
    interfaces: tuple[ElectronicsInterface, ...]

    def __post_init__(self) -> None:
        if not self.board_id.strip():
            raise ValueError("board_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        ids = [interface.interface_id for interface in self.interfaces]
        if len(set(ids)) != len(ids):
            raise ValueError("interface IDs must be unique")


@dataclass(frozen=True)
class ElectronicsComponent:
    component_id: str
    name: str
    interfaces: tuple[ElectronicsInterface, ...]
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.component_id.strip():
            raise ValueError("component_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        ids = [interface.interface_id for interface in self.interfaces]
        if len(set(ids)) != len(ids):
            raise ValueError("interface IDs must be unique")


@dataclass(frozen=True)
class CircuitRequirement:
    requirement_id: str
    interface_kind: ElectronicsInterfaceKind
    required_capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.required_capabilities:
            raise ValueError("required_capabilities must be non-empty")
        if len(set(self.required_capabilities)) != len(self.required_capabilities):
            raise ValueError("required_capabilities must be unique")


@dataclass(frozen=True)
class ElectronicsPlan:
    board_id: str
    component_ids: tuple[str, ...]
    requirement_ids: tuple[str, ...]


class ElectronicsPlanner:
    """Deterministic electronics compatibility planning only."""

    def normalize_components(
        self, components: tuple[ElectronicsComponent, ...]
    ) -> tuple[ElectronicsComponent, ...]:
        ids = [component.component_id for component in components]
        if len(set(ids)) != len(ids):
            raise ValueError("component IDs must be unique")
        return tuple(sorted(components, key=lambda item: item.component_id))

    def normalize_requirements(
        self, requirements: tuple[CircuitRequirement, ...]
    ) -> tuple[CircuitRequirement, ...]:
        ids = [requirement.requirement_id for requirement in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def plan(
        self,
        board: ElectronicsBoard,
        components: tuple[ElectronicsComponent, ...],
        requirements: tuple[CircuitRequirement, ...],
        max_components: int = 8,
    ) -> ElectronicsPlan:
        if max_components <= 0:
            raise ValueError("max_components must be positive")

        normalized_components = self.normalize_components(components)
        normalized_requirements = self.normalize_requirements(requirements)

        board_support = {
            interface.kind: set(interface.capabilities)
            for interface in board.interfaces
        }
        selected: list[ElectronicsComponent] = []

        for requirement in normalized_requirements:
            board_capabilities = board_support.get(requirement.interface_kind)
            if board_capabilities is None or not set(
                requirement.required_capabilities
            ).issubset(board_capabilities):
                raise ValueError("board lacks required interface capability")

            compatible = [
                component
                for component in normalized_components
                if component.enabled
                and any(
                    interface.kind == requirement.interface_kind
                    and set(requirement.required_capabilities).issubset(
                        set(interface.capabilities)
                    )
                    for interface in component.interfaces
                )
            ]
            if not compatible:
                raise ValueError("no compatible electronics component")
            selected.append(compatible[0])

        selected_ids = tuple(component.component_id for component in selected)
        if len(set(selected_ids)) > max_components:
            raise ValueError("circuit exceeds component limit")

        return ElectronicsPlan(
            board_id=board.board_id,
            component_ids=selected_ids,
            requirement_ids=tuple(
                requirement.requirement_id for requirement in normalized_requirements
            ),
        )
