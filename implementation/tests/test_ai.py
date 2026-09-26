from alpha_core.ai import (
    AICorePlanner,
    AIExecutionRequest,
    AIRegistry,
    ModelDescriptor,
    ModelKind,
)


def model(model_id: str, provider_id: str = "local") -> ModelDescriptor:
    return ModelDescriptor(model_id, provider_id, ModelKind.CHAT, ("chat",))


def test_registry_normalization_is_deterministic() -> None:
    registry = AICorePlanner().normalize((model("z-model"), model("a-model")))
    assert tuple(item.model_id for item in registry.models) == ("a-model", "z-model")


def test_duplicate_model_ids_are_rejected() -> None:
    try:
        AIRegistry((model("a-model"), model("a-model")))
    except ValueError as exc:
        assert str(exc) == "model identifiers must be unique"
    else:
        raise AssertionError("expected duplicate model rejection")


def test_unknown_model_selection_is_rejected() -> None:
    registry = AIRegistry((model("a-model"),))
    try:
        AICorePlanner().select_model(registry, "missing")
    except ValueError as exc:
        assert str(exc) == "requested model is unavailable"
    else:
        raise AssertionError("expected unavailable model rejection")


def test_request_validates_against_registry() -> None:
    registry = AIRegistry((model("a-model"),))
    request = AIExecutionRequest("request-1", "a-model", "hello")
    assert AICorePlanner().validate_request(registry, request).model_id == "a-model"


def test_unknown_request_model_is_rejected() -> None:
    registry = AIRegistry((model("a-model"),))
    request = AIExecutionRequest("request-1", "missing", "hello")
    try:
        AICorePlanner().validate_request(registry, request)
    except ValueError as exc:
        assert str(exc) == "requested model is unavailable"
    else:
        raise AssertionError("expected unavailable request model rejection")


def test_capabilities_are_deterministic_and_unique() -> None:
    descriptor = ModelDescriptor(
        "a-model", "local", ModelKind.CHAT, ("chat", "tools")
    )
    assert descriptor.capabilities == ("chat", "tools")
