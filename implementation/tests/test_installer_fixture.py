from pathlib import Path

import pytest

from alpha_core.installer_fixture import create_gpt_fixture, sha256
from alpha_core.installer_safety import (
    InstallerIntent,
    SafetyLevel,
    StorageObservation,
    StorageState,
    propose_changes,
)


@pytest.mark.skipif(
    __import__("shutil").which("sgdisk") is None,
    reason="sgdisk is required for disposable disk fixture tests",
)
def test_disposable_gpt_fixture_is_file_only_and_non_destructive(tmp_path: Path):
    fixture = create_gpt_fixture(tmp_path / "alpha-installer-fixture.img")
    before = sha256(fixture)

    observation = StorageObservation(
        "fixture-file-only",
        "gpt",
        (StorageState.GPT,),
        has_esp=True,
        writable=True,
    )
    plan = propose_changes(observation, InstallerIntent.ALPHA_ONLY)

    after = sha256(fixture)
    assert fixture.is_file()
    assert fixture.stat().st_size == 64 * 1024 * 1024
    assert before == after
    assert plan.safety is SafetyLevel.REQUIRES_CONFIRMATION
    assert plan.requires_explicit_confirmation is True
