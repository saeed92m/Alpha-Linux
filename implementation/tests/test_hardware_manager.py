from alpha_core.hardware import HardwareSnapshot
from alpha_core.hardware_manager import HardwareManager


def test_hardware_manager_normalizes_available_evidence():
    snapshot = HardwareSnapshot(
        cpu={"architecture": "x86_64", "logical_cpus": 8},
        memory={"available": True, "total_bytes": 16_000},
        firmware={"available": True, "fields": {"product_name": "AlphaBook"}},
        power={"available": True, "batteries": [{"name": "BAT0", "capacity_percent": "87"}]},
    )

    inventory = HardwareManager().inventory(snapshot)

    assert [record.category for record in inventory.records] == [
        "cpu",
        "firmware",
        "memory",
        "power",
    ]
    assert inventory.by_category("cpu")[0].capabilities == ("compute",)
    assert inventory.by_category("power")[0].available


def test_hardware_manager_preserves_missing_evidence():
    snapshot = HardwareSnapshot(
        cpu={"architecture": "unknown", "logical_cpus": 0},
        memory={"available": False},
        firmware={"available": False, "fields": {}},
        power={"available": False, "batteries": []},
    )

    inventory = HardwareManager().inventory(snapshot)

    assert all(not record.available for record in inventory.records)
    assert all(record.capabilities == () for record in inventory.records)
