from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re


@dataclass(frozen=True)
class AlphaArtifactSpec:
    artifact_id: str
    version: str
    platform: str
    architecture: str
    artifact_type: str

    def __post_init__(self) -> None:
        for name, value in (
            ("artifact_id", self.artifact_id),
            ("version", self.version),
            ("platform", self.platform),
            ("architecture", self.architecture),
            ("artifact_type", self.artifact_type),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not re.fullmatch(r"0\.\d+(?:\.\d+)?", self.version):
            raise ValueError("version must use Alpha 0.x format")


@dataclass(frozen=True)
class AlphaArtifactEvidence:
    artifact_id: str
    filename: str
    sha256: str
    size_bytes: int

    def __post_init__(self) -> None:
        if not self.artifact_id.strip() or not self.filename.strip():
            raise ValueError("artifact_id and filename are required")
        if not re.fullmatch(r"[0-9a-f]{64}", self.sha256):
            raise ValueError("sha256 must be a lowercase 64-character hex digest")
        if self.size_bytes <= 0:
            raise ValueError("size_bytes must be positive")


@dataclass(frozen=True)
class AlphaArtifactPlan:
    artifact_ids: tuple[str, ...]
    missing_artifact_ids: tuple[str, ...]
    invalid_evidence_ids: tuple[str, ...]


class AlphaArtifactPlanner:
    """Deterministic artifact evidence validation; no publication or mutation."""

    def normalize_specs(
        self, specs: tuple[AlphaArtifactSpec, ...]
    ) -> tuple[AlphaArtifactSpec, ...]:
        ids = [item.artifact_id for item in specs]
        if len(set(ids)) != len(ids):
            raise ValueError("artifact IDs must be unique")
        return tuple(sorted(specs, key=lambda item: item.artifact_id))

    def normalize_evidence(
        self, evidence: tuple[AlphaArtifactEvidence, ...]
    ) -> tuple[AlphaArtifactEvidence, ...]:
        ids = [item.artifact_id for item in evidence]
        if len(set(ids)) != len(ids):
            raise ValueError("evidence artifact IDs must be unique")
        return tuple(sorted(evidence, key=lambda item: item.artifact_id))

    def plan(
        self,
        specs: tuple[AlphaArtifactSpec, ...],
        evidence: tuple[AlphaArtifactEvidence, ...],
        max_artifacts: int = 32,
    ) -> AlphaArtifactPlan:
        if max_artifacts <= 0:
            raise ValueError("max_artifacts must be positive")
        normalized_specs = self.normalize_specs(specs)
        if len(normalized_specs) > max_artifacts:
            raise ValueError("artifact plan exceeds artifact limit")

        evidence_by_id = {
            item.artifact_id: item for item in self.normalize_evidence(evidence)
        }
        missing = tuple(
            item.artifact_id
            for item in normalized_specs
            if item.artifact_id not in evidence_by_id
        )
        invalid = tuple(
            item.artifact_id
            for item in normalized_specs
            if item.artifact_id in evidence_by_id
            and not self._valid_filename(evidence_by_id[item.artifact_id].filename, item)
        )
        return AlphaArtifactPlan(
            artifact_ids=tuple(item.artifact_id for item in normalized_specs),
            missing_artifact_ids=missing,
            invalid_evidence_ids=invalid,
        )

    @staticmethod
    def _valid_filename(filename: str, spec: AlphaArtifactSpec) -> bool:
        expected = (
            f"alpha-linux-{spec.version}-{spec.platform}-"
            f"{spec.architecture}-{spec.artifact_type}"
        )
        return filename.startswith(expected) and filename.endswith(
            (".iso", ".img", ".tar.zst", ".zip")
        )


def sha256_hex(payload: bytes) -> str:
    """Pure checksum computation over caller-supplied bytes."""
    return hashlib.sha256(payload).hexdigest()
