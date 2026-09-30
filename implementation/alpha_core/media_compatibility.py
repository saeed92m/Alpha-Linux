from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BootMode(str, Enum):
    UEFI = "uefi"
    LEGACY_BIOS = "legacy-bios"


class PartitionScheme(str, Enum):
    GPT = "gpt"
    MBR = "mbr"


@dataclass(frozen=True)
class MediaCase:
    boot_mode: BootMode
    partition_scheme: PartitionScheme
    bootable: bool
    evidence: str


@dataclass(frozen=True)
class MediaCompatibilityReport:
    cases: tuple[MediaCase, ...]
    missing_required_cases: tuple[tuple[BootMode, PartitionScheme], ...]
    unsupported_claims: tuple[str, ...]

    @property
    def complete_for_declared_matrix(self) -> bool:
        return not self.missing_required_cases and not self.unsupported_claims


def validate_media_matrix(
    cases: tuple[MediaCase, ...],
    *,
    require_legacy: bool = True,
    require_uefi: bool = True,
    require_gpt: bool = True,
    require_mbr: bool = True,
) -> MediaCompatibilityReport:
    required_modes = []
    if require_uefi:
        required_modes.append(BootMode.UEFI)
    if require_legacy:
        required_modes.append(BootMode.LEGACY_BIOS)

    required_schemes = []
    if require_gpt:
        required_schemes.append(PartitionScheme.GPT)
    if require_mbr:
        required_schemes.append(PartitionScheme.MBR)

    missing: list[tuple[BootMode, PartitionScheme]] = []
    unsupported: list[str] = []

    by_key = {(case.boot_mode, case.partition_scheme): case for case in cases}
    for mode in required_modes:
        for scheme in required_schemes:
            case = by_key.get((mode, scheme))
            if case is None:
                missing.append((mode, scheme))
                continue
            if not case.bootable:
                unsupported.append(
                    f"{mode.value}/{scheme.value} is declared but not bootable"
                )
            if not case.evidence.strip():
                unsupported.append(
                    f"{mode.value}/{scheme.value} has no evidence reference"
                )

    return MediaCompatibilityReport(
        cases=cases,
        missing_required_cases=tuple(missing),
        unsupported_claims=tuple(unsupported),
    )
