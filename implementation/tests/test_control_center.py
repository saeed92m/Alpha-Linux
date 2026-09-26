from alpha_core.control_center import ControlCenter
from alpha_core.hardware import HardwareDiscovery
from alpha_core.observatory import SystemObservatory
from alpha_core.system_integration import ConfigurationStore, HealthAggregator, SystemDiscovery


def test_control_center_aggregates_read_only_state(tmp_path):
    config = ConfigurationStore()
    config.set("ui", "theme", "system")
    control = ControlCenter(
        SystemObservatory(SystemDiscovery(), HealthAggregator()),
        HardwareDiscovery(sys_root=tmp_path / "sys", proc_root=tmp_path / "proc"),
        config,
    )
    snapshot = control.snapshot()
    assert snapshot.configuration["ui.theme"] == "system"
    assert snapshot.observatory.system["machine"]
    assert snapshot.hardware.cpu["logical_cpus"] > 0
