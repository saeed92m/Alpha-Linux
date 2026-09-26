from alpha_core.agent_runtime import (
    AgentDescriptor,
    AgentRequest,
    AgentRuntimePlanner,
)


def agents() -> tuple[AgentDescriptor, ...]:
    return (
        AgentDescriptor("research", "Research Agent", ("search", "summarize"), 4),
        AgentDescriptor("disabled", "Disabled Agent", ("search",), 2, False),
        AgentDescriptor("coding", "Coding Agent", ("code", "test"), 3),
    )


def test_agent_normalization_is_deterministic() -> None:
    normalized = AgentRuntimePlanner().normalize(agents())
    assert [agent.agent_id for agent in normalized] == [
        "coding",
        "disabled",
        "research",
    ]
    assert normalized[-1].capabilities == ("search", "summarize")


def test_agent_plan_resolves_allowed_capabilities() -> None:
    plan = AgentRuntimePlanner().plan(
        agents(),
        AgentRequest("research", "find relevant references", ("summarize",), 2),
    )
    assert plan.agent.agent_id == "research"
    assert plan.capabilities == ("summarize",)


def test_unknown_agent_is_rejected() -> None:
    try:
        AgentRuntimePlanner().plan(agents(), AgentRequest("missing", "task"))
    except ValueError as exc:
        assert str(exc) == "unknown agent"
    else:
        raise AssertionError("expected rejection")


def test_disabled_agent_is_rejected() -> None:
    try:
        AgentRuntimePlanner().plan(agents(), AgentRequest("disabled", "task"))
    except ValueError as exc:
        assert str(exc) == "agent is unavailable"
    else:
        raise AssertionError("expected rejection")


def test_step_budget_is_enforced() -> None:
    try:
        AgentRuntimePlanner().plan(
            agents(), AgentRequest("coding", "task", ("code",), 4)
        )
    except ValueError as exc:
        assert str(exc) == "step budget exceeded"
    else:
        raise AssertionError("expected rejection")


def test_capability_allowlist_is_enforced() -> None:
    try:
        AgentRuntimePlanner().plan(
            agents(), AgentRequest("research", "task", ("code",))
        )
    except ValueError as exc:
        assert str(exc) == "capability not allowed"
    else:
        raise AssertionError("expected rejection")


def test_duplicate_capabilities_are_rejected() -> None:
    try:
        AgentRequest("research", "task", ("search", "search"))
    except ValueError as exc:
        assert str(exc) == "capabilities must be unique"
    else:
        raise AssertionError("expected rejection")
