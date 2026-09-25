import pytest

from alpha_core.agent import AgentRuntime, AgentStage
from alpha_core.models import ActionDecision, ActionRequest, PermissionLevel


def request(permission=PermissionLevel.EXECUTE_SAFE):
    return ActionRequest("a1", "agent", "test", permission, "system")


def test_denied_action_cannot_enter_execution():
    runtime = AgentRuntime()
    runtime.bind_request(request(PermissionLevel.RESTRICTED_ADMIN))
    for stage in (AgentStage.INSPECT, AgentStage.PLAN, AgentStage.AUTHORIZE):
        runtime.transition(stage)
    with pytest.raises(PermissionError):
        runtime.authorize(request(PermissionLevel.RESTRICTED_ADMIN), ActionDecision(False, "approval", "P1"))
    with pytest.raises(PermissionError):
        runtime.transition(AgentStage.EXECUTE)


def test_state_changing_action_requires_verification_before_report():
    runtime = AgentRuntime()
    req = request()
    runtime.bind_request(req)
    for stage in (AgentStage.INSPECT, AgentStage.PLAN, AgentStage.AUTHORIZE):
        runtime.transition(stage)
    runtime.authorize(req, ActionDecision(True, "allowed", "P1"))
    runtime.transition(AgentStage.EXECUTE)
    runtime.mark_executed()
    runtime.transition(AgentStage.VERIFY)
    with pytest.raises(RuntimeError):
        runtime.transition(AgentStage.REPORT)
    runtime.transition(AgentStage.REPORT)


def test_read_action_can_report_without_verification():
    runtime = AgentRuntime()
    req = request(PermissionLevel.READ)
    runtime.bind_request(req)
    for stage in (AgentStage.INSPECT, AgentStage.PLAN, AgentStage.AUTHORIZE):
        runtime.transition(stage)
    runtime.authorize(req, ActionDecision(True, "allowed", "P1"))
    runtime.transition(AgentStage.EXECUTE)
    runtime.mark_executed()
    runtime.transition(AgentStage.VERIFY)
    runtime.mark_verified()
    runtime.transition(AgentStage.REPORT)
