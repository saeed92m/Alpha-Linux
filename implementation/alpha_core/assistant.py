from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .ai import AIExecutionRequest


class TurnRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class AssistantTurn:
    sequence: int
    role: TurnRole
    content: str

    def __post_init__(self) -> None:
        if self.sequence < 0:
            raise ValueError("sequence must be non-negative")
        if not self.content.strip():
            raise ValueError("content is required")
        if not isinstance(self.role, TurnRole):
            raise ValueError("role must be a TurnRole")


@dataclass(frozen=True)
class AssistantSession:
    session_id: str
    assistant_id: str
    max_context_tokens: int
    turns: tuple[AssistantTurn, ...] = ()

    def __post_init__(self) -> None:
        if not self.session_id.strip():
            raise ValueError("session_id is required")
        if not self.assistant_id.strip():
            raise ValueError("assistant_id is required")
        if self.max_context_tokens <= 0:
            raise ValueError("max_context_tokens must be positive")
        sequences = [turn.sequence for turn in self.turns]
        if sequences != list(range(len(sequences))):
            raise ValueError("turn sequences must be contiguous and ordered")


@dataclass(frozen=True)
class AssistantRequest:
    session_id: str
    execution_request: AIExecutionRequest
    context_tokens: int


class AssistantPlanner:
    def normalize(self, session: AssistantSession) -> AssistantSession:
        turns = tuple(sorted(session.turns, key=lambda turn: turn.sequence))
        return AssistantSession(session.session_id, session.assistant_id, session.max_context_tokens, turns)

    def build_request(self, session: AssistantSession, execution_request: AIExecutionRequest, context_tokens: int) -> AssistantRequest:
        if context_tokens < 0:
            raise ValueError("context_tokens must be non-negative")
        if context_tokens > session.max_context_tokens:
            raise ValueError("context budget exceeded")
        return AssistantRequest(session.session_id, execution_request, context_tokens)
