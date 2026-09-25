from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .observability import ObservabilityEvent


@dataclass(frozen=True)
class EventSubscription:
    subscription_id: str
    event_name: str
    callback: Callable[[ObservabilityEvent], None]


class EventBus:
    """In-process notification boundary; observer failures cannot alter control flow."""

    def __init__(self) -> None:
        self._subscriptions: dict[str, EventSubscription] = {}
        self._last_failures: tuple[str, ...] = ()

    def subscribe(self, subscription: EventSubscription) -> None:
        if not subscription.subscription_id.strip() or not subscription.event_name.strip():
            raise ValueError("subscription identity is required")
        if subscription.subscription_id in self._subscriptions:
            raise ValueError("subscription already exists")
        self._subscriptions[subscription.subscription_id] = subscription

    def unsubscribe(self, subscription_id: str) -> None:
        self._subscriptions.pop(subscription_id, None)

    @property
    def last_failures(self) -> tuple[str, ...]:
        return self._last_failures

    def publish(self, event: ObservabilityEvent) -> int:
        delivered = 0
        failures: list[str] = []
        for subscription in tuple(self._subscriptions.values()):
            if subscription.event_name not in {event.event, "*"}:
                continue
            try:
                subscription.callback(event)
            except Exception as exc:  # observers are isolated from the control plane
                failures.append(f"{subscription.subscription_id}: {type(exc).__name__}: {exc}")
                continue
            delivered += 1
        self._last_failures = tuple(failures)
        return delivered
