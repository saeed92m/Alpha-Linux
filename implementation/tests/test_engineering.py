from alpha_core.engineering import (
    AnalysisKind,
    EngineeringPlanner,
    EngineeringProject,
    EngineeringResource,
    EngineeringValue,
)


def resource(
    resource_id: str,
    *,
    cpu: int = 8,
    memory: int = 16384,
    kinds: tuple[AnalysisKind, ...] = (AnalysisKind.STRUCTURAL,),
    enabled: bool = True,
) -> EngineeringResource:
    return EngineeringResource(resource_id, resource_id, cpu, memory, kinds, enabled)


def project(
    *kinds: AnalysisKind,
) -> EngineeringProject:
    return EngineeringProject("project-1", "Alpha Engineering", kinds)


def test_value_requires_unit() -> None:
    assert EngineeringValue(10.0, "m").unit == "m"
    try:
        EngineeringValue(10.0, "")
    except ValueError as exc:
        assert str(exc) == "unit is required"
    else:
        raise AssertionError("expected ValueError")


def test_resource_normalization_is_deterministic() -> None:
    planner = EngineeringPlanner()
    result = planner.normalize_resources((resource("solver-b"), resource("solver-a")))
    assert tuple(item.resource_id for item in result) == ("solver-a", "solver-b")


def test_analysis_capability_is_enforced() -> None:
    planner = EngineeringPlanner()
    result = planner.plan(project(AnalysisKind.STRUCTURAL), (resource("solver-a"),))
    assert result.resource_ids == ("solver-a",)

    try:
        planner.plan(project(AnalysisKind.THERMAL), (resource("solver-a"),))
    except ValueError as exc:
        assert str(exc) == "no compatible engineering resource"
    else:
        raise AssertionError("expected ValueError")


def test_disabled_resource_is_rejected() -> None:
    planner = EngineeringPlanner()
    try:
        planner.plan(
            project(AnalysisKind.STRUCTURAL),
            (resource("offline", enabled=False),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible engineering resource"
    else:
        raise AssertionError("expected ValueError")


def test_resource_requirements_are_enforced() -> None:
    planner = EngineeringPlanner()
    try:
        planner.plan(
            project(AnalysisKind.STRUCTURAL),
            (resource("small", cpu=2, memory=2048),),
            min_cpu_cores=4,
            min_memory_mib=8192,
        )
    except ValueError as exc:
        assert str(exc) == "no compatible engineering resource"
    else:
        raise AssertionError("expected ValueError")


def test_resource_limit_is_bounded() -> None:
    planner = EngineeringPlanner()
    result = planner.plan(
        project(AnalysisKind.STRUCTURAL),
        (resource("solver-b"), resource("solver-a")),
        max_resources=1,
    )
    assert result.resource_ids == ("solver-a",)


def test_duplicate_analysis_kinds_are_rejected() -> None:
    try:
        project(AnalysisKind.STRUCTURAL, AnalysisKind.STRUCTURAL)
    except ValueError as exc:
        assert str(exc) == "analysis_kinds must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_duplicate_resource_ids_are_rejected() -> None:
    planner = EngineeringPlanner()
    item = resource("same")
    try:
        planner.normalize_resources((item, item))
    except ValueError as exc:
        assert str(exc) == "resource IDs must be unique"
    else:
        raise AssertionError("expected ValueError")
