from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class CapabilityState(str, Enum):
    SUPPORTED = "supported"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class DisplayDescriptor:
    display_id: str
    width_px: int
    height_px: int
    scale_factor: float

    def __post_init__(self) -> None:
        if not self.display_id.strip():
            raise ValueError("display_id is required")
        if self.width_px <= 0 or self.height_px <= 0:
            raise ValueError("display dimensions must be positive")
        if self.scale_factor <= 0:
            raise ValueError("scale_factor must be positive")


@dataclass(frozen=True)
class InteractionCapabilities:
    touch: CapabilityState
    pen: CapabilityState
    hidpi: CapabilityState
    multi_display: CapabilityState


@dataclass(frozen=True)
class DesktopCapabilities:
    displays: tuple[DisplayDescriptor, ...]
    interaction: InteractionCapabilities
    theme: Mapping[str, object]

    def __post_init__(self) -> None:
        ids = [display.display_id for display in self.displays]
        if ids != sorted(ids):
            raise ValueError("displays must be ordered by display_id")
        if len(ids) != len(set(ids)):
            raise ValueError("display identifiers must be unique")


@dataclass(frozen=True)
class DesktopSessionConfig:
    session_id: str
    theme: str
    hidpi_scale: float = 1.0
    display_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.session_id.strip():
            raise ValueError("session_id is required")
        if not self.theme.strip():
            raise ValueError("theme is required")
        if self.hidpi_scale <= 0:
            raise ValueError("hidpi_scale must be positive")
        if tuple(sorted(self.display_ids)) != self.display_ids:
            raise ValueError("display_ids must be ordered")


class DesktopCapabilityDiscovery:
    """Reference, read-only capability provider until the COSMIC adapter exists."""

    def snapshot(
        self,
        displays: tuple[DisplayDescriptor, ...] = (),
        *,
        touch: CapabilityState = CapabilityState.UNAVAILABLE,
        pen: CapabilityState = CapabilityState.UNAVAILABLE,
    ) -> DesktopCapabilities:
        ordered = tuple(sorted(displays, key=lambda display: display.display_id))
        hidpi = (
            CapabilityState.SUPPORTED
            if any(display.scale_factor > 1.0 for display in ordered)
            else CapabilityState.DEGRADED
        )
        multi = (
            CapabilityState.SUPPORTED
            if len(ordered) > 1
            else CapabilityState.DEGRADED if ordered else CapabilityState.UNAVAILABLE
        )
        return DesktopCapabilities(
            displays=ordered,
            interaction=InteractionCapabilities(touch, pen, hidpi, multi),
            theme={"managed": True, "source": "declarative"},
        )


class DesktopSessionPlanner:
    """Validates declarative session plans without changing the host."""

    def plan(self, config: DesktopSessionConfig, capabilities: DesktopCapabilities) -> DesktopSessionConfig:
        available = {display.display_id for display in capabilities.displays}
        if any(display_id not in available for display_id in config.display_ids):
            raise ValueError("session references unavailable display")
        if config.hidpi_scale != 1.0 and capabilities.interaction.hidpi is CapabilityState.UNAVAILABLE:
            raise ValueError("requested HiDPI scale is unavailable")
        return config
