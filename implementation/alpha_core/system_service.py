from dataclasses import dataclass
from typing import Callable, Mapping

from .models import ActionRequest, HealthResult
from .policy import PolicyEngine


@dataclass(frozen=True)
class ServiceResult:
    success: bool
    action_id: str
    message: str
    evidence: Mapping[str, object]


class SystemService:
    """Non-privileged reference service boundary.

    Real privileged backends must remain behind OS-enforced authorization.
    This class never treats agent/model/UI output as authorization.
    """

    def __init__(self, policy: PolicyEngine):
        self._policy = policy

    def execute(
        self,
        request: ActionRequest,
        *,
        approved: bool = False,
        handler: Callable[[ActionRequest], Mapping[str, object]],
    ) -> ServiceResult:
        decision = self._policy.decide(request, approved=approved)
        if not decision.allowed:
            raise PermissionError(decision.reason)

        evidence = dict(handler(request))
        return ServiceResult(
            success=True,
            action_id=request.action_id,
            message="operation completed",
            evidence=evidence,
        )

    def health(self) -> HealthResult:
        return HealthResult("system-service", True, {"authorization": "policy-engine"})
