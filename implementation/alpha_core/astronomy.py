from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class SkyPosition:
    ra_deg: float
    dec_deg: float

    def __post_init__(self) -> None:
        if not isfinite(self.ra_deg) or not 0.0 <= self.ra_deg < 360.0:
            raise ValueError("ra_deg must be in [0, 360)")
        if not isfinite(self.dec_deg) or not -90.0 <= self.dec_deg <= 90.0:
            raise ValueError("dec_deg must be in [-90, 90]")


@dataclass(frozen=True)
class Photometry:
    magnitude: float

    def __post_init__(self) -> None:
        if not isfinite(self.magnitude):
            raise ValueError("magnitude must be finite")


@dataclass(frozen=True)
class AstronomyObservation:
    observation_id: str
    object_id: str
    source: str
    timestamp: str
    position: SkyPosition
    photometry: Photometry | None = None

    def __post_init__(self) -> None:
        if not self.observation_id.strip():
            raise ValueError("observation_id is required")
        if not self.object_id.strip():
            raise ValueError("object_id is required")
        if not self.source.strip():
            raise ValueError("source is required")
        if not self.timestamp.strip():
            raise ValueError("timestamp is required")


@dataclass(frozen=True)
class AstronomyObservationPlan:
    object_id: str
    observation_ids: tuple[str, ...]


class AstronomyPlanner:
    """Deterministic astronomy observation planning only."""

    def normalize(
        self, observations: tuple[AstronomyObservation, ...]
    ) -> tuple[AstronomyObservation, ...]:
        ids = [observation.observation_id for observation in observations]
        if len(set(ids)) != len(ids):
            raise ValueError("observation IDs must be unique")
        return tuple(
            sorted(
                observations,
                key=lambda item: (item.timestamp, item.observation_id),
            )
        )

    def plan(
        self,
        object_id: str,
        observations: tuple[AstronomyObservation, ...],
        max_observations: int = 100,
    ) -> AstronomyObservationPlan:
        if not object_id.strip():
            raise ValueError("object_id is required")
        if max_observations <= 0:
            raise ValueError("max_observations must be positive")

        normalized = self.normalize(observations)
        matching = [
            observation
            for observation in normalized
            if observation.object_id == object_id
        ]
        if not matching:
            raise ValueError("no observations for object")
        selected = matching[:max_observations]
        return AstronomyObservationPlan(
            object_id=object_id,
            observation_ids=tuple(
                observation.observation_id for observation in selected
            ),
        )
