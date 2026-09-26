import pytest

from alpha_core.input import (
    InputCapabilityPlanner,
    InputDeviceDescriptor,
    InputDeviceKind,
    InputProfile,
)


def devices():
    return (
        InputDeviceDescriptor("pen-2", "Studio Pen", InputDeviceKind.PEN, ("pressure", "tilt")),
        InputDeviceDescriptor("touch-1", "Touchscreen", InputDeviceKind.TOUCH, ("contact",)),
    )


def test_input_snapshot_is_deterministic():
    planner = InputCapabilityPlanner()
    first = planner.snapshot(tuple(reversed(devices())))
    second = planner.snapshot(devices())

    assert first == second
    assert [device.device_id for device in first.devices] == ["pen-2", "touch-1"]


def test_devices_can_be_selected_by_kind():
    snapshot = InputCapabilityPlanner().snapshot(devices())

    selected = InputCapabilityPlanner().devices_for_kind(snapshot, InputDeviceKind.PEN)

    assert [device.device_id for device in selected] == ["pen-2"]


def test_duplicate_device_ids_are_rejected():
    duplicate = (
        InputDeviceDescriptor("touch-1", "Touchscreen", InputDeviceKind.TOUCH),
        InputDeviceDescriptor("touch-1", "Second Touchscreen", InputDeviceKind.TOUCH),
    )

    with pytest.raises(ValueError, match="device identifiers"):
        InputCapabilityPlanner().snapshot(duplicate)


def test_profile_rejects_unknown_device():
    snapshot = InputCapabilityPlanner().snapshot(devices())

    with pytest.raises(ValueError, match="unavailable device"):
        InputCapabilityPlanner().validate_profile(
            InputProfile(("pen-9",)),
            snapshot,
        )


def test_profile_is_deterministic():
    snapshot = InputCapabilityPlanner().snapshot(devices())
    profile = InputProfile(("pen-2", "touch-1"))

    assert InputCapabilityPlanner().validate_profile(profile, snapshot) == profile


def test_capabilities_are_unique_and_ordered():
    with pytest.raises(ValueError):
        InputDeviceDescriptor(
            "pen-1",
            "Pen",
            InputDeviceKind.PEN,
            ("tilt", "pressure"),
        )

    with pytest.raises(ValueError):
        InputDeviceDescriptor(
            "pen-1",
            "Pen",
            InputDeviceKind.PEN,
            ("pressure", "pressure"),
        )
