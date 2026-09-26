from alpha_core.astronomy import (
    AstronomyObservation,
    AstronomyPlanner,
    Photometry,
    SkyPosition,
)


def observation(
    observation_id: str,
    timestamp: str,
    *,
    object_id: str = "obj-1",
    ra: float = 10.0,
    dec: float = 20.0,
) -> AstronomyObservation:
    return AstronomyObservation(
        observation_id,
        object_id,
        "survey-a",
        timestamp,
        SkyPosition(ra, dec),
        Photometry(18.2),
    )


def test_sky_position_validates_coordinate_bounds() -> None:
    assert SkyPosition(0.0, -90.0).ra_deg == 0.0
    assert SkyPosition(359.999, 90.0).dec_deg == 90.0


def test_invalid_sky_position_is_rejected() -> None:
    try:
        SkyPosition(360.0, 0.0)
    except ValueError as exc:
        assert str(exc) == "ra_deg must be in [0, 360)"
    else:
        raise AssertionError("expected ValueError")


def test_normalization_is_deterministic() -> None:
    planner = AstronomyPlanner()
    result = planner.normalize(
        (
            observation("obs-b", "2026-01-02T00:00:00Z"),
            observation("obs-a", "2026-01-01T00:00:00Z"),
        )
    )
    assert tuple(item.observation_id for item in result) == ("obs-a", "obs-b")


def test_plan_filters_object_and_is_bounded() -> None:
    planner = AstronomyPlanner()
    result = planner.plan(
        "obj-1",
        (
            observation("obs-c", "2026-01-03T00:00:00Z"),
            observation("obs-a", "2026-01-01T00:00:00Z"),
            observation("other", "2026-01-01T00:00:00Z", object_id="obj-2"),
        ),
        max_observations=1,
    )
    assert result.observation_ids == ("obs-a",)


def test_duplicate_observation_ids_are_rejected() -> None:
    planner = AstronomyPlanner()
    item = observation("same", "2026-01-01T00:00:00Z")
    try:
        planner.normalize((item, item))
    except ValueError as exc:
        assert str(exc) == "observation IDs must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_missing_object_observations_are_rejected() -> None:
    planner = AstronomyPlanner()
    try:
        planner.plan("obj-2", (observation("obs-a", "2026-01-01T00:00:00Z"),))
    except ValueError as exc:
        assert str(exc) == "no observations for object"
    else:
        raise AssertionError("expected ValueError")


def test_photometry_rejects_non_finite_magnitude() -> None:
    try:
        Photometry(float("nan"))
    except ValueError as exc:
        assert str(exc) == "magnitude must be finite"
    else:
        raise AssertionError("expected ValueError")
