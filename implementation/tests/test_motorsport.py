from alpha_core.motorsport import (
    MotorsportComponent,
    MotorsportComponentKind,
    MotorsportPlanner,
    MotorsportVehicle,
    SetupRequirement,
)


def vehicle(*capabilities: str) -> MotorsportVehicle:
    return MotorsportVehicle("car-1", "Alpha Race Car", capabilities)


def component(
    component_id: str,
    kind: MotorsportComponentKind = MotorsportComponentKind.POWERTRAIN,
    capabilities: tuple[str, ...] = ("track",),
    enabled: bool = True,
) -> MotorsportComponent:
    return MotorsportComponent(component_id, component_id, kind, capabilities, enabled)


def requirement(
    requirement_id: str,
    kind: MotorsportComponentKind = MotorsportComponentKind.POWERTRAIN,
    capabilities: tuple[str, ...] = ("track",),
) -> SetupRequirement:
    return SetupRequirement(requirement_id, kind, capabilities)


def test_component_normalization_is_deterministic() -> None:
    planner = MotorsportPlanner()
    result = planner.normalize_components((component("component-b"), component("component-a")))
    assert tuple(item.component_id for item in result) == ("component-a", "component-b")


def test_requirement_normalization_is_deterministic() -> None:
    planner = MotorsportPlanner()
    result = planner.normalize_requirements((requirement("req-b"), requirement("req-a")))
    assert tuple(item.requirement_id for item in result) == ("req-a", "req-b")


def test_setup_plan_is_deterministic_and_compatible() -> None:
    planner = MotorsportPlanner()
    result = planner.plan(
        vehicle("track"),
        (component("power-b"), component("power-a")),
        (requirement("power"),),
    )
    assert result.vehicle_id == "car-1"
    assert result.component_ids == ("power-a",)
    assert result.requirement_ids == ("power",)


def test_vehicle_capability_is_enforced() -> None:
    planner = MotorsportPlanner()
    try:
        planner.plan(
            vehicle("track"),
            (component("power"),),
            (requirement("power", capabilities=("drag",)),),
        )
    except ValueError as exc:
        assert str(exc) == "vehicle lacks required setup capabilities"
    else:
        raise AssertionError("expected ValueError")


def test_component_kind_and_capability_are_enforced() -> None:
    planner = MotorsportPlanner()
    try:
        planner.plan(
            vehicle("track"),
            (component("chassis", MotorsportComponentKind.CHASSIS),),
            (requirement("power"),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible motorsport component"
    else:
        raise AssertionError("expected ValueError")


def test_disabled_component_is_rejected() -> None:
    planner = MotorsportPlanner()
    try:
        planner.plan(
            vehicle("track"),
            (component("offline", enabled=False),),
            (requirement("power"),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible motorsport component"
    else:
        raise AssertionError("expected ValueError")


def test_component_limit_is_bounded() -> None:
    planner = MotorsportPlanner()
    requirements = (
        requirement("power"),
        requirement("drive", MotorsportComponentKind.DRIVETRAIN),
    )
    components = (
        component("drive", MotorsportComponentKind.DRIVETRAIN),
        component("power"),
    )
    result = planner.plan(vehicle("track"), components, requirements, max_components=2)
    assert result.component_ids == ("drive", "power")

    try:
        planner.plan(vehicle("track"), components, requirements, max_components=1)
    except ValueError as exc:
        assert str(exc) == "setup exceeds component limit"
    else:
        raise AssertionError("expected ValueError")


def test_duplicate_ids_are_rejected() -> None:
    planner = MotorsportPlanner()
    item = component("same")
    try:
        planner.normalize_components((item, item))
    except ValueError as exc:
        assert str(exc) == "component IDs must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_duplicate_requirement_ids_are_rejected() -> None:
    planner = MotorsportPlanner()
    item = requirement("same")
    try:
        planner.normalize_requirements((item, item))
    except ValueError as exc:
        assert str(exc) == "requirement IDs must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_invalid_empty_contracts_are_rejected() -> None:
    try:
        MotorsportVehicle("", "Alpha Race Car", ())
    except ValueError as exc:
        assert str(exc) == "vehicle_id is required"
    else:
        raise AssertionError("expected ValueError")

    try:
        SetupRequirement("req", MotorsportComponentKind.DATA, ())
    except ValueError as exc:
        assert str(exc) == "required_capabilities must be non-empty"
    else:
        raise AssertionError("expected ValueError")
