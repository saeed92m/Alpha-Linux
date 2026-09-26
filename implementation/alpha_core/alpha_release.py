from __future__ import annotations

from dataclasses import dataclass
import re

_ALPHA_VERSION = re.compile(r"0\.\d+(?:\.\d+)?(?:a\d+|b\d+|rc\d+)$")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_GIT_SHA = re.compile(r"[0-9a-f]{40,64}")


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
        if not _SHA256.fullmatch(self.artifact_sha256):
            raise ValueError("artifact_sha256 must be a lowercase 64-character hex digest")
        if not _GIT_SHA.fullmatch(self.source_commit):
            raise ValueError("source_commit must be a Git commit SHA")


@dataclass(frozen=True)
class ReleasePublicationPlan:
    release_id: str
    tag: str
    ready: bool
    missing_gate_ids: tuple[str, ...]
    failed_gate_ids: tuple[str, ...]


@dataclass(frozen=True)
class AlphaReleaseCandidateEvidence:
    release_id: str
    version: str
    tag: str
    source_commit: str
    package_artifact_id: str
    package_artifact_sha256: str
    package_ci_run_id: str
    os_artifact_id: str
    os_artifact_sha256: str
    os_ci_run_id: str
    required_gate_ids: tuple[str, ...]
    passing_gate_ids: tuple[str, ...]
    failed_gate_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (
            ("release_id", self.release_id),
            ("version", self.version),
            ("tag", self.tag),
            ("source_commit", self.source_commit),
            ("package_artifact_id", self.package_artifact_id),
            ("package_ci_run_id", self.package_ci_run_id),
            ("os_artifact_id", self.os_artifact_id),
            ("os_ci_run_id", self.os_ci_run_id),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not _ALPHA_VERSION.fullmatch(self.version):
            raise ValueError("version must be an Alpha prerelease")
        if self.tag != f"v{self.version}":
            raise ValueError("tag does not match deterministic version tag")
        if not _GIT_SHA.fullmatch(self.source_commit):
            raise ValueError("source_commit must be a Git commit SHA")
        for name, digest in (
            ("package_artifact_sha256", self.package_artifact_sha256),
            ("os_artifact_sha256", self.os_artifact_sha256),
        ):
            if not _SHA256.fullmatch(digest):
                raise ValueError(f"{name} must be a lowercase 64-character hex digest")
        for name, gates in (
            ("required_gate_ids", self.required_gate_ids),
            ("passing_gate_ids", self.passing_gate_ids),
            ("failed_gate_ids", self.failed_gate_ids),
        ):
            if len(set(gates)) != len(gates):
                raise ValueError(f"{name} must be unique")

    @property
    def ready(self) -> bool:
        required = set(self.required_gate_ids)
        passing = set(self.passing_gate_ids)
        failed = set(self.failed_gate_ids)
        return not (required - passing - failed) and not (required & failed)

    @property
    def to_dict(self) -> dict[str, object]:
        return {
            "release_id": self.release_id,
            "version": self.version,
            "tag": self.tag,
            "source_commit": self.source_commit,
            "package_artifact_id": self.package_artifact_id,
            "package_artifact_sha256": self.package_artifact_sha256,
            "package_ci_run_id": self.package_ci_run_id,
            "os_artifact_id": self.os_artifact_id,
            "os_artifact_sha256": self.os_artifact_sha256,
            "os_ci_run_id": self.os_ci_run_id,
            "required_gate_ids": list(self.required_gate_ids),
            "passing_gate_ids": list(self.passing_gate_ids),
            "failed_gate_ids": list(self.failed_gate_ids),
            "missing_gate_ids": list(self.missing_gate_ids),
            "ready": self.ready,
        }

    @property
    def missing_gate_ids(self) -> tuple[str, ...]:
        required = set(self.required_gate_ids)
        passing = set(self.passing_gate_ids)
        failed = set(self.failed_gate_ids)
        return tuple(sorted(required - passing - failed))

    @classmethod
    def from_manifests(
        cls,
        package: AlphaReleaseManifest,
        *,
        os_release_id: str,
        os_version: str,
        os_artifact_id: str,
        os_artifact_sha256: str,
        os_source_commit: str,
        os_ci_run_id: str,
        required_gate_ids: tuple[str, ...],
        passing_gate_ids: tuple[str, ...],
        failed_gate_ids: tuple[str, ...] = (),
    ) -> "AlphaReleaseCandidateEvidence":
        if package.version != os_version:
            raise ValueError("package and OS versions must match")
        if package.source_commit != os_source_commit:
            raise ValueError("package and OS source commits must match")
        return cls(
            release_id="alpha-release-" + package.version.replace(".", "-"),
            version=package.version,
            tag=f"v{package.version}",
            source_commit=package.source_commit,
            package_artifact_id=package.artifact_id,
            package_artifact_sha256=package.artifact_sha256,
            package_ci_run_id=package.ci_run_id,
            os_artifact_id=os_artifact_id,
            os_artifact_sha256=os_artifact_sha256,
            os_ci_run_id=os_ci_run_id,
            required_gate_ids=required_gate_ids,
            passing_gate_ids=passing_gate_ids,
            failed_gate_ids=failed_gate_ids,
        )


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
