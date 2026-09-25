import pytest

from alpha_core.observability import ObservabilityEvent, PrivacyClass, Severity


def test_event_has_identity_and_utc_timestamp():
    event = ObservabilityEvent.create("core", "health.check", Severity.INFO, "corr-1", PrivacyClass.INTERNAL, {"ok": True})
    assert event.correlation_id == "corr-1"
    assert event.timestamp.tzinfo is not None


def test_event_redacts_nested_secret_fields():
    event = ObservabilityEvent.create(
        "core", "auth", Severity.WARNING, "corr-1", PrivacyClass.SENSITIVE,
        {"credentials": {"api_key": "secret-value"}, "items": [{"token": "hidden"}]},
    )
    assert event.data["credentials"] == "[REDACTED]"
    assert event.data["items"][0]["token"] == "[REDACTED]"


def test_event_rejects_invalid_severity():
    with pytest.raises(TypeError):
        ObservabilityEvent.create("core", "event", "info", "corr-1", PrivacyClass.PUBLIC, {})


def test_event_requires_identity():
    with pytest.raises(ValueError):
        ObservabilityEvent.create("", "event", Severity.INFO, "corr-1", PrivacyClass.PUBLIC, {})
