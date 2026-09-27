from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .installer_safety import InstallerIntent, ProposedChange, SafetyLevel


@dataclass(frozen=True)
class TransactionResult:
    target: Path
    committed: bool
    rolled_back: bool
    backup: Path
    operations: tuple[str, ...]


def _require_disposable_file(path: Path) -> None:
    resolved = path.resolve()
    if not resolved.is_file():
        raise ValueError("transaction target must be an existing regular file")
    if str(resolved).startswith("/dev/"):
        raise ValueError("physical block devices are forbidden")


def execute_disposable_transaction(plan: ProposedChange, target: Path, *, confirmed: bool) -> TransactionResult:
    """Execute an Alpha-only plan against a regular-file fixture only."""
    _require_disposable_file(target)
    if plan.safety is SafetyLevel.BLOCKED:
        raise ValueError("blocked plan cannot execute")
    if not plan.requires_explicit_confirmation or not confirmed:
        raise PermissionError("explicit confirmation is required")
    if plan.intent is not InstallerIntent.ALPHA_ONLY:
        raise ValueError("only alpha-only disposable transactions are supported")

    backup = target.with_suffix(target.suffix + ".before")
    shutil.copy2(target, backup)
    try:
        subprocess.run(["sgdisk", "--zap-all", str(target)], check=True, capture_output=True, text=True)
        subprocess.run(
            ["sgdisk", "--clear", "--new=1:2048:+16M", "--typecode=1:ef00",
             "--change-name=1:Alpha-EFI", str(target)],
            check=True, capture_output=True, text=True,
        )
        subprocess.run(["sgdisk", "--verify", str(target)], check=True, capture_output=True, text=True)
    except Exception:
        shutil.copy2(backup, target)
        return TransactionResult(target, False, True, backup, plan.operations)

    return TransactionResult(target, True, False, backup, plan.operations)
