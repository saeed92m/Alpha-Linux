from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MemoryClass(str, Enum):
    SESSION = "session"
    PREFERENCE = "preference"
    KNOWLEDGE = "knowledge"


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    namespace: str
    memory_class: MemoryClass
    content: str
    priority: int = 0

    def __post_init__(self) -> None:
        if not self.memory_id.strip():
            raise ValueError("memory_id is required")
        if not self.namespace.strip():
            raise ValueError("namespace is required")
        if not self.content.strip():
            raise ValueError("content is required")
        if self.priority < 0:
            raise ValueError("priority must be non-negative")


@dataclass(frozen=True)
class MemoryQuery:
    namespace: str
    max_records: int

    def __post_init__(self) -> None:
        if not self.namespace.strip():
            raise ValueError("namespace is required")
        if self.max_records <= 0:
            raise ValueError("max_records must be positive")


@dataclass(frozen=True)
class MemoryRetrievalPlan:
    query: MemoryQuery
    memory_ids: tuple[str, ...]


class MemoryPlanner:
    """Deterministic planning only; no memory persistence or retrieval I/O."""

    def normalize(self, records: tuple[MemoryRecord, ...]) -> tuple[MemoryRecord, ...]:
        return tuple(sorted(records, key=lambda record: (-record.priority, record.memory_id)))

    def plan(
        self,
        records: tuple[MemoryRecord, ...],
        query: MemoryQuery,
    ) -> MemoryRetrievalPlan:
        candidates = [
            record for record in self.normalize(records)
            if record.namespace == query.namespace
        ]
        return MemoryRetrievalPlan(
            query=query,
            memory_ids=tuple(record.memory_id for record in candidates[: query.max_records]),
        )
