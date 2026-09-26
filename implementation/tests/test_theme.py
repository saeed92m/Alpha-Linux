import pytest

from alpha_core.theme import ThemeDefinition, ThemeResolver, ThemeTokens

def base_theme() -> ThemeDefinition:
    return ThemeDefinition("alpha-dark", "Alpha Dark", ThemeTokens("#101820", "#f4f7fa", "#4da3ff", "#18232e", "#334455"), {"family": "alpha"})

def test_theme_resolution_is_deterministic():
    resolver = ThemeResolver()
    first = resolver.resolve(base_theme(), ({"accent": "#00aaff"}, {"surface": "#202a35"}))
    second = resolver.resolve(base_theme(), ({"accent": "#00aaff"}, {"surface": "#202a35"}))
    assert first == second
    assert first.identity.startswith("theme-")
    assert first.tokens.accent == "#00aaff"
    assert first.metadata["source"] == "declarative"

def test_later_overlay_wins_deterministically():
    result = ThemeResolver().resolve(base_theme(), ({"accent": "#00aaff"}, {"accent": "#ffaa00"}))
    assert result.tokens.accent == "#ffaa00"

def test_unknown_token_is_rejected():
    with pytest.raises(ValueError):
        ThemeResolver().resolve(base_theme(), ({"not-a-token": "#ffffff"},))

def test_invalid_colors_are_rejected():
    with pytest.raises(ValueError):
        ThemeTokens("#000", "#ffffff", "#000000", "#000000", "#000000")

def test_invalid_theme_id_is_rejected():
    with pytest.raises(ValueError):
        ThemeDefinition("Alpha Dark", "Alpha", ThemeTokens("#101820", "#f4f7fa", "#4da3ff", "#18232e", "#334455"))
