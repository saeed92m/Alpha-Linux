from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SecurityClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    SENSITIVE = "sensitive"
    RESTRICTED = "restricted"


class SecurityControlKind(str, Enum):
    AUTHORIZATION = "authorization"
    INTEGRITY = "integrity"
    PRIVACY = "privacy"
    RECOVERY = "recovery"


class SecurityDisposition(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class SecurityControl:
    control_id: str
    kind: SecurityControlKind
    classification: SecurityClassification
    actions: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.control_id.strip():
            raise ValueError("control_id is required")
        if not self.actions:
            raise ValueError("actions must be non-empty")
        if len(set(self.actions)) != len(self.actions):
            raise ValueError("actions must be unique")
        if any(not action.strip() for action in self.actions):
            raise ValueError("actions must be non-empty")


@dataclass(frozen=True)
class SecurityAuditEvent:
    event_id: str
    action: str
    classification: SecurityClassification
    disposition: SecurityDisposition
    control_id: str | None = None

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id is required")
        if not self.action.strip():
            raise ValueError("action is required")
        if not isinstance(self.disposition, SecurityDisposition):
            raise ValueError("disposition must be a SecurityDisposition")


@dataclass(frozen=True)
class SecurityHardeningPlan:
    controls: tuple[str, ...]
    events: tuple[str, ...]


class SecurityHardeningPlanner:
    """Deterministic security-hardening planning only; no live enforcement."""

    def normalize_controls(
        self, controls: tuple[SecurityControl, ...]
    ) -> tuple[SecurityControl, ...]:
        ids = [control.control_id for control in controls]
        if len(set(ids)) != len(ids):
            raise ValueError("control IDs must be unique")
        return tuple(sorted(controls, key=lambda item: item.control_id))

    def normalize_events(
        self, events: tuple[SecurityAuditEvent, ...]
    ) -> tuple[SecurityAuditEvent, ...]:
        ids = [event.event_id for event in events]
        if len(set(ids)) != len(ids):
            raise ValueError("event IDs must be unique")
        return tuple(sorted(events, key=lambda item: item.event_id))

    def plan(
        self,
        actions: tuple[str, ...],
        controls: tuple[SecurityControl, ...],
        max_controls: int = 16,
    ) -> SecurityHardeningPlan:
        if max_controls <= 0:
            raise ValueError("max_controls must be positive")
        normalized = self.normalize_controls(controls)
        requested = tuple(sorted(set(actions)))
        if any(not action.strip() for action in actions):
            raise ValueError("actions must be non-empty")

        selected: list[SecurityControl] = []
        for action in requested:
            matches = [
                control for control in normalized if action in control.actions
            ]
            if not matches:
                continue
            selected.append(matches[0])

        selected_ids = tuple(control.control_id for control in selected)
        if len(selected_ids) > max_controls:
            raise ValueError("security plan exceeds control limit")

        return SecurityHardeningPlan(
            controls=selected_ids,
            events=tuple(f"deny:{action}" for action in requested if action and
                         action not in {
                             item for control in selected for item in control.actions
                         }),
        )
