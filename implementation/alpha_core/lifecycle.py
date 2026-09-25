from enum import Enum

from .events import EventBus
from .observability import ObservabilityEvent, PrivacyClass, Severity


class CoreState(str, Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    READY = "ready"
    STOPPING = "stopping"
    FAILED = "failed"


class CoreLifecycle:
    """Deterministic lifecycle state machine for the Alpha Core process boundary."""

    def __init__(self, events: EventBus) -> None:
        self.state = CoreState.STOPPED
        self.events = events

    def start(self) -> None:
        if self.state is not CoreState.STOPPED:
            raise RuntimeError("core can only start from stopped state")
        self.state = CoreState.STARTING
        self._emit("core.starting")
        self.state = CoreState.READY
        self._emit("core.ready")

    def stop(self) -> None:
        if self.state is not CoreState.READY:
            raise RuntimeError("core can only stop from ready state")
        self.state = CoreState.STOPPING
        self._emit("core.stopping")
        self.state = CoreState.STOPPED
        self._emit("core.stopped")

    def fail(self, reason: str) -> None:
        if not reason.strip():
            raise ValueError("failure reason is required")
        self.state = CoreState.FAILED
        self._emit("core.failed", {"reason": reason})

    def _emit(self, name: str, data=None) -> None:
        event = ObservabilityEvent.create(
            "alpha-core", name, Severity.INFO if self.state is not CoreState.FAILED else Severity.ERROR,
            "core-lifecycle", PrivacyClass.INTERNAL, data or {"state": self.state.value},
        )
        self.events.publish(event)
