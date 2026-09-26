from alpha_core.alpha_artifacts import (
    AlphaArtifactEvidence,
    AlphaArtifactPlanner,
    AlphaArtifactSpec,
    sha256_hex,
)


def spec(artifact_id: str = "iso") -> AlphaArtifactSpec:
    return AlphaArtifactSpec(artifact_id, "0.1", "linux", "x86_64", "iso")


def evidence(
    artifact_id: str = "iso",
    filename: str = "alpha-linux-0.1-linux-x86_64-iso.iso",
) -> AlphaArtifactEvidence:
    return AlphaArtifactEvidence(artifact_id, filename, "a" * 64, 1024)


def test_sha256_helper_is_deterministic():
    assert sha256_hex(b"alpha") == sha256_hex(b"alpha")


def test_specs_are_normalized():
    result = AlphaArtifactPlanner().normalize_specs((spec("b"), spec("a")))
    assert tuple(item.artifact_id for item in result) == ("a", "b")


def test_valid_artifact_evidence():
    result = AlphaArtifactPlanner().plan((spec(),), (evidence(),))
    assert result.missing_artifact_ids == ()
    assert result.invalid_evidence_ids == ()


def test_missing_artifact_is_reported():
    result = AlphaArtifactPlanner().plan((spec(),), ())
    assert result.missing_artifact_ids == ("iso",)


def test_invalid_filename_is_reported():
    result = AlphaArtifactPlanner().plan(
        (spec(),), (evidence(filename="wrong-name.iso"),)
    )
    assert result.invalid_evidence_ids == ("iso",)


def test_duplicate_specs_rejected():
    try:
        AlphaArtifactPlanner().normalize_specs((spec("a"), spec("a")))
    except ValueError as exc:
        assert str(exc) == "artifact IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_duplicate_evidence_rejected():
    try:
        AlphaArtifactPlanner().normalize_evidence(
            (evidence("a"), evidence("a"))
        )
    except ValueError as exc:
        assert str(exc) == "evidence artifact IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_alpha_version_required():
    try:
        AlphaArtifactSpec("a", "1.0.0", "linux", "x86_64", "iso")
    except ValueError as exc:
        assert str(exc) == "version must use Alpha 0.x format"
    else:
        raise AssertionError("expected alpha version rejection")


def test_plan_is_bounded():
    try:
        AlphaArtifactPlanner().plan(
            (spec("a"), spec("b")), (), max_artifacts=1
        )
    except ValueError as exc:
        assert str(exc) == "artifact plan exceeds artifact limit"
    else:
        raise AssertionError("expected bound rejection")
