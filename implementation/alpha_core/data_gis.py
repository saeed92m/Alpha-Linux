from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DataKind(str, Enum):
    TABULAR = "tabular"
    RASTER = "raster"
    VECTOR = "vector"
    TIMESERIES = "timeseries"


class LayerRole(str, Enum):
    SOURCE = "source"
    DERIVED = "derived"
    OUTPUT = "output"


class SpatialReferenceKind(str, Enum):
    GEOGRAPHIC = "geographic"
    PROJECTED = "projected"
    LOCAL = "local"


@dataclass(frozen=True)
class SpatialReference:
    reference_id: str
    kind: SpatialReferenceKind
    authority: str
    code: str

    def __post_init__(self) -> None:
        if not self.reference_id.strip():
            raise ValueError("reference_id is required")
        if not self.authority.strip():
            raise ValueError("authority is required")
        if not self.code.strip():
            raise ValueError("code is required")


@dataclass(frozen=True)
class DataLayer:
    layer_id: str
    name: str
    data_kind: DataKind
    role: LayerRole
    spatial_reference: SpatialReference | None = None

    def __post_init__(self) -> None:
        if not self.layer_id.strip():
            raise ValueError("layer_id is required")
        if not self.name.strip():
            raise ValueError("name is required")


@dataclass(frozen=True)
class DataProject:
    project_id: str
    name: str
    data_kinds: tuple[DataKind, ...]
    layers: tuple[DataLayer, ...] = ()

    def __post_init__(self) -> None:
        if not self.project_id.strip():
            raise ValueError("project_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.data_kinds:
            raise ValueError("data_kinds must be non-empty")
        if len(set(self.data_kinds)) != len(self.data_kinds):
            raise ValueError("data_kinds must be unique")

        layer_ids = [layer.layer_id for layer in self.layers]
        if len(set(layer_ids)) != len(layer_ids):
            raise ValueError("layer IDs must be unique")

        scope = set(self.data_kinds)
        if any(layer.data_kind not in scope for layer in self.layers):
            raise ValueError("layer data kind is outside project scope")


@dataclass(frozen=True)
class DataAnalysisRequirement:
    requirement_id: str
    data_kind: DataKind
    required_capabilities: tuple[str, ...]
    spatial_reference_kind: SpatialReferenceKind | None = None

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.required_capabilities:
            raise ValueError("required_capabilities must be non-empty")
        if len(set(self.required_capabilities)) != len(self.required_capabilities):
            raise ValueError("required_capabilities must be unique")
        if any(not capability.strip() for capability in self.required_capabilities):
            raise ValueError("required_capabilities must be non-empty")


@dataclass(frozen=True)
class DataTool:
    tool_id: str
    name: str
    data_kinds: tuple[DataKind, ...]
    capabilities: tuple[str, ...]
    spatial_reference_kinds: tuple[SpatialReferenceKind, ...] = ()
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.tool_id.strip():
            raise ValueError("tool_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.data_kinds:
            raise ValueError("data_kinds must be non-empty")
        if len(set(self.data_kinds)) != len(self.data_kinds):
            raise ValueError("data_kinds must be unique")
        if not self.capabilities:
            raise ValueError("capabilities must be non-empty")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")


@dataclass(frozen=True)
class DataPlan:
    project_id: str
    layer_ids: tuple[str, ...]
    tool_ids: tuple[str, ...]
    requirement_ids: tuple[str, ...]


class DataGISPlanner:
    def normalize_layers(
        self, layers: tuple[DataLayer, ...]
    ) -> tuple[DataLayer, ...]:
        ids = [layer.layer_id for layer in layers]
        if len(set(ids)) != len(ids):
            raise ValueError("layer IDs must be unique")
        return tuple(sorted(layers, key=lambda layer: layer.layer_id))

    def normalize_tools(
        self, tools: tuple[DataTool, ...]
    ) -> tuple[DataTool, ...]:
        ids = [tool.tool_id for tool in tools]
        if len(set(ids)) != len(ids):
            raise ValueError("tool IDs must be unique")
        return tuple(sorted(tools, key=lambda tool: tool.tool_id))

    def normalize_requirements(
        self, requirements: tuple[DataAnalysisRequirement, ...]
    ) -> tuple[DataAnalysisRequirement, ...]:
        ids = [requirement.requirement_id for requirement in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(
            sorted(requirements, key=lambda requirement: requirement.requirement_id)
        )

    def plan(
        self,
        project: DataProject,
        tools: tuple[DataTool, ...],
        requirements: tuple[DataAnalysisRequirement, ...],
        max_tools: int = 8,
    ) -> DataPlan:
        if max_tools <= 0:
            raise ValueError("max_tools must be positive")

        layers = self.normalize_layers(project.layers)
        normalized_tools = self.normalize_tools(tools)
        normalized_requirements = self.normalize_requirements(requirements)
        scope = set(project.data_kinds)
        selected: list[DataTool] = []

        for requirement in normalized_requirements:
            if requirement.data_kind not in scope:
                raise ValueError("project lacks required data kind")

            compatible = [
                tool
                for tool in normalized_tools
                if tool.enabled
                and requirement.data_kind in tool.data_kinds
                and set(requirement.required_capabilities).issubset(
                    set(tool.capabilities)
                )
                and (
                    requirement.spatial_reference_kind is None
                    or requirement.spatial_reference_kind
                    in tool.spatial_reference_kinds
                )
            ]
            if not compatible:
                raise ValueError("no compatible data tool")
            selected.append(compatible[0])

        tool_ids = tuple(tool.tool_id for tool in selected)
        if len(set(tool_ids)) > max_tools:
            raise ValueError("data plan exceeds tool limit")

        return DataPlan(
            project_id=project.project_id,
            layer_ids=tuple(layer.layer_id for layer in layers),
            tool_ids=tool_ids,
            requirement_ids=tuple(
                requirement.requirement_id
                for requirement in normalized_requirements
            ),
        )
