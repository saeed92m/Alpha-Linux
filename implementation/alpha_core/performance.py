from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PerformanceDisposition(str, Enum):
    MEETS_TARGET = "meets_target"
    MISSES_TARGET = "misses_target"


@dataclass(frozen=True)
class PerformanceTarget:
    target_id: str
    workload: str
    latency_ms: float
    throughput_per_second: float
    resource_budget: float

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id is required")
        if not self.workload.strip():
            raise ValueError("workload is required")
        if self.latency_ms < 0:
            raise ValueError("latency_ms must be non-negative")
        if self.throughput_per_second < 0:
            raise ValueError("throughput_per_second must be non-negative")
        if self.resource_budget < 0:
            raise ValueError("resource_budget must be non-negative")


@dataclass(frozen=True)
class PerformanceRequirement:
    requirement_id: str
    workload: str
    max_latency_ms: float
    min_throughput_per_second: float
    max_resource_budget: float

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.workload.strip():
            raise ValueError("workload is required")
        if self.max_latency_ms < 0:
            raise ValueError("max_latency_ms must be non-negative")
        if self.min_throughput_per_second < 0:
            raise ValueError("min_throughput_per_second must be non-negative")
        if self.max_resource_budget < 0:
            raise ValueError("max_resource_budget must be non-negative")


@dataclass(frozen=True)
class PerformanceDecision:
    requirement_id: str
    target_id: str | None
    disposition: PerformanceDisposition


@dataclass(frozen=True)
class PerformancePlan:
    target_ids: tuple[str, ...]
    missed_requirement_ids: tuple[str, ...]


class PerformancePlanner:
    """Deterministic performance planning only; no benchmarking or host probing."""

    def normalize_targets(self, targets: tuple[PerformanceTarget, ...]) -> tuple[PerformanceTarget, ...]:
        ids = [item.target_id for item in targets]
        if len(set(ids)) != len(ids):
            raise ValueError("target IDs must be unique")
        return tuple(sorted(targets, key=lambda item: item.target_id))

    def normalize_requirements(self, requirements: tuple[PerformanceRequirement, ...]) -> tuple[PerformanceRequirement, ...]:
        ids = [item.requirement_id for item in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def evaluate(self, requirement: PerformanceRequirement, targets: tuple[PerformanceTarget, ...]) -> PerformanceDecision:
        for target in self.normalize_targets(targets):
            if target.workload != requirement.workload:
                continue
            if target.latency_ms > requirement.max_latency_ms:
                continue
            if target.throughput_per_second < requirement.min_throughput_per_second:
                continue
            if target.resource_budget > requirement.max_resource_budget:
                continue
            return PerformanceDecision(requirement.requirement_id, target.target_id, PerformanceDisposition.MEETS_TARGET)
        return PerformanceDecision(requirement.requirement_id, None, PerformanceDisposition.MISSES_TARGET)

    def plan(self, targets: tuple[PerformanceTarget, ...], requirements: tuple[PerformanceRequirement, ...], max_targets: int = 16) -> PerformancePlan:
        if max_targets <= 0:
            raise ValueError("max_targets must be positive")
        normalized = self.normalize_targets(targets)
        if len(normalized) > max_targets:
            raise ValueError("performance plan exceeds target limit")
        decisions = tuple(self.evaluate(item, normalized) for item in self.normalize_requirements(requirements))
        return PerformancePlan(
            target_ids=tuple(item.target_id for item in normalized),
            missed_requirement_ids=tuple(
                item.requirement_id for item in decisions
                if item.disposition == PerformanceDisposition.MISSES_TARGET
            ),
        )
