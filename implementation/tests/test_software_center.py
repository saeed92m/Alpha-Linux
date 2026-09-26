from pathlib import Path

import pytest

from alpha_core.software_center import (
    SoftwareCatalogEntry,
    SoftwareCatalogLoader,
    SoftwareTransactionPlanner,
)


def test_catalog_loader_is_deterministic_and_skips_invalid_manifests(tmp_path: Path):
    (tmp_path / "b.json").write_text(
        '{"package_id":"zeta","name":"Zeta","version":"2.0","summary":"Z"}',
        encoding="utf-8",
    )
    (tmp_path / "a.json").write_text(
        '{"package_id":"alpha","name":"Alpha","version":"1.0","summary":"A"}',
        encoding="utf-8",
    )
    (tmp_path / "invalid.json").write_text("{not-json", encoding="utf-8")
    (tmp_path / "bad.json").write_text(
        '{"package_id":"bad id","name":"Bad","version":"1","summary":"B"}',
        encoding="utf-8",
    )

    catalog = SoftwareCatalogLoader(tmp_path).load()

    assert [entry.package_id for entry in catalog.entries] == ["alpha", "zeta"]
    assert catalog.get("alpha").name == "Alpha"


def test_missing_catalog_is_safe(tmp_path: Path):
    assert SoftwareCatalogLoader(tmp_path / "missing").load().entries == ()


def test_catalog_entry_validates_identity_and_metadata():
    with pytest.raises(ValueError):
        SoftwareCatalogEntry("bad id", "Bad", "1.0", "summary")
    with pytest.raises(ValueError):
        SoftwareCatalogEntry("valid", "", "1.0", "summary")


def test_transaction_plan_is_stable_and_dry_run():
    planner = SoftwareTransactionPlanner()
    first = planner.plan("install", ("zeta", "alpha", "alpha"))
    second = planner.plan("install", ("alpha", "zeta"))

    assert first == second
    assert first.plan_id.startswith("software-")
    assert first.package_ids == ("alpha", "zeta")
    assert first.dry_run
    assert first.requires_privilege


def test_transaction_planner_rejects_invalid_actions():
    with pytest.raises(ValueError):
        SoftwareTransactionPlanner().plan("upgrade", ("alpha",))
    with pytest.raises(ValueError):
        SoftwareTransactionPlanner().plan("install", ())
