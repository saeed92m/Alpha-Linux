from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from typing import Mapping

_THEME_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")

@dataclass(frozen=True)
class ThemeTokens:
    background: str
    foreground: str
    accent: str
    surface: str
    border: str

    def __post_init__(self) -> None:
        for name, value in (("background", self.background), ("foreground", self.foreground), ("accent", self.accent), ("surface", self.surface), ("border", self.border)):
            if not _COLOR.fullmatch(value):
                raise ValueError(f"{name} must be a six-digit hexadecimal color")

@dataclass(frozen=True)
class ThemeDefinition:
    theme_id: str
    name: str
    tokens: ThemeTokens
    metadata: Mapping[str, object] = ()

    def __post_init__(self) -> None:
        if not _THEME_ID.fullmatch(self.theme_id):
            raise ValueError("invalid theme identifier")
        if not self.name.strip():
            raise ValueError("theme name is required")

@dataclass(frozen=True)
class ResolvedTheme:
    theme_id: str
    identity: str
    tokens: ThemeTokens
    metadata: Mapping[str, object]

class ThemeResolver:
    """Deterministic declarative theme resolution; never mutates the host."""

    def resolve(self, base: ThemeDefinition, overlays: tuple[Mapping[str, str], ...] = ()) -> ResolvedTheme:
        values = {"background": base.tokens.background, "foreground": base.tokens.foreground, "accent": base.tokens.accent, "surface": base.tokens.surface, "border": base.tokens.border}
        for overlay in overlays:
            for key in sorted(overlay):
                if key not in values:
                    raise ValueError(f"unknown theme token: {key}")
                values[key] = overlay[key]
        tokens = ThemeTokens(**values)
        canonical = "\0".join((base.theme_id, base.name, tokens.background, tokens.foreground, tokens.accent, tokens.surface, tokens.border))
        identity = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
        metadata = dict(base.metadata)
        metadata["source"] = "declarative"
        metadata["overlay_count"] = len(overlays)
        return ResolvedTheme(base.theme_id, f"theme-{identity}", tokens, metadata)
