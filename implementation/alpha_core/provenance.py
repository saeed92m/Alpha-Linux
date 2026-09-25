from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def project_version(root: Path) -> str:
    metadata = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    try:
        version = metadata["project"]["version"]
    except KeyError as exc:
        raise ValueError("pyproject.toml project.version is required") from exc
    if not isinstance(version, str) or not version.strip():
        raise ValueError("pyproject.toml project.version must be a non-empty string")
    return version


def git_tree_digest(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    digest = hashlib.sha256()
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        path = root / raw_path.decode("utf-8")
        digest.update(raw_path)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def create_provenance(
    *,
    root: Path,
    artifact: Path,
    artifact_id: str,
    artifact_type: str,
    channel: str,
    source_commit: str,
    build_id: str,
    builder_identity: str,
    package_set: str,
    configuration_digest: str,
    dependency_inventory: str,
    test_evidence: str,
    signature: str | None = None,
    promotion_record: str | None = None,
) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "version": project_version(root),
        "channel": channel,
        "source_commit": source_commit,
        "source_tree_digest": git_tree_digest(root),
        "build_id": build_id,
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "builder_identity": builder_identity,
        "toolchain": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "package_set": package_set,
        "configuration_digest": configuration_digest,
        "dependency_inventory": dependency_inventory,
        "test_evidence": test_evidence,
        "artifact_digest": sha256_file(artifact),
        "signature": signature,
        "promotion_record": promotion_record,
    }


def write_provenance(record: dict[str, Any], destination: Path) -> None:
    destination.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
