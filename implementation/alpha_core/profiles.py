from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Profile:
    profile_id: str
    name: str
    description: str
    settings: Mapping[str, object]

    def __post_init__(self) -> None:
        if not self.profile_id.strip():
            raise ValueError("profile_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.description.strip():
            raise ValueError("description is required")
        for key in self.settings:
            if not isinstance(key, str) or not key.strip() or "." not in key:
                raise ValueError("profile setting keys must be non-empty namespaced strings")


class ProfileRegistry:
    """Deterministic declarative profile registry; profiles never authorize actions."""

    def __init__(self, profiles: tuple[Profile, ...] = ()) -> None:
        ordered = tuple(sorted(profiles, key=lambda profile: profile.profile_id))
        ids = [profile.profile_id for profile in ordered]
        if len(ids) != len(set(ids)):
            raise ValueError("profile identifiers must be unique")
        self._profiles = ordered

    def list(self) -> tuple[Profile, ...]:
        return self._profiles

    def get(self, profile_id: str) -> Profile | None:
        return next((profile for profile in self._profiles if profile.profile_id == profile_id), None)


class ProfileResolver:
    """Resolves declarative overlays without granting authorization or mutating the host."""

    def __init__(self, registry: ProfileRegistry) -> None:
        self._registry = registry

    def resolve(self, profile_ids: tuple[str, ...]) -> Mapping[str, object]:
        resolved: dict[str, object] = {}
        for profile_id in profile_ids:
            profile = self._registry.get(profile_id)
            if profile is None:
                continue
            for key in sorted(profile.settings):
                resolved[key] = profile.settings[key]
        return dict(resolved)
