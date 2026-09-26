from alpha_core.data_gis import DataAnalysisRequirement,DataGISPlanner,DataKind,DataLayer,DataProject,DataTool,LayerRole,SpatialReference,SpatialReferenceKind

def layer(i,k=DataKind.TABULAR,r=LayerRole.SOURCE,s=None): return DataLayer(i,i,k,r,s)
def tool(i,k=(DataKind.TABULAR,),c=("query",),s=(),e=True): return DataTool(i,i,k,c,s,e)
def req(i="req-1",k=DataKind.TABULAR,c=("query",),s=None): return DataAnalysisRequirement(i,k,c,s)
def project(k=(DataKind.TABULAR,),layers=()): return DataProject("project-1","Alpha Data Project",k,layers)

def test_layer_roles_and_normalization():
    p=DataGISPlanner(); r=p.normalize_layers((layer("z",r=LayerRole.OUTPUT),layer("a"),layer("m",r=LayerRole.DERIVED)))
    assert tuple(x.layer_id for x in r)==("a","m","z"); assert {x.role for x in r}==set(LayerRole)

def test_spatial_reference_contract():
    s=SpatialReference("epsg-4326",SpatialReferenceKind.GEOGRAPHIC,"EPSG","4326")
    assert s.code=="4326"
    try: SpatialReference("","","EPSG","4326")
    except ValueError as e: assert str(e)=="authority is required"
    else: raise AssertionError("expected ValueError")

def test_planning_and_spatial_compatibility():
    s=SpatialReference("epsg-4326",SpatialReferenceKind.GEOGRAPHIC,"EPSG","4326")
    r=DataGISPlanner().plan(project(layers=(layer("roads",DataKind.VECTOR,s=s),)),
      (tool("gis",k=(DataKind.VECTOR,),c=("query","buffer"),s=(SpatialReferenceKind.GEOGRAPHIC,)),),
      (req(k=DataKind.VECTOR,c=("query","buffer"),s=SpatialReferenceKind.GEOGRAPHIC),))
    assert r.layer_ids==("roads",) and r.tool_ids==("gis",)
    try: DataGISPlanner().plan(project(),(tool("tab",c=("query",)),),(req(k=DataKind.RASTER),))
    except ValueError as e: assert str(e)=="project lacks required data kind"
    else: raise AssertionError("expected ValueError")

def test_incompatible_and_disabled_tools():
    try: DataGISPlanner().plan(project(),(tool("off",e=False),),(req(),))
    except ValueError as e: assert str(e)=="no compatible data tool"
    else: raise AssertionError("expected ValueError")
    try: DataGISPlanner().plan(project(),(tool("bad",c=("edit",)),),(req(),))
    except ValueError as e: assert str(e)=="no compatible data tool"
    else: raise AssertionError("expected ValueError")

def test_bounded_and_duplicate_ids():
    p=DataGISPlanner()
    try: p.plan(project(),(tool("a"),tool("b")),(req("a"),req("b")),max_tools=0)
    except ValueError as e: assert str(e)=="max_tools must be positive"
    else: raise AssertionError("expected ValueError")
    try: p.normalize_tools((tool("a"),tool("a")))
    except ValueError as e: assert str(e)=="tool IDs must be unique"
    else: raise AssertionError("expected ValueError")

def test_project_scope_and_invalid_contracts():
    try: DataProject("p","P",(),())
    except ValueError as e: assert str(e)=="data_kinds must be non-empty"
    else: raise AssertionError("expected ValueError")
    try: DataProject("p","P",(DataKind.TABULAR,),(layer("r",DataKind.RASTER),))
    except ValueError as e: assert str(e)=="layer data kind is outside project scope"
    else: raise AssertionError("expected ValueError")
    try: DataAnalysisRequirement("r",DataKind.TABULAR,())
    except ValueError as e: assert str(e)=="required_capabilities must be non-empty"
    else: raise AssertionError("expected ValueError")
