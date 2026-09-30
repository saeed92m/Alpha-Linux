from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .install_staging import InstallManifest, build_manifest


@dataclass(frozen=True)
class PostInstallReport:
    filesystem_ok: bool
    boot_configuration_ok: bool
    health_ok: bool
    manifest: InstallManifest | None
    errors: tuple[str, ...]

    @property
    def success(self) -> bool:
        return self.filesystem_ok and self.boot_configuration_ok and self.health_ok


def verify_post_install(
    target: Path,
    expected_manifest: InstallManifest,
    *,
    boot_entry: Path | None = None,
    health_marker: Path | None = None,
) -> PostInstallReport:
    errors: list[str] = []
    filesystem_ok = target.is_dir()
    actual = None
    if filesystem_ok:
        actual = build_manifest(target)
        if actual != expected_manifest:
            filesystem_ok = False
            errors.append("installed filesystem manifest mismatch")

    boot_ok = boot_entry is not None and boot_entry.is_file()
    if not boot_ok:
        errors.append("boot configuration evidence is missing")

    health_ok = health_marker is not None and health_marker.is_file()
    if not health_ok:
        errors.append("post-install health evidence is missing")

    return PostInstallReport(filesystem_ok, boot_ok, health_ok, actual, tuple(errors))
