from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping


class PrivacyClass(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    SENSITIVE = "sensitive"


_SECRET_KEYS = frozenset({"password", "token", "secret", "api_key", "private_key", "credential"})


def _redact(data: Mapping[str, object]) -> dict[str, object]:
    return {
        key: "[REDACTED]" if key.lower() in _SECRET_KEYS else value
        for key, value in data.items()
    }


@dataclass(frozen=True)
class ObservabilityEvent:
    subsystem: str
    event: str
    severity: str
    correlation_id: str
    privacy: PrivacyClass
    timestamp: datetime
    data: Mapping[str, object]

    @classmethod
    def create(cls, subsystem, event, severity, correlation_id, privacy, data):
        if not subsystem or not event or not correlation_id:
            raise ValueError("observability identity fields are required")
        if not isinstance(privacy, PrivacyClass):
            raise TypeError("privacy must be a PrivacyClass")
        return cls(
            subsystem,
            event,
            severity,
            correlation_id,
            privacy,
            datetime.now(timezone.utc),
            _redact(dict(data)),
        )
