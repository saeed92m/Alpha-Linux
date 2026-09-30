from alpha_core.install_staging import build_manifest, stage_install


def test_stage_install_preserves_manifest(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "etc").mkdir()
    (source / "etc" / "alpha-release").write_text("0.1.0a2\n")
    (source / "usr.txt").write_text("alpha")

    target = tmp_path / "target"
    result = stage_install(source, target)

    assert result.committed is True
    assert result.rolled_back is False
    assert target.is_dir()
    assert build_manifest(target) == result.manifest


def test_stage_install_rejects_existing_target(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "file").write_text("alpha")
    target = tmp_path / "target"
    target.mkdir()

    try:
        stage_install(source, target)
    except ValueError as exc:
        assert "must not already exist" in str(exc)
    else:
        raise AssertionError("existing target must be rejected")
