from alpha_core.aerospace import AerospacePlanner, AerospaceVehicle, MissionPhase


def vehicle(*capabilities: str) -> AerospaceVehicle:
    return AerospaceVehicle("vehicle-1", "Alpha Vehicle", capabilities)


def test_phase_normalization_is_deterministic() -> None:
    planner = AerospacePlanner()
    phases = (
        MissionPhase("descent", 3),
        MissionPhase("launch", 1),
        MissionPhase("ascent", 2),
    )
    result = planner.normalize_phases(phases)
    assert tuple(phase.phase_id for phase in result) == ("launch", "ascent", "descent")


def test_capability_requirements_are_enforced() -> None:
    planner = AerospacePlanner()
    phases = (MissionPhase("launch", 1, ("guidance",)),)
    assert planner.plan(vehicle("guidance"), phases).phase_ids == ("launch",)
    try:
        planner.plan(vehicle("payload"), phases)
    except ValueError as exc:
        assert str(exc) == "vehicle lacks required mission capabilities"
    else:
        raise AssertionError("expected ValueError")


def test_duplicate_phase_ids_are_rejected() -> None:
    planner = AerospacePlanner()
    phases = (MissionPhase("launch", 1), MissionPhase("launch", 2))
    try:
        planner.normalize_phases(phases)
    except ValueError as exc:
        assert str(exc) == "phase IDs must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_duplicate_phase_sequences_are_rejected() -> None:
    planner = AerospacePlanner()
    phases = (MissionPhase("launch", 1), MissionPhase("ascent", 1))
    try:
        planner.normalize_phases(phases)
    except ValueError as exc:
        assert str(exc) == "phase sequences must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_mission_phase_limit_is_bounded() -> None:
    planner = AerospacePlanner()
    phases = (MissionPhase("launch", 1), MissionPhase("ascent", 2))
    try:
        planner.plan(vehicle("guidance"), phases, max_phases=1)
    except ValueError as exc:
        assert str(exc) == "mission exceeds phase limit"
    else:
        raise AssertionError("expected ValueError")


def test_invalid_vehicle_contract_is_rejected() -> None:
    try:
        AerospaceVehicle("vehicle-1", "Alpha Vehicle", ("guidance", "guidance"))
    except ValueError as exc:
        assert str(exc) == "capabilities must be unique"
    else:
        raise AssertionError("expected ValueError")
