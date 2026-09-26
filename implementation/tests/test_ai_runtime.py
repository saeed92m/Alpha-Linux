from alpha_core.ai import AIExecutionRequest, AIRegistry, ModelDescriptor, ModelKind
from alpha_core.ai_runtime import (
    AIExecutionPlan,
    AIRuntimePlanner,
    ExecutionMode,
    ProviderDescriptor,
)


def model(model_id: str = "alpha-chat") -> ModelDescriptor:
    return ModelDescriptor(model_id, "local", ModelKind.CHAT, ("chat",))


def registry() -> AIRegistry:
    return AIRegistry((model(),))


def test_provider_descriptor_is_deterministic() -> None:
    provider = ProviderDescriptor("local", ("alpha-chat",))
    assert provider.model_ids == ("alpha-chat",)


def test_execution_plan_is_deterministic() -> None:
    plan = AIRuntimePlanner().plan(
        registry(),
        (ProviderDescriptor("local", ("alpha-chat",)),),
        AIExecutionRequest("req-1", "alpha-chat", "hello"),
    )
    assert plan == AIExecutionPlan("req-1", "local", "alpha-chat", ExecutionMode.INFERENCE)


def test_incompatible_provider_is_rejected() -> None:
    try:
        AIRuntimePlanner().plan(
            registry(),
            (ProviderDescriptor("remote", ("other-model",)),),
            AIExecutionRequest("req-1", "alpha-chat", "hello"),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible provider is available"
    else:
        raise AssertionError("expected provider rejection")


def test_provider_model_membership_is_required() -> None:
    try:
        AIRuntimePlanner().plan(
            registry(),
            (ProviderDescriptor("local", ("other-model",)),),
            AIExecutionRequest("req-1", "alpha-chat", "hello"),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible provider is available"
    else:
        raise AssertionError("expected provider membership rejection")
