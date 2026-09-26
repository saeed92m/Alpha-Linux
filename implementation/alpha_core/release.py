from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReleaseChannel(str, Enum):
    ALPHA = "alpha"
    BETA = "beta"
    STABLE = "stable"


class ReleaseReadinessDisposition(str, Enum):
    READY = "ready"
    NOT_READY = "not_ready"


@dataclass(frozen=True)
class ReleaseManifest:
    release_id: str
    version: str
    channel: ReleaseChannel
    artifact_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.release_id.strip():
            raise ValueError("release_id is required")
        if not self.version.strip():
            raise ValueError("version is required")
        if not self.artifact_ids and self.channel in {ReleaseChannel.ALPHA, ReleaseChannel.BETA, ReleaseChannel.STABLE}:
            raise ValueError("artifact_ids must be non-empty")


@dataclass(frozen=True)
class ReleaseEvidence:
    evidence_id: str
    gate_id: str
    passed: bool

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id is required")
        if not self.gate_id.strip():
            raise ValueError("gate_id is required")


@dataclass(frozen=True)
class ReleaseReadinessResult:
    disposition: ReleaseReadinessDisposition
    missing_evidence_gate_ids: tuple[str, ...]
    failed_evidence_gate_ids: tuple[str, ...]


class ReleasePlanner:
    """Deterministic release-readiness planning; no publication or mutation."""

    def normalize_evidence(self, evidence: tuple[ReleaseEvidence, ...]) -> tuple[ReleaseEvidence, ...]:
        ids = [item.evidence_id for item in evidence]
        if len(set(ids)) != len(ids):
            raise ValueError("evidence IDs must be unique")
        return tuple(sorted(evidence, key=lambda item: item.evidence_id))

    def evaluate(
        self,
        manifest: ReleaseManifest,
        required_gate_ids: tuple[str, ...],
        evidence: tuple[ReleaseEvidence, ...],
    ) -> ReleaseReadinessResult:
        if len(set(required_gate_ids)) != len(required_gate_ids):
            raise ValueError("required gate IDs must be unique")
        normalized = self.normalize_evidence(evidence)
        by_gate = {item.gate_id: item for item in normalized}
        missing = tuple(sorted(gate for gate in required_gate_ids if gate not in by_gate))
        failed = tuple(sorted(gate for gate in required_gate_ids if gate in by_gate and not by_gate[gate].passed))
        disposition = ReleaseReadinessDisposition.READY if not missing and not failed else ReleaseReadinessDisposition.NOT_READY
        return ReleaseReadinessResult(disposition, missing, failed)
