from enum import Enum

from .models import ActionDecision, ActionRequest, PermissionLevel


class AgentStage(str, Enum):
    UNDERSTAND = "understand"
    INSPECT = "inspect"
    PLAN = "plan"
    AUTHORIZE = "authorize"
    EXECUTE = "execute"
    VERIFY = "verify"
    REPORT = "report"


class AgentRuntime:
    """Minimal state machine enforcing authorization and verification ordering."""

    ORDER = (
        AgentStage.UNDERSTAND, AgentStage.INSPECT, AgentStage.PLAN,
        AgentStage.AUTHORIZE, AgentStage.EXECUTE, AgentStage.VERIFY, AgentStage.REPORT,
    )

    def __init__(self) -> None:
        self.stage = AgentStage.UNDERSTAND
        self._authorized = False
        self._executed = False
        self._verified = False

    def transition(self, target: AgentStage) -> None:
        if target == self.stage:
            return
        try:
            current_index = self.ORDER.index(self.stage)
            target_index = self.ORDER.index(target)
        except ValueError as exc:
            raise ValueError("unknown agent stage") from exc
        if target_index != current_index + 1:
            raise RuntimeError(f"invalid agent transition: {self.stage.value} -> {target.value}")
        if target is AgentStage.EXECUTE and not self._authorized:
            raise PermissionError("execution requires successful authorization")
        if target is AgentStage.VERIFY and not self._executed:
            raise RuntimeError("verification requires execution")
        if target is AgentStage.REPORT and self.requires_verification_for_current_action() and not self._verified:
            raise RuntimeError("state-changing action must be verified before report")
        self.stage = target

    def authorize(self, request: ActionRequest, decision: ActionDecision) -> None:
        if self.stage is not AgentStage.AUTHORIZE:
            raise RuntimeError("authorization is only valid in authorize stage")
        if not decision.allowed:
            raise PermissionError(decision.reason)
        self._authorized = True

    def mark_executed(self) -> None:
        if self.stage is not AgentStage.EXECUTE or not self._authorized:
            raise RuntimeError("execution is not authorized")
        self._executed = True

    def mark_verified(self) -> None:
        if self.stage is not AgentStage.VERIFY or not self._executed:
            raise RuntimeError("verification is not available")
        self._verified = True

    def requires_verification(self, request: ActionRequest) -> bool:
        return request.permission not in {PermissionLevel.EXPLAIN, PermissionLevel.READ}

    def bind_request(self, request: ActionRequest) -> None:
        self._request = request

    def requires_verification_for_current_action(self) -> bool:
        return not hasattr(self, "_request") or self.requires_verification(self._request)
