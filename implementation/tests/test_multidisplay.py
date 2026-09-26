from alpha_core.multidisplay import DisplayNode, DisplayTopology, MultiDisplayPlanner


def test_normalize_orders_displays_and_selects_primary() -> None:
    topology = MultiDisplayPlanner().normalize(
        (
            DisplayNode("display-b", 2560, 1440, 1.5),
            DisplayNode("display-a", 1920, 1080, 1.0),
        )
    )
    assert tuple(display.display_id for display in topology.displays) == (
        "display-a",
        "display-b",
    )
    assert tuple(display.primary for display in topology.displays) == (True, False)


def test_explicit_primary_is_preserved() -> None:
    topology = MultiDisplayPlanner().normalize(
        (
            DisplayNode("display-b", 2560, 1440, 1.5, primary=True),
            DisplayNode("display-a", 1920, 1080, 1.0),
        )
    )
    assert tuple(display.primary for display in topology.displays) == (False, True)


def test_duplicate_display_ids_are_rejected() -> None:
    try:
        DisplayTopology(
            (
                DisplayNode("display-a", 1920, 1080, 1.0, primary=True),
                DisplayNode("display-a", 2560, 1440, 1.5),
            )
        )
    except ValueError as exc:
        assert str(exc) == "display identifiers must be unique"
    else:
        raise AssertionError("expected duplicate display rejection")


def test_multiple_primary_displays_are_rejected() -> None:
    try:
        DisplayTopology(
            (
                DisplayNode("display-a", 1920, 1080, 1.0, primary=True),
                DisplayNode("display-b", 2560, 1440, 1.5, primary=True),
            )
        )
    except ValueError as exc:
        assert str(exc) == "topology must contain exactly one primary display"
    else:
        raise AssertionError("expected primary display rejection")


def test_unknown_display_selection_is_rejected() -> None:
    topology = DisplayTopology(
        (DisplayNode("display-a", 1920, 1080, 1.0, primary=True),)
    )
    try:
        MultiDisplayPlanner().select(("display-b",), topology)
    except ValueError as exc:
        assert str(exc) == "requested display is unavailable"
    else:
        raise AssertionError("expected unavailable display rejection")


def test_selection_is_deterministic() -> None:
    topology = DisplayTopology(
        (
            DisplayNode("display-a", 1920, 1080, 1.0, primary=True),
            DisplayNode("display-b", 2560, 1440, 1.5),
        )
    )
    result = MultiDisplayPlanner().select(("display-b", "display-a"), topology)
    assert tuple(display.display_id for display in result) == (
        "display-a",
        "display-b",
    )
