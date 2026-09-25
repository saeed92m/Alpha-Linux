from pathlib import Path

from alpha_core.hardware import HardwareDiscovery


def test_hardware_discovery_degrades_gracefully(tmp_path: Path):
    snapshot = HardwareDiscovery(
        sys_root=tmp_path / "sys",
        proc_root=tmp_path / "proc",
    ).snapshot()
    assert snapshot.memory["available"] is False
    assert snapshot.firmware["available"] is False
    assert snapshot.power["available"] is False
    assert snapshot.cpu["logical_cpus"] > 0


def test_hardware_discovery_reads_safe_sysfs_evidence(tmp_path: Path):
    sys_root = tmp_path / "sys"
    dmi = sys_root / "class/dmi/id"
    power = sys_root / "class/power_supply/BAT0"
    proc = tmp_path / "proc"
    dmi.mkdir(parents=True)
    power.mkdir(parents=True)
    proc.mkdir(parents=True)
    (dmi / "sys_vendor").write_text("AlphaVendor\n", encoding="utf-8")
    (dmi / "product_name").write_text("AlphaBook\n", encoding="utf-8")
    (power / "type").write_text("Battery\n", encoding="utf-8")
    (power / "status").write_text("Charging\n", encoding="utf-8")
    (power / "capacity").write_text("87\n", encoding="utf-8")
    (proc / "meminfo").write_text("MemTotal:       1024 kB\nMemAvailable:    512 kB\n", encoding="utf-8")

    snapshot = HardwareDiscovery(sys_root=sys_root, proc_root=proc).snapshot()
    assert snapshot.firmware["fields"]["product_name"] == "AlphaBook"
    assert snapshot.power["batteries"][0]["capacity_percent"] == "87"
    assert snapshot.memory["total_bytes"] == 1024 * 1024
