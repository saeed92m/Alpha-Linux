from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AudioKind(str, Enum):
    MONO = "mono"
    STEREO = "stereo"
    SURROUND = "surround"
    MIDI = "midi"


class TrackRole(str, Enum):
    SOURCE = "source"
    PROCESSED = "processed"
    RENDERED = "rendered"


class AudioCapabilityKind(str, Enum):
    INPUT = "input"
    OUTPUT = "output"
    PROCESSING = "processing"
    MIDI = "midi"


@dataclass(frozen=True)
class AudioCapability:
    capability_id: str
    kind: AudioCapabilityKind
    audio_kinds: tuple[AudioKind, ...]
    capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("capability_id is required")
        if not self.audio_kinds:
            raise ValueError("audio_kinds must be non-empty")
        if len(set(self.audio_kinds)) != len(self.audio_kinds):
            raise ValueError("audio_kinds must be unique")
        if not self.capabilities:
            raise ValueError("capabilities must be non-empty")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")
        if any(not item.strip() for item in self.capabilities):
            raise ValueError("capabilities must be non-empty")


@dataclass(frozen=True)
class AudioTrack:
    track_id: str
    name: str
    audio_kind: AudioKind
    role: TrackRole

    def __post_init__(self) -> None:
        if not self.track_id.strip():
            raise ValueError("track_id is required")
        if not self.name.strip():
            raise ValueError("name is required")


@dataclass(frozen=True)
class AudioSession:
    session_id: str
    name: str
    audio_kinds: tuple[AudioKind, ...]
    tracks: tuple[AudioTrack, ...] = ()

    def __post_init__(self) -> None:
        if not self.session_id.strip():
            raise ValueError("session_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.audio_kinds:
            raise ValueError("audio_kinds must be non-empty")
        if len(set(self.audio_kinds)) != len(self.audio_kinds):
            raise ValueError("audio_kinds must be unique")
        track_ids = [track.track_id for track in self.tracks]
        if len(set(track_ids)) != len(track_ids):
            raise ValueError("track IDs must be unique")
        scope = set(self.audio_kinds)
        if any(track.audio_kind not in scope for track in self.tracks):
            raise ValueError("track audio kind is outside session scope")


@dataclass(frozen=True)
class AudioRoutingRequirement:
    requirement_id: str
    capability_kind: AudioCapabilityKind
    audio_kind: AudioKind
    required_capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.required_capabilities:
            raise ValueError("required_capabilities must be non-empty")
        if len(set(self.required_capabilities)) != len(self.required_capabilities):
            raise ValueError("required_capabilities must be unique")
        if any(not item.strip() for item in self.required_capabilities):
            raise ValueError("required_capabilities must be non-empty")


@dataclass(frozen=True)
class AudioPlan:
    session_id: str
    track_ids: tuple[str, ...]
    capability_ids: tuple[str, ...]
    requirement_ids: tuple[str, ...]


class MusicAudioPlanner:
    """Deterministic audio capability/routing planning only."""

    def normalize_tracks(self, tracks: tuple[AudioTrack, ...]) -> tuple[AudioTrack, ...]:
        ids = [track.track_id for track in tracks]
        if len(set(ids)) != len(ids):
            raise ValueError("track IDs must be unique")
        return tuple(sorted(tracks, key=lambda item: item.track_id))

    def normalize_capabilities(self, capabilities: tuple[AudioCapability, ...]) -> tuple[AudioCapability, ...]:
        ids = [item.capability_id for item in capabilities]
        if len(set(ids)) != len(ids):
            raise ValueError("capability IDs must be unique")
        return tuple(sorted(capabilities, key=lambda item: item.capability_id))

    def normalize_requirements(self, requirements: tuple[AudioRoutingRequirement, ...]) -> tuple[AudioRoutingRequirement, ...]:
        ids = [item.requirement_id for item in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def plan(
        self,
        session: AudioSession,
        capabilities: tuple[AudioCapability, ...],
        requirements: tuple[AudioRoutingRequirement, ...],
        max_capabilities: int = 8,
    ) -> AudioPlan:
        if max_capabilities <= 0:
            raise ValueError("max_capabilities must be positive")

        tracks = self.normalize_tracks(session.tracks)
        normalized_capabilities = self.normalize_capabilities(capabilities)
        normalized_requirements = self.normalize_requirements(requirements)
        scope = set(session.audio_kinds)
        selected: list[AudioCapability] = []

        for requirement in normalized_requirements:
            if requirement.audio_kind not in scope:
                raise ValueError("session lacks required audio kind")
            compatible = [
                capability for capability in normalized_capabilities
                if capability.kind == requirement.capability_kind
                and requirement.audio_kind in capability.audio_kinds
                and set(requirement.required_capabilities).issubset(set(capability.capabilities))
            ]
            if not compatible:
                raise ValueError("no compatible audio capability")
            selected.append(compatible[0])

        selected_ids = tuple(item.capability_id for item in selected)
        if len(set(selected_ids)) > max_capabilities:
            raise ValueError("audio plan exceeds capability limit")

        return AudioPlan(
            session_id=session.session_id,
            track_ids=tuple(track.track_id for track in tracks),
            capability_ids=selected_ids,
            requirement_ids=tuple(item.requirement_id for item in normalized_requirements),
        )
