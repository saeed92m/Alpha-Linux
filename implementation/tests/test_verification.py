from alpha_core.verification import (
    VerificationCheck,
    VerificationPlanner,
    VerificationRequest,
    VerificationStatus,
)


def checks() -> tuple[VerificationCheck, ...]:
    return (
        VerificationCheck("security", "security", VerificationStatus.PASS, "clean"),
        VerificationCheck("tests", "tests", VerificationStatus.PASS, "green"),
        VerificationCheck("docs", "docs", VerificationStatus.FAIL, "broken"),
    )


def test_check_normalization_is_deterministic() -> None:
    normalized = VerificationPlanner().normalize(checks())
    assert [check.check_id for check in normalized] == ["docs", "security", "tests"]


def test_all_pass_checks_produce_pass_report() -> None:
    passing = (
        VerificationCheck("a", "tests", VerificationStatus.PASS, "green"),
        VerificationCheck("b", "security", VerificationStatus.PASS, "clean"),
    )
    report = VerificationPlanner().build_report(
        passing, VerificationRequest(2)
    )
    assert report.status is VerificationStatus.PASS


def test_any_failed_check_fails_report() -> None:
    report = VerificationPlanner().build_report(checks(), VerificationRequest(3))
    assert report.status is VerificationStatus.FAIL


def test_check_limit_is_enforced() -> None:
    try:
        VerificationPlanner().build_report(checks(), VerificationRequest(2))
    except ValueError as exc:
        assert str(exc) == "check limit exceeded"
    else:
        raise AssertionError("expected rejection")


def test_duplicate_check_ids_are_rejected() -> None:
    duplicate = (
        VerificationCheck("same", "tests", VerificationStatus.PASS, "a"),
        VerificationCheck("same", "security", VerificationStatus.PASS, "b"),
    )
    try:
        VerificationPlanner().build_report(duplicate, VerificationRequest(2))
    except ValueError as exc:
        assert str(exc) == "check IDs must be unique"
    else:
        raise AssertionError("expected rejection")


def test_invalid_request_is_rejected() -> None:
    try:
        VerificationRequest(0)
    except ValueError as exc:
        assert str(exc) == "max_checks must be positive"
    else:
        raise AssertionError("expected rejection")
