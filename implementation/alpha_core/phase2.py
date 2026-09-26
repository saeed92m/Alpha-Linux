from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .control_center import ControlCenter, ControlCenterSnapshot
from .profiles import ProfileRegistry, ProfileResolver
from .recovery import RecoveryCheckpoint, RecoveryPlan, RecoveryPlanner
from .software_center import SoftwareCatalog, SoftwareCatalogLoader, SoftwareTransactionPlan, SoftwareTransactionPlanner
from .system_integration import UpdatePlan, UpdatePlanner


@dataclass(frozen=True)
class Phase2Snapshot:
    control_center: ControlCenterSnapshot
    software_catalog: SoftwareCatalog
    profile_ids: tuple[str, ...]
    resolved_profile_settings: Mapping[str, object]


@dataclass(frozen=True)
class Phase2Plans:
    update: UpdatePlan | None
    software: SoftwareTransactionPlan | None
    recovery: RecoveryPlan | None


class Phase2IntegrationFacade:
    """Single read/plan facade over Phase 2 surfaces; it never authorizes mutation."""

    def __init__(
        self,
        *,
        control_center: ControlCenter,
        software_catalog_loader: SoftwareCatalogLoader,
        profiles: ProfileRegistry,
        update_planner: UpdatePlanner | None = None,
        software_planner: SoftwareTransactionPlanner | None = None,
        recovery_planner: RecoveryPlanner | None = None,
    ) -> None:
        self._control_center = control_center
        self._catalog_loader = software_catalog_loader
        self._profiles = profiles
        self._profile_resolver = ProfileResolver(profiles)
        self._update_planner = update_planner or UpdatePlanner()
        self._software_planner = software_planner or SoftwareTransactionPlanner()
        self._recovery_planner = recovery_planner or RecoveryPlanner()

    def snapshot(self, selected_profiles: tuple[str, ...] = ()) -> Phase2Snapshot:
        return Phase2Snapshot(
            control_center=self._control_center.snapshot(),
            software_catalog=self._catalog_loader.load(),
            profile_ids=tuple(profile.profile_id for profile in self._profiles.list()),
            resolved_profile_settings=self._profile_resolver.resolve(selected_profiles),
        )

    def plan_update(self, actions: tuple[str, ...]) -> UpdatePlan:
        return self._update_planner.plan(actions)

    def plan_software(self, action: str, package_ids: tuple[str, ...]) -> SoftwareTransactionPlan:
        return self._software_planner.plan(action, package_ids)

    def plan_recovery(self, checkpoint: RecoveryCheckpoint | str) -> RecoveryPlan:
        checkpoint_obj = (
            self._recovery_planner.checkpoint(checkpoint)
            if isinstance(checkpoint, str)
            else checkpoint
        )
        return self._recovery_planner.plan(checkpoint_obj)
