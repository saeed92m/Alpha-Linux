import pytest

from alpha_core.profiles import Profile, ProfileRegistry, ProfileResolver


def test_profile_registry_is_deterministic():
    registry = ProfileRegistry(
        (
            Profile("work", "Work", "Workstation profile", {"ui.theme": "dark"}),
            Profile("default", "Default", "Default profile", {"ui.theme": "system"}),
        )
    )

    assert [profile.profile_id for profile in registry.list()] == ["default", "work"]
    assert registry.get("work").name == "Work"


def test_profile_resolver_applies_overlay_precedence():
    registry = ProfileRegistry(
        (
            Profile("base", "Base", "Base settings", {"ui.theme": "system", "power.mode": "balanced"}),
            Profile("work", "Work", "Work settings", {"ui.theme": "dark"}),
        )
    )

    resolved = ProfileResolver(registry).resolve(("base", "work"))

    assert resolved == {"power.mode": "balanced", "ui.theme": "dark"}


def test_unknown_profiles_are_ignored_safely():
    registry = ProfileRegistry()
    assert ProfileResolver(registry).resolve(("missing",)) == {}


def test_profile_settings_require_namespaced_keys():
    with pytest.raises(ValueError):
        Profile("bad", "Bad", "Bad profile", {"theme": "dark"})


def test_duplicate_profile_ids_are_rejected():
    with pytest.raises(ValueError):
        ProfileRegistry(
            (
                Profile("same", "A", "A", {}),
                Profile("same", "B", "B", {}),
            )
        )
