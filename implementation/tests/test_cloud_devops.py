from alpha_core.cloud_devops import (
    CloudDevOpsPlanner,
    CloudEnvironment,
    CloudRequirement,
    CloudService,
    CloudCapabilityKind,
    EnvironmentKind,
    ServiceKind,
)


def service(
    service_id: str = "svc-1",
    kind: ServiceKind = ServiceKind.COMPUTE,
    environment_kinds: tuple[EnvironmentKind, ...] = (EnvironmentKind.DEVELOPMENT,),
    capabilities: tuple[str, ...] = ("build",),
) -> CloudService:
    return CloudService(service_id, kind, environment_kinds, capabilities)


def test_environment_rejects_duplicate_services() -> None:
    item = service()
    try:
        CloudEnvironment(
            "env-1",
            "Development",
            (EnvironmentKind.DEVELOPMENT,),
            (item, item),
        )
    except ValueError as exc:
        assert str(exc) == "service IDs must be unique"
    else:
        raise AssertionError("expected duplicate service rejection")


def test_environment_rejects_out_of_scope_service() -> None:
    item = service(environment_kinds=(EnvironmentKind.PRODUCTION,))
    try:
        CloudEnvironment(
            "env-1",
            "Development",
            (EnvironmentKind.DEVELOPMENT,),
            (item,),
        )
    except ValueError as exc:
        assert str(exc) == "service environment kind is outside environment scope"
    else:
        raise AssertionError("expected scope rejection")


def test_planner_normalizes_and_selects_compatible_service() -> None:
    environment = CloudEnvironment(
        "env-1",
        "Development",
        (EnvironmentKind.DEVELOPMENT,),
        (
            service("svc-2"),
            service("svc-1"),
        ),
    )
    requirement = CloudRequirement(
        "req-1",
        CloudCapabilityKind.PROVISIONING,
        EnvironmentKind.DEVELOPMENT,
        ("build",),
    )
    plan = CloudDevOpsPlanner().plan(environment, (requirement,))
    assert plan.service_ids == ("svc-1",)
    assert plan.requirement_ids == ("req-1",)


def test_planner_rejects_out_of_scope_requirement() -> None:
    environment = CloudEnvironment(
        "env-1", "Development", (EnvironmentKind.DEVELOPMENT,)
    )
    requirement = CloudRequirement(
        "req-1",
        CloudCapabilityKind.SECURITY,
        EnvironmentKind.PRODUCTION,
        ("scan",),
    )
    try:
        CloudDevOpsPlanner().plan(environment, (requirement,))
    except ValueError as exc:
        assert str(exc) == "environment lacks required environment kind"
    else:
        raise AssertionError("expected scope rejection")


def test_planner_rejects_incompatible_service() -> None:
    environment = CloudEnvironment(
        "env-1", "Development", (EnvironmentKind.DEVELOPMENT,), (service(),)
    )
    requirement = CloudRequirement(
        "req-1",
        CloudCapabilityKind.SECURITY,
        EnvironmentKind.DEVELOPMENT,
        ("scan",),
    )
    try:
        CloudDevOpsPlanner().plan(environment, (requirement,))
    except ValueError as exc:
        assert str(exc) == "no compatible cloud service"
    else:
        raise AssertionError("expected compatibility rejection")


def test_planner_rejects_invalid_bound() -> None:
    environment = CloudEnvironment(
        "env-1", "Development", (EnvironmentKind.DEVELOPMENT,)
    )
    try:
        CloudDevOpsPlanner().plan(environment, (), max_services=0)
    except ValueError as exc:
        assert str(exc) == "max_services must be positive"
    else:
        raise AssertionError("expected bound rejection")


def test_requirement_rejects_empty_capabilities() -> None:
    try:
        CloudRequirement(
            "req-1",
            CloudCapabilityKind.OBSERVABILITY,
            EnvironmentKind.DEVELOPMENT,
            (),
        )
    except ValueError as exc:
        assert str(exc) == "required_capabilities must be non-empty"
    else:
        raise AssertionError("expected empty capability rejection")
