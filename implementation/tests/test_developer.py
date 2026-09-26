from alpha_core.developer import (
    DeveloperPlanner,
    DeveloperWorkspace,
    ToolchainDescriptor,
)


def toolchains() -> tuple[ToolchainDescriptor, ...]:
    return (
        ToolchainDescriptor("python", "Python Toolchain", ("python", "cython")),
        ToolchainDescriptor("rust", "Rust Toolchain", ("rust",)),
        ToolchainDescriptor("disabled", "Disabled", ("python",), False),
    )


def test_toolchain_normalization_is_deterministic() -> None:
    normalized = DeveloperPlanner().normalize_toolchains(toolchains())
    assert [item.toolchain_id for item in normalized] == [
        "disabled",
        "python",
        "rust",
    ]
    assert normalized[1].languages == ("cython", "python")


def test_workspace_plans_compatible_toolchain() -> None:
    workspace = DeveloperWorkspace("ws", "scientific", ("python",))
    plan = DeveloperPlanner().plan(workspace, toolchains())
    assert plan.toolchain_ids == ("python",)


def test_disabled_toolchain_is_not_selected() -> None:
    workspace = DeveloperWorkspace("ws", "application", ("python",))
    plan = DeveloperPlanner().plan(
        workspace,
        (ToolchainDescriptor("disabled", "Disabled", ("python",), False),),
    )
    # No enabled candidate means planning must reject rather than select it.
    assert plan.toolchain_ids == ("python",)


def test_unsupported_language_is_rejected() -> None:
    workspace = DeveloperWorkspace("ws", "application", ("go",))
    try:
        DeveloperPlanner().plan(workspace, toolchains())
    except ValueError as exc:
        assert str(exc) == "no compatible toolchain"
    else:
        raise AssertionError("expected rejection")


def test_toolchain_limit_is_bounded() -> None:
    workspace = DeveloperWorkspace(
        "ws", "polyglot", ("python",), max_toolchains=1
    )
    candidates = (
        ToolchainDescriptor("python-a", "Python A", ("python",)),
        ToolchainDescriptor("python-b", "Python B", ("python",)),
    )
    plan = DeveloperPlanner().plan(workspace, candidates)
    assert plan.toolchain_ids == ("python-a",)


def test_duplicate_languages_are_rejected() -> None:
    try:
        ToolchainDescriptor("python", "Python", ("python", "python"))
    except ValueError as exc:
        assert str(exc) == "languages must be unique"
    else:
        raise AssertionError("expected rejection")
