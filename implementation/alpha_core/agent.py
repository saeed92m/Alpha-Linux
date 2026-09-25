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
        AgentStage.UNDERSTAND,
        AgentStage.INSPECT,
        AgentStage.PLAN,
        AgentStage.AUTHORIZE,
        AgentStage.EXECUTE,
        AgentStage.VERIFY,
        AgentStage.REPORT,
    )

    def __init__(self) -> None:
        self.stage = AgentStage.UNDERSTAND
        self._request: ActionRequest | None = None
        self._authorized = False
        self._executed = False
        self._verified = False

    def transition(self, target: AgentStage) -> None:
        if target == self.stage:
            return
        if not isinstance(target, AgentStage):
            raise ValueError("target must be an AgentStage")
        current_index = self.ORDER.index(self.stage)
        target_index = self.ORDER.index(target)
        if target_index != current_index + 1:
            raise RuntimeError(f"invalid agent transition: {self.stage.value} -> {target.value}")
        if target is AgentStage.EXECUTE and not self._authorized:
            raise PermissionError("execution requires successful authorization")
        if target is AgentStage.VERIFY and not self._executed:
            raise RuntimeError("verification requires execution")
        if target is AgentStage.REPORT:
            if self._request is None:
                raise RuntimeError("report requires a bound action request")
            if self.requires_verification(self._request) and not self._verified:
                raise RuntimeError("state-changing action must be verified before report")
        self.stage = target

    def authorize(self, request: ActionRequest, decision: ActionDecision) -> None:
        if self.stage is not AgentStage.AUTHORIZE:
            raise RuntimeError("authorization is only valid in authorize stage")
        if not decision.allowed:
            raise PermissionError(decision.reason)
        self.bind_request(request)
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
        if not isinstance(request, ActionRequest):
            raise TypeError("request must be an ActionRequest")
        self._request = request
