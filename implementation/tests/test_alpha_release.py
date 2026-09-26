from alpha_core.alpha_release import AlphaReleaseCandidateEvidence, AlphaReleaseManifest, AlphaReleasePlanner


def manifest():
    return AlphaReleaseManifest(
        "alpha-0-1-0a1",
        "0.1.0a1",
        "alpha_linux_core-0.1.0a1-py3-none-any.whl",
        "a" * 64,
        "871e1ba5fb24555766262df3cb9234e0022de78a",
        "36270066321",
    )


def test_tag_is_deterministic():
    assert AlphaReleasePlanner.tag_for("0.1.0a1") == "v0.1.0a1"


def test_ready_plan_requires_all_gates():
    result = AlphaReleasePlanner().plan(manifest(), ("ci", "qa"), ("ci", "qa"))
    assert result.ready is True
    assert result.missing_gate_ids == ()


def test_missing_gate_blocks_plan():
    result = AlphaReleasePlanner().plan(manifest(), ("ci", "qa"), ("ci",))
    assert result.ready is False
    assert result.missing_gate_ids == ("qa",)


def test_failed_gate_blocks_plan():
    result = AlphaReleasePlanner().plan(manifest(), ("ci", "qa"), ("ci",), ("qa",))
    assert result.ready is False
    assert result.failed_gate_ids == ("qa",)


def test_duplicate_gate_ids_rejected():
    try:
        AlphaReleasePlanner().plan(manifest(), ("ci", "ci"), ("ci",))
    except ValueError as exc:
        assert str(exc) == "required gate IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_manifest_rejects_non_alpha_version():
    try:
        AlphaReleaseManifest("x", "1.0.0", "a.whl", "a" * 64, "sha", "1")
    except ValueError as exc:
        assert str(exc) == "version must be an Alpha prerelease"
    else:
        raise AssertionError("expected version rejection")

def candidate_package():
    return AlphaReleaseManifest(
        "alpha-os-0-1-0a1", "0.1.0a1",
        "alpha_linux_core-0.1.0a1-py3-none-any.whl", "a" * 64,
        "7f649163ba3dada9975afee13ed792cb95ebd9fe", "36277302593",
    )


def candidate_kwargs(**overrides):
    values = {
        "os_release_id": "alpha-os-0-1-0a1",
        "os_version": "0.1.0a1",
        "os_artifact_id": "alpha-linux-0.1.0a1-alpha-amd64.iso",
        "os_artifact_sha256": "b" * 64,
        "os_source_commit": "7f649163ba3dada9975afee13ed792cb95ebd9fe",
        "os_ci_run_id": "36277327395",
        "required_gate_ids": ("package", "os", "security"),
        "passing_gate_ids": ("package", "os", "security"),
    }
    values.update(overrides)
    return values


def test_release_candidate_binds_package_and_os_evidence():
    result = AlphaReleaseCandidateEvidence.from_manifests(candidate_package(), **candidate_kwargs())
    assert result.ready is True
    assert result.tag == "v0.1.0a1"
    assert result.source_commit == "7f649163ba3dada9975afee13ed792cb95ebd9fe"
    assert result.package_ci_run_id == "36277302593"
    assert result.os_ci_run_id == "36277327395"


def test_release_candidate_rejects_version_mismatch():
    with pytest.raises(ValueError, match="versions must match"):
        AlphaReleaseCandidateEvidence.from_manifests(
            candidate_package(), **candidate_kwargs(os_version="0.1.0b1")
        )


def test_release_candidate_rejects_source_mismatch():
    with pytest.raises(ValueError, match="source commits must match"):
        AlphaReleaseCandidateEvidence.from_manifests(
            candidate_package(),
            **candidate_kwargs(os_source_commit="0" * 40),
        )


def test_release_candidate_blocks_on_missing_gate():
    result = AlphaReleaseCandidateEvidence.from_manifests(
        candidate_package(), **candidate_kwargs(passing_gate_ids=("package", "os"))
    )
    assert result.ready is False
    assert result.missing_gate_ids == ("security",)


def test_release_candidate_rejects_invalid_os_digest():
    with pytest.raises(ValueError, match="os_artifact_sha256"):
        AlphaReleaseCandidateEvidence.from_manifests(
            candidate_package(), **candidate_kwargs(os_artifact_sha256="g" * 64)
        )
