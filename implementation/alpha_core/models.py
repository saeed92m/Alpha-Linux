from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class PermissionLevel(str, Enum):
    EXPLAIN = "explain"
    READ = "read"
    SUGGEST = "suggest"
    EXECUTE_SAFE = "execute_safe"
    EXECUTE_APPROVAL = "execute_approval"
    RESTRICTED_ADMIN = "restricted_admin"


@dataclass(frozen=True)
class ActionRequest:
    action_id: str
    actor: str
    description: str
    permission: PermissionLevel
    parameters: Mapping[str, object]


@dataclass(frozen=True)
class ActionDecision:
    allowed: bool
    reason: str
    policy_id: str


@dataclass(frozen=True)
class HealthResult:
    component: str
    healthy: bool
    evidence: Mapping[str, object]
