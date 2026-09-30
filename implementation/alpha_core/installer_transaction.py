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

