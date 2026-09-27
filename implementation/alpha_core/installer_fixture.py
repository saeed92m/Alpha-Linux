from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


def create_gpt_fixture(path: Path, size_mib: int = 64) -> Path:
    """Create a disposable regular-file GPT fixture; never touches a block device."""
    if size_mib < 8:
        raise ValueError("fixture must be at least 8 MiB")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        handle.truncate(size_mib * 1024 * 1024)
    subprocess.run(
        ["sgdisk", "--clear", "--new=1:2048:+16M", "--typecode=1:ef00", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
