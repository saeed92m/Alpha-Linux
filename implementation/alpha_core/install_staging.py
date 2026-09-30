from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InstallManifest:
    files: tuple[str, ...]
    sha256: str


@dataclass(frozen=True)
class InstallResult:
    target: Path
    committed: bool
    rolled_back: bool
    manifest: InstallManifest
    error: str | None = None


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root).as_posix().encode()
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build_manifest(root: Path) -> InstallManifest:
    if not root.is_dir():
        raise ValueError("install source must be a directory")
    files = tuple(
        sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
    )
    return InstallManifest(files=files, sha256=_tree_digest(root))


def stage_install(source: Path, target: Path) -> InstallResult:
    manifest = build_manifest(source)
    if target.exists():
        raise ValueError("install target must not already exist")
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.with_name(target.name + ".staging")
    backup = target.with_name(target.name + ".before")

    try:
        if staging.exists():
            shutil.rmtree(staging)
        shutil.copytree(source, staging)
        if build_manifest(staging) != manifest:
            raise RuntimeError("staged filesystem manifest mismatch")
        staging.replace(target)
        if build_manifest(target) != manifest:
            raise RuntimeError("post-install filesystem manifest mismatch")
        return InstallResult(target, True, False, manifest)
    except Exception as exc:
        if target.exists():
            shutil.rmtree(target)
        if staging.exists():
            shutil.rmtree(staging)
        if backup.exists():
            backup.replace(target)
        return InstallResult(
            target, False, True, manifest, f"{type(exc).__name__}: {exc}"
        )
