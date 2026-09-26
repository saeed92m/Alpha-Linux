from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AerospaceVehicle:
    vehicle_id: str
    name: str
    capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.vehicle_id.strip():
            raise ValueError("vehicle_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.capabilities or any(not capability.strip() for capability in self.capabilities):
            raise ValueError("capabilities must be non-empty")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")


@dataclass(frozen=True)
class MissionPhase:
    phase_id: str
    sequence: int
    required_capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.phase_id.strip():
            raise ValueError("phase_id is required")
        if self.sequence <= 0:
            raise ValueError("sequence must be positive")
        if any(not capability.strip() for capability in self.required_capabilities):
            raise ValueError("required capabilities must be non-empty strings")
        if len(set(self.required_capabilities)) != len(self.required_capabilities):
            raise ValueError("required capabilities must be unique")


@dataclass(frozen=True)
class AerospaceMissionPlan:
    vehicle_id: str
    phase_ids: tuple[str, ...]


class AerospacePlanner:
    """Deterministic aerospace mission planning only."""

    def normalize_phases(
        self, phases: tuple[MissionPhase, ...]
    ) -> tuple[MissionPhase, ...]:
        ids = [phase.phase_id for phase in phases]
        if len(set(ids)) != len(ids):
            raise ValueError("phase IDs must be unique")
        sequences = [phase.sequence for phase in phases]
        if len(set(sequences)) != len(sequences):
            raise ValueError("phase sequences must be unique")
        return tuple(sorted(phases, key=lambda item: (item.sequence, item.phase_id)))

    def plan(
        self,
        vehicle: AerospaceVehicle,
        phases: tuple[MissionPhase, ...],
        max_phases: int = 32,
    ) -> AerospaceMissionPlan:
        if max_phases <= 0:
            raise ValueError("max_phases must be positive")

        normalized = self.normalize_phases(phases)
        capabilities = set(vehicle.capabilities)
        incompatible = [
            phase.phase_id
            for phase in normalized
            if not set(phase.required_capabilities).issubset(capabilities)
        ]
        if incompatible:
            raise ValueError("vehicle lacks required mission capabilities")
        if len(normalized) > max_phases:
            raise ValueError("mission exceeds phase limit")

        return AerospaceMissionPlan(
            vehicle_id=vehicle.vehicle_id,
            phase_ids=tuple(phase.phase_id for phase in normalized),
        )
