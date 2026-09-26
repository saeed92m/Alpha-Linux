from pathlib import Path

import pytest

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
        "reproducibility_result": "not-run",
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
        reproducibility_result="not-run",
    )
    assert evidence.artifact_size == len(b"alpha-image")
    assert evidence.artifact_sha256 == __import__("hashlib").sha256(b"alpha-image").hexdigest()
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
            reproducibility_result="not-run",
        )


def test_invalid_sha256_rejected():
    with pytest.raises(ValueError, match="SHA-256 hex digest"):
        make_evidence(artifact_sha256="g" * 64)


def test_invalid_artifact_format_rejected():
    with pytest.raises(ValueError, match="artifact_format must be iso or img"):
        make_evidence(artifact_format="tar")
