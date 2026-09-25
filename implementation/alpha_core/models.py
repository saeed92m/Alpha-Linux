from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class PermissionLevel(str, Enum):
    EXPLAIN = "explain"
    READ = "read"
    SUGGEST = "suggest"
    EXECUTE_SAFE = "execute_safe"
    EXECUTE_APPROVAL = "execute_approval"
    RESTRICTED_ADMIN = "restricted_admin"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class ActionRequest:
    action_id: str
    actor: str
    description: str
    permission: PermissionLevel
    target: str
    required_capability: str | None = None
    capabilities: frozenset[str] = field(default_factory=frozenset)
    risk: RiskLevel = RiskLevel.LOW
    parameters: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionDecision:
    allowed: bool
    reason: str
    policy_id: str
    requires_approval: bool = False


@dataclass(frozen=True)
class HealthResult:
    component: str
    healthy: bool
    evidence: Mapping[str, object]
