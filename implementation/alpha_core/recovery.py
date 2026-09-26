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


class RecoveryKind(str, Enum):
    RESTORE = "restore"
    ROLLBACK = "rollback"
    REBUILD = "rebuild"


class BackupScope(str, Enum):
    CONFIGURATION = "configuration"
    STATE = "state"
    ARTIFACT = "artifact"
    FULL = "full"


class RecoveryDisposition(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


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
    policy_ids: tuple[str, ...] = ()
    denied_request_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class RecoveryResult:
    plan_id: str
    state: RecoveryState
    history: tuple[RecoveryState, ...]
    dry_run: bool
    evidence: dict[str, object]


@dataclass(frozen=True)
class RecoveryPolicy:
    policy_id: str
    kind: RecoveryKind
    scope: BackupScope
    retention_days: int
    requires_verified_backup: bool

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id is required")
        if self.retention_days < 0:
            raise ValueError("retention_days must be non-negative")


@dataclass(frozen=True)
class RecoveryRequest:
    request_id: str
    kind: RecoveryKind
    scope: BackupScope
    backup_verified: bool
    backup_age_days: int

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id is required")
        if self.backup_age_days < 0:
            raise ValueError("backup_age_days must be non-negative")


@dataclass(frozen=True)
class RecoveryDecision:
    request_id: str
    disposition: RecoveryDisposition
    policy_id: str | None


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

    def normalize(self, policies: tuple[RecoveryPolicy, ...]) -> tuple[RecoveryPolicy, ...]:
        ids = [policy.policy_id for policy in policies]
        if len(set(ids)) != len(ids):
            raise ValueError("policy IDs must be unique")
        return tuple(sorted(policies, key=lambda item: item.policy_id))

    def evaluate(self, policies: tuple[RecoveryPolicy, ...], request: RecoveryRequest) -> RecoveryDecision:
        for policy in self.normalize(policies):
            if policy.kind != request.kind or policy.scope != request.scope:
                continue
            if policy.requires_verified_backup and not request.backup_verified:
                return RecoveryDecision(request.request_id, RecoveryDisposition.DENY, policy.policy_id)
            if request.backup_age_days > policy.retention_days:
                return RecoveryDecision(request.request_id, RecoveryDisposition.DENY, policy.policy_id)
            return RecoveryDecision(request.request_id, RecoveryDisposition.ALLOW, policy.policy_id)
        return RecoveryDecision(request.request_id, RecoveryDisposition.DENY, None)

    def plan(self, checkpoint: RecoveryCheckpoint, requests: tuple[RecoveryRequest, ...] = ()) -> RecoveryPlan:
        if not checkpoint.checkpoint_id.strip():
            raise ValueError("checkpoint identity is required")
        return RecoveryPlan(
            plan_id=f"restore-{checkpoint.checkpoint_id}",
            checkpoint_id=checkpoint.checkpoint_id,
            dry_run=True,
            denied_request_ids=tuple(
                decision.request_id
                for decision in (
                    self.evaluate((), request)
                    for request in sorted(requests, key=lambda item: item.request_id)
                )
                if decision.disposition == RecoveryDisposition.DENY
            ),
        )

    def plan_with_policies(
        self,
        checkpoint: RecoveryCheckpoint,
        policies: tuple[RecoveryPolicy, ...],
        requests: tuple[RecoveryRequest, ...],
        max_policies: int = 16,
    ) -> RecoveryPlan:
        normalized = self.normalize(policies)
        if max_policies <= 0:
            raise ValueError("max_policies must be positive")
        if len(normalized) > max_policies:
            raise ValueError("recovery plan exceeds policy limit")
        decisions = tuple(
            self.evaluate(normalized, request)
            for request in sorted(requests, key=lambda item: item.request_id)
        )
        return RecoveryPlan(
            plan_id=f"restore-{checkpoint.checkpoint_id}",
            checkpoint_id=checkpoint.checkpoint_id,
            dry_run=True,
            policy_ids=tuple(policy.policy_id for policy in normalized),
            denied_request_ids=tuple(
                decision.request_id
                for decision in decisions
                if decision.disposition == RecoveryDisposition.DENY
            ),
        )


class RecoveryEngine:
    """Recovery orchestration independent of Control Center UI and authorization."""

    def __init__(self, backend: RecoveryBackend) -> None:
        self._backend = backend

    def execute(self, checkpoint: RecoveryCheckpoint, plan: RecoveryPlan) -> RecoveryResult:
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
