from pathlib import Path

import pytest

from alpha_core.installer_fixture import create_gpt_fixture, sha256
from alpha_core.installer_orchestration import InstallerSession, InstallerStage
from alpha_core.installer_safety import (
    InstallerIntent,
    StorageObservation,
    StorageState,
)


def observation(*states, has_esp=True, writable=True):
    return StorageObservation(
        "fixture-disk", "gpt", tuple(states), has_esp, writable
    )


def test_execution_requires_inspection_and_plan():
    with pytest.raises(RuntimeError):
        InstallerSession().execute(Path("missing.img"))


def test_blocked_plan_cannot_be_confirmed():
    session = (
        InstallerSession()
        .inspect(
            observation(
                StorageState.GPT,
                StorageState.WINDOWS_NTFS,
                StorageState.BITLOCKER,
            )
        )
        .plan_install(InstallerIntent.ALONGSIDE_WINDOWS)
    )
    assert session.stage is InstallerStage.BLOCKED
    with pytest.raises(ValueError):
        session.confirm()


def test_confirmation_is_a_distinct_gate():
    session = (
        InstallerSession()
        .inspect(observation(StorageState.GPT))
        .plan_install(InstallerIntent.ALPHA_ONLY)
    )
    with pytest.raises(PermissionError):
        session.execute(Path("missing.img"))


def test_confirmed_disposable_execution_commits(tmp_path):
    fixture = create_gpt_fixture(tmp_path / "disk.img")
    session = (
        InstallerSession()
        .inspect(observation(StorageState.GPT))
        .plan_install(InstallerIntent.ALPHA_ONLY)
        .confirm()
    )
    result = session.execute(fixture, runner=lambda command: None)
    assert result.stage is InstallerStage.COMMITTED
    assert result.transaction is not None
    assert result.transaction.committed is True


def test_fault_injection_transitions_to_rollback(tmp_path):
    fixture = create_gpt_fixture(tmp_path / "disk.img")
    before = sha256(fixture)
    session = (
        InstallerSession()
        .inspect(observation(StorageState.GPT))
        .plan_install(InstallerIntent.ALPHA_ONLY)
        .confirm()
    )
    result = session.execute(fixture, runner=lambda command: None, fail_at=2)
    assert result.stage is InstallerStage.ROLLED_BACK
    assert result.transaction is not None
    assert result.transaction.rolled_back is True
    assert sha256(fixture) == before
