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


class BackupScope(str, Enum):
    CONFIGURATION = "configuration"
    STATE = "state"
    ARTIFACT = "artifact"
    FULL = "full"


class RecoveryBackupDisposition(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class RecoveryBackupPolicy:
    policy_id: str
    recovery_state: RecoveryState
    scope: BackupScope
    retention_days: int
    requires_verified_backup: bool

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id is required")
        if self.retention_days < 0:
            raise ValueError("retention_days must be non-negative")


@dataclass(frozen=True)
class RecoveryBackupRequest:
    request_id: str
    recovery_state: RecoveryState
    scope: BackupScope
    backup_verified: bool
    backup_age_days: int

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id is required")
        if self.backup_age_days < 0:
            raise ValueError("backup_age_days must be non-negative")


@dataclass(frozen=True)
class RecoveryBackupDecision:
    request_id: str
    disposition: RecoveryBackupDisposition
    policy_id: str | None


@dataclass(frozen=True)
class RecoveryBackupPlanningResult:
    policy_ids: tuple[str, ...]
    denied_request_ids: tuple[str, ...]


class RecoveryBackupPlanner:
    """Deterministic recovery/backup policy planning; no side effects."""

    def normalize(
        self, policies: tuple[RecoveryBackupPolicy, ...]
    ) -> tuple[RecoveryBackupPolicy, ...]:
        ids = [policy.policy_id for policy in policies]
        if len(set(ids)) != len(ids):
            raise ValueError("policy IDs must be unique")
        return tuple(sorted(policies, key=lambda item: item.policy_id))

    def evaluate(
        self,
        policies: tuple[RecoveryBackupPolicy, ...],
        request: RecoveryBackupRequest,
    ) -> RecoveryBackupDecision:
        for policy in self.normalize(policies):
            if policy.recovery_state != request.recovery_state or policy.scope != request.scope:
                continue
            if policy.requires_verified_backup and not request.backup_verified:
                return RecoveryBackupDecision(
                    request.request_id, RecoveryBackupDisposition.DENY, policy.policy_id
                )
            if request.backup_age_days > policy.retention_days:
                return RecoveryBackupDecision(
                    request.request_id, RecoveryBackupDisposition.DENY, policy.policy_id
                )
            return RecoveryBackupDecision(
                request.request_id, RecoveryBackupDisposition.ALLOW, policy.policy_id
            )
        return RecoveryBackupDecision(
            request.request_id, RecoveryBackupDisposition.DENY, None
        )

    def plan(
        self,
        policies: tuple[RecoveryBackupPolicy, ...],
        requests: tuple[RecoveryBackupRequest, ...],
        max_policies: int = 16,
    ) -> RecoveryBackupPlanningResult:
        if max_policies <= 0:
            raise ValueError("max_policies must be positive")
        normalized = self.normalize(policies)
        if len(normalized) > max_policies:
            raise ValueError("recovery plan exceeds policy limit")
        decisions = tuple(
            self.evaluate(normalized, request)
            for request in sorted(requests, key=lambda item: item.request_id)
        )
        return RecoveryBackupPlanningResult(
            policy_ids=tuple(policy.policy_id for policy in normalized),
            denied_request_ids=tuple(
                decision.request_id
                for decision in decisions
                if decision.disposition == RecoveryBackupDisposition.DENY
            ),
        )
