from alpha_core.memory import MemoryClass, MemoryPlanner, MemoryQuery, MemoryRecord


def records() -> tuple[MemoryRecord, ...]:
    return (
        MemoryRecord("b", "session-1", MemoryClass.SESSION, "second", 1),
        MemoryRecord("a", "session-1", MemoryClass.SESSION, "first", 2),
        MemoryRecord("c", "other", MemoryClass.KNOWLEDGE, "other", 9),
    )


def test_record_contract() -> None:
    record = records()[0]
    assert record.memory_class is MemoryClass.SESSION


def test_normalization_is_deterministic() -> None:
    normalized = MemoryPlanner().normalize(records())
    assert [record.memory_id for record in normalized] == ["c", "a", "b"]


def test_query_is_bounded() -> None:
    plan = MemoryPlanner().plan(records(), MemoryQuery("session-1", 1))
    assert plan.memory_ids == ("a",)


def test_namespace_is_respected() -> None:
    plan = MemoryPlanner().plan(records(), MemoryQuery("session-1", 10))
    assert plan.memory_ids == ("a", "b")


def test_invalid_query_is_rejected() -> None:
    try:
        MemoryQuery("session-1", 0)
    except ValueError as exc:
        assert str(exc) == "max_records must be positive"
    else:
        raise AssertionError("expected rejection")
