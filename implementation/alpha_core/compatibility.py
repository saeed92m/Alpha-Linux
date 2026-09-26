from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CompatibilityDisposition(str, Enum):
    COMPATIBLE = "compatible"
    INCOMPATIBLE = "incompatible"


@dataclass(frozen=True)
class CompatibilityTarget:
    target_id: str
    platform: str
    version: str
    capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id is required")
        if not self.platform.strip():
            raise ValueError("platform is required")
        if not self.version.strip():
            raise ValueError("version is required")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")
        if any(not item.strip() for item in self.capabilities):
            raise ValueError("capabilities must be non-empty")


@dataclass(frozen=True)
class CompatibilityRequirement:
    requirement_id: str
    platform: str
    minimum_version: str
    required_capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.platform.strip():
            raise ValueError("platform is required")
        if not self.minimum_version.strip():
            raise ValueError("minimum_version is required")
        if len(set(self.required_capabilities)) != len(self.required_capabilities):
            raise ValueError("required_capabilities must be unique")
        if any(not item.strip() for item in self.required_capabilities):
            raise ValueError("required_capabilities must be non-empty")


@dataclass(frozen=True)
class CompatibilityDecision:
    requirement_id: str
    target_id: str | None
    disposition: CompatibilityDisposition
    missing_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True)
class CompatibilityPlan:
    target_ids: tuple[str, ...]
    incompatible_requirement_ids: tuple[str, ...]


def _version_parts(value: str) -> tuple[int | str, ...]:
    parts: list[int | str] = []
    for token in value.strip().replace("-", ".").split("."):
        if not token:
            continue
        parts.append(int(token) if token.isdigit() else token.lower())
    return tuple(parts)


class CompatibilityPlanner:
    """Deterministic compatibility planning only; no host probing or mutation."""

    def normalize_targets(self, targets: tuple[CompatibilityTarget, ...]) -> tuple[CompatibilityTarget, ...]:
        ids = [item.target_id for item in targets]
        if len(set(ids)) != len(ids):
            raise ValueError("target IDs must be unique")
        return tuple(sorted(targets, key=lambda item: item.target_id))

    def normalize_requirements(self, requirements: tuple[CompatibilityRequirement, ...]) -> tuple[CompatibilityRequirement, ...]:
        ids = [item.requirement_id for item in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def evaluate(self, requirement: CompatibilityRequirement, targets: tuple[CompatibilityTarget, ...]) -> CompatibilityDecision:
        for target in self.normalize_targets(targets):
            if target.platform != requirement.platform:
                continue
            if _version_parts(target.version) < _version_parts(requirement.minimum_version):
                continue
            missing = tuple(sorted(set(requirement.required_capabilities) - set(target.capabilities)))
            if missing:
                continue
            return CompatibilityDecision(requirement.requirement_id, target.target_id, CompatibilityDisposition.COMPATIBLE)
        return CompatibilityDecision(requirement.requirement_id, None, CompatibilityDisposition.INCOMPATIBLE)

    def plan(self, targets: tuple[CompatibilityTarget, ...], requirements: tuple[CompatibilityRequirement, ...], max_targets: int = 16) -> CompatibilityPlan:
        if max_targets <= 0:
            raise ValueError("max_targets must be positive")
        normalized_targets = self.normalize_targets(targets)
        if len(normalized_targets) > max_targets:
            raise ValueError("compatibility plan exceeds target limit")
        decisions = tuple(self.evaluate(requirement, normalized_targets) for requirement in self.normalize_requirements(requirements))
        return CompatibilityPlan(
            target_ids=tuple(item.target_id for item in normalized_targets),
            incompatible_requirement_ids=tuple(
                item.requirement_id for item in decisions
                if item.disposition == CompatibilityDisposition.INCOMPATIBLE
            ),
        )
