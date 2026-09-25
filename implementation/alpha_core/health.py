from .models import HealthResult


def evaluate_component(component: str, checks: dict[str, bool]) -> HealthResult:
    healthy = bool(checks) and all(checks.values())
    return HealthResult(component=component, healthy=healthy, evidence=dict(checks))
