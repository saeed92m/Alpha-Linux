from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


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


@dataclass(frozen=True)
class RecoveryPlan:
    policy_ids: tuple[str, ...]
    denied_request_ids: tuple[str, ...]


class RecoveryPlanner:
    """Deterministic recovery and backup planning only; no side effects."""

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

    def plan(
        self,
        policies: tuple[RecoveryPolicy, ...],
        requests: tuple[RecoveryRequest, ...],
        max_policies: int = 16,
    ) -> RecoveryPlan:
        if max_policies <= 0:
            raise ValueError("max_policies must be positive")
        normalized = self.normalize(policies)
        if len(normalized) > max_policies:
            raise ValueError("recovery plan exceeds policy limit")
        decisions = tuple(
            self.evaluate(normalized, request)
            for request in sorted(requests, key=lambda item: item.request_id)
        )
        return RecoveryPlan(
            policy_ids=tuple(policy.policy_id for policy in normalized),
            denied_request_ids=tuple(
                decision.request_id
                for decision in decisions
                if decision.disposition == RecoveryDisposition.DENY
            ),
        )
