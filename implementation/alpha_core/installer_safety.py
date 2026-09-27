from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StorageState(str, Enum):
    EMPTY = "empty"
    GPT = "gpt"
    WINDOWS_NTFS = "windows-ntfs"
    BITLOCKER = "bitlocker"
    ENCRYPTED = "encrypted"
    UNSUPPORTED = "unsupported"


class InstallerIntent(str, Enum):
    ALPHA_ONLY = "alpha-only"
    ALONGSIDE_WINDOWS = "alongside-windows"
    SECOND_DISK = "second-disk"
    MANUAL = "manual"


class SafetyLevel(str, Enum):
    SAFE = "safe"
    REQUIRES_CONFIRMATION = "requires-confirmation"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class StorageObservation:
    disk_id: str
    partition_table: str
    states: tuple[StorageState, ...]
    has_esp: bool
    writable: bool

    def __post_init__(self) -> None:
        if not self.disk_id.strip():
            raise ValueError("disk_id is required")
        if self.partition_table not in {"gpt", "mbr", "unknown"}:
            raise ValueError("unsupported partition table value")
        if not self.states:
            raise ValueError("at least one storage state is required")


@dataclass(frozen=True)
class ProposedChange:
    disk_id: str
    intent: InstallerIntent
    operations: tuple[str, ...]
    safety: SafetyLevel
    requires_explicit_confirmation: bool
    reason: str


def propose_changes(observation: StorageObservation, intent: InstallerIntent) -> ProposedChange:
    if not observation.writable:
        return ProposedChange(
            observation.disk_id, intent, (), SafetyLevel.BLOCKED, False,
            "storage target is not writable",
        )

    if StorageState.UNSUPPORTED in observation.states:
        return ProposedChange(
            observation.disk_id, intent, (), SafetyLevel.BLOCKED, False,
            "storage layout contains an unsupported state",
        )

    if intent == InstallerIntent.ALONGSIDE_WINDOWS:
        if StorageState.BITLOCKER in observation.states:
            return ProposedChange(
                observation.disk_id, intent, (), SafetyLevel.BLOCKED, False,
                "BitLocker-protected Windows storage requires recovery-aware handling",
            )
        if StorageState.WINDOWS_NTFS not in observation.states or not observation.has_esp:
            return ProposedChange(
                observation.disk_id, intent, (), SafetyLevel.BLOCKED, False,
                "alongside-Windows installation requires detected NTFS and ESP",
            )
        return ProposedChange(
            observation.disk_id, intent,
            ("create-or-select-free-space", "install-alpha", "configure-uefi-entry"),
            SafetyLevel.REQUIRES_CONFIRMATION, True,
            "Windows layout detected; no mutation is proposed without explicit confirmation",
        )

    if intent == InstallerIntent.SECOND_DISK:
        return ProposedChange(
            observation.disk_id, intent,
            ("validate-target", "install-alpha", "configure-uefi-entry"),
            SafetyLevel.REQUIRES_CONFIRMATION, True,
            "second-disk installation requires explicit target confirmation",
        )

    if intent == InstallerIntent.MANUAL:
        return ProposedChange(
            observation.disk_id, intent,
            ("validate-user-partition-plan", "install-alpha", "configure-uefi-entry"),
            SafetyLevel.REQUIRES_CONFIRMATION, True,
            "manual partitioning requires explicit confirmation",
        )

    return ProposedChange(
        observation.disk_id, intent,
        ("reinitialize-target", "create-gpt", "create-esp", "install-alpha", "configure-uefi-entry"),
        SafetyLevel.REQUIRES_CONFIRMATION, True,
        "Alpha-only installation is destructive and must never execute implicitly",
    )
