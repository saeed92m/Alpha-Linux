from alpha_core.localization import Locale, LocalizationPlan, LocalizationPlanner, TranslationBundle


def locale(locale_id):
    return Locale(locale_id, locale_id.split("-")[0], "")


def bundle(bundle_id, locale_id):
    return TranslationBundle(bundle_id, locale_id, ("title", "menu"))


def test_locale_normalization_is_deterministic():
    result = LocalizationPlanner().normalize_locales((locale("b"), locale("a")))
    assert tuple(item.locale_id for item in result) == ("a", "b")


def test_requested_locale_is_selected():
    result = LocalizationPlanner().plan(
        (locale("en-US"), locale("fa-IR")),
        (bundle("en", "en-US"), bundle("fa", "fa-IR")),
        "fa-IR",
        "en-US",
    )
    assert isinstance(result, LocalizationPlan)
    assert result.fallback_locale_id == "fa-IR"
    assert result.missing_bundle_locale_ids == ()


def test_unsupported_locale_falls_back_to_default():
    result = LocalizationPlanner().plan(
        (locale("en-US"), locale("fa-IR")),
        (bundle("en", "en-US"),),
        "de-DE",
        "en-US",
    )
    assert result.fallback_locale_id == "en-US"


def test_missing_bundle_is_reported():
    result = LocalizationPlanner().plan(
        (locale("en-US"), locale("fa-IR")),
        (bundle("en", "en-US"),),
        "fa-IR",
        "en-US",
    )
    assert result.missing_bundle_locale_ids == ("fa-IR",)


def test_default_locale_must_be_supported():
    try:
        LocalizationPlanner().plan((locale("en-US"),), (), "en-US", "fa-IR")
    except ValueError as exc:
        assert str(exc) == "default locale is not supported"
    else:
        raise AssertionError("expected unsupported default rejection")


def test_duplicate_locale_ids_rejected():
    try:
        LocalizationPlanner().normalize_locales((locale("a"), locale("a")))
    except ValueError as exc:
        assert str(exc) == "locale IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_duplicate_bundle_ids_rejected():
    try:
        LocalizationPlanner().normalize_bundles((bundle("a", "en"), bundle("a", "fa")))
    except ValueError as exc:
        assert str(exc) == "bundle IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_plan_rejects_excess_locales():
    try:
        LocalizationPlanner().plan(
            (locale("a"), locale("b")), (), "a", "a", max_locales=1
        )
    except ValueError as exc:
        assert str(exc) == "localization plan exceeds locale limit"
    else:
        raise AssertionError("expected bound rejection")
