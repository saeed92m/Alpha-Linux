import pytest

from alpha_core.desktop import (
    CapabilityState,
    DesktopCapabilityDiscovery,
    DesktopSessionConfig,
    DesktopSessionPlanner,
    DisplayDescriptor,
)


def test_desktop_capabilities_are_deterministic():
    discovery = DesktopCapabilityDiscovery()
    snapshot = discovery.snapshot(
        (
            DisplayDescriptor("display-b", 1920, 1080, 1.0),
            DisplayDescriptor("display-a", 3840, 2160, 2.0),
        ),
        touch=CapabilityState.SUPPORTED,
        pen=CapabilityState.DEGRADED,
    )

    assert tuple(d.display_id for d in snapshot.displays) == ("display-a", "display-b")
    assert snapshot.interaction.hidpi is CapabilityState.SUPPORTED
    assert snapshot.interaction.multi_display is CapabilityState.SUPPORTED
    assert snapshot.theme["source"] == "declarative"


def test_session_planner_validates_display_references():
    discovery = DesktopCapabilityDiscovery()
    capabilities = discovery.snapshot(
        (DisplayDescriptor("display-a", 1920, 1080, 1.0),)
    )
    planner = DesktopSessionPlanner()

    config = DesktopSessionConfig(
        "session-1", "alpha", 1.0, ("display-a",)
    )
    assert planner.plan(config, capabilities) == config

    with pytest.raises(ValueError):
        planner.plan(
            DesktopSessionConfig("session-2", "alpha", 1.0, ("missing",)),
            capabilities,
        )


def test_session_config_is_validated():
    with pytest.raises(ValueError):
        DesktopSessionConfig("", "alpha")
    with pytest.raises(ValueError):
        DesktopSessionConfig("session", "alpha", 0)


def test_display_validation():
    with pytest.raises(ValueError):
        DisplayDescriptor("display", 0, 1080, 1.0)
