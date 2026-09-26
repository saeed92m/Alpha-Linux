from pathlib import Path

from alpha_core.control_center import ControlCenter
from alpha_core.hardware import HardwareDiscovery
from alpha_core.observatory import SystemObservatory
from alpha_core.phase2 import Phase2IntegrationFacade
from alpha_core.profiles import Profile, ProfileRegistry
from alpha_core.system_integration import ConfigurationStore, HealthAggregator, SystemDiscovery
from alpha_core.software_center import SoftwareCatalogLoader


def _facade(tmp_path: Path) -> Phase2IntegrationFacade:
    configuration = ConfigurationStore()
    configuration.set("ui", "theme", "system")
    control = ControlCenter(
        SystemObservatory(SystemDiscovery(), HealthAggregator()),
        HardwareDiscovery(sys_root=tmp_path / "sys", proc_root=tmp_path / "proc"),
        configuration,
    )
    profiles = ProfileRegistry(
        (
            Profile("daily", "Daily", "Daily workstation", {"ui.theme": "system"}),
            Profile("science", "Science", "Science workstation", {"compute.mode": "scientific"}),
        )
    )
    return Phase2IntegrationFacade(
        control_center=control,
        software_catalog_loader=SoftwareCatalogLoader(tmp_path / "catalog"),
        profiles=profiles,
    )


def test_phase2_snapshot_unifies_reference_surfaces(tmp_path: Path):
    snapshot = _facade(tmp_path).snapshot(("science",))

    assert snapshot.control_center.configuration["ui.theme"] == "system"
    assert snapshot.profile_ids == ("daily", "science")
    assert snapshot.resolved_profile_settings["compute.mode"] == "scientific"
    assert snapshot.software_catalog.entries == ()


def test_phase2_plans_are_deterministic_and_dry_run(tmp_path: Path):
    facade = _facade(tmp_path)

    update = facade.plan_update(("install:example",))
    software = facade.plan_software("install", ("example",))
    recovery = facade.plan_recovery("phase-2-baseline")

    assert update.dry_run
    assert software.dry_run
    assert recovery.dry_run
    assert facade.plan_update(("install:example",)).plan_id == update.plan_id
    assert facade.plan_software("install", ("example",)).plan_id == software.plan_id
    assert facade.plan_recovery("phase-2-baseline").plan_id == recovery.plan_id
