from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import os
from pathlib import Path

from .desktop import DesktopCapabilities, DesktopSessionConfig


class IntegrationState(str, Enum):
    SUPPORTED = "supported"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class CosmicIntegrationDescriptor:
    compositor: str
    session_type: str
    protocol: str
    version: str

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.compositor, self.session_type, self.protocol, self.version)):
            raise ValueError("COSMIC integration metadata is required")


@dataclass(frozen=True)
class CosmicSessionBinding:
    binding_id: str
    session_id: str
    integration: CosmicIntegrationDescriptor
    state: IntegrationState
    display_ids: tuple[str, ...]
    theme: str


@dataclass(frozen=True)
class CosmicLiveImageEvidence:
    package_names: tuple[str, ...] = ("cosmic-session", "cosmic-desktop")
    desktop_file: str = "cosmic.desktop"
    session_launcher: str = "start-cosmic"

    def validate_root(self, root: Path) -> dict[str, object]:
        desktop_candidates = (
            root / "usr/share/xsessions" / self.desktop_file,
            root / "usr/share/wayland-sessions" / self.desktop_file,
        )
        launcher_candidates = (
            root / "usr/bin" / self.session_launcher,
            root / "usr/local/bin" / self.session_launcher,
        )

        desktop_path = next((path for path in desktop_candidates if path.exists()), None)
        if desktop_path is None:
            raise ValueError("missing cosmic.desktop in live rootfs")

        launcher_path = next(
            (path for path in launcher_candidates if path.exists() and os.access(path, os.X_OK)),
            None,
        )
        if launcher_path is None:
            raise ValueError("missing executable start-cosmic in live rootfs")

        status_path = root / "var/lib/dpkg/status"
        if not status_path.exists():
            raise ValueError("dpkg status file is missing; live rootfs is incomplete")

        status_text = status_path.read_text(encoding="utf-8", errors="ignore")
        missing_packages = [
            package for package in self.package_names if f"Package: {package}" not in status_text
        ]
        if missing_packages:
            raise ValueError(f"missing COSMIC packages: {missing_packages}")

        payload = {
            "desktop_file": str(desktop_path),
            "session_launcher": str(launcher_path),
            "required_packages": list(self.package_names),
            "state": "validated",
        }
        return payload


class CosmicReferenceAdapter:
    """Non-mutating COSMIC boundary for future runtime/session integration."""

    def describe(
        self,
        config: DesktopSessionConfig,
        capabilities: DesktopCapabilities,
        integration: CosmicIntegrationDescriptor,
    ) -> CosmicSessionBinding:
        available = {display.display_id for display in capabilities.displays}
        missing = tuple(sorted(set(config.display_ids) - available))
        if missing:
            state = IntegrationState.UNAVAILABLE
        elif config.hidpi_scale != 1.0 and capabilities.interaction.hidpi.value == "unavailable":
            state = IntegrationState.DEGRADED
        else:
            state = IntegrationState.SUPPORTED

        identity = hashlib.sha256(
            "\0".join(
                (
                    config.session_id,
                    integration.compositor,
                    integration.session_type,
                    integration.protocol,
                    integration.version,
                    config.theme,
                    *config.display_ids,
                )
            ).encode("utf-8")
        ).hexdigest()[:16]

        return CosmicSessionBinding(
            binding_id=f"cosmic-{identity}",
            session_id=config.session_id,
            integration=integration,
            state=state,
            display_ids=tuple(config.display_ids),
            theme=config.theme,
        )
