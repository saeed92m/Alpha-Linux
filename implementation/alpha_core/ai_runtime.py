from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from alpha_core.ai import AICorePlanner, AIExecutionRequest, AIRegistry, ModelDescriptor


class ExecutionMode(str, Enum):
    INFERENCE = "inference"


@dataclass(frozen=True)
class ProviderDescriptor:
    provider_id: str
    model_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.provider_id.strip():
            raise ValueError("provider_id is required")
        if tuple(sorted(self.model_ids)) != self.model_ids:
            raise ValueError("model_ids must be ordered")
        if len(self.model_ids) != len(set(self.model_ids)):
            raise ValueError("model_ids must be unique")


@dataclass(frozen=True)
class AIExecutionPlan:
    request_id: str
    provider_id: str
    model_id: str
    mode: ExecutionMode


@dataclass(frozen=True)
class AIExecutionResult:
    request_id: str
    provider_id: str
    model_id: str
    status: str


class AIRuntimePlanner:
    def plan(
        self,
        registry: AIRegistry,
        providers: tuple[ProviderDescriptor, ...],
        request: AIExecutionRequest,
    ) -> AIExecutionPlan:
        model = AICorePlanner().validate_request(registry, request)
        provider = self._select_provider(providers, model)
        return AIExecutionPlan(
            request_id=request.request_id,
            provider_id=provider.provider_id,
            model_id=model.model_id,
            mode=ExecutionMode.INFERENCE,
        )

    def _select_provider(
        self, providers: tuple[ProviderDescriptor, ...], model: ModelDescriptor
    ) -> ProviderDescriptor:
        candidates = tuple(
            provider
            for provider in providers
            if provider.provider_id == model.provider_id
            and model.model_id in provider.model_ids
        )
        if not candidates:
            raise ValueError("no compatible provider is available")
        return sorted(candidates, key=lambda provider: provider.provider_id)[0]
