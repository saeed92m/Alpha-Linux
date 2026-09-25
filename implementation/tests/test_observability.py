import pytest

from alpha_core.observability import ObservabilityEvent, PrivacyClass


def test_event_has_identity_and_utc_timestamp():
    event = ObservabilityEvent.create(
        "core", "health.check", "info", "corr-1", PrivacyClass.INTERNAL, {"ok": True}
    )
    assert event.correlation_id == "corr-1"
    assert event.timestamp.tzinfo is not None


def test_event_requires_identity():
    with pytest.raises(ValueError):
        ObservabilityEvent.create("", "event", "info", "corr-1", PrivacyClass.PUBLIC, {})
