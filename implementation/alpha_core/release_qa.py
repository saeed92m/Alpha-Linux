from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReleaseQADisposition(str, Enum):
    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True)
class ReleaseQAGate:
    gate_id: str
    required: bool = True

    def __post_init__(self) -> None:
        if not self.gate_id.strip():
            raise ValueError("gate_id is required")


@dataclass(frozen=True)
class ReleaseQAEvidence:
    gate_id: str
    passed: bool
    evidence_id: str = ""

    def __post_init__(self) -> None:
        if not self.gate_id.strip():
            raise ValueError("gate_id is required")
        if self.passed and not self.evidence_id.strip():
            raise ValueError("evidence_id is required for passed evidence")


@dataclass(frozen=True)
class ReleaseQAResult:
    disposition: ReleaseQADisposition
    passed_gate_ids: tuple[str, ...]
    failed_gate_ids: tuple[str, ...]
    missing_gate_ids: tuple[str, ...]


class ReleaseQAPlanner:
    """Deterministic release-QA evidence aggregation; no publication or mutation."""

    def normalize_gates(self, gates: tuple[ReleaseQAGate, ...]) -> tuple[ReleaseQAGate, ...]:
        ids = [item.gate_id for item in gates]
        if len(set(ids)) != len(ids):
            raise ValueError("gate IDs must be unique")
        return tuple(sorted(gates, key=lambda item: item.gate_id))

    def normalize_evidence(self, evidence: tuple[ReleaseQAEvidence, ...]) -> tuple[ReleaseQAEvidence, ...]:
        ids = [item.gate_id for item in evidence]
        if len(set(ids)) != len(ids):
            raise ValueError("evidence gate IDs must be unique")
        return tuple(sorted(evidence, key=lambda item: item.gate_id))

    def evaluate(self, gates: tuple[ReleaseQAGate, ...], evidence: tuple[ReleaseQAEvidence, ...]) -> ReleaseQAResult:
        normalized_gates = self.normalize_gates(gates)
        evidence_by_id = {item.gate_id: item for item in self.normalize_evidence(evidence)}
        passed: list[str] = []
        failed: list[str] = []
        missing: list[str] = []
        for gate in normalized_gates:
            item = evidence_by_id.get(gate.gate_id)
            if item is None:
                if gate.required:
                    missing.append(gate.gate_id)
                continue
            if item.passed:
                passed.append(gate.gate_id)
            elif gate.required:
                failed.append(gate.gate_id)
        disposition = (
            ReleaseQADisposition.PASS
            if not failed and not missing
            else ReleaseQADisposition.FAIL
        )
        return ReleaseQAResult(disposition, tuple(passed), tuple(failed), tuple(missing))
