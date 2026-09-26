from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ModelKind(str, Enum):
    CHAT = "chat"
    EMBEDDING = "embedding"
    VISION = "vision"


@dataclass(frozen=True)
class ModelDescriptor:
    model_id: str
    provider_id: str
    kind: ModelKind
    capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.model_id.strip():
            raise ValueError("model_id is required")
        if not self.provider_id.strip():
            raise ValueError("provider_id is required")
        if not isinstance(self.kind, ModelKind):
            raise ValueError("kind must be a ModelKind")
        if any(not capability.strip() for capability in self.capabilities):
            raise ValueError("capabilities must be non-empty strings")
        if tuple(sorted(self.capabilities)) != self.capabilities:
            raise ValueError("capabilities must be ordered")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")


@dataclass(frozen=True)
class AIRegistry:
    models: tuple[ModelDescriptor, ...]

    def __post_init__(self) -> None:
        ids = [model.model_id for model in self.models]
        if ids != sorted(ids):
            raise ValueError("models must be ordered by model_id")
        if len(ids) != len(set(ids)):
            raise ValueError("model identifiers must be unique")


@dataclass(frozen=True)
class AIExecutionRequest:
    request_id: str
    model_id: str
    payload: str

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id is required")
        if not self.model_id.strip():
            raise ValueError("model_id is required")


class AICorePlanner:
    """Deterministic AI-core planning with no provider or host side effects."""

    def normalize(self, models: tuple[ModelDescriptor, ...]) -> AIRegistry:
        ordered = tuple(sorted(models, key=lambda model: model.model_id))
        return AIRegistry(ordered)

    def select_model(self, registry: AIRegistry, model_id: str) -> ModelDescriptor:
        for model in registry.models:
            if model.model_id == model_id:
                return model
        raise ValueError("requested model is unavailable")

    def validate_request(
        self, registry: AIRegistry, request: AIExecutionRequest
    ) -> ModelDescriptor:
        return self.select_model(registry, request.model_id)
