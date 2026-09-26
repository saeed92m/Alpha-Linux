from alpha_core.sdr_rf import (
    RFMode,
    RFRequirement,
    RFFrequencyBand,
    SDRDevice,
    SDRRFPlanner,
)


def device(
    device_id: str,
    *,
    min_frequency: int = 1_000,
    max_frequency: int = 1_000_000,
    sample_rate: int = 2_000_000,
    modes: tuple[RFMode, ...] = (RFMode.IQ,),
    enabled: bool = True,
) -> SDRDevice:
    return SDRDevice(
        device_id,
        device_id,
        min_frequency,
        max_frequency,
        sample_rate,
        modes,
        enabled,
    )


def requirement(
    requirement_id: str = "req-1",
    *,
    frequency: int = 100_000,
    sample_rate: int = 1_000_000,
    mode: RFMode = RFMode.IQ,
) -> RFRequirement:
    return RFRequirement(requirement_id, frequency, sample_rate, mode)


def test_band_contract_validates_frequency_and_modes() -> None:
    band = RFFrequencyBand("vhf", "VHF", 30_000_000, 300_000_000, (RFMode.FM,))
    assert band.end_hz == 300_000_000

    try:
        RFFrequencyBand("invalid", "Invalid", 100, 100, (RFMode.FM,))
    except ValueError as exc:
        assert str(exc) == "frequency range is invalid"
    else:
        raise AssertionError("expected ValueError")


def test_device_normalization_is_deterministic() -> None:
    planner = SDRRFPlanner()
    result = planner.normalize_devices((device("device-b"), device("device-a")))
    assert tuple(item.device_id for item in result) == ("device-a", "device-b")


def test_requirement_normalization_is_deterministic() -> None:
    planner = SDRRFPlanner()
    result = planner.normalize_requirements((requirement("req-b"), requirement("req-a")))
    assert tuple(item.requirement_id for item in result) == ("req-a", "req-b")


def test_frequency_sample_rate_and_mode_are_enforced() -> None:
    planner = SDRRFPlanner()
    result = planner.plan(
        (requirement(),),
        (device("sdr-a"),),
    )
    assert result.requirement_ids == ("req-1",)
    assert result.device_ids == ("sdr-a",)

    try:
        planner.plan(
            (requirement(frequency=2_000_000),),
            (device("sdr-a"),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible SDR device"
    else:
        raise AssertionError("expected ValueError")


def test_mode_incompatibility_is_rejected() -> None:
    planner = SDRRFPlanner()
    try:
        planner.plan(
            (requirement(mode=RFMode.FM),),
            (device("iq-only"),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible SDR device"
    else:
        raise AssertionError("expected ValueError")


def test_disabled_device_is_rejected() -> None:
    planner = SDRRFPlanner()
    try:
        planner.plan(
            (requirement(),),
            (device("offline", enabled=False),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible SDR device"
    else:
        raise AssertionError("expected ValueError")


def test_device_limit_is_bounded() -> None:
    planner = SDRRFPlanner()
    requirements = (
        requirement("iq", frequency=100_000),
        requirement("fm", frequency=200_000, mode=RFMode.FM),
    )
    devices = (
        device("iq-device"),
        device("fm-device", modes=(RFMode.FM,)),
    )
    result = planner.plan(requirements, devices, max_devices=2)
    assert result.device_ids == ("fm-device", "iq-device")

    try:
        planner.plan(requirements, devices, max_devices=1)
    except ValueError as exc:
        assert str(exc) == "RF plan exceeds device limit"
    else:
        raise AssertionError("expected ValueError")


def test_duplicate_ids_are_rejected() -> None:
    planner = SDRRFPlanner()
    item = device("same")
    try:
        planner.normalize_devices((item, item))
    except ValueError as exc:
        assert str(exc) == "device IDs must be unique"
    else:
        raise AssertionError("expected ValueError")

    item = requirement("same")
    try:
        planner.normalize_requirements((item, item))
    except ValueError as exc:
        assert str(exc) == "requirement IDs must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_invalid_device_and_requirement_contracts_are_rejected() -> None:
    try:
        device("invalid", min_frequency=1_000, max_frequency=1_000)
    except ValueError as exc:
        assert str(exc) == "frequency range is invalid"
    else:
        raise AssertionError("expected ValueError")

    try:
        requirement("invalid", sample_rate=0)
    except ValueError as exc:
        assert str(exc) == "sample_rate_sps must be positive"
    else:
        raise AssertionError("expected ValueError")
