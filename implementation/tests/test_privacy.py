from alpha_core.privacy import (
    PrivacyClassification,
    PrivacyDisposition,
    PrivacyPlanner,
    PrivacyPolicy,
    PrivacyPurpose,
    PrivacyRequest,
)


def policy(
    policy_id: str = "p1",
    *,
    retention_days: int = 30,
    consent_required: bool = True,
) -> PrivacyPolicy:
    return PrivacyPolicy(
        policy_id,
        PrivacyPurpose.RESEARCH,
        PrivacyClassification.PERSONAL,
        retention_days,
        consent_required,
    )


def request(
    request_id: str = "r1",
    *,
    consent_granted: bool = True,
    age_days: int = 1,
    purpose: PrivacyPurpose | None = PrivacyPurpose.RESEARCH,
) -> PrivacyRequest:
    return PrivacyRequest(request_id, purpose, consent_granted, age_days)


def test_normalization_is_deterministic() -> None:
    result = PrivacyPlanner().normalize((policy("b"), policy("a")))
    assert tuple(item.policy_id for item in result) == ("a", "b")


def test_missing_consent_is_denied() -> None:
    decision = PrivacyPlanner().evaluate((policy(),), request(consent_granted=False))
    assert decision.disposition == PrivacyDisposition.DENY
    assert decision.policy_id == "p1"


def test_expired_retention_is_denied() -> None:
    decision = PrivacyPlanner().evaluate(
        (policy(retention_days=3),), request(age_days=4)
    )
    assert decision.disposition == PrivacyDisposition.DENY


def test_missing_purpose_is_denied() -> None:
    decision = PrivacyPlanner().evaluate((policy(),), request(purpose=None))
    assert decision.disposition == PrivacyDisposition.DENY
    assert decision.policy_id is None


def test_valid_request_is_allowed() -> None:
    decision = PrivacyPlanner().evaluate((policy(),), request())
    assert decision.disposition == PrivacyDisposition.ALLOW


def test_duplicate_policy_ids_are_rejected() -> None:
    try:
        PrivacyPlanner().normalize((policy("a"), policy("a")))
    except ValueError as exc:
        assert str(exc) == "policy IDs must be unique"
    else:
        raise AssertionError("expected duplicate rejection")


def test_negative_retention_is_rejected() -> None:
    try:
        policy(retention_days=-1)
    except ValueError as exc:
        assert str(exc) == "retention_days must be non-negative"
    else:
        raise AssertionError("expected retention rejection")


def test_plan_is_bounded_and_sorted() -> None:
    policies = (policy("b"), policy("a"))
    plan = PrivacyPlanner().plan(policies, (request("r2"), request("r1")))
    assert plan.policy_ids == ("a", "b")
    assert plan.denied_request_ids == ()


def test_plan_rejects_excess_policy_count() -> None:
    try:
        PrivacyPlanner().plan((policy("a"), policy("b")), (), max_policies=1)
    except ValueError as exc:
        assert str(exc) == "privacy plan exceeds policy limit"
    else:
        raise AssertionError("expected bound rejection")
