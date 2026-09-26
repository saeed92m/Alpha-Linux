from alpha_core.education_research import (
    EducationCapability,
    EducationCapabilityKind,
    EducationKind,
    EducationResearchPlanner,
    EducationRequirement,
    EducationWorkspace,
    EducationWorkflow,
    ResearchRole,
)


def capability(
    capability_id: str = "cap-1",
    kind: EducationCapabilityKind = EducationCapabilityKind.LEARNING,
    education_kinds: tuple[EducationKind, ...] = (EducationKind.STUDY,),
    capabilities: tuple[str, ...] = ("curriculum",),
) -> EducationCapability:
    return EducationCapability(capability_id, kind, education_kinds, capabilities)


def test_workspace_rejects_duplicate_workflows() -> None:
    workflow = EducationWorkflow(
        "wf-1", "Study", EducationKind.STUDY, ResearchRole.INVESTIGATE
    )
    try:
        EducationWorkspace(
            "ws-1", "Workspace", (EducationKind.STUDY,), (workflow, workflow)
        )
    except ValueError as exc:
        assert str(exc) == "workflow IDs must be unique"
    else:
        raise AssertionError("expected duplicate workflow rejection")


def test_workspace_rejects_out_of_scope_workflow() -> None:
    workflow = EducationWorkflow(
        "wf-1", "Research", EducationKind.RESEARCH, ResearchRole.INVESTIGATE
    )
    try:
        EducationWorkspace(
            "ws-1", "Workspace", (EducationKind.STUDY,), (workflow,)
        )
    except ValueError as exc:
        assert str(exc) == "workflow education kind is outside workspace scope"
    else:
        raise AssertionError("expected scope rejection")


def test_planner_normalizes_and_selects_compatible_capability() -> None:
    workspace = EducationWorkspace(
        "ws-1",
        "Research",
        (EducationKind.RESEARCH,),
        (
            EducationWorkflow(
                "wf-2", "Output", EducationKind.RESEARCH, ResearchRole.OUTPUT
            ),
            EducationWorkflow(
                "wf-1", "Investigation", EducationKind.RESEARCH, ResearchRole.INVESTIGATE
            ),
        ),
    )
    requirements = (
        EducationRequirement(
            "req-1",
            EducationCapabilityKind.ANALYSIS,
            EducationKind.RESEARCH,
            ("statistics",),
        ),
    )
    plan = EducationResearchPlanner().plan(
        workspace,
        (
            capability(
                "cap-2", EducationCapabilityKind.ANALYSIS,
                (EducationKind.RESEARCH,), ("statistics",)
            ),
            capability(
                "cap-1", EducationCapabilityKind.ANALYSIS,
                (EducationKind.RESEARCH,), ("statistics",)
            ),
        ),
        requirements,
    )
    assert plan.workflow_ids == ("wf-1", "wf-2")
    assert plan.capability_ids == ("cap-1",)
    assert plan.requirement_ids == ("req-1",)


def test_planner_rejects_out_of_scope_requirement() -> None:
    workspace = EducationWorkspace(
        "ws-1", "Study", (EducationKind.STUDY,)
    )
    requirement = EducationRequirement(
        "req-1",
        EducationCapabilityKind.ANALYSIS,
        EducationKind.RESEARCH,
        ("statistics",),
    )
    try:
        EducationResearchPlanner().plan(workspace, (), (requirement,))
    except ValueError as exc:
        assert str(exc) == "workspace lacks required education kind"
    else:
        raise AssertionError("expected scope rejection")


def test_planner_rejects_incompatible_capability() -> None:
    workspace = EducationWorkspace(
        "ws-1", "Study", (EducationKind.STUDY,)
    )
    requirement = EducationRequirement(
        "req-1",
        EducationCapabilityKind.EXPERIMENT,
        EducationKind.STUDY,
        ("lab",),
    )
    try:
        EducationResearchPlanner().plan(workspace, (capability(),), (requirement,))
    except ValueError as exc:
        assert str(exc) == "no compatible education capability"
    else:
        raise AssertionError("expected compatibility rejection")


def test_planner_rejects_invalid_bound() -> None:
    workspace = EducationWorkspace(
        "ws-1", "Study", (EducationKind.STUDY,)
    )
    try:
        EducationResearchPlanner().plan(workspace, (), (), max_capabilities=0)
    except ValueError as exc:
        assert str(exc) == "max_capabilities must be positive"
    else:
        raise AssertionError("expected bound rejection")


def test_requirement_rejects_empty_capabilities() -> None:
    try:
        EducationRequirement(
            "req-1",
            EducationCapabilityKind.PUBLICATION,
            EducationKind.RESEARCH,
            (),
        )
    except ValueError as exc:
        assert str(exc) == "required_capabilities must be non-empty"
    else:
        raise AssertionError("expected empty capability rejection")
