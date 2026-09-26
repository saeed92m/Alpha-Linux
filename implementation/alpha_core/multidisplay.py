from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DisplayNode:
    display_id: str
    width_px: int
    height_px: int
    scale_factor: float
    primary: bool = False

    def __post_init__(self) -> None:
        if not self.display_id.strip():
            raise ValueError("display_id is required")
        if self.width_px <= 0 or self.height_px <= 0:
            raise ValueError("display dimensions must be positive")
        if self.scale_factor <= 0:
            raise ValueError("scale_factor must be positive")


@dataclass(frozen=True)
class DisplayTopology:
    displays: tuple[DisplayNode, ...]

    def __post_init__(self) -> None:
        ids = [display.display_id for display in self.displays]
        if ids != sorted(ids):
            raise ValueError("displays must be ordered by display_id")
        if len(ids) != len(set(ids)):
            raise ValueError("display identifiers must be unique")
        primary_count = sum(display.primary for display in self.displays)
        if self.displays and primary_count != 1:
            raise ValueError("topology must contain exactly one primary display")


class MultiDisplayPlanner:
    """Deterministic, declarative multi-display planning; never mutates the host."""

    def normalize(self, displays: tuple[DisplayNode, ...]) -> DisplayTopology:
        ordered = tuple(sorted(displays, key=lambda display: display.display_id))
        if ordered and not any(display.primary for display in ordered):
            ordered = tuple(
                DisplayNode(
                    display.display_id,
                    display.width_px,
                    display.height_px,
                    display.scale_factor,
                    index == 0,
                )
                for index, display in enumerate(ordered)
            )
        return DisplayTopology(ordered)

    def select(self, display_ids: tuple[str, ...], topology: DisplayTopology) -> tuple[DisplayNode, ...]:
        requested = set(display_ids)
        available = {display.display_id: display for display in topology.displays}
        if not requested.issubset(available):
            raise ValueError("requested display is unavailable")
        return tuple(available[display_id] for display_id in sorted(requested))
