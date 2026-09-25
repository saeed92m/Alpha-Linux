from alpha_core.health import evaluate_component


def test_health_requires_all_checks():
    assert evaluate_component("core", {"service": True, "config": True}).healthy
    assert not evaluate_component("core", {"service": True, "config": False}).healthy
