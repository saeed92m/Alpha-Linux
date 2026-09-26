from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .hardware import HardwareSnapshot


@dataclass(frozen=True)
class HardwareRecord:
    category: str
    identity: str
    available: bool
    capabilities: tuple[str, ...]
    evidence: Mapping[str, object]


@dataclass(frozen=True)
class HardwareInventory:
    records: tuple[HardwareRecord, ...]

    def by_category(self, category: str) -> tuple[HardwareRecord, ...]:
        return tuple(record for record in self.records if record.category == category)


class HardwareManager:
    """Read-only normalized hardware inventory; it never authorizes or mutates hardware."""

    def inventory(self, snapshot: HardwareSnapshot) -> HardwareInventory:
        records: list[HardwareRecord] = []

        cpu = snapshot.cpu
        records.append(
            HardwareRecord(
                category="cpu",
                identity=str(cpu.get("architecture", "unknown")),
                available=bool(cpu.get("logical_cpus", 0)),
                capabilities=("compute",) if cpu.get("logical_cpus", 0) else (),
                evidence=dict(cpu),
            )
        )

        memory = snapshot.memory
        records.append(
            HardwareRecord(
                category="memory",
                identity="system-memory",
                available=bool(memory.get("available", False)),
                capabilities=("memory",) if memory.get("available", False) else (),
                evidence=dict(memory),
            )
        )

        firmware = snapshot.firmware
        records.append(
            HardwareRecord(
                category="firmware",
                identity="dmi",
                available=bool(firmware.get("available", False)),
                capabilities=("identify",) if firmware.get("available", False) else (),
                evidence=dict(firmware),
            )
        )

        power = snapshot.power
        batteries = power.get("batteries", ())
        records.append(
            HardwareRecord(
                category="power",
                identity="battery",
                available=bool(power.get("available", False)),
                capabilities=("battery-state",) if batteries else (),
                evidence=dict(power),
            )
        )

        records.sort(key=lambda record: (record.category, record.identity))
        return HardwareInventory(tuple(records))
