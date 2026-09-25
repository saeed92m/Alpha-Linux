from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
from typing import Mapping


@dataclass(frozen=True)
class HardwareSnapshot:
    cpu: Mapping[str, object]
    memory: Mapping[str, object]
    firmware: Mapping[str, object]
    power: Mapping[str, object]


class HardwareDiscovery:
    """Read-only Linux hardware discovery with graceful evidence degradation."""

    def __init__(
        self,
        *,
        sys_root: Path = Path("/sys"),
        proc_root: Path = Path("/proc"),
    ) -> None:
        self._sys = sys_root
        self._proc = proc_root

    def snapshot(self) -> HardwareSnapshot:
        return HardwareSnapshot(
            cpu=self._cpu(),
            memory=self._memory(),
            firmware=self._firmware(),
            power=self._power(),
        )

    def _cpu(self) -> Mapping[str, object]:
        return {
            "architecture": os.uname().machine,
            "logical_cpus": os.cpu_count() or 0,
        }

    def _memory(self) -> Mapping[str, object]:
        meminfo = self._proc / "meminfo"
        if not meminfo.is_file():
            return {"available": False}
        values: dict[str, int] = {}
        for line in meminfo.read_text(encoding="utf-8", errors="replace").splitlines():
            key, sep, raw = line.partition(":")
            if not sep:
                continue
            number = raw.strip().split()[0] if raw.strip() else ""
            if number.isdigit():
                values[key] = int(number) * 1024
        return {
            "available": True,
            "total_bytes": values.get("MemTotal", 0),
            "available_bytes": values.get("MemAvailable", 0),
        }

    def _firmware(self) -> Mapping[str, object]:
        dmi = self._sys / "class/dmi/id"
        fields = {}
        for name in ("sys_vendor", "product_name", "product_version", "board_name"):
            path = dmi / name
            if path.is_file():
                value = path.read_text(encoding="utf-8", errors="replace").strip()
                if value:
                    fields[name] = value
        return {"available": bool(fields), "fields": fields}

    def _power(self) -> Mapping[str, object]:
        root = self._sys / "class/power_supply"
        batteries: list[dict[str, object]] = []
        if not root.is_dir():
            return {"available": False, "batteries": batteries}
        for device in sorted(root.iterdir()):
            if not device.is_dir():
                continue
            kind = self._read(device / "type")
            if kind != "Battery":
                continue
            batteries.append({
                "name": device.name,
                "status": self._read(device / "status"),
                "capacity_percent": self._read(device / "capacity"),
            })
        return {"available": True, "batteries": batteries}

    @staticmethod
    def _read(path: Path) -> str | None:
        try:
            return path.read_text(encoding="utf-8", errors="replace").strip() or None
        except OSError:
            return None
