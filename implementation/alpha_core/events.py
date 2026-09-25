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
    """In-process event boundary; subscribers cannot grant permissions."""

    def __init__(self) -> None:
        self._subscriptions: dict[str, EventSubscription] = {}

    def subscribe(self, subscription: EventSubscription) -> None:
        if not subscription.subscription_id.strip() or not subscription.event_name.strip():
            raise ValueError("subscription identity is required")
        if subscription.subscription_id in self._subscriptions:
            raise ValueError("subscription already exists")
        self._subscriptions[subscription.subscription_id] = subscription

    def unsubscribe(self, subscription_id: str) -> None:
        self._subscriptions.pop(subscription_id, None)

    def publish(self, event: ObservabilityEvent) -> int:
        delivered = 0
        for subscription in tuple(self._subscriptions.values()):
            if subscription.event_name in {event.event, "*"}:
                subscription.callback(event)
                delivered += 1
        return delivered
