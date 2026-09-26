from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class HardwareValidationDisposition(str, Enum):
    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True)
class HardwareCapability:
    capability_id: str
    device_class: str
    attributes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("capability_id is required")
        if not self.device_class.strip():
            raise ValueError("device_class is required")
        if len(set(self.attributes)) != len(self.attributes):
            raise ValueError("attributes must be unique")
        if any(not item.strip() for item in self.attributes):
            raise ValueError("attributes must be non-empty")


@dataclass(frozen=True)
class HardwareRequirement:
    requirement_id: str
    device_class: str
    required_attributes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.device_class.strip():
            raise ValueError("device_class is required")
        if len(set(self.required_attributes)) != len(self.required_attributes):
            raise ValueError("required_attributes must be unique")
        if any(not item.strip() for item in self.required_attributes):
            raise ValueError("required_attributes must be non-empty")


@dataclass(frozen=True)
class HardwareValidationDecision:
    requirement_id: str
    capability_id: str | None
    disposition: HardwareValidationDisposition


@dataclass(frozen=True)
class HardwareValidationPlan:
    capability_ids: tuple[str, ...]
    failed_requirement_ids: tuple[str, ...]


class HardwareValidationPlanner:
    """Deterministic hardware validation planning; no hardware probing or I/O."""

    def normalize_capabilities(self, capabilities: tuple[HardwareCapability, ...]) -> tuple[HardwareCapability, ...]:
        ids = [item.capability_id for item in capabilities]
        if len(set(ids)) != len(ids):
            raise ValueError("capability IDs must be unique")
        return tuple(sorted(capabilities, key=lambda item: item.capability_id))

    def normalize_requirements(self, requirements: tuple[HardwareRequirement, ...]) -> tuple[HardwareRequirement, ...]:
        ids = [item.requirement_id for item in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def evaluate(self, requirement: HardwareRequirement, capabilities: tuple[HardwareCapability, ...]) -> HardwareValidationDecision:
        needed = set(requirement.required_attributes)
        for capability in self.normalize_capabilities(capabilities):
            if capability.device_class != requirement.device_class:
                continue
            if needed.issubset(capability.attributes):
                return HardwareValidationDecision(requirement.requirement_id, capability.capability_id, HardwareValidationDisposition.PASS)
        return HardwareValidationDecision(requirement.requirement_id, None, HardwareValidationDisposition.FAIL)

    def plan(self, capabilities: tuple[HardwareCapability, ...], requirements: tuple[HardwareRequirement, ...], max_capabilities: int = 16) -> HardwareValidationPlan:
        if max_capabilities <= 0:
            raise ValueError("max_capabilities must be positive")
        normalized = self.normalize_capabilities(capabilities)
        if len(normalized) > max_capabilities:
            raise ValueError("hardware validation plan exceeds capability limit")
        decisions = tuple(self.evaluate(item, normalized) for item in self.normalize_requirements(requirements))
        return HardwareValidationPlan(
            capability_ids=tuple(item.capability_id for item in normalized),
            failed_requirement_ids=tuple(
                item.requirement_id for item in decisions
                if item.disposition == HardwareValidationDisposition.FAIL
            ),
        )
