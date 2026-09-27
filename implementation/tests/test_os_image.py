from pathlib import Path
import hashlib

import pytest

from alpha_core.cosmic import CosmicLiveImageEvidence
from alpha_core.os_image import OSImageEvidence


def make_evidence(**overrides) -> OSImageEvidence:
    values = {
        "release_id": "alpha-os-0-1-0a1",
        "version": "0.1.0a1",
        "channel": "alpha",
        "architecture": "amd64",
        "artifact_format": "iso",
        "artifact_filename": "alpha-linux-0.1.0a1-alpha-amd64.iso",
        "artifact_size": 1,
        "artifact_sha256": "a" * 64,
        "source_commit": "commit",
        "ci_run_id": "206",
        "build_environment": "github-hosted-ubuntu-latest",
        "reproducibility_result": "passed",
        "reproducibility_reference_sha256": "b" * 64,
    }
    values.update(overrides)
    return OSImageEvidence(**values)


def test_deterministic_filename():
    make_evidence().validate_filename()


def test_invalid_filename_rejected():
    evidence = make_evidence(artifact_filename="wrong.iso")
    with pytest.raises(ValueError, match="deterministic naming"):
        evidence.validate_filename()


def test_file_evidence_binds_size_and_sha256(tmp_path: Path):
    image = tmp_path / "alpha-linux-0.1.0a1-alpha-amd64.img"
    image.write_bytes(b"alpha-image")
    evidence = OSImageEvidence.from_file(
        image,
        release_id="alpha-os-0-1-0a1",
        version="0.1.0a1",
        channel="alpha",
        architecture="amd64",
        source_commit="abc123",
        ci_run_id="206",
        build_environment="github-hosted-ubuntu-latest",
        reproducibility_result="passed",
        reproducibility_reference_sha256="b" * 64,
    )
    assert evidence.artifact_size == len(b"alpha-image")
    assert evidence.artifact_sha256 == hashlib.sha256(b"alpha-image").hexdigest()
    evidence.validate_filename()


def test_non_image_format_rejected(tmp_path: Path):
    file = tmp_path / "alpha.txt"
    file.write_text("not an image")
    with pytest.raises(ValueError, match="must be .iso or .img"):
        OSImageEvidence.from_file(
            file,
            release_id="alpha-os-0-1-0a1",
            version="0.1.0a1",
            channel="alpha",
            architecture="amd64",
            source_commit="abc123",
            ci_run_id="206",
            build_environment="github-hosted-ubuntu-latest",
            reproducibility_result="passed",
            reproducibility_reference_sha256="b" * 64,
        )


def test_invalid_sha256_rejected():
    with pytest.raises(ValueError, match="artifact_sha256"):
        make_evidence(artifact_sha256="g" * 64)


def test_invalid_reference_sha256_rejected():
    with pytest.raises(ValueError, match="reproducibility_reference_sha256"):
        make_evidence(reproducibility_reference_sha256="g" * 64)


def test_invalid_artifact_format_rejected():
    with pytest.raises(ValueError, match="artifact_format must be iso or img"):
        make_evidence(artifact_format="tar")


def test_invalid_reproducibility_result_rejected():
    with pytest.raises(ValueError, match="reproducibility_result"):
        make_evidence(reproducibility_result="unknown")


def test_cosmic_live_image_evidence_accepts_valid_runtime(tmp_path: Path):
    desktop_dir = tmp_path / "usr/share/xsessions"
    desktop_dir.mkdir(parents=True)
    (desktop_dir / "cosmic.desktop").write_text("[Desktop Entry]\nExec=start-cosmic\n", encoding="utf-8")
    launcher_dir = tmp_path / "usr/bin"
    launcher_dir.mkdir(parents=True)
    launcher = launcher_dir / "start-cosmic"
    launcher.write_text("#!/bin/sh\n", encoding="utf-8")
    launcher.chmod(0o755)
    status = tmp_path / "var/lib/dpkg/status"
    status.parent.mkdir(parents=True)
    status.write_text("Package: cosmic-session\n\nPackage: cosmic-desktop\n", encoding="utf-8")

    payload = CosmicLiveImageEvidence().validate_root(tmp_path)
    assert payload["state"] == "validated"
    assert payload["required_packages"] == ["cosmic-session", "cosmic-desktop"]


def test_cosmic_live_image_evidence_rejects_missing_runtime(tmp_path: Path):
    with pytest.raises(ValueError, match="missing cosmic.desktop"):
        CosmicLiveImageEvidence().validate_root(tmp_path)

