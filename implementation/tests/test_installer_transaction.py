from pathlib import Path

import pytest

from alpha_core.installer_fixture import create_gpt_fixture, sha256
from alpha_core.installer_safety import InstallerIntent, StorageObservation, StorageState, propose_changes
from alpha_core.installer_transaction import execute_disposable_transaction


def test_transaction_requires_confirmation(tmp_path: Path):
    fixture = create_gpt_fixture(tmp_path / "disk.img")
    plan = propose_changes(StorageObservation("fixture", "gpt", (StorageState.GPT,), True, True), InstallerIntent.ALPHA_ONLY)
    with pytest.raises(PermissionError):
        execute_disposable_transaction(plan, fixture, confirmed=False)


def test_transaction_commits_only_to_regular_file(tmp_path: Path):
    fixture = create_gpt_fixture(tmp_path / "disk.img")
    original = sha256(fixture)
    plan = propose_changes(StorageObservation("fixture", "gpt", (StorageState.GPT,), True, True), InstallerIntent.ALPHA_ONLY)
    result = execute_disposable_transaction(plan, fixture, confirmed=True)
    assert result.committed is True
    assert result.rolled_back is False
    assert fixture.is_file()
    assert sha256(result.backup) == original
    assert sha256(fixture) != original


def test_blocked_plan_cannot_execute(tmp_path: Path):
    fixture = create_gpt_fixture(tmp_path / "disk.img")
    plan = propose_changes(StorageObservation("fixture", "gpt", (StorageState.BITLOCKER,), True, True), InstallerIntent.ALONGSIDE_WINDOWS)
    with pytest.raises(ValueError):
        execute_disposable_transaction(plan, fixture, confirmed=True)
