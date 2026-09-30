from alpha_core.install_staging import stage_install
from alpha_core.post_install import verify_post_install


def test_post_install_requires_all_evidence(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "alpha-release").write_text("0.1.0a2\n")
    target = tmp_path / "target"
    result = stage_install(source, target)

    report = verify_post_install(target, result.manifest)
    assert report.success is False
    assert report.filesystem_ok is True
    assert report.boot_configuration_ok is False
    assert report.health_ok is False


def test_post_install_passes_with_boot_and_health_evidence(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "alpha-release").write_text("0.1.0a2\n")
    target = tmp_path / "target"
    result = stage_install(source, target)

    boot = tmp_path / "efi-entry"
    boot.write_text("Alpha")
    health = tmp_path / "health"
    health.write_text("healthy")

    report = verify_post_install(
        target, result.manifest, boot_entry=boot, health_marker=health
    )
    assert report.success is True
