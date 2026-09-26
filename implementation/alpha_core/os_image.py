from __future__ import annotations

from dataclasses import dataclass
import hashlib
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
        )
        missing = [name for name, value in fields if not str(value).strip()]
        if missing:
            raise ValueError(f"missing required fields: {missing}")
        if self.artifact_format not in {"iso", "img"}:
            raise ValueError("artifact_format must be iso or img")
        if self.artifact_size <= 0:
            raise ValueError("artifact_size must be positive")
        if (
            len(self.artifact_sha256) != 64
            or any(character not in string.hexdigits for character in self.artifact_sha256)
        ):
            raise ValueError("artifact_sha256 must be a SHA-256 hex digest")

    @property
    def deterministic_filename(self) -> str:
        return (
            f"alpha-linux-{self.version}-{self.channel}-"
            f"{self.architecture}.{self.artifact_format}"
        )

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
        )
