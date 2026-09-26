from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PermissionEffect(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class PermissionRule:
    rule_id: str
    capability: str
    effect: PermissionEffect

    def __post_init__(self) -> None:
        if not self.rule_id.strip():
            raise ValueError("rule_id is required")
        if not self.capability.strip():
            raise ValueError("capability is required")
        if not isinstance(self.effect, PermissionEffect):
            raise ValueError("effect must be a PermissionEffect")


@dataclass(frozen=True)
class PermissionRequest:
    capability: str

    def __post_init__(self) -> None:
        if not self.capability.strip():
            raise ValueError("capability is required")


@dataclass(frozen=True)
class PermissionDecision:
    capability: str
    effect: PermissionEffect
    rule_id: str | None


class PermissionPlanner:
    """Deterministic policy evaluation only; no authorization side effects."""

    def normalize(
        self, rules: tuple[PermissionRule, ...]
    ) -> tuple[PermissionRule, ...]:
        return tuple(sorted(rules, key=lambda rule: rule.rule_id))

    def evaluate(
        self,
        rules: tuple[PermissionRule, ...],
        request: PermissionRequest,
    ) -> PermissionDecision:
        normalized = self.normalize(rules)
        rule_ids = [rule.rule_id for rule in normalized]
        if len(set(rule_ids)) != len(rule_ids):
            raise ValueError("rule IDs must be unique")
        matches = [
            rule for rule in normalized if rule.capability == request.capability
        ]
        if not matches:
            return PermissionDecision(
                request.capability, PermissionEffect.DENY, None
            )
        rule = matches[0]
        return PermissionDecision(
            request.capability, rule.effect, rule.rule_id
        )
