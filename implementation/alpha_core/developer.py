from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolchainDescriptor:
    toolchain_id: str
    name: str
    languages: tuple[str, ...]
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.toolchain_id.strip():
            raise ValueError("toolchain_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.languages or any(not language.strip() for language in self.languages):
            raise ValueError("languages must be non-empty")
        if len(set(self.languages)) != len(self.languages):
            raise ValueError("languages must be unique")


@dataclass(frozen=True)
class DeveloperWorkspace:
    workspace_id: str
    project_type: str
    languages: tuple[str, ...]
    max_toolchains: int = 1

    def __post_init__(self) -> None:
        if not self.workspace_id.strip():
            raise ValueError("workspace_id is required")
        if not self.project_type.strip():
            raise ValueError("project_type is required")
        if not self.languages or any(not language.strip() for language in self.languages):
            raise ValueError("languages must be non-empty")
        if len(set(self.languages)) != len(self.languages):
            raise ValueError("languages must be unique")
        if self.max_toolchains <= 0:
            raise ValueError("max_toolchains must be positive")


@dataclass(frozen=True)
class DeveloperPlan:
    workspace: DeveloperWorkspace
    toolchain_ids: tuple[str, ...]


class DeveloperPlanner:
    """Deterministic developer-domain planning only; no tool execution."""

    def normalize_toolchains(
        self, toolchains: tuple[ToolchainDescriptor, ...]
    ) -> tuple[ToolchainDescriptor, ...]:
        return tuple(
            ToolchainDescriptor(
                toolchain.toolchain_id,
                toolchain.name,
                tuple(sorted(toolchain.languages)),
                toolchain.enabled,
            )
            for toolchain in sorted(toolchains, key=lambda item: item.toolchain_id)
        )

    def plan(
        self,
        workspace: DeveloperWorkspace,
        toolchains: tuple[ToolchainDescriptor, ...],
    ) -> DeveloperPlan:
        normalized = self.normalize_toolchains(toolchains)
        ids = [toolchain.toolchain_id for toolchain in normalized]
        if len(set(ids)) != len(ids):
            raise ValueError("toolchain IDs must be unique")

        required = set(workspace.languages)
        compatible = [
            toolchain
            for toolchain in normalized
            if toolchain.enabled and required.issubset(toolchain.languages)
        ]
        if not compatible:
            raise ValueError("no compatible toolchain")
        if len(compatible) > workspace.max_toolchains:
            compatible = compatible[: workspace.max_toolchains]
        return DeveloperPlan(
            workspace=workspace,
            toolchain_ids=tuple(toolchain.toolchain_id for toolchain in compatible),
        )
