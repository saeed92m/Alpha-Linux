import pytest

from alpha_core.cosmic import (
    CosmicIntegrationDescriptor,
    CosmicReferenceAdapter,
    IntegrationState,
)
from alpha_core.desktop import (
    CapabilityState,
    DesktopCapabilityDiscovery,
    DesktopSessionConfig,
    DisplayDescriptor,
)


def descriptor():
    return CosmicIntegrationDescriptor("COSMIC", "wayland", "xdg-shell", "1")


def test_cosmic_binding_is_deterministic_and_supported():
    capabilities = DesktopCapabilityDiscovery().snapshot(
        (DisplayDescriptor("DP-1", 2560, 1440, 1.25),)
    )
    config = DesktopSessionConfig("default", "alpha", 1.25, ("DP-1",))
    adapter = CosmicReferenceAdapter()

    first = adapter.describe(config, capabilities, descriptor())
    second = adapter.describe(config, capabilities, descriptor())

    assert first == second
    assert first.binding_id.startswith("cosmic-")
    assert first.state is IntegrationState.SUPPORTED


def test_cosmic_binding_degrades_when_hidpi_is_not_available():
    capabilities = DesktopCapabilityDiscovery().snapshot(
        (DisplayDescriptor("DP-1", 1920, 1080, 1.0),)
    )
    capabilities = capabilities.__class__(
        displays=capabilities.displays,
        interaction=capabilities.interaction.__class__(
            touch=capabilities.interaction.touch,
            pen=capabilities.interaction.pen,
            hidpi=CapabilityState.UNAVAILABLE,
            multi_display=capabilities.interaction.multi_display,
        ),
        theme=capabilities.theme,
    )
    config = DesktopSessionConfig("default", "alpha", 1.25, ("DP-1",))

    result = CosmicReferenceAdapter().describe(config, capabilities, descriptor())

    assert result.state is IntegrationState.DEGRADED


def test_cosmic_binding_rejects_missing_display_as_unavailable():
    capabilities = DesktopCapabilityDiscovery().snapshot(
        (DisplayDescriptor("DP-1", 1920, 1080, 1.0),)
    )
    config = DesktopSessionConfig("default", "alpha", 1.0, ("HDMI-1",))

    result = CosmicReferenceAdapter().describe(config, capabilities, descriptor())

    assert result.state is IntegrationState.UNAVAILABLE


def test_cosmic_metadata_is_required():
    with pytest.raises(ValueError):
        CosmicIntegrationDescriptor("", "wayland", "xdg-shell", "1")
