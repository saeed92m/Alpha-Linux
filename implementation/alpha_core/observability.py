from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping


class PrivacyClass(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    SENSITIVE = "sensitive"


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
        return cls(
            subsystem, event, severity, correlation_id, privacy,
            datetime.now(timezone.utc), dict(data)
        )
