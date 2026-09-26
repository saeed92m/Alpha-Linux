from alpha_core.business import (
    BusinessCapability,
    BusinessCapabilityKind,
    BusinessKind,
    BusinessPlanner,
    BusinessRequirement,
    BusinessWorkspace,
    BusinessWorkflow,
    WorkflowRole,
)


def capability(
    capability_id: str = "cap-1",
    kind: BusinessCapabilityKind = BusinessCapabilityKind.PLANNING,
    business_kinds: tuple[BusinessKind, ...] = (BusinessKind.OPERATIONS,),
    capabilities: tuple[str, ...] = ("forecast",),
) -> BusinessCapability:
    return BusinessCapability(capability_id, kind, business_kinds, capabilities)


def test_workspace_rejects_duplicate_workflows() -> None:
    workflow = BusinessWorkflow(
        "wf-1", "Operations", BusinessKind.OPERATIONS, WorkflowRole.PROCESS
    )
    try:
        BusinessWorkspace(
            "ws-1",
            "Workspace",
            (BusinessKind.OPERATIONS,),
            (workflow, workflow),
        )
    except ValueError as exc:
        assert str(exc) == "workflow IDs must be unique"
    else:
        raise AssertionError("expected duplicate workflow rejection")


def test_workspace_rejects_out_of_scope_workflow() -> None:
    workflow = BusinessWorkflow(
        "wf-1", "Sales", BusinessKind.SALES, WorkflowRole.PROCESS
    )
    try:
        BusinessWorkspace(
            "ws-1",
            "Workspace",
            (BusinessKind.OPERATIONS,),
            (workflow,),
        )
    except ValueError as exc:
        assert str(exc) == "workflow business kind is outside workspace scope"
    else:
        raise AssertionError("expected scope rejection")


def test_planner_normalizes_and_selects_compatible_capability() -> None:
    workspace = BusinessWorkspace(
        "ws-1",
        "Operations",
        (BusinessKind.OPERATIONS,),
        (
            BusinessWorkflow(
                "wf-2", "Output", BusinessKind.OPERATIONS, WorkflowRole.OUTPUT
            ),
            BusinessWorkflow(
                "wf-1", "Input", BusinessKind.OPERATIONS, WorkflowRole.INPUT
            ),
        ),
    )
    requirements = (
        BusinessRequirement(
            "req-1",
            BusinessCapabilityKind.PLANNING,
            BusinessKind.OPERATIONS,
            ("forecast",),
        ),
    )
    plan = BusinessPlanner().plan(
        workspace,
        (capability("cap-2"), capability("cap-1")),
        requirements,
    )
    assert plan.workflow_ids == ("wf-1", "wf-2")
    assert plan.capability_ids == ("cap-1",)
    assert plan.requirement_ids == ("req-1",)


def test_planner_rejects_out_of_scope_requirement() -> None:
    workspace = BusinessWorkspace(
        "ws-1", "Operations", (BusinessKind.OPERATIONS,)
    )
    requirement = BusinessRequirement(
        "req-1",
        BusinessCapabilityKind.ANALYSIS,
        BusinessKind.FINANCE,
        ("cashflow",),
    )
    try:
        BusinessPlanner().plan(workspace, (), (requirement,))
    except ValueError as exc:
        assert str(exc) == "workspace lacks required business kind"
    else:
        raise AssertionError("expected scope rejection")


def test_planner_rejects_incompatible_capability() -> None:
    workspace = BusinessWorkspace(
        "ws-1", "Operations", (BusinessKind.OPERATIONS,)
    )
    requirement = BusinessRequirement(
        "req-1",
        BusinessCapabilityKind.ANALYSIS,
        BusinessKind.OPERATIONS,
        ("cashflow",),
    )
    try:
        BusinessPlanner().plan(workspace, (capability(),), (requirement,))
    except ValueError as exc:
        assert str(exc) == "no compatible business capability"
    else:
        raise AssertionError("expected compatibility rejection")


def test_planner_rejects_invalid_bound() -> None:
    workspace = BusinessWorkspace(
        "ws-1", "Operations", (BusinessKind.OPERATIONS,)
    )
    try:
        BusinessPlanner().plan(workspace, (), (), max_capabilities=0)
    except ValueError as exc:
        assert str(exc) == "max_capabilities must be positive"
    else:
        raise AssertionError("expected bound rejection")


def test_requirement_rejects_empty_capabilities() -> None:
    try:
        BusinessRequirement(
            "req-1",
            BusinessCapabilityKind.REPORTING,
            BusinessKind.OPERATIONS,
            (),
        )
    except ValueError as exc:
        assert str(exc) == "required_capabilities must be non-empty"
    else:
        raise AssertionError("expected empty capability rejection")
