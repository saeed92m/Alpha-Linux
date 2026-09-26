from alpha_core.release import (
    ReleaseChannel,
    ReleaseEvidence,
    ReleaseManifest,
    ReleasePlanner,
    ReleaseReadinessDisposition,
)


def manifest():
    return ReleaseManifest("alpha-0-1", "0.1.0-alpha.1", ReleaseChannel.ALPHA, ("source",))


def evidence(evidence_id, gate_id, passed=True):
    return ReleaseEvidence(evidence_id, gate_id, passed)


def test_evidence_normalization_is_deterministic():
    result = ReleasePlanner().normalize_evidence((evidence("b", "b"), evidence("a", "a")))
    assert tuple(item.evidence_id for item in result) == ("a", "b")


def test_ready_when_all_required_evidence_passes():
    result = ReleasePlanner().evaluate(
        manifest(), ("ci", "qa"), (evidence("e1", "ci"), evidence("e2", "qa"))
    )
    assert result.disposition == ReleaseReadinessDisposition.READY


def test_missing_evidence_blocks_release():
    result = ReleasePlanner().evaluate(manifest(), ("ci", "qa"), (evidence("e1", "ci"),))
    assert result.disposition == ReleaseReadinessDisposition.NOT_READY
    assert result.missing_evidence_gate_ids == ("qa",)


def test_failed_evidence_blocks_release():
    result = ReleasePlanner().evaluate(
        manifest(), ("ci",), (evidence("e1", "ci", False),)
    )
    assert result.disposition == ReleaseReadinessDisposition.NOT_READY
    assert result.failed_evidence_gate_ids == ("ci",)


def test_duplicate_required_gate_ids_rejected():
    try:
        ReleasePlanner().evaluate(manifest(), ("ci", "ci"), ())
    except ValueError as exc:
        assert str(exc) == "required gate IDs must be unique"
    else:
        raise AssertionError("expected duplicate gate rejection")


def test_duplicate_evidence_ids_rejected():
    try:
        ReleasePlanner().normalize_evidence((evidence("a", "ci"), evidence("a", "qa")))
    except ValueError as exc:
        assert str(exc) == "evidence IDs must be unique"
    else:
        raise AssertionError("expected duplicate evidence rejection")


def test_release_manifest_requires_artifacts():
    try:
        ReleaseManifest("x", "0.1.0-alpha.1", ReleaseChannel.ALPHA, ())
    except ValueError as exc:
        assert str(exc) == "artifact_ids must be non-empty"
    else:
        raise AssertionError("expected artifact requirement")
