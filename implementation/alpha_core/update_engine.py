from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from .system_integration import UpdatePlan


class UpdateState(str, Enum):
    CHECK = "check"
    RESOLVE = "resolve"
    SNAPSHOT = "snapshot"
    APPLY = "apply"
    HEALTH_CHECK = "health_check"
    KEEP = "keep"
    ROLLBACK = "rollback"


@dataclass(frozen=True)
class UpdateExecutionResult:
    plan_id: str
    state: UpdateState
    history: tuple[UpdateState, ...]
    dry_run: bool
    evidence: dict[str, object]


class UpdateBackend(Protocol):
    def check(self, plan: UpdatePlan) -> dict[str, object]: ...
    def resolve(self, plan: UpdatePlan) -> dict[str, object]: ...
    def snapshot(self, plan: UpdatePlan) -> dict[str, object]: ...
    def apply(self, plan: UpdatePlan) -> dict[str, object]: ...
    def health_check(self, plan: UpdatePlan) -> bool: ...
    def rollback(self, plan: UpdatePlan) -> dict[str, object]: ...


class ReferenceUpdateBackend:
    """Deterministic, non-mutating backend used until privileged OS adapters exist."""

    def __init__(self, *, health_ok: bool = True) -> None:
        self.health_ok = health_ok

    def check(self, plan: UpdatePlan) -> dict[str, object]:
        return {"checked": True, "dry_run": plan.dry_run}

    def resolve(self, plan: UpdatePlan) -> dict[str, object]:
        return {"resolved_actions": len(plan.package_actions)}

    def snapshot(self, plan: UpdatePlan) -> dict[str, object]:
        return {"snapshot": "reference-no-op", "created": False}

    def apply(self, plan: UpdatePlan) -> dict[str, object]:
        return {"applied": False, "reason": "privileged backend not configured"}

    def health_check(self, plan: UpdatePlan) -> bool:
        return self.health_ok

    def rollback(self, plan: UpdatePlan) -> dict[str, object]:
        return {"rolled_back": False, "reason": "privileged backend not configured"}


class UpdateEngine:
    """Transactional update state machine; authorization and mutation remain external."""

    _ORDER = (
        UpdateState.CHECK,
        UpdateState.RESOLVE,
        UpdateState.SNAPSHOT,
        UpdateState.APPLY,
        UpdateState.HEALTH_CHECK,
        UpdateState.KEEP,
    )

    def __init__(self, backend: UpdateBackend) -> None:
        self._backend = backend

    def execute(self, plan: UpdatePlan) -> UpdateExecutionResult:
        if not plan.plan_id.strip():
            raise ValueError("update plan identity is required")
        history: list[UpdateState] = []
        evidence: dict[str, object] = {}

        self._enter(UpdateState.CHECK, history)
        evidence["check"] = self._backend.check(plan)

        self._enter(UpdateState.RESOLVE, history)
        evidence["resolve"] = self._backend.resolve(plan)

        self._enter(UpdateState.SNAPSHOT, history)
        evidence["snapshot"] = self._backend.snapshot(plan)

        self._enter(UpdateState.APPLY, history)
        evidence["apply"] = self._backend.apply(plan)

        self._enter(UpdateState.HEALTH_CHECK, history)
        healthy = self._backend.health_check(plan)
        evidence["health_check"] = {"healthy": healthy}

        if healthy:
            self._enter(UpdateState.KEEP, history)
            return UpdateExecutionResult(
                plan.plan_id, UpdateState.KEEP, tuple(history), plan.dry_run, evidence
            )

        self._enter(UpdateState.ROLLBACK, history)
        evidence["rollback"] = self._backend.rollback(plan)
        return UpdateExecutionResult(
            plan.plan_id, UpdateState.ROLLBACK, tuple(history), plan.dry_run, evidence
        )

    @staticmethod
    def _enter(state: UpdateState, history: list[UpdateState]) -> None:
        history.append(state)
