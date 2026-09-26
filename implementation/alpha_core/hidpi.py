from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_SCALES = (1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 3.0, 4.0)


@dataclass(frozen=True)
class DisplayScaleDescriptor:
    display_id: str
    scale_factor: float

    def __post_init__(self) -> None:
        if not self.display_id.strip():
            raise ValueError("display_id is required")
        if self.scale_factor not in _ALLOWED_SCALES:
            raise ValueError("scale_factor must use a supported deterministic value")


@dataclass(frozen=True)
class HiDPISnapshot:
    displays: tuple[DisplayScaleDescriptor, ...]

    def __post_init__(self) -> None:
        ids = [display.display_id for display in self.displays]
        if ids != sorted(ids):
            raise ValueError("displays must be ordered by display_id")
        if len(ids) != len(set(ids)):
            raise ValueError("display identifiers must be unique")


@dataclass(frozen=True)
class HiDPIPolicy:
    default_scale: float = 1.0
    display_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.default_scale not in _ALLOWED_SCALES:
            raise ValueError("default_scale must use a supported deterministic value")
        if self.display_ids != tuple(sorted(self.display_ids)):
            raise ValueError("display_ids must be ordered")
        if len(self.display_ids) != len(set(self.display_ids)):
            raise ValueError("display identifiers must be unique")


class HiDPIPlanner:
    """Deterministic, declarative HiDPI planning; never mutates the host."""

    def normalize(
        self,
        displays: tuple[DisplayScaleDescriptor, ...],
    ) -> HiDPISnapshot:
        return HiDPISnapshot(tuple(sorted(displays, key=lambda display: display.display_id)))

    def validate_policy(
        self,
        policy: HiDPIPolicy,
        snapshot: HiDPISnapshot,
    ) -> HiDPIPolicy:
        available = {display.display_id for display in snapshot.displays}
        if any(display_id not in available for display_id in policy.display_ids):
            raise ValueError("policy references unavailable display")
        return policy

    def scales_for_displays(
        self,
        display_ids: tuple[str, ...],
        snapshot: HiDPISnapshot,
    ) -> tuple[DisplayScaleDescriptor, ...]:
        requested = set(display_ids)
        available = {display.display_id: display for display in snapshot.displays}
        if not requested.issubset(available):
            raise ValueError("requested display is unavailable")
        return tuple(available[display_id] for display_id in sorted(requested))
