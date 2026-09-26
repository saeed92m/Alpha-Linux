from __future__ import annotations

from dataclasses import dataclass


def _validate_capabilities(capabilities: tuple[str, ...]) -> None:
    if any(not capability.strip() for capability in capabilities):
        raise ValueError("capabilities must be non-empty")
    if len(set(capabilities)) != len(capabilities):
        raise ValueError("capabilities must be unique")


@dataclass(frozen=True)
class AgentDescriptor:
    agent_id: str
    name: str
    capabilities: tuple[str, ...] = ()
    max_steps: int = 1
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise ValueError("agent_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if self.max_steps <= 0:
            raise ValueError("max_steps must be positive")
        _validate_capabilities(self.capabilities)


@dataclass(frozen=True)
class AgentRequest:
    agent_id: str
    task: str
    capabilities: tuple[str, ...] = ()
    max_steps: int = 1

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise ValueError("agent_id is required")
        if not self.task.strip():
            raise ValueError("task is required")
        if self.max_steps <= 0:
            raise ValueError("max_steps must be positive")
        _validate_capabilities(self.capabilities)


@dataclass(frozen=True)
class AgentPlan:
    agent: AgentDescriptor
    request: AgentRequest
    capabilities: tuple[str, ...]


class AgentRuntimePlanner:
    """Deterministic planning only; no autonomous agent execution."""

    def normalize(
        self, agents: tuple[AgentDescriptor, ...]
    ) -> tuple[AgentDescriptor, ...]:
        return tuple(
            AgentDescriptor(
                agent.agent_id,
                agent.name,
                tuple(sorted(agent.capabilities)),
                agent.max_steps,
                agent.enabled,
            )
            for agent in sorted(agents, key=lambda item: item.agent_id)
        )

    def plan(
        self,
        agents: tuple[AgentDescriptor, ...],
        request: AgentRequest,
    ) -> AgentPlan:
        matches = {
            agent.agent_id: agent for agent in self.normalize(agents)
        }
        agent = matches.get(request.agent_id)
        if agent is None:
            raise ValueError("unknown agent")
        if not agent.enabled:
            raise ValueError("agent is unavailable")
        if request.max_steps > agent.max_steps:
            raise ValueError("step budget exceeded")
        unknown = set(request.capabilities) - set(agent.capabilities)
        if unknown:
            raise ValueError("capability not allowed")
        return AgentPlan(
            agent=agent,
            request=request,
            capabilities=tuple(sorted(request.capabilities)),
        )
