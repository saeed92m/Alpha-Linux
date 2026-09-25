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
    """Execution state machine; authorization is delegated to PolicyEngine."""

    ORDER = (
        AgentStage.UNDERSTAND,
        AgentStage.INSPECT,
        AgentStage.PLAN,
        AgentStage.AUTHORIZE,
        AgentStage.EXECUTE,
        AgentStage.VERIFY,
        AgentStage.REPORT,
    )

    def authorize(self, request: ActionRequest, decision: ActionDecision) -> None:
        if not decision.allowed:
            raise PermissionError(decision.reason)

    def requires_verification(self, request: ActionRequest) -> bool:
        return request.permission not in {PermissionLevel.EXPLAIN, PermissionLevel.READ}
