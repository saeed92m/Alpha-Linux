from alpha_core.ai import AIExecutionRequest
from alpha_core.assistant import AssistantPlanner, AssistantSession, AssistantTurn, TurnRole


def session() -> AssistantSession:
    return AssistantSession("session-1", "alpha-assistant", 100)


def test_turn_contract() -> None:
    turn = AssistantTurn(0, TurnRole.USER, "hello")
    assert turn.sequence == 0


def test_session_turn_order() -> None:
    turns = (
        AssistantTurn(0, TurnRole.USER, "question"),
        AssistantTurn(1, TurnRole.ASSISTANT, "answer"),
    )
    normalized = AssistantPlanner().normalize(AssistantSession("session-1", "alpha-assistant", 100, turns))
    assert [turn.sequence for turn in normalized.turns] == [0, 1]


def test_non_contiguous_turns_are_rejected() -> None:
    try:
        AssistantSession("session-1", "alpha-assistant", 100, (AssistantTurn(1, TurnRole.USER, "hello"),))
    except ValueError as exc:
        assert str(exc) == "turn sequences must be contiguous and ordered"
    else:
        raise AssertionError("expected rejection")


def test_request_respects_context_budget() -> None:
    request = AIExecutionRequest("req-1", "alpha-chat", "hello")
    built = AssistantPlanner().build_request(session(), request, 50)
    assert built.session_id == "session-1"


def test_context_overflow_is_rejected() -> None:
    request = AIExecutionRequest("req-1", "alpha-chat", "hello")
    try:
        AssistantPlanner().build_request(session(), request, 101)
    except ValueError as exc:
        assert str(exc) == "context budget exceeded"
    else:
        raise AssertionError("expected rejection")
