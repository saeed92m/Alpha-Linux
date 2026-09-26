import pytest

from alpha_core.multitasking import (
    MultitaskingPlanner,
    WindowDescriptor,
    WorkspaceDescriptor,
)


def workspaces():
    return (
        WorkspaceDescriptor("ws-0", "Main", 0),
        WorkspaceDescriptor("ws-1", "Engineering", 1),
    )


def test_normalization_is_deterministic():
    planner = MultitaskingPlanner()
    windows = (
        WindowDescriptor("win-b", "Terminal", "org.cosmic.Terminal", "ws-1"),
        WindowDescriptor("win-a", "Editor", "org.cosmic.Editor", "ws-0"),
    )

    first = planner.normalize(tuple(reversed(workspaces())), windows)
    second = planner.normalize(workspaces(), tuple(reversed(windows)))

    assert first == second
    assert [item.workspace_id for item in first.workspaces] == ["ws-0", "ws-1"]
    assert [item.window_id for item in first.windows] == ["win-a", "win-b"]


def test_windows_can_be_selected_deterministically():
    snapshot = MultitaskingPlanner().normalize(
        workspaces(),
        (
            WindowDescriptor("win-b", "Terminal", "org.cosmic.Terminal", "ws-1"),
            WindowDescriptor("win-a", "Editor", "org.cosmic.Editor", "ws-0"),
            WindowDescriptor("win-c", "Browser", "org.cosmic.Browser", "ws-1"),
        ),
    )

    selected = MultitaskingPlanner().windows_for_workspace(snapshot, "ws-1")

    assert [item.window_id for item in selected] == ["win-b", "win-c"]


def test_unknown_workspace_is_rejected():
    snapshot = MultitaskingPlanner().normalize(workspaces(), ())
    with pytest.raises(ValueError, match="unknown workspace"):
        MultitaskingPlanner().windows_for_workspace(snapshot, "ws-9")


def test_duplicate_window_ids_are_rejected():
    windows = (
        WindowDescriptor("win-a", "Editor", "org.cosmic.Editor", "ws-0"),
        WindowDescriptor("win-a", "Terminal", "org.cosmic.Terminal", "ws-0"),
    )
    with pytest.raises(ValueError, match="window identifiers"):
        MultitaskingPlanner().normalize(workspaces(), windows)


def test_window_cannot_reference_unknown_workspace():
    windows = (
        WindowDescriptor("win-a", "Editor", "org.cosmic.Editor", "ws-9"),
    )
    with pytest.raises(ValueError, match="unavailable workspace"):
        MultitaskingPlanner().normalize(workspaces(), windows)


def test_invalid_window_state_is_not_silently_coerced():
    with pytest.raises(ValueError):
        WindowDescriptor(
            "win-a",
            "Editor",
            "org.cosmic.Editor",
            "ws-0",
            state="invalid",  # type: ignore[arg-type]
        )
