from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .system_integration import ComponentHealth, HealthAggregator, HealthState, SystemDiscovery


@dataclass(frozen=True)
class ObservatorySnapshot:
    system: Mapping[str, object]
    health: ComponentHealth


class SystemObservatory:
    """Read-only system observatory facade for future Control Center/UI consumers."""

    def __init__(self, discovery: SystemDiscovery, health: HealthAggregator) -> None:
        self._discovery = discovery
        self._health = health

    def snapshot(self, components: tuple[ComponentHealth, ...] = ()) -> ObservatorySnapshot:
        return ObservatorySnapshot(
            system=self._discovery.snapshot(),
            health=self._health.aggregate(components),
        )
