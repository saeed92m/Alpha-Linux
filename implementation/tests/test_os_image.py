from pathlib import Path

import pytest

from alpha_core.os_image import OSImageEvidence


def test_deterministic_filename():
    evidence = OSImageEvidence(
        "alpha-os-0-1-0a1",
        "0.1.0a1",
        "alpha",
        "amd64",
        "iso",
        "alpha-linux-0.1.0a1-alpha-amd64.iso",
        1,
        "a" * 64,
        "commit",
        "206",
    )
    evidence.validate_filename()


def test_invalid_filename_rejected():
    evidence = OSImageEvidence(
        "alpha-os-0-1-0a1",
        "0.1.0a1",
        "alpha",
        "amd64",
        "iso",
        "wrong.iso",
        1,
        "a" * 64,
        "commit",
        "206",
    )
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
    )
    assert evidence.artifact_size == len(b"alpha-image")
    assert len(evidence.artifact_sha256) == 64
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
        )
