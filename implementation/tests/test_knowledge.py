from alpha_core.knowledge import (
    KnowledgeDocument,
    KnowledgePlanner,
    KnowledgeQuery,
    KnowledgeSource,
    SourceKind,
)


def sources() -> tuple[KnowledgeSource, ...]:
    return (
        KnowledgeSource("source-b", "engineering", SourceKind.CURATED),
        KnowledgeSource("source-a", "engineering", SourceKind.LOCAL),
        KnowledgeSource("source-x", "other", SourceKind.GENERATED),
    )


def documents() -> tuple[KnowledgeDocument, ...]:
    return (
        KnowledgeDocument("doc-b", "source-b", "B", "content", "source-b"),
        KnowledgeDocument("doc-a", "source-a", "A", "content", "source-a"),
        KnowledgeDocument("doc-x", "source-x", "X", "content", "source-x"),
    )


def test_source_and_document_contracts() -> None:
    assert sources()[0].kind is SourceKind.CURATED
    assert documents()[0].provenance == "source-b"


def test_document_normalization_is_deterministic() -> None:
    normalized = KnowledgePlanner().normalize_documents(documents())
    assert [document.document_id for document in normalized] == ["doc-a", "doc-b", "doc-x"]


def test_plan_is_namespace_scoped_and_bounded() -> None:
    plan = KnowledgePlanner().plan(
        sources(), documents(), KnowledgeQuery("engineering", 1)
    )
    assert plan.document_ids == ("doc-a",)


def test_all_namespace_documents_are_selected_in_order() -> None:
    plan = KnowledgePlanner().plan(
        sources(), documents(), KnowledgeQuery("engineering", 10)
    )
    assert plan.document_ids == ("doc-a", "doc-b")


def test_invalid_limit_is_rejected() -> None:
    try:
        KnowledgeQuery("engineering", 0)
    except ValueError as exc:
        assert str(exc) == "max_documents must be positive"
    else:
        raise AssertionError("expected rejection")
