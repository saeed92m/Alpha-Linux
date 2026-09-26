from alpha_core.orchestrator import (
    OrchestrationNode,
    OrchestrationRequest,
    OrchestratorPlanner,
)


def graph() -> tuple[OrchestrationNode, ...]:
    return (
        OrchestrationNode("final", "assistant", ("prepare",)),
        OrchestrationNode("prepare", "agent", ("source",)),
        OrchestrationNode("source", "knowledge"),
    )


def test_graph_normalization_is_deterministic() -> None:
    normalized = OrchestratorPlanner().normalize(graph())
    assert [node.node_id for node in normalized] == ["final", "prepare", "source"]
    assert normalized[1].dependencies == ("source",)


def test_topological_plan_is_deterministic() -> None:
    plan = OrchestratorPlanner().plan(graph(), OrchestrationRequest(3))
    assert plan.node_ids == ("source", "prepare", "final")


def test_missing_dependency_is_rejected() -> None:
    try:
        OrchestratorPlanner().plan(
            (OrchestrationNode("final", "assistant", ("missing",)),),
            OrchestrationRequest(1),
        )
    except ValueError as exc:
        assert str(exc) == "missing dependency"
    else:
        raise AssertionError("expected rejection")


def test_cycle_is_rejected() -> None:
    nodes = (
        OrchestrationNode("a", "agent", ("b",)),
        OrchestrationNode("b", "agent", ("a",)),
    )
    try:
        OrchestratorPlanner().plan(nodes, OrchestrationRequest(2))
    except ValueError as exc:
        assert str(exc) == "orchestration graph contains a cycle"
    else:
        raise AssertionError("expected rejection")


def test_node_limit_is_enforced() -> None:
    try:
        OrchestratorPlanner().plan(graph(), OrchestrationRequest(2))
    except ValueError as exc:
        assert str(exc) == "node limit exceeded"
    else:
        raise AssertionError("expected rejection")


def test_duplicate_node_ids_are_rejected() -> None:
    nodes = (
        OrchestrationNode("same", "agent"),
        OrchestrationNode("same", "assistant"),
    )
    try:
        OrchestratorPlanner().plan(nodes, OrchestrationRequest(2))
    except ValueError as exc:
        assert str(exc) == "node IDs must be unique"
    else:
        raise AssertionError("expected rejection")
