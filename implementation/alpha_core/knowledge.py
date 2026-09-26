from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SourceKind(str, Enum):
    LOCAL = "local"
    GENERATED = "generated"
    CURATED = "curated"


@dataclass(frozen=True)
class KnowledgeSource:
    source_id: str
    namespace: str
    kind: SourceKind

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id is required")
        if not self.namespace.strip():
            raise ValueError("namespace is required")


@dataclass(frozen=True)
class KnowledgeDocument:
    document_id: str
    source_id: str
    title: str
    content: str
    provenance: str

    def __post_init__(self) -> None:
        if not self.document_id.strip():
            raise ValueError("document_id is required")
        if not self.source_id.strip():
            raise ValueError("source_id is required")
        if not self.title.strip():
            raise ValueError("title is required")
        if not self.content.strip():
            raise ValueError("content is required")
        if not self.provenance.strip():
            raise ValueError("provenance is required")


@dataclass(frozen=True)
class KnowledgeQuery:
    namespace: str
    max_documents: int

    def __post_init__(self) -> None:
        if not self.namespace.strip():
            raise ValueError("namespace is required")
        if self.max_documents <= 0:
            raise ValueError("max_documents must be positive")


@dataclass(frozen=True)
class KnowledgePlan:
    query: KnowledgeQuery
    document_ids: tuple[str, ...]


class KnowledgePlanner:
    """Deterministic planning only; no retrieval I/O or ranking model."""

    def normalize_documents(
        self, documents: tuple[KnowledgeDocument, ...]
    ) -> tuple[KnowledgeDocument, ...]:
        return tuple(sorted(documents, key=lambda document: document.document_id))

    def plan(
        self,
        sources: tuple[KnowledgeSource, ...],
        documents: tuple[KnowledgeDocument, ...],
        query: KnowledgeQuery,
    ) -> KnowledgePlan:
        allowed_sources = {
            source.source_id
            for source in sources
            if source.namespace == query.namespace
        }
        candidates = [
            document
            for document in self.normalize_documents(documents)
            if document.source_id in allowed_sources
        ]
        return KnowledgePlan(
            query=query,
            document_ids=tuple(
                document.document_id for document in candidates[: query.max_documents]
            ),
        )
