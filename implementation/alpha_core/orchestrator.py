from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OrchestrationNode:
    node_id: str
    node_kind: str
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise ValueError("node_id is required")
        if not self.node_kind.strip():
            raise ValueError("node_kind is required")
        if any(not dependency.strip() for dependency in self.dependencies):
            raise ValueError("dependencies must be non-empty")
        if self.node_id in self.dependencies:
            raise ValueError("node cannot depend on itself")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise ValueError("dependencies must be unique")


@dataclass(frozen=True)
class OrchestrationRequest:
    max_nodes: int

    def __post_init__(self) -> None:
        if self.max_nodes <= 0:
            raise ValueError("max_nodes must be positive")


@dataclass(frozen=True)
class OrchestrationPlan:
    request: OrchestrationRequest
    node_ids: tuple[str, ...]


class OrchestratorPlanner:
    """Deterministic graph planning only; no workflow execution."""

    def normalize(
        self, nodes: tuple[OrchestrationNode, ...]
    ) -> tuple[OrchestrationNode, ...]:
        return tuple(
            sorted(
                (
                    OrchestrationNode(
                        node.node_id,
                        node.node_kind,
                        tuple(sorted(node.dependencies)),
                    )
                    for node in nodes
                ),
                key=lambda node: node.node_id,
            )
        )

    def plan(
        self,
        nodes: tuple[OrchestrationNode, ...],
        request: OrchestrationRequest,
    ) -> OrchestrationPlan:
        normalized = self.normalize(nodes)
        if len(normalized) > request.max_nodes:
            raise ValueError("node limit exceeded")
        node_map = {node.node_id: node for node in normalized}
        if len(node_map) != len(normalized):
            raise ValueError("node IDs must be unique")
        if any(
            dependency not in node_map
            for node in normalized
            for dependency in node.dependencies
        ):
            raise ValueError("missing dependency")

        indegree = {
            node.node_id: len(node.dependencies) for node in normalized
        }
        dependents: dict[str, list[str]] = {
            node.node_id: [] for node in normalized
        }
        for node in normalized:
            for dependency in node.dependencies:
                dependents[dependency].append(node.node_id)

        ready = sorted(
            node_id for node_id, degree in indegree.items() if degree == 0
        )
        ordered: list[str] = []
        while ready:
            node_id = ready.pop(0)
            ordered.append(node_id)
            for dependent in sorted(dependents[node_id]):
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    ready.append(dependent)
                    ready.sort()

        if len(ordered) != len(normalized):
            raise ValueError("orchestration graph contains a cycle")
        return OrchestrationPlan(request=request, node_ids=tuple(ordered))
