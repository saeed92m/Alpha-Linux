from pathlib import Path

import pytest

from alpha_core.installer_fixture import create_gpt_fixture, sha256
from alpha_core.installer_safety import InstallerIntent, StorageObservation, StorageState, propose_changes
from alpha_core.installer_transaction import execute_disposable_transaction


def alpha_plan():
    return propose_changes(StorageObservation("fixture", "gpt", (StorageState.GPT,), True, True), InstallerIntent.ALPHA_ONLY)


def test_transaction_requires_confirmation(tmp_path: Path):
    fixture = create_gpt_fixture(tmp_path / "disk.img")
    with pytest.raises(PermissionError):
        execute_disposable_transaction(alpha_plan(), fixture, confirmed=False)


def test_transaction_commits_only_to_regular_file(tmp_path: Path):
    fixture = create_gpt_fixture(tmp_path / "disk.img")
    original = sha256(fixture)
    result = execute_disposable_transaction(alpha_plan(), fixture, confirmed=True)
    assert result.committed is True
    assert result.rolled_back is False
    assert result.error is None
    assert fixture.is_file()
    assert sha256(result.backup) == original
    assert sha256(fixture) != original


def test_blocked_plan_cannot_execute(tmp_path: Path):
    fixture = create_gpt_fixture(tmp_path / "disk.img")
    plan = propose_changes(StorageObservation("fixture", "gpt", (StorageState.BITLOCKER,), True, True), InstallerIntent.ALONGSIDE_WINDOWS)
    with pytest.raises(ValueError):
        execute_disposable_transaction(plan, fixture, confirmed=True)


@pytest.mark.parametrize("fail_at", [1, 2, 3])
def test_fault_injection_restores_original_fixture(tmp_path: Path, fail_at: int):
    fixture = create_gpt_fixture(tmp_path / f"fault-{fail_at}.img")
    original = sha256(fixture)
    result = execute_disposable_transaction(alpha_plan(), fixture, confirmed=True, fail_at=fail_at)
    assert result.committed is False
    assert result.rolled_back is True
    assert result.error is not None
    assert sha256(fixture) == original
    assert sha256(result.backup) == original


def test_runner_failure_is_rolled_back(tmp_path: Path):
    fixture = create_gpt_fixture(tmp_path / "runner-failure.img")
    original = sha256(fixture)
    calls = []

    def failing_runner(command):
        calls.append(tuple(command))
        if len(calls) == 2:
            raise RuntimeError("simulated sgdisk failure")

    result = execute_disposable_transaction(alpha_plan(), fixture, confirmed=True, runner=failing_runner)
    assert len(calls) == 2
    assert result.committed is False
    assert result.rolled_back is True
    assert result.error is not None
    assert "simulated sgdisk failure" in result.error
    assert sha256(fixture) == original
