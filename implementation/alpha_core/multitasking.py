from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class WindowState(str, Enum):
    NORMAL = "normal"
    MINIMIZED = "minimized"
    MAXIMIZED = "maximized"
    FULLSCREEN = "fullscreen"


@dataclass(frozen=True)
class WindowDescriptor:
    window_id: str
    title: str
    application_id: str
    workspace_id: str
    state: WindowState = WindowState.NORMAL
    metadata: Mapping[str, object] = None

    def __post_init__(self) -> None:
        if not self.window_id.strip():
            raise ValueError("window_id is required")
        if not self.title.strip():
            raise ValueError("title is required")
        if not self.application_id.strip():
            raise ValueError("application_id is required")
        if not self.workspace_id.strip():
            raise ValueError("workspace_id is required")
        if self.metadata is None:
            object.__setattr__(self, "metadata", {})


@dataclass(frozen=True)
class WorkspaceDescriptor:
    workspace_id: str
    name: str
    index: int

    def __post_init__(self) -> None:
        if not self.workspace_id.strip():
            raise ValueError("workspace_id is required")
        if not self.name.strip():
            raise ValueError("workspace name is required")
        if self.index < 0:
            raise ValueError("workspace index must be non-negative")


@dataclass(frozen=True)
class MultitaskingSnapshot:
    workspaces: tuple[WorkspaceDescriptor, ...]
    windows: tuple[WindowDescriptor, ...]

    def __post_init__(self) -> None:
        workspace_ids = [item.workspace_id for item in self.workspaces]
        if workspace_ids != sorted(workspace_ids, key=lambda value: next(
            item.index for item in self.workspaces if item.workspace_id == value
        )):
            raise ValueError("workspaces must be ordered by index")
        if len(workspace_ids) != len(set(workspace_ids)):
            raise ValueError("workspace identifiers must be unique")
        window_ids = [item.window_id for item in self.windows]
        if len(window_ids) != len(set(window_ids)):
            raise ValueError("window identifiers must be unique")
        available = set(workspace_ids)
        if any(item.workspace_id not in available for item in self.windows):
            raise ValueError("window references unavailable workspace")


class MultitaskingPlanner:
    """Read-only planner for deterministic workspace/window state."""

    def normalize(
        self,
        workspaces: tuple[WorkspaceDescriptor, ...],
        windows: tuple[WindowDescriptor, ...],
    ) -> MultitaskingSnapshot:
        ordered_workspaces = tuple(sorted(workspaces, key=lambda item: (item.index, item.workspace_id)))
        ordered_windows = tuple(
            sorted(windows, key=lambda item: (item.workspace_id, item.window_id))
        )
        return MultitaskingSnapshot(ordered_workspaces, ordered_windows)

    def windows_for_workspace(
        self,
        snapshot: MultitaskingSnapshot,
        workspace_id: str,
    ) -> tuple[WindowDescriptor, ...]:
        if workspace_id not in {item.workspace_id for item in snapshot.workspaces}:
            raise ValueError("unknown workspace")
        return tuple(
            item for item in snapshot.windows if item.workspace_id == workspace_id
        )
