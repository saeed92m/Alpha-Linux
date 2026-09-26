from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class DataKind(str, Enum):
    TABULAR="tabular"
    RASTER="raster"
    VECTOR="vector"
    TIMESERIES="timeseries"

class LayerRole(str, Enum):
    SOURCE="source"
    DERIVED="derived"
    OUTPUT="output"

class SpatialReferenceKind(str, Enum):
    GEOGRAPHIC="geographic"
    PROJECTED="projected"
    LOCAL="local"

@dataclass(frozen=True)
class SpatialReference:
    reference_id: str
    kind: SpatialReferenceKind
    authority: str
    code: str
    def __post_init__(self)->None:
        if not self.reference_id.strip(): raise ValueError("reference_id is required")
        if not self.authority.strip(): raise ValueError("authority is required")
        if not self.code.strip(): raise ValueError("code is required")

@dataclass(frozen=True)
class DataLayer:
    layer_id: str
    name: str
    data_kind: DataKind
    role: LayerRole
    spatial_reference: SpatialReference | None = None
    def __post_init__(self)->None:
        if not self.layer_id.strip(): raise ValueError("layer_id is required")
        if not self.name.strip(): raise ValueError("name is required")

@dataclass(frozen=True)
class DataProject:
    project_id: str
    name: str
    data_kinds: tuple[DataKind,...]
    layers: tuple[DataLayer,...]=()
    def __post_init__(self)->None:
        if not self.project_id.strip(): raise ValueError("project_id is required")
        if not self.name.strip(): raise ValueError("name is required")
        if not self.data_kinds: raise ValueError("data_kinds must be non-empty")
        if len(set(self.data_kinds)) != len(self.data_kinds): raise ValueError("data_kinds must be unique")
        ids=[x.layer_id for x in self.layers]
        if len(set(ids)) != len(ids): raise ValueError("layer IDs must be unique")
        scope=set(self.data_kinds)
        if any(x.data_kind not in scope for x in self.layers): raise ValueError("layer data kind is outside project scope")

@dataclass(frozen=True)
class DataAnalysisRequirement:
    requirement_id: str
    data_kind: DataKind
    required_capabilities: tuple[str,...]
    spatial_reference_kind: SpatialReferenceKind | None=None
    def __post_init__(self)->None:
        if not self.requirement_id.strip(): raise ValueError("requirement_id is required")
        if not self.required_capabilities: raise ValueError("required_capabilities must be non-empty")
        if len(set(self.required_capabilities)) != len(self.required_capabilities): raise ValueError("required_capabilities must be unique")
        if any(not x.strip() for x in self.required_capabilities): raise ValueError("required_capabilities must be non-empty")

@dataclass(frozen=True)
class DataTool:
    tool_id: str
    name: str
    data_kinds: tuple[DataKind,...]
    capabilities: tuple[str,...]
    spatial_reference_kinds: tuple[SpatialReferenceKind,...]=()
    enabled: bool=True
    def __post_init__(self)->None:
        if not self.tool_id.strip(): raise ValueError("tool_id is required")
        if not self.name.strip(): raise ValueError("name is required")
        if not self.data_kinds: raise ValueError("data_kinds must be non-empty")
        if len(set(self.data_kinds)) != len(self.data_kinds): raise ValueError("data_kinds must be unique")
        if not self.capabilities: raise ValueError("capabilities must be non-empty")
        if len(set(self.capabilities)) != len(self.capabilities): raise ValueError("capabilities must be unique")

@dataclass(frozen=True)
class DataPlan:
    project_id: str
    layer_ids: tuple[str,...]
    tool_ids: tuple[str,...]
    requirement_ids: tuple[str,...]

class DataGISPlanner:
    def normalize_layers(self,layers:tuple[DataLayer,...])->tuple[DataLayer,...]:
        ids=[x.layer_id for x in layers]
        if len(set(ids))!=len(ids): raise ValueError("layer IDs must be unique")
        return tuple(sorted(layers,key=lambda x:x.layer_id))
    def normalize_tools(self,tools:tuple[DataTool,...])->tuple[DataTool,...]:
        ids=[x.tool_id for x in tools]
        if len(set(ids))!=len(ids): raise ValueError("tool IDs must be unique")
        return tuple(sorted(tools,key=lambda x:x.tool_id))
    def normalize_requirements(self,requirements:tuple[DataAnalysisRequirement,...])->tuple[DataAnalysisRequirement,...]:
        ids=[x.requirement_id for x in requirements]
        if len(set(ids))!=len(ids): raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements,key=lambda x:x.requirement_id))
    def plan(self,project:DataProject,tools:tuple[DataTool,...],requirements:tuple[DataAnalysisRequirement,...],max_tools:int=8)->DataPlan:
        if max_tools<=0: raise ValueError("max_tools must be positive")
        layers=self.normalize_layers(project.layers); tools=self.normalize_tools(tools); requirements=self.normalize_requirements(requirements)
        scope=set(project.data_kinds); selected=[]
        for req in requirements:
            if req.data_kind not in scope: raise ValueError("project lacks required data kind")
            compatible=[t for t in tools if t.enabled and req.data_kind in t.data_kinds and set(req.required_capabilities).issubset(set(t.capabilities))
                        and (req.spatial_reference_kind is None or req.spatial_reference_kind in t.spatial_reference_kinds)]
            if not compatible: raise ValueError("no compatible data tool")
            selected.append(compatible[0])
        ids=tuple(t.tool_id for t in selected)
        if len(set(ids))>max_tools: raise ValueError("data plan exceeds tool limit")
        return DataPlan(project.project_id,tuple(x.layer_id for x in layers),ids,tuple(x.requirement_id for x in requirements))
