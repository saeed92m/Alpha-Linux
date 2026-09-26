from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Locale:
    locale_id: str
    language: str
    region: str = ""

    def __post_init__(self) -> None:
        if not self.locale_id.strip():
            raise ValueError("locale_id is required")
        if not self.language.strip():
            raise ValueError("language is required")


@dataclass(frozen=True)
class TranslationBundle:
    bundle_id: str
    locale_id: str
    keys: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.bundle_id.strip():
            raise ValueError("bundle_id is required")
        if not self.locale_id.strip():
            raise ValueError("locale_id is required")
        if len(set(self.keys)) != len(self.keys):
            raise ValueError("keys must be unique")
        if any(not item.strip() for item in self.keys):
            raise ValueError("keys must be non-empty")


@dataclass(frozen=True)
class LocalizationPlan:
    locale_ids: tuple[str, ...]
    fallback_locale_id: str | None
    missing_bundle_locale_ids: tuple[str, ...]


class LocalizationPlanner:
    """Deterministic localization planning only; no external translation or I/O."""

    def normalize_locales(self, locales: tuple[Locale, ...]) -> tuple[Locale, ...]:
        ids = [item.locale_id for item in locales]
        if len(set(ids)) != len(ids):
            raise ValueError("locale IDs must be unique")
        return tuple(sorted(locales, key=lambda item: item.locale_id))

    def normalize_bundles(self, bundles: tuple[TranslationBundle, ...]) -> tuple[TranslationBundle, ...]:
        ids = [item.bundle_id for item in bundles]
        if len(set(ids)) != len(ids):
            raise ValueError("bundle IDs must be unique")
        return tuple(sorted(bundles, key=lambda item: item.bundle_id))

    def plan(
        self,
        locales: tuple[Locale, ...],
        bundles: tuple[TranslationBundle, ...],
        requested_locale_id: str,
        default_locale_id: str,
        max_locales: int = 32,
    ) -> LocalizationPlan:
        if max_locales <= 0:
            raise ValueError("max_locales must be positive")
        normalized_locales = self.normalize_locales(locales)
        if len(normalized_locales) > max_locales:
            raise ValueError("localization plan exceeds locale limit")
        locale_ids = {item.locale_id for item in normalized_locales}
        if default_locale_id not in locale_ids:
            raise ValueError("default locale is not supported")
        fallback = requested_locale_id if requested_locale_id in locale_ids else default_locale_id
        bundle_locale_ids = {item.locale_id for item in self.normalize_bundles(bundles)}
        missing = tuple(sorted(locale_ids - bundle_locale_ids))
        return LocalizationPlan(
            locale_ids=tuple(item.locale_id for item in normalized_locales),
            fallback_locale_id=fallback,
            missing_bundle_locale_ids=missing,
        )
