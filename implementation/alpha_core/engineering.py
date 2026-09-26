from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AnalysisKind(str, Enum):
    STRUCTURAL = "structural"
    THERMAL = "thermal"
    FLUID = "fluid"


@dataclass(frozen=True)
class EngineeringValue:
    value: float
    unit: str

    def __post_init__(self) -> None:
        if not self.unit.strip():
            raise ValueError("unit is required")


@dataclass(frozen=True)
class EngineeringProject:
    project_id: str
    name: str
    analysis_kinds: tuple[AnalysisKind, ...]

    def __post_init__(self) -> None:
        if not self.project_id.strip():
            raise ValueError("project_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.analysis_kinds:
            raise ValueError("analysis_kinds must be non-empty")
        if len(set(self.analysis_kinds)) != len(self.analysis_kinds):
            raise ValueError("analysis_kinds must be unique")


@dataclass(frozen=True)
class EngineeringResource:
    resource_id: str
    name: str
    cpu_cores: int
    memory_mib: int
    solver_kinds: tuple[AnalysisKind, ...]
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.resource_id.strip():
            raise ValueError("resource_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if self.cpu_cores <= 0:
            raise ValueError("cpu_cores must be positive")
        if self.memory_mib <= 0:
            raise ValueError("memory_mib must be positive")
        if not self.solver_kinds:
            raise ValueError("solver_kinds must be non-empty")
        if len(set(self.solver_kinds)) != len(self.solver_kinds):
            raise ValueError("solver_kinds must be unique")


@dataclass(frozen=True)
class EngineeringPlan:
    project_id: str
    resource_ids: tuple[str, ...]


class EngineeringPlanner:
    """Deterministic engineering analysis planning only."""

    def normalize_resources(
        self, resources: tuple[EngineeringResource, ...]
    ) -> tuple[EngineeringResource, ...]:
        ids = [resource.resource_id for resource in resources]
        if len(set(ids)) != len(ids):
            raise ValueError("resource IDs must be unique")
        return tuple(sorted(resources, key=lambda item: item.resource_id))

    def plan(
        self,
        project: EngineeringProject,
        resources: tuple[EngineeringResource, ...],
        min_cpu_cores: int = 1,
        min_memory_mib: int = 1,
        max_resources: int = 1,
    ) -> EngineeringPlan:
        if min_cpu_cores <= 0:
            raise ValueError("min_cpu_cores must be positive")
        if min_memory_mib <= 0:
            raise ValueError("min_memory_mib must be positive")
        if max_resources <= 0:
            raise ValueError("max_resources must be positive")

        normalized = self.normalize_resources(resources)
        required = set(project.analysis_kinds)
        compatible = [
            resource
            for resource in normalized
            if resource.enabled
            and resource.cpu_cores >= min_cpu_cores
            and resource.memory_mib >= min_memory_mib
            and required.issubset(set(resource.solver_kinds))
        ]
        if not compatible:
            raise ValueError("no compatible engineering resource")

        selected = compatible[:max_resources]
        return EngineeringPlan(
            project_id=project.project_id,
            resource_ids=tuple(resource.resource_id for resource in selected),
        )
