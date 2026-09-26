from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class InputDeviceKind(str, Enum):
    TOUCH = "touch"
    PEN = "pen"


@dataclass(frozen=True)
class InputDeviceDescriptor:
    device_id: str
    name: str
    kind: InputDeviceKind
    capabilities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.device_id.strip():
            raise ValueError("device_id is required")
        if not self.name.strip():
            raise ValueError("device name is required")
        if not isinstance(self.kind, InputDeviceKind):
            raise ValueError("kind must be an InputDeviceKind")
        if tuple(sorted(self.capabilities)) != self.capabilities:
            raise ValueError("capabilities must be ordered")
        if len(self.capabilities) != len(set(self.capabilities)):
            raise ValueError("capabilities must be unique")
        if any(not capability.strip() for capability in self.capabilities):
            raise ValueError("capabilities must be non-empty strings")


@dataclass(frozen=True)
class InputDeviceSnapshot:
    devices: tuple[InputDeviceDescriptor, ...]

    def __post_init__(self) -> None:
        device_ids = [device.device_id for device in self.devices]
        ordered_ids = [
            device.device_id
            for device in sorted(
                self.devices, key=lambda device: (device.kind.value, device.device_id)
            )
        ]
        if device_ids != ordered_ids:
            raise ValueError("devices must be ordered by kind and device_id")
        if len(device_ids) != len(set(device_ids)):
            raise ValueError("device identifiers must be unique")


@dataclass(frozen=True)
class InputProfile:
    device_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if tuple(sorted(self.device_ids)) != self.device_ids:
            raise ValueError("device_ids must be ordered")
        if len(self.device_ids) != len(set(self.device_ids)):
            raise ValueError("device_ids must be unique")


class InputCapabilityPlanner:
    """Read-only planner for deterministic touch and pen capability state."""

    def snapshot(
        self, devices: tuple[InputDeviceDescriptor, ...]
    ) -> InputDeviceSnapshot:
        ordered = tuple(
            sorted(devices, key=lambda device: (device.kind.value, device.device_id))
        )
        return InputDeviceSnapshot(ordered)

    def devices_for_kind(
        self, snapshot: InputDeviceSnapshot, kind: InputDeviceKind
    ) -> tuple[InputDeviceDescriptor, ...]:
        return tuple(device for device in snapshot.devices if device.kind is kind)

    def validate_profile(
        self, profile: InputProfile, snapshot: InputDeviceSnapshot
    ) -> InputProfile:
        available = {device.device_id for device in snapshot.devices}
        if any(device_id not in available for device_id in profile.device_ids):
            raise ValueError("input profile references unavailable device")
        return profile
