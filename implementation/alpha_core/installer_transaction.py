from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from .installer_safety import InstallerIntent, ProposedChange, SafetyLevel

CommandRunner = Callable[[Sequence[str]], None]

@dataclass(frozen=True)
class TransactionResult:
    target: Path
    committed: bool
    rolled_back: bool
    backup: Path
    operations: tuple[str, ...]
    error: str | None = None

def _require_disposable_file(path: Path) -> None:
    resolved = path.resolve()
    if not resolved.is_file():
        raise ValueError("transaction target must be an existing regular file")
    if resolved.is_relative_to(Path("/dev")):
        raise ValueError("physical block devices are forbidden")

def _default_runner(command: Sequence[str]) -> None:
    subprocess.run(list(command), check=True, capture_output=True, text=True)

def execute_disposable_transaction(plan: ProposedChange, target: Path, *, confirmed: bool, runner: CommandRunner | None = None, fail_at: int | None = None) -> TransactionResult:
    _require_disposable_file(target)
    if plan.safety is SafetyLevel.BLOCKED:
        raise ValueError("blocked plan cannot execute")
    if not plan.requires_explicit_confirmation or not confirmed:
        raise PermissionError("explicit confirmation is required")
    if plan.intent is not InstallerIntent.ALPHA_ONLY:
        raise ValueError("only alpha-only disposable transactions are supported")
    if fail_at is not None and fail_at < 1:
        raise ValueError("fail_at must be a positive command index")

    run = runner or _default_runner
    backup = target.with_suffix(target.suffix + ".before")
    shutil.copy2(target, backup)
    commands: tuple[tuple[str, ...], ...] = (
        ("sgdisk", "--zap-all", str(target)),
        ("sgdisk", "--clear", "--new=1:2048:+16M", "--typecode=1:ef00", "--change-name=1:Alpha-EFI", str(target)),
        ("sgdisk", "--verify", str(target)),
    )
    executed = 0
    try:
        for index, command in enumerate(commands, start=1):
            if fail_at == index:
                raise RuntimeError(f"fault injected before command {index}")
            run(command)
            executed += 1
    except Exception as exc:
        shutil.copy2(backup, target)
        return TransactionResult(target, False, True, backup, plan.operations, f"{type(exc).__name__}: {exc}")
    if executed != len(commands):
        raise RuntimeError("transaction execution accounting mismatch")
    return TransactionResult(target, True, False, backup, plan.operations)
