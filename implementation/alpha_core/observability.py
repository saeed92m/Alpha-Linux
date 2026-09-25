from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping


class PrivacyClass(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    SENSITIVE = "sensitive"


class Severity(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


_SECRET_KEYS = frozenset({"password", "token", "secret", "api_key", "private_key", "credential"})


def _redact(value: object) -> object:
    if isinstance(value, Mapping):
        return {
            key: "[REDACTED]" if any(secret in key.lower() for secret in _SECRET_KEYS)
            else _redact(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return type(value)(_redact(item) for item in value)
    return value


@dataclass(frozen=True)
class ObservabilityEvent:
    subsystem: str
    event: str
    severity: Severity
    correlation_id: str
    privacy: PrivacyClass
    timestamp: datetime
    data: Mapping[str, object]

    @classmethod
    def create(cls, subsystem, event, severity, correlation_id, privacy, data):
        if not subsystem or not event or not correlation_id:
            raise ValueError("observability identity fields are required")
        if not isinstance(severity, Severity):
            raise TypeError("severity must be a Severity")
        if not isinstance(privacy, PrivacyClass):
            raise TypeError("privacy must be a PrivacyClass")
        if not isinstance(data, Mapping):
            raise TypeError("data must be a mapping")
        return cls(
            subsystem, event, severity, correlation_id, privacy,
            datetime.now(timezone.utc), _redact(dict(data)),
        )
