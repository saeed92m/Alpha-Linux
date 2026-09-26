from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib

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
        elif config.hidpi_scale != 1.0 and capabilities.interaction.hidpi is IntegrationState.UNAVAILABLE:
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
