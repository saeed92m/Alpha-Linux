from alpha_core.electronics import (
    CircuitRequirement,
    ElectronicsBoard,
    ElectronicsComponent,
    ElectronicsInterface,
    ElectronicsInterfaceKind,
    ElectronicsPlanner,
)


def interface(
    interface_id: str,
    kind: ElectronicsInterfaceKind = ElectronicsInterfaceKind.DIGITAL,
    capabilities: tuple[str, ...] = ("gpio",),
) -> ElectronicsInterface:
    return ElectronicsInterface(interface_id, kind, capabilities)


def board() -> ElectronicsBoard:
    return ElectronicsBoard(
        "board-1",
        "Alpha Control Board",
        (interface("digital-1"),),
    )


def component(
    component_id: str,
    *,
    capabilities: tuple[str, ...] = ("gpio",),
    enabled: bool = True,
) -> ElectronicsComponent:
    return ElectronicsComponent(
        component_id,
        component_id,
        (interface(f"{component_id}-if", capabilities=capabilities),),
        enabled,
    )


def requirement(
    requirement_id: str = "req-1",
    *,
    capabilities: tuple[str, ...] = ("gpio",),
) -> CircuitRequirement:
    return CircuitRequirement(
        requirement_id,
        ElectronicsInterfaceKind.DIGITAL,
        capabilities,
    )


def test_component_normalization_is_deterministic() -> None:
    planner = ElectronicsPlanner()
    result = planner.normalize_components((component("component-b"), component("component-a")))
    assert tuple(item.component_id for item in result) == ("component-a", "component-b")


def test_requirement_normalization_is_deterministic() -> None:
    planner = ElectronicsPlanner()
    result = planner.normalize_requirements((requirement("req-b"), requirement("req-a")))
    assert tuple(item.requirement_id for item in result) == ("req-a", "req-b")


def test_board_and_component_capabilities_are_enforced() -> None:
    planner = ElectronicsPlanner()
    result = planner.plan(
        board(),
        (component("sensor"),),
        (requirement(),),
    )
    assert result.board_id == "board-1"
    assert result.component_ids == ("sensor",)
    assert result.requirement_ids == ("req-1",)

    try:
        planner.plan(
            board(),
            (component("sensor", capabilities=("adc",)),),
            (requirement(capabilities=("pwm",)),),
        )
    except ValueError as exc:
        assert str(exc) == "board lacks required interface capability"
    else:
        raise AssertionError("expected ValueError")


def test_component_incompatibility_is_rejected() -> None:
    planner = ElectronicsPlanner()
    try:
        planner.plan(
            board(),
            (component("sensor", capabilities=("adc",)),),
            (requirement(),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible electronics component"
    else:
        raise AssertionError("expected ValueError")


def test_disabled_component_is_rejected() -> None:
    planner = ElectronicsPlanner()
    try:
        planner.plan(
            board(),
            (component("offline", enabled=False),),
            (requirement(),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible electronics component"
    else:
        raise AssertionError("expected ValueError")


def test_component_limit_is_bounded() -> None:
    planner = ElectronicsPlanner()
    components = (
        component("sensor-a"),
        component("sensor-b"),
    )
    requirements = (
        requirement("req-a"),
        requirement("req-b"),
    )
    result = planner.plan(board(), components, requirements, max_components=2)
    assert result.component_ids == ("sensor-a", "sensor-a")

    try:
        planner.plan(board(), components, requirements, max_components=0)
    except ValueError as exc:
        assert str(exc) == "max_components must be positive"
    else:
        raise AssertionError("expected ValueError")


def test_duplicate_ids_are_rejected() -> None:
    planner = ElectronicsPlanner()
    item = component("same")
    try:
        planner.normalize_components((item, item))
    except ValueError as exc:
        assert str(exc) == "component IDs must be unique"
    else:
        raise AssertionError("expected ValueError")

    item = requirement("same")
    try:
        planner.normalize_requirements((item, item))
    except ValueError as exc:
        assert str(exc) == "requirement IDs must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_invalid_interface_contract_is_rejected() -> None:
    try:
        interface("", capabilities=("gpio",))
    except ValueError as exc:
        assert str(exc) == "interface_id is required"
    else:
        raise AssertionError("expected ValueError")

    try:
        interface("empty", capabilities=())
    except ValueError as exc:
        assert str(exc) == "capabilities must be non-empty"
    else:
        raise AssertionError("expected ValueError")
