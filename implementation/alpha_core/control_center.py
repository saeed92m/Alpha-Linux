from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .hardware import HardwareDiscovery, HardwareSnapshot
from .observatory import ObservatorySnapshot, SystemObservatory
from .system_integration import ConfigurationStore, UpdatePlan


@dataclass(frozen=True)
class ControlCenterSnapshot:
    observatory: ObservatorySnapshot
    hardware: HardwareSnapshot
    configuration: Mapping[str, object]


class ControlCenter:
    """Read/plan aggregation facade; it does not authorize or perform privileged actions."""

    def __init__(
        self,
        observatory: SystemObservatory,
        hardware: HardwareDiscovery,
        configuration: ConfigurationStore,
    ) -> None:
        self._observatory = observatory
        self._hardware = hardware
        self._configuration = configuration

    def snapshot(self) -> ControlCenterSnapshot:
        return ControlCenterSnapshot(
            observatory=self._observatory.snapshot(),
            hardware=self._hardware.snapshot(),
            configuration=self._configuration.snapshot(),
        )

    @staticmethod
    def describe_update(plan: UpdatePlan) -> Mapping[str, object]:
        return {
            "plan_id": plan.plan_id,
            "package_actions": plan.package_actions,
            "requires_privilege": plan.requires_privilege,
            "dry_run": plan.dry_run,
        }
