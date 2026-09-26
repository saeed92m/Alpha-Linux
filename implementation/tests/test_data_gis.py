from alpha_core.data_gis import (
    DataAnalysisRequirement,
    DataGISPlanner,
    DataKind,
    DataLayer,
    DataProject,
    DataTool,
    LayerRole,
    SpatialReference,
    SpatialReferenceKind,
)


def layer(
    layer_id: str,
    data_kind: DataKind = DataKind.TABULAR,
    role: LayerRole = LayerRole.SOURCE,
    spatial_reference: SpatialReference | None = None,
) -> DataLayer:
    return DataLayer(layer_id, layer_id, data_kind, role, spatial_reference)


def tool(
    tool_id: str,
    data_kinds: tuple[DataKind, ...] = (DataKind.TABULAR,),
    capabilities: tuple[str, ...] = ("query",),
    spatial_reference_kinds: tuple[SpatialReferenceKind, ...] = (),
    enabled: bool = True,
) -> DataTool:
    return DataTool(
        tool_id,
        tool_id,
        data_kinds,
        capabilities,
        spatial_reference_kinds,
        enabled,
    )


def req(
    requirement_id: str = "req-1",
    data_kind: DataKind = DataKind.TABULAR,
    capabilities: tuple[str, ...] = ("query",),
    spatial_reference_kind: SpatialReferenceKind | None = None,
) -> DataAnalysisRequirement:
    return DataAnalysisRequirement(
        requirement_id, data_kind, capabilities, spatial_reference_kind
    )


def project(
    data_kinds: tuple[DataKind, ...] = (DataKind.TABULAR,),
    layers: tuple[DataLayer, ...] = (),
) -> DataProject:
    return DataProject("project-1", "Alpha Data Project", data_kinds, layers)


def test_layer_roles_and_normalization() -> None:
    planner = DataGISPlanner()
    result = planner.normalize_layers(
        (
            layer("z", role=LayerRole.OUTPUT),
            layer("a"),
            layer("m", role=LayerRole.DERIVED),
        )
    )
    assert tuple(item.layer_id for item in result) == ("a", "m", "z")
    assert {item.role for item in result} == set(LayerRole)


def test_spatial_reference_contract() -> None:
    spatial_reference = SpatialReference(
        "epsg-4326", SpatialReferenceKind.GEOGRAPHIC, "EPSG", "4326"
    )
    assert spatial_reference.code == "4326"

    try:
        SpatialReference("epsg-4326", SpatialReferenceKind.GEOGRAPHIC, "", "4326")
    except ValueError as exc:
        assert str(exc) == "authority is required"
    else:
        raise AssertionError("expected ValueError")


def test_planning_and_spatial_compatibility() -> None:
    spatial_reference = SpatialReference(
        "epsg-4326", SpatialReferenceKind.GEOGRAPHIC, "EPSG", "4326"
    )
    result = DataGISPlanner().plan(
        project(
            data_kinds=(DataKind.VECTOR,),
            layers=(layer("roads", DataKind.VECTOR, spatial_reference=spatial_reference),),
        ),
        (
            tool(
                "gis",
                data_kinds=(DataKind.VECTOR,),
                capabilities=("query", "buffer"),
                spatial_reference_kinds=(SpatialReferenceKind.GEOGRAPHIC,),
            ),
        ),
        (
            req(
                data_kind=DataKind.VECTOR,
                capabilities=("query", "buffer"),
                spatial_reference_kind=SpatialReferenceKind.GEOGRAPHIC,
            ),
        ),
    )
    assert result.layer_ids == ("roads",)
    assert result.tool_ids == ("gis",)

    try:
        DataGISPlanner().plan(
            project(data_kinds=(DataKind.TABULAR,)),
            (tool("tab"),),
            (req(data_kind=DataKind.RASTER),),
        )
    except ValueError as exc:
        assert str(exc) == "project lacks required data kind"
    else:
        raise AssertionError("expected ValueError")


def test_incompatible_and_disabled_tools() -> None:
    try:
        DataGISPlanner().plan(project(), (tool("off", enabled=False),), (req(),))
    except ValueError as exc:
        assert str(exc) == "no compatible data tool"
    else:
        raise AssertionError("expected ValueError")

    try:
        DataGISPlanner().plan(
            project(), (tool("bad", capabilities=("edit",)),), (req(),)
        )
    except ValueError as exc:
        assert str(exc) == "no compatible data tool"
    else:
        raise AssertionError("expected ValueError")


def test_bounded_and_duplicate_ids() -> None:
    planner = DataGISPlanner()

    try:
        planner.plan(
            project(),
            (tool("a"), tool("b")),
            (req("a"), req("b")),
            max_tools=0,
        )
    except ValueError as exc:
        assert str(exc) == "max_tools must be positive"
    else:
        raise AssertionError("expected ValueError")

    try:
        planner.normalize_tools((tool("a"), tool("a")))
    except ValueError as exc:
        assert str(exc) == "tool IDs must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_project_scope_and_invalid_contracts() -> None:
    try:
        DataProject("p", "P", (), ())
    except ValueError as exc:
        assert str(exc) == "data_kinds must be non-empty"
    else:
        raise AssertionError("expected ValueError")

    try:
        DataProject(
            "p",
            "P",
            (DataKind.TABULAR,),
            (layer("r", DataKind.RASTER),),
        )
    except ValueError as exc:
        assert str(exc) == "layer data kind is outside project scope"
    else:
        raise AssertionError("expected ValueError")

    try:
        DataAnalysisRequirement("r", DataKind.TABULAR, ())
    except ValueError as exc:
        assert str(exc) == "required_capabilities must be non-empty"
    else:
        raise AssertionError("expected ValueError")
