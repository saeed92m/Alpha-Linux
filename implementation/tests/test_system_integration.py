from alpha_core.system_integration import (
    ComponentHealth,
    ConfigurationStore,
    DiagnosticsEngine,
    HealthAggregator,
    HealthState,
    SystemDiscovery,
    UpdatePlanner,
)


def test_configuration_store_is_namespaced():
    store = ConfigurationStore()
    store.set("core", "mode", "adaptive")
    assert store.get("core", "mode") == "adaptive"
    assert store.get("other", "mode") is None


def test_system_discovery_is_read_only_and_structured():
    snapshot = SystemDiscovery().snapshot()
    assert set(snapshot) == {"machine", "platform", "processor"}


def test_diagnostics_are_deterministic():
    health = ComponentHealth("gpu", HealthState.DEGRADED, {"driver": "unknown"})
    findings = DiagnosticsEngine().evaluate(health)
    assert findings[0].severity == "warning"
    assert findings[0].evidence["driver"] == "unknown"


def test_update_planner_is_explicitly_dry_run():
    plan = UpdatePlanner().plan(("install:example",))
    assert plan.dry_run
    assert plan.requires_privilege


def test_health_aggregation():
    aggregate = HealthAggregator().aggregate((
        ComponentHealth("core", HealthState.HEALTHY),
        ComponentHealth("network", HealthState.DEGRADED),
    ))
    assert aggregate.state is HealthState.DEGRADED


def test_failed_health_dominates():
    aggregate = HealthAggregator().aggregate((
        ComponentHealth("core", HealthState.HEALTHY),
        ComponentHealth("storage", HealthState.FAILED),
    ))
    assert aggregate.state is HealthState.FAILED
