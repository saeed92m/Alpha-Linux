from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RFMode(str, Enum):
    AM = "am"
    FM = "fm"
    SSB = "ssb"
    IQ = "iq"


@dataclass(frozen=True)
class RFFrequencyBand:
    band_id: str
    name: str
    start_hz: int
    end_hz: int
    modes: tuple[RFMode, ...]

    def __post_init__(self) -> None:
        if not self.band_id.strip():
            raise ValueError("band_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if self.start_hz < 0 or self.end_hz <= self.start_hz:
            raise ValueError("frequency range is invalid")
        if not self.modes:
            raise ValueError("modes must be non-empty")
        if len(set(self.modes)) != len(self.modes):
            raise ValueError("modes must be unique")


@dataclass(frozen=True)
class SDRDevice:
    device_id: str
    name: str
    min_frequency_hz: int
    max_frequency_hz: int
    max_sample_rate_sps: int
    modes: tuple[RFMode, ...]
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.device_id.strip():
            raise ValueError("device_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if self.min_frequency_hz < 0 or self.max_frequency_hz <= self.min_frequency_hz:
            raise ValueError("frequency range is invalid")
        if self.max_sample_rate_sps <= 0:
            raise ValueError("max_sample_rate_sps must be positive")
        if not self.modes:
            raise ValueError("modes must be non-empty")
        if len(set(self.modes)) != len(self.modes):
            raise ValueError("modes must be unique")


@dataclass(frozen=True)
class RFRequirement:
    requirement_id: str
    center_frequency_hz: int
    sample_rate_sps: int
    mode: RFMode

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if self.center_frequency_hz < 0:
            raise ValueError("center_frequency_hz must be non-negative")
        if self.sample_rate_sps <= 0:
            raise ValueError("sample_rate_sps must be positive")


@dataclass(frozen=True)
class SDRPlan:
    requirement_ids: tuple[str, ...]
    device_ids: tuple[str, ...]


class SDRRFPlanner:
    """Deterministic SDR/RF compatibility planning only."""

    def normalize_devices(
        self, devices: tuple[SDRDevice, ...]
    ) -> tuple[SDRDevice, ...]:
        ids = [device.device_id for device in devices]
        if len(set(ids)) != len(ids):
            raise ValueError("device IDs must be unique")
        return tuple(sorted(devices, key=lambda item: item.device_id))

    def normalize_requirements(
        self, requirements: tuple[RFRequirement, ...]
    ) -> tuple[RFRequirement, ...]:
        ids = [requirement.requirement_id for requirement in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def plan(
        self,
        requirements: tuple[RFRequirement, ...],
        devices: tuple[SDRDevice, ...],
        max_devices: int = 4,
    ) -> SDRPlan:
        if max_devices <= 0:
            raise ValueError("max_devices must be positive")

        normalized_devices = self.normalize_devices(devices)
        normalized_requirements = self.normalize_requirements(requirements)
        selected: list[SDRDevice] = []

        for requirement in normalized_requirements:
            compatible = [
                device
                for device in normalized_devices
                if device.enabled
                and device.min_frequency_hz
                <= requirement.center_frequency_hz
                <= device.max_frequency_hz
                and device.max_sample_rate_sps >= requirement.sample_rate_sps
                and requirement.mode in device.modes
            ]
            if not compatible:
                raise ValueError("no compatible SDR device")
            selected.append(compatible[0])

        device_ids = tuple(device.device_id for device in selected)
        if len(set(device_ids)) > max_devices:
            raise ValueError("RF plan exceeds device limit")

        return SDRPlan(
            requirement_ids=tuple(
                requirement.requirement_id for requirement in normalized_requirements
            ),
            device_ids=device_ids,
        )
