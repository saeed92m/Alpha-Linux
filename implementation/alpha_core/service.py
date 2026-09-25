from dataclasses import dataclass
from typing import Callable

from .models import ActionDecision, ActionRequest
from .policy import PolicyEngine


@dataclass(frozen=True)
class OperationResult:
    action_id: str
    executed: bool
    verified: bool
    decision: ActionDecision
    evidence: dict[str, object]


class AlphaService:
    """Minimal service boundary: authorize, execute a supplied safe handler, verify."""

    def __init__(self, policy: PolicyEngine | None = None):
        self.policy = policy or PolicyEngine()

    def execute(
        self,
        request: ActionRequest,
        handler: Callable[[], object],
        *,
        approved: bool = False,
        verifier: Callable[[object], bool] | None = None,
    ) -> OperationResult:
        decision = self.policy.decide(request, approved=approved)
        if not decision.allowed:
            return OperationResult(request.action_id, False, False, decision, {})

        result = handler()
        verified = True if verifier is None else bool(verifier(result))
        return OperationResult(
            request.action_id,
            True,
            verified,
            decision,
            {"handler_result": result},
        )
