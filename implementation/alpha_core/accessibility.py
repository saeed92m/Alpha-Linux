from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AccessibilityDisposition(str, Enum):
    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True)
class AccessibilityCapability:
    capability_id: str
    category: str
    features: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("capability_id is required")
        if not self.category.strip():
            raise ValueError("category is required")
        if len(set(self.features)) != len(self.features):
            raise ValueError("features must be unique")
        if any(not item.strip() for item in self.features):
            raise ValueError("features must be non-empty")


@dataclass(frozen=True)
class AccessibilityRequirement:
    requirement_id: str
    category: str
    required_features: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.category.strip():
            raise ValueError("category is required")
        if len(set(self.required_features)) != len(self.required_features):
            raise ValueError("required_features must be unique")
        if any(not item.strip() for item in self.required_features):
            raise ValueError("required_features must be non-empty")


@dataclass(frozen=True)
class AccessibilityDecision:
    requirement_id: str
    capability_id: str | None
    disposition: AccessibilityDisposition


@dataclass(frozen=True)
class AccessibilityPlan:
    capability_ids: tuple[str, ...]
    failed_requirement_ids: tuple[str, ...]


class AccessibilityPlanner:
    """Deterministic accessibility planning only; no UI probing or mutation."""

    def normalize_capabilities(self, capabilities: tuple[AccessibilityCapability, ...]) -> tuple[AccessibilityCapability, ...]:
        ids = [item.capability_id for item in capabilities]
        if len(set(ids)) != len(ids):
            raise ValueError("capability IDs must be unique")
        return tuple(sorted(capabilities, key=lambda item: item.capability_id))

    def normalize_requirements(self, requirements: tuple[AccessibilityRequirement, ...]) -> tuple[AccessibilityRequirement, ...]:
        ids = [item.requirement_id for item in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def evaluate(self, requirement: AccessibilityRequirement, capabilities: tuple[AccessibilityCapability, ...]) -> AccessibilityDecision:
        needed = set(requirement.required_features)
        for capability in self.normalize_capabilities(capabilities):
            if capability.category != requirement.category:
                continue
            if needed.issubset(capability.features):
                return AccessibilityDecision(requirement.requirement_id, capability.capability_id, AccessibilityDisposition.PASS)
        return AccessibilityDecision(requirement.requirement_id, None, AccessibilityDisposition.FAIL)

    def plan(self, capabilities: tuple[AccessibilityCapability, ...], requirements: tuple[AccessibilityRequirement, ...], max_capabilities: int = 16) -> AccessibilityPlan:
        if max_capabilities <= 0:
            raise ValueError("max_capabilities must be positive")
        normalized = self.normalize_capabilities(capabilities)
        if len(normalized) > max_capabilities:
            raise ValueError("accessibility plan exceeds capability limit")
        decisions = tuple(self.evaluate(item, normalized) for item in self.normalize_requirements(requirements))
        return AccessibilityPlan(
            capability_ids=tuple(item.capability_id for item in normalized),
            failed_requirement_ids=tuple(
                item.requirement_id for item in decisions
                if item.disposition == AccessibilityDisposition.FAIL
            ),
        )
