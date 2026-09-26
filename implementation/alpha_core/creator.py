from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CreatorMediaKind(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    VFX = "vfx"
    GRAPHICS = "graphics"


class CreatorAssetRole(str, Enum):
    SOURCE = "source"
    PROXY = "proxy"
    CACHE = "cache"
    GENERATED_OUTPUT = "generated-output"


@dataclass(frozen=True)
class CreatorAsset:
    asset_id: str
    name: str
    media_kind: CreatorMediaKind
    role: CreatorAssetRole

    def __post_init__(self) -> None:
        if not self.asset_id.strip():
            raise ValueError("asset_id is required")
        if not self.name.strip():
            raise ValueError("name is required")


@dataclass(frozen=True)
class CreatorProject:
    project_id: str
    name: str
    media_kinds: tuple[CreatorMediaKind, ...]
    assets: tuple[CreatorAsset, ...] = ()

    def __post_init__(self) -> None:
        if not self.project_id.strip():
            raise ValueError("project_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.media_kinds:
            raise ValueError("media_kinds must be non-empty")
        if len(set(self.media_kinds)) != len(self.media_kinds):
            raise ValueError("media_kinds must be unique")
        asset_ids = [asset.asset_id for asset in self.assets]
        if len(set(asset_ids)) != len(asset_ids):
            raise ValueError("asset IDs must be unique")
        project_media = set(self.media_kinds)
        if any(asset.media_kind not in project_media for asset in self.assets):
            raise ValueError("asset media kind is outside project scope")


@dataclass(frozen=True)
class CreatorTool:
    tool_id: str
    name: str
    media_kinds: tuple[CreatorMediaKind, ...]
    capabilities: tuple[str, ...]
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.tool_id.strip():
            raise ValueError("tool_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.media_kinds:
            raise ValueError("media_kinds must be non-empty")
        if len(set(self.media_kinds)) != len(self.media_kinds):
            raise ValueError("media_kinds must be unique")
        if not self.capabilities:
            raise ValueError("capabilities must be non-empty")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")
        if any(not capability.strip() for capability in self.capabilities):
            raise ValueError("capabilities must be non-empty")


@dataclass(frozen=True)
class CreatorRequirement:
    requirement_id: str
    media_kind: CreatorMediaKind
    required_capabilities: tuple[str, ...]

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
class CreatorPlan:
    project_id: str
    asset_ids: tuple[str, ...]
    tool_ids: tuple[str, ...]
    requirement_ids: tuple[str, ...]


class CreatorPlanner:
    """Deterministic creator-tool planning only."""

    def normalize_assets(
        self, assets: tuple[CreatorAsset, ...]
    ) -> tuple[CreatorAsset, ...]:
        ids = [asset.asset_id for asset in assets]
        if len(set(ids)) != len(ids):
            raise ValueError("asset IDs must be unique")
        return tuple(sorted(assets, key=lambda item: item.asset_id))

    def normalize_tools(
        self, tools: tuple[CreatorTool, ...]
    ) -> tuple[CreatorTool, ...]:
        ids = [tool.tool_id for tool in tools]
        if len(set(ids)) != len(ids):
            raise ValueError("tool IDs must be unique")
        return tuple(sorted(tools, key=lambda item: item.tool_id))

    def normalize_requirements(
        self, requirements: tuple[CreatorRequirement, ...]
    ) -> tuple[CreatorRequirement, ...]:
        ids = [requirement.requirement_id for requirement in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def plan(
        self,
        project: CreatorProject,
        tools: tuple[CreatorTool, ...],
        requirements: tuple[CreatorRequirement, ...],
        max_tools: int = 4,
    ) -> CreatorPlan:
        if max_tools <= 0:
            raise ValueError("max_tools must be positive")

        normalized_assets = self.normalize_assets(project.assets)
        normalized_tools = self.normalize_tools(tools)
        normalized_requirements = self.normalize_requirements(requirements)
        project_media = set(project.media_kinds)
        selected: list[CreatorTool] = []

        for requirement in normalized_requirements:
            if requirement.media_kind not in project_media:
                raise ValueError("project lacks required media kind")

            compatible = [
                tool
                for tool in normalized_tools
                if tool.enabled
                and requirement.media_kind in tool.media_kinds
                and set(requirement.required_capabilities).issubset(
                    set(tool.capabilities)
                )
            ]
            if not compatible:
                raise ValueError("no compatible creator tool")
            selected.append(compatible[0])

        selected_ids = tuple(tool.tool_id for tool in selected)
        if len(set(selected_ids)) > max_tools:
            raise ValueError("creator plan exceeds tool limit")

        return CreatorPlan(
            project_id=project.project_id,
            asset_ids=tuple(asset.asset_id for asset in normalized_assets),
            tool_ids=selected_ids,
            requirement_ids=tuple(
                requirement.requirement_id for requirement in normalized_requirements
            ),
        )
