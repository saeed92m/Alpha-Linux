from alpha_core.command_bar import (
    CommandBarPlanner,
    CommandDescriptor,
    CommandInvocation,
)


def commands() -> tuple[CommandDescriptor, ...]:
    return (
        CommandDescriptor("system.status", "System Status", 0),
        CommandDescriptor("open.app", "Open Application", 1),
        CommandDescriptor("disabled.command", "Disabled", 2, False),
    )


def test_command_normalization_is_deterministic() -> None:
    normalized = CommandBarPlanner().normalize(commands())
    assert [command.command_id for command in normalized] == [
        "disabled.command",
        "open.app",
        "system.status",
    ]


def test_command_plan_resolves_known_command() -> None:
    plan = CommandBarPlanner().plan(
        commands(),
        CommandInvocation("open.app", ("terminal",)),
    )
    assert plan.command.command_id == "open.app"
    assert plan.invocation.arguments == ("terminal",)


def test_unknown_command_is_rejected() -> None:
    try:
        CommandBarPlanner().plan(commands(), CommandInvocation("missing"))
    except ValueError as exc:
        assert str(exc) == "unknown command"
    else:
        raise AssertionError("expected rejection")


def test_unavailable_command_is_rejected() -> None:
    try:
        CommandBarPlanner().plan(
            commands(), CommandInvocation("disabled.command")
        )
    except ValueError as exc:
        assert str(exc) == "command is unavailable"
    else:
        raise AssertionError("expected rejection")


def test_argument_limit_is_enforced() -> None:
    try:
        CommandBarPlanner().plan(
            commands(), CommandInvocation("open.app", ("one", "two"))
        )
    except ValueError as exc:
        assert str(exc) == "argument limit exceeded"
    else:
        raise AssertionError("expected rejection")


def test_invalid_command_contract_is_rejected() -> None:
    try:
        CommandDescriptor(" ", "Invalid")
    except ValueError as exc:
        assert str(exc) == "command_id is required"
    else:
        raise AssertionError("expected rejection")
