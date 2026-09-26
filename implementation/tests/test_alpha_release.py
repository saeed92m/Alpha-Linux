from alpha_core.alpha_release import AlphaReleaseManifest, AlphaReleasePlanner


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
