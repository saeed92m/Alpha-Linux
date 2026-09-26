from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandDescriptor:
    command_id: str
    title: str
    max_arguments: int = 0
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.command_id.strip():
            raise ValueError("command_id is required")
        if not self.title.strip():
            raise ValueError("title is required")
        if self.max_arguments < 0:
            raise ValueError("max_arguments must be non-negative")


@dataclass(frozen=True)
class CommandInvocation:
    command_id: str
    arguments: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.command_id.strip():
            raise ValueError("command_id is required")
        if any(not argument.strip() for argument in self.arguments):
            raise ValueError("arguments must be non-empty")


@dataclass(frozen=True)
class CommandPlan:
    command: CommandDescriptor
    invocation: CommandInvocation


class CommandBarPlanner:
    """Deterministic planning only; no command execution or host mutation."""

    def normalize(
        self, commands: tuple[CommandDescriptor, ...]
    ) -> tuple[CommandDescriptor, ...]:
        return tuple(sorted(commands, key=lambda command: command.command_id))

    def plan(
        self,
        commands: tuple[CommandDescriptor, ...],
        invocation: CommandInvocation,
    ) -> CommandPlan:
        matches = {
            command.command_id: command
            for command in self.normalize(commands)
        }
        command = matches.get(invocation.command_id)
        if command is None:
            raise ValueError("unknown command")
        if not command.enabled:
            raise ValueError("command is unavailable")
        if len(invocation.arguments) > command.max_arguments:
            raise ValueError("argument limit exceeded")
        return CommandPlan(command=command, invocation=invocation)
