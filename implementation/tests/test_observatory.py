from alpha_core.observatory import SystemObservatory
from alpha_core.system_integration import ComponentHealth, HealthAggregator, HealthState, SystemDiscovery


def test_observatory_provides_read_only_snapshot():
    observatory = SystemObservatory(SystemDiscovery(), HealthAggregator())
    snapshot = observatory.snapshot((
        ComponentHealth("core", HealthState.HEALTHY),
        ComponentHealth("network", HealthState.DEGRADED),
    ))
    assert snapshot.system["machine"]
    assert snapshot.health.state is HealthState.DEGRADED
