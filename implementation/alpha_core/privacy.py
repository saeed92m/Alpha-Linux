from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PrivacyClassification(str, Enum):
    PUBLIC = "public"
    PERSONAL = "personal"
    SENSITIVE = "sensitive"
    RESTRICTED = "restricted"


class PrivacyPurpose(str, Enum):
    OPERATION = "operation"
    ANALYSIS = "analysis"
    RESEARCH = "research"
    SUPPORT = "support"


class PrivacyDisposition(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class PrivacyPolicy:
    policy_id: str
    purpose: PrivacyPurpose
    classification: PrivacyClassification
    retention_days: int
    consent_required: bool

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id is required")
        if self.retention_days < 0:
            raise ValueError("retention_days must be non-negative")


@dataclass(frozen=True)
class PrivacyRequest:
    request_id: str
    purpose: PrivacyPurpose | None
    consent_granted: bool
    age_days: int

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id is required")
        if self.age_days < 0:
            raise ValueError("age_days must be non-negative")


@dataclass(frozen=True)
class PrivacyDecision:
    request_id: str
    disposition: PrivacyDisposition
    policy_id: str | None


@dataclass(frozen=True)
class PrivacyPlan:
    policy_ids: tuple[str, ...]
    denied_request_ids: tuple[str, ...]


class PrivacyPlanner:
    """Deterministic privacy policy planning only; no privacy side effects."""

    def normalize(
        self, policies: tuple[PrivacyPolicy, ...]
    ) -> tuple[PrivacyPolicy, ...]:
        ids = [policy.policy_id for policy in policies]
        if len(set(ids)) != len(ids):
            raise ValueError("policy IDs must be unique")
        return tuple(sorted(policies, key=lambda item: item.policy_id))

    def evaluate(
        self,
        policies: tuple[PrivacyPolicy, ...],
        request: PrivacyRequest,
    ) -> PrivacyDecision:
        for policy in self.normalize(policies):
            if policy.purpose != request.purpose:
                continue
            if policy.consent_required and not request.consent_granted:
                return PrivacyDecision(
                    request.request_id, PrivacyDisposition.DENY, policy.policy_id
                )
            if request.age_days > policy.retention_days:
                return PrivacyDecision(
                    request.request_id, PrivacyDisposition.DENY, policy.policy_id
                )
            return PrivacyDecision(
                request.request_id, PrivacyDisposition.ALLOW, policy.policy_id
            )
        return PrivacyDecision(request.request_id, PrivacyDisposition.DENY, None)

    def plan(
        self,
        policies: tuple[PrivacyPolicy, ...],
        requests: tuple[PrivacyRequest, ...],
        max_policies: int = 16,
    ) -> PrivacyPlan:
        if max_policies <= 0:
            raise ValueError("max_policies must be positive")
        normalized = self.normalize(policies)
        if len(normalized) > max_policies:
            raise ValueError("privacy plan exceeds policy limit")
        decisions = tuple(
            self.evaluate(normalized, request) for request in sorted(
                requests, key=lambda item: item.request_id
            )
        )
        return PrivacyPlan(
            policy_ids=tuple(policy.policy_id for policy in normalized),
            denied_request_ids=tuple(
                decision.request_id
                for decision in decisions
                if decision.disposition == PrivacyDisposition.DENY
            ),
        )
