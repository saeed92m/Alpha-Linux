from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import string


@dataclass(frozen=True)
class OSImageEvidence:
    release_id: str
    version: str
    channel: str
    architecture: str
    artifact_format: str
    artifact_filename: str
    artifact_size: int
    artifact_sha256: str
    source_commit: str
    ci_run_id: str
    build_environment: str
    reproducibility_result: str
    reproducibility_reference_sha256: str

    def __post_init__(self) -> None:
        fields = (
            ("release_id", self.release_id),
            ("version", self.version),
            ("channel", self.channel),
            ("architecture", self.architecture),
            ("artifact_format", self.artifact_format),
            ("artifact_filename", self.artifact_filename),
            ("artifact_sha256", self.artifact_sha256),
            ("source_commit", self.source_commit),
            ("ci_run_id", self.ci_run_id),
            ("build_environment", self.build_environment),
            ("reproducibility_result", self.reproducibility_result),
            ("reproducibility_reference_sha256", self.reproducibility_reference_sha256),
        )
        missing = [name for name, value in fields if not str(value).strip()]
        if missing:
            raise ValueError(f"missing required fields: {missing}")
        if self.artifact_format not in {"iso", "img"}:
            raise ValueError("artifact_format must be iso or img")
        if self.artifact_size <= 0:
            raise ValueError("artifact_size must be positive")
        for name, digest in (
            ("artifact_sha256", self.artifact_sha256),
            ("reproducibility_reference_sha256", self.reproducibility_reference_sha256),
        ):
            if len(digest) != 64 or any(character not in string.hexdigits for character in digest):
                raise ValueError(f"{name} must be a SHA-256 hex digest")
        if self.reproducibility_result not in {"not-run", "passed", "failed"}:
            raise ValueError("reproducibility_result must be not-run, passed, or failed")

    @property
    def deterministic_filename(self) -> str:
        return f"alpha-linux-{self.version}-{self.channel}-{self.architecture}.{self.artifact_format}"

    def validate_filename(self) -> None:
        if self.artifact_filename != self.deterministic_filename:
            raise ValueError("artifact_filename does not match deterministic naming")

    @classmethod
    def from_file(
        cls,
        path: Path,
        *,
        release_id: str,
        version: str,
        channel: str,
        architecture: str,
        source_commit: str,
        ci_run_id: str,
        build_environment: str,
        reproducibility_result: str,
        reproducibility_reference_sha256: str,
    ) -> "OSImageEvidence":
        if path.suffix.lower() not in {".iso", ".img"}:
            raise ValueError("OS image format must be .iso or .img")
        data = path.read_bytes()
        return cls(
            release_id=release_id,
            version=version,
            channel=channel,
            architecture=architecture,
            artifact_format=path.suffix[1:].lower(),
            artifact_filename=path.name,
            artifact_size=len(data),
            artifact_sha256=hashlib.sha256(data).hexdigest(),
            source_commit=source_commit,
            ci_run_id=ci_run_id,
            build_environment=build_environment,
            reproducibility_result=reproducibility_result,
            reproducibility_reference_sha256=reproducibility_reference_sha256,
        )


@dataclass(frozen=True)
class CosmicLiveImageEvidence:
    package_names: tuple[str, ...] = ("cosmic-session", "cosmic-desktop")
    desktop_file: str = "cosmic.desktop"
    session_launcher: str = "start-cosmic"

    def validate_root(self, root: Path) -> dict[str, object]:
        desktop_candidates = (
            root / "usr/share/xsessions" / self.desktop_file,
            root / "usr/share/wayland-sessions" / self.desktop_file,
        )
        launcher_candidates = (
            root / "usr/bin" / self.session_launcher,
            root / "usr/local/bin" / self.session_launcher,
        )

        desktop_path = next((path for path in desktop_candidates if path.exists()), None)
        if desktop_path is None:
            raise ValueError("missing cosmic.desktop in live rootfs")

        launcher_path = next(
            (path for path in launcher_candidates if path.exists() and os.access(path, os.X_OK)),
            None,
        )
        if launcher_path is None:
            raise ValueError("missing executable start-cosmic in live rootfs")

        status_path = root / "var/lib/dpkg/status"
        if not status_path.exists():
            raise ValueError("dpkg status file is missing; live rootfs is incomplete")

        status_text = status_path.read_text(encoding="utf-8", errors="ignore")
        missing_packages = [
            package for package in self.package_names if f"Package: {package}" not in status_text
        ]
        if missing_packages:
            raise ValueError(f"missing COSMIC packages: {missing_packages}")

        payload = {
            "desktop_file": str(desktop_path),
            "session_launcher": str(launcher_path),
            "required_packages": list(self.package_names),
            "state": "validated",
        }
        return payload

