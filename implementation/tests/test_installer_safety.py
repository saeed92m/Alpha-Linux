import pytest

from alpha_core.installer_safety import (
    InstallerIntent,
    SafetyLevel,
    StorageObservation,
    StorageState,
    propose_changes,
)


def obs(*states, has_esp=True, writable=True):
    return StorageObservation("fixture-disk", "gpt", tuple(states), has_esp, writable)


def test_alpha_only_requires_explicit_confirmation():
    plan = propose_changes(obs(StorageState.GPT), InstallerIntent.ALPHA_ONLY)
    assert plan.safety is SafetyLevel.REQUIRES_CONFIRMATION
    assert plan.requires_explicit_confirmation is True
    assert "reinitialize-target" in plan.operations


def test_windows_bitlocker_is_blocked():
    plan = propose_changes(
        obs(StorageState.GPT, StorageState.WINDOWS_NTFS, StorageState.BITLOCKER),
        InstallerIntent.ALONGSIDE_WINDOWS,
    )
    assert plan.safety is SafetyLevel.BLOCKED
    assert plan.operations == ()


def test_windows_without_esp_is_blocked():
    plan = propose_changes(
        obs(StorageState.GPT, StorageState.WINDOWS_NTFS, has_esp=False),
        InstallerIntent.ALONGSIDE_WINDOWS,
    )
    assert plan.safety is SafetyLevel.BLOCKED


def test_windows_layout_is_non_destructive_until_confirmation():
    plan = propose_changes(
        obs(StorageState.GPT, StorageState.WINDOWS_NTFS),
        InstallerIntent.ALONGSIDE_WINDOWS,
    )
    assert plan.safety is SafetyLevel.REQUIRES_CONFIRMATION
    assert all("delete" not in op and "format" not in op for op in plan.operations)


def test_unsupported_storage_is_blocked():
    plan = propose_changes(obs(StorageState.UNSUPPORTED), InstallerIntent.SECOND_DISK)
    assert plan.safety is SafetyLevel.BLOCKED
    assert plan.operations == ()


def test_read_only_storage_is_blocked():
    plan = propose_changes(obs(StorageState.GPT, writable=False), InstallerIntent.SECOND_DISK)
    assert plan.safety is SafetyLevel.BLOCKED


def test_manual_partitioning_requires_confirmation():
    plan = propose_changes(obs(StorageState.GPT), InstallerIntent.MANUAL)
    assert plan.safety is SafetyLevel.REQUIRES_CONFIRMATION
    assert plan.requires_explicit_confirmation is True
