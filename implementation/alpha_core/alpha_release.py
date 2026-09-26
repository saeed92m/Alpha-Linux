from __future__ import annotations

from dataclasses import dataclass
import re

_ALPHA_VERSION = re.compile(r"0\.\d+(?:\.\d+)?(?:a\d+|b\d+|rc\d+)$")


@dataclass(frozen=True)
class AlphaReleaseManifest:
    release_id: str
    version: str
    artifact_id: str
    artifact_sha256: str
    source_commit: str
    ci_run_id: str

    def __post_init__(self) -> None:
        for name, value in (
            ("release_id", self.release_id),
            ("version", self.version),
            ("artifact_id", self.artifact_id),
            ("artifact_sha256", self.artifact_sha256),
            ("source_commit", self.source_commit),
            ("ci_run_id", self.ci_run_id),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not _ALPHA_VERSION.fullmatch(self.version):
            raise ValueError("version must be an Alpha prerelease")
        if not re.fullmatch(r"[0-9a-f]{64}", self.artifact_sha256):
            raise ValueError("artifact_sha256 must be a lowercase 64-character hex digest")


@dataclass(frozen=True)
class ReleasePublicationPlan:
    release_id: str
    tag: str
    ready: bool
    missing_gate_ids: tuple[str, ...]
    failed_gate_ids: tuple[str, ...]


class AlphaReleasePlanner:
    """Deterministic publication planning; never creates tags or publishes releases."""

    @staticmethod
    def tag_for(version: str) -> str:
        if not _ALPHA_VERSION.fullmatch(version):
            raise ValueError("version must be an Alpha prerelease")
        return f"v{version}"

    def plan(
        self,
        manifest: AlphaReleaseManifest,
        required_gate_ids: tuple[str, ...],
        passing_gate_ids: tuple[str, ...],
        failed_gate_ids: tuple[str, ...] = (),
    ) -> ReleasePublicationPlan:
        if len(set(required_gate_ids)) != len(required_gate_ids):
            raise ValueError("required gate IDs must be unique")
        if len(set(passing_gate_ids)) != len(passing_gate_ids):
            raise ValueError("passing gate IDs must be unique")
        if len(set(failed_gate_ids)) != len(failed_gate_ids):
            raise ValueError("failed gate IDs must be unique")
        missing = tuple(sorted(set(required_gate_ids) - set(passing_gate_ids) - set(failed_gate_ids)))
        failed = tuple(sorted(set(required_gate_ids) & set(failed_gate_ids)))
        return ReleasePublicationPlan(
            release_id=manifest.release_id,
            tag=self.tag_for(manifest.version),
            ready=not missing and not failed,
            missing_gate_ids=missing,
            failed_gate_ids=failed,
        )
