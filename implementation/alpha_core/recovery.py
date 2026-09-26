from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
from typing import Protocol


class RecoveryState(str, Enum):
    CHECKPOINT = "checkpoint"
    PREPARE = "prepare"
    RESTORE = "restore"
    VERIFY = "verify"
    KEEP = "keep"
    FAIL = "fail"


@dataclass(frozen=True)
class RecoveryCheckpoint:
    checkpoint_id: str
    label: str
    source: str = "reference"


@dataclass(frozen=True)
class RecoveryPlan:
    plan_id: str
    checkpoint_id: str
    dry_run: bool = True


@dataclass(frozen=True)
class RecoveryResult:
    plan_id: str
    state: RecoveryState
    history: tuple[RecoveryState, ...]
    dry_run: bool
    evidence: dict[str, object]


class RecoveryBackend(Protocol):
    def checkpoint(self, checkpoint: RecoveryCheckpoint) -> dict[str, object]: ...
    def prepare(self, plan: RecoveryPlan) -> dict[str, object]: ...
    def restore(self, plan: RecoveryPlan) -> dict[str, object]: ...
    def verify(self, plan: RecoveryPlan) -> bool: ...


class ReferenceRecoveryBackend:
    """Non-mutating backend for recovery orchestration until OS adapters exist."""

    def __init__(self, *, verification_ok: bool = True) -> None:
        self.verification_ok = verification_ok

    def checkpoint(self, checkpoint: RecoveryCheckpoint) -> dict[str, object]:
        return {"created": False, "reason": "reference-no-op", "checkpoint_id": checkpoint.checkpoint_id}

    def prepare(self, plan: RecoveryPlan) -> dict[str, object]:
        return {"prepared": True, "checkpoint_id": plan.checkpoint_id}

    def restore(self, plan: RecoveryPlan) -> dict[str, object]:
        return {"restored": False, "reason": "privileged recovery backend not configured"}

    def verify(self, plan: RecoveryPlan) -> bool:
        return self.verification_ok


class RecoveryPlanner:
    def checkpoint(self, label: str) -> RecoveryCheckpoint:
        normalized = label.strip()
        if not normalized:
            raise ValueError("checkpoint label is required")
        identity = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
        return RecoveryCheckpoint(checkpoint_id=f"checkpoint-{identity}", label=normalized)

    def plan(self, checkpoint: RecoveryCheckpoint) -> RecoveryPlan:
        if not checkpoint.checkpoint_id.strip():
            raise ValueError("checkpoint identity is required")
        return RecoveryPlan(
            plan_id=f"restore-{checkpoint.checkpoint_id}",
            checkpoint_id=checkpoint.checkpoint_id,
            dry_run=True,
        )


class RecoveryEngine:
    """Recovery orchestration independent of Control Center UI and authorization."""

    def __init__(self, backend: RecoveryBackend) -> None:
        self._backend = backend

    def execute(
        self,
        checkpoint: RecoveryCheckpoint,
        plan: RecoveryPlan,
    ) -> RecoveryResult:
        if plan.checkpoint_id != checkpoint.checkpoint_id:
            raise ValueError("recovery plan/checkpoint mismatch")

        history: list[RecoveryState] = []
        evidence: dict[str, object] = {}

        history.append(RecoveryState.CHECKPOINT)
        evidence["checkpoint"] = self._backend.checkpoint(checkpoint)

        history.append(RecoveryState.PREPARE)
        evidence["prepare"] = self._backend.prepare(plan)

        history.append(RecoveryState.RESTORE)
        evidence["restore"] = self._backend.restore(plan)

        history.append(RecoveryState.VERIFY)
        verified = self._backend.verify(plan)
        evidence["verify"] = {"verified": verified}

        if not verified:
            history.append(RecoveryState.FAIL)
            return RecoveryResult(plan.plan_id, RecoveryState.FAIL, tuple(history), plan.dry_run, evidence)

        history.append(RecoveryState.KEEP)
        return RecoveryResult(plan.plan_id, RecoveryState.KEEP, tuple(history), plan.dry_run, evidence)
