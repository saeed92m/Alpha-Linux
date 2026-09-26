from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class VerificationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True)
class VerificationCheck:
    check_id: str
    category: str
    status: VerificationStatus
    evidence: str

    def __post_init__(self) -> None:
        if not self.check_id.strip():
            raise ValueError("check_id is required")
        if not self.category.strip():
            raise ValueError("category is required")
        if not self.evidence.strip():
            raise ValueError("evidence is required")
        if not isinstance(self.status, VerificationStatus):
            raise ValueError("status must be a VerificationStatus")


@dataclass(frozen=True)
class VerificationRequest:
    max_checks: int

    def __post_init__(self) -> None:
        if self.max_checks <= 0:
            raise ValueError("max_checks must be positive")


@dataclass(frozen=True)
class VerificationReport:
    request: VerificationRequest
    checks: tuple[VerificationCheck, ...]
    status: VerificationStatus


class VerificationPlanner:
    """Deterministic evidence aggregation only; no external verification I/O."""

    def normalize(
        self, checks: tuple[VerificationCheck, ...]
    ) -> tuple[VerificationCheck, ...]:
        return tuple(sorted(checks, key=lambda check: check.check_id))

    def build_report(
        self,
        checks: tuple[VerificationCheck, ...],
        request: VerificationRequest,
    ) -> VerificationReport:
        normalized = self.normalize(checks)
        if not normalized:
            raise ValueError("at least one check is required")
        if len(normalized) > request.max_checks:
            raise ValueError("check limit exceeded")
        check_ids = [check.check_id for check in normalized]
        if len(set(check_ids)) != len(check_ids):
            raise ValueError("check IDs must be unique")
        status = (
            VerificationStatus.PASS
            if all(check.status is VerificationStatus.PASS for check in normalized)
            else VerificationStatus.FAIL
        )
        return VerificationReport(
            request=request,
            checks=normalized,
            status=status,
        )
