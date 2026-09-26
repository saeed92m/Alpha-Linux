from alpha_core.release_qa import (
    ReleaseQADisposition,
    ReleaseQAEvidence,
    ReleaseQAGate,
    ReleaseQAPlanner,
)


def gate(gate_id, required=True):
    return ReleaseQAGate(gate_id, required)


def evidence(gate_id, passed=True):
    return ReleaseQAEvidence(gate_id, passed, gate_id + "-evidence")


def test_gate_normalization_is_deterministic():
    result = ReleaseQAPlanner().normalize_gates((gate("b"), gate("a")))
    assert tuple(item.gate_id for item in result) == ("a", "b")


def test_all_required_evidence_passes():
    result = ReleaseQAPlanner().evaluate((gate("a"), gate("b")), (evidence("a"), evidence("b")))
    assert result.disposition == ReleaseQADisposition.PASS
    assert result.passed_gate_ids == ("a", "b")


def test_failed_required_gate_fails():
    result = ReleaseQAPlanner().evaluate((gate("a"),), (evidence("a", False),))
    assert result.disposition == ReleaseQADisposition.FAIL
    assert result.failed_gate_ids == ("a",)


def test_missing_required_gate_fails():
    result = ReleaseQAPlanner().evaluate((gate("a"),), ())
    assert result.disposition == ReleaseQADisposition.FAIL
    assert result.missing_gate_ids == ("a",)


def test_optional_missing_gate_does_not_fail():
    result = ReleaseQAPlanner().evaluate((gate("a", False),), ())
    assert result.disposition == ReleaseQADisposition.PASS


def test_duplicate_gate_ids_rejected():
    try:
        ReleaseQAPlanner().normalize_gates((gate("a"), gate("a")))
    except ValueError as exc:
        assert str(exc) == "gate IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_duplicate_evidence_ids_rejected():
    try:
        ReleaseQAPlanner().normalize_evidence((evidence("a"), evidence("a")))
    except ValueError as exc:
        assert str(exc) == "evidence gate IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_passed_evidence_requires_identifier():
    try:
        ReleaseQAEvidence("a", True, "")
    except ValueError as exc:
        assert str(exc) == "evidence_id is required for passed evidence"
    else:
        raise AssertionError("expected evidence identifier rejection")
