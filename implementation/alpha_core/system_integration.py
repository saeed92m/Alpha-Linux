from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from platform import machine, platform, processor
from typing import Mapping


class HealthState(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"


@dataclass(frozen=True)
class ComponentHealth:
    component: str
    state: HealthState
    evidence: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class DiagnosticFinding:
    finding_id: str
    severity: str
    component: str
    message: str
    evidence: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class UpdatePlan:
    plan_id: str
    package_actions: tuple[str, ...]
    requires_privilege: bool
    dry_run: bool = True


class ConfigurationStore:
    """Typed namespaced state store; it is not a secrets or authorization store."""

    def __init__(self) -> None:
        self._values: dict[str, object] = {}

    def set(self, namespace: str, key: str, value: object) -> None:
        if not namespace.strip() or not key.strip():
            raise ValueError("namespace and key are required")
        self._values[f"{namespace}.{key}"] = value

    def get(self, namespace: str, key: str, default: object = None) -> object:
        return self._values.get(f"{namespace}.{key}", default)

    def delete(self, namespace: str, key: str) -> None:
        self._values.pop(f"{namespace}.{key}", None)


class SystemDiscovery:
    """Read-only host discovery with no privileged operations."""

    def snapshot(self) -> Mapping[str, object]:
        return {
            "machine": machine(),
            "platform": platform(),
            "processor": processor(),
        }


class DiagnosticsEngine:
    def evaluate(self, health: ComponentHealth) -> tuple[DiagnosticFinding, ...]:
        if health.state is HealthState.HEALTHY:
            return ()
        severity = "error" if health.state is HealthState.FAILED else "warning"
        return (
            DiagnosticFinding(
                finding_id=f"diag.{health.component}.{health.state.value}",
                severity=severity,
                component=health.component,
                message=f"component is {health.state.value}",
                evidence=dict(health.evidence),
            ),
        )


class UpdatePlanner:
    """Reference planner; creates dry-run plans and never mutates host packages."""

    def plan(self, package_actions: tuple[str, ...], *, requires_privilege: bool = True) -> UpdatePlan:
        if any(not action.strip() for action in package_actions):
            raise ValueError("package actions must be non-empty")
        return UpdatePlan(
            plan_id="update-plan",
            package_actions=tuple(package_actions),
            requires_privilege=requires_privilege,
            dry_run=True,
        )


class HealthAggregator:
    def aggregate(self, components: tuple[ComponentHealth, ...]) -> ComponentHealth:
        if not components:
            return ComponentHealth("system", HealthState.DEGRADED, {"reason": "no components"})
        states = {component.state for component in components}
        if HealthState.FAILED in states:
            state = HealthState.FAILED
        elif HealthState.DEGRADED in states:
            state = HealthState.DEGRADED
        else:
            state = HealthState.HEALTHY
        return ComponentHealth(
            "system",
            state,
            {"components": {c.component: c.state.value for c in components}},
        )
