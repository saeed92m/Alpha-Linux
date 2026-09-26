from alpha_core.creator import (
    CreatorMediaKind,
    CreatorPlanner,
    CreatorProject,
    CreatorRequirement,
    CreatorTool,
)


def tool(
    tool_id: str,
    *,
    media_kinds: tuple[CreatorMediaKind, ...] = (CreatorMediaKind.IMAGE,),
    capabilities: tuple[str, ...] = ("edit",),
    enabled: bool = True,
) -> CreatorTool:
    return CreatorTool(
        tool_id,
        tool_id,
        media_kinds,
        capabilities,
        enabled,
    )


def requirement(
    requirement_id: str = "req-1",
    *,
    media_kind: CreatorMediaKind = CreatorMediaKind.IMAGE,
    capabilities: tuple[str, ...] = ("edit",),
) -> CreatorRequirement:
    return CreatorRequirement(requirement_id, media_kind, capabilities)


def project(
    *,
    media_kinds: tuple[CreatorMediaKind, ...] = (CreatorMediaKind.IMAGE,),
) -> CreatorProject:
    return CreatorProject("project-1", "Alpha Creator Project", media_kinds)


def test_tool_normalization_is_deterministic() -> None:
    planner = CreatorPlanner()
    result = planner.normalize_tools((tool("tool-b"), tool("tool-a")))
    assert tuple(item.tool_id for item in result) == ("tool-a", "tool-b")


def test_requirement_normalization_is_deterministic() -> None:
    planner = CreatorPlanner()
    result = planner.normalize_requirements(
        (requirement("req-b"), requirement("req-a"))
    )
    assert tuple(item.requirement_id for item in result) == ("req-a", "req-b")


def test_media_kind_and_capabilities_are_enforced() -> None:
    planner = CreatorPlanner()
    result = planner.plan(
        project(),
        (tool("image-editor"),),
        (requirement(),),
    )
    assert result.project_id == "project-1"
    assert result.tool_ids == ("image-editor",)
    assert result.requirement_ids == ("req-1",)

    try:
        planner.plan(
            project(),
            (tool("image-editor", capabilities=("retouch",)),),
            (requirement(capabilities=("edit", "export")),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible creator tool"
    else:
        raise AssertionError("expected ValueError")


def test_project_media_kind_is_enforced() -> None:
    planner = CreatorPlanner()
    try:
        planner.plan(
            project(),
            (tool("video-editor", media_kinds=(CreatorMediaKind.VIDEO,)),),
            (
                requirement(
                    media_kind=CreatorMediaKind.VIDEO,
                ),
            ),
        )
    except ValueError as exc:
        assert str(exc) == "project lacks required media kind"
    else:
        raise AssertionError("expected ValueError")


def test_disabled_tool_is_rejected() -> None:
    planner = CreatorPlanner()
    try:
        planner.plan(
            project(),
            (tool("offline", enabled=False),),
            (requirement(),),
        )
    except ValueError as exc:
        assert str(exc) == "no compatible creator tool"
    else:
        raise AssertionError("expected ValueError")


def test_tool_limit_is_bounded() -> None:
    planner = CreatorPlanner()
    requirements = (
        requirement("image", media_kind=CreatorMediaKind.IMAGE),
        requirement(
            "video",
            media_kind=CreatorMediaKind.VIDEO,
            capabilities=("edit",),
        ),
    )
    tools = (
        tool("image-tool", media_kinds=(CreatorMediaKind.IMAGE,)),
        tool("video-tool", media_kinds=(CreatorMediaKind.VIDEO,)),
    )
    result = planner.plan(
        CreatorProject(
            "project-2",
            "Mixed Creator Project",
            (CreatorMediaKind.IMAGE, CreatorMediaKind.VIDEO),
        ),
        tools,
        requirements,
        max_tools=2,
    )
    assert result.tool_ids == ("image-tool", "video-tool")

    try:
        planner.plan(
            CreatorProject(
                "project-2",
                "Mixed Creator Project",
                (CreatorMediaKind.IMAGE, CreatorMediaKind.VIDEO),
            ),
            tools,
            requirements,
            max_tools=1,
        )
    except ValueError as exc:
        assert str(exc) == "creator plan exceeds tool limit"
    else:
        raise AssertionError("expected ValueError")


def test_duplicate_ids_are_rejected() -> None:
    planner = CreatorPlanner()
    item = tool("same")
    try:
        planner.normalize_tools((item, item))
    except ValueError as exc:
        assert str(exc) == "tool IDs must be unique"
    else:
        raise AssertionError("expected ValueError")

    item = requirement("same")
    try:
        planner.normalize_requirements((item, item))
    except ValueError as exc:
        assert str(exc) == "requirement IDs must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_invalid_creator_contracts_are_rejected() -> None:
    try:
        CreatorProject(
            "project-1",
            "Alpha",
            (),
        )
    except ValueError as exc:
        assert str(exc) == "media_kinds must be non-empty"
    else:
        raise AssertionError("expected ValueError")

    try:
        tool("invalid", capabilities=())
    except ValueError as exc:
        assert str(exc) == "capabilities must be non-empty"
    else:
        raise AssertionError("expected ValueError")
