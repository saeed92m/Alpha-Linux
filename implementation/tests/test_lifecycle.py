import pytest

from alpha_core.events import EventBus, EventSubscription
from alpha_core.lifecycle import CoreLifecycle, CoreState


def test_lifecycle_start_and_stop():
    bus = EventBus()
    seen = []
    bus.subscribe(EventSubscription("s1", "*", lambda event: seen.append(event.event)))
    lifecycle = CoreLifecycle(bus)
    lifecycle.start()
    assert lifecycle.state is CoreState.READY
    lifecycle.stop()
    assert lifecycle.state is CoreState.STOPPED
    assert seen == ["core.starting", "core.ready", "core.stopping", "core.stopped"]


def test_invalid_lifecycle_transition_is_rejected():
    lifecycle = CoreLifecycle(EventBus())
    with pytest.raises(RuntimeError):
        lifecycle.stop()


def test_failure_emits_event():
    bus = EventBus()
    seen = []
    bus.subscribe(EventSubscription("s1", "core.failed", lambda event: seen.append(event.data["reason"])))
    lifecycle = CoreLifecycle(bus)
    lifecycle.fail("test failure")
    assert lifecycle.state is CoreState.FAILED
    assert seen == ["test failure"]


def test_duplicate_subscription_is_rejected():
    bus = EventBus()
    sub = EventSubscription("s1", "*", lambda event: None)
    bus.subscribe(sub)
    with pytest.raises(ValueError):
        bus.subscribe(sub)
