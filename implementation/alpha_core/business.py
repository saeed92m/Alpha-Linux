from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BusinessKind(str, Enum):
    OPERATIONS = "operations"
    SALES = "sales"
    FINANCE = "finance"
    PROJECT = "project"


class WorkflowRole(str, Enum):
    INPUT = "input"
    PROCESS = "process"
    OUTPUT = "output"


class BusinessCapabilityKind(str, Enum):
    PLANNING = "planning"
    ANALYSIS = "analysis"
    REPORTING = "reporting"
    AUTOMATION = "automation"


@dataclass(frozen=True)
class BusinessCapability:
    capability_id: str
    kind: BusinessCapabilityKind
    business_kinds: tuple[BusinessKind, ...]
    capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("capability_id is required")
        if not self.business_kinds:
            raise ValueError("business_kinds must be non-empty")
        if len(set(self.business_kinds)) != len(self.business_kinds):
            raise ValueError("business_kinds must be unique")
        if not self.capabilities:
            raise ValueError("capabilities must be non-empty")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")
        if any(not item.strip() for item in self.capabilities):
            raise ValueError("capabilities must be non-empty")


@dataclass(frozen=True)
class BusinessWorkflow:
    workflow_id: str
    name: str
    business_kind: BusinessKind
    role: WorkflowRole

    def __post_init__(self) -> None:
        if not self.workflow_id.strip():
            raise ValueError("workflow_id is required")
        if not self.name.strip():
            raise ValueError("name is required")


@dataclass(frozen=True)
class BusinessWorkspace:
    workspace_id: str
    name: str
    business_kinds: tuple[BusinessKind, ...]
    workflows: tuple[BusinessWorkflow, ...] = ()

    def __post_init__(self) -> None:
        if not self.workspace_id.strip():
            raise ValueError("workspace_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.business_kinds:
            raise ValueError("business_kinds must be non-empty")
        if len(set(self.business_kinds)) != len(self.business_kinds):
            raise ValueError("business_kinds must be unique")
        workflow_ids = [workflow.workflow_id for workflow in self.workflows]
        if len(set(workflow_ids)) != len(workflow_ids):
            raise ValueError("workflow IDs must be unique")
        scope = set(self.business_kinds)
        if any(workflow.business_kind not in scope for workflow in self.workflows):
            raise ValueError("workflow business kind is outside workspace scope")


@dataclass(frozen=True)
class BusinessRequirement:
    requirement_id: str
    capability_kind: BusinessCapabilityKind
    business_kind: BusinessKind
    required_capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("requirement_id is required")
        if not self.required_capabilities:
            raise ValueError("required_capabilities must be non-empty")
        if len(set(self.required_capabilities)) != len(self.required_capabilities):
            raise ValueError("required_capabilities must be unique")
        if any(not item.strip() for item in self.required_capabilities):
            raise ValueError("required_capabilities must be non-empty")


@dataclass(frozen=True)
class BusinessPlan:
    workspace_id: str
    workflow_ids: tuple[str, ...]
    capability_ids: tuple[str, ...]
    requirement_ids: tuple[str, ...]


class BusinessPlanner:
    """Deterministic business capability/workflow planning only."""

    def normalize_workflows(
        self, workflows: tuple[BusinessWorkflow, ...]
    ) -> tuple[BusinessWorkflow, ...]:
        ids = [workflow.workflow_id for workflow in workflows]
        if len(set(ids)) != len(ids):
            raise ValueError("workflow IDs must be unique")
        return tuple(sorted(workflows, key=lambda item: item.workflow_id))

    def normalize_capabilities(
        self, capabilities: tuple[BusinessCapability, ...]
    ) -> tuple[BusinessCapability, ...]:
        ids = [item.capability_id for item in capabilities]
        if len(set(ids)) != len(ids):
            raise ValueError("capability IDs must be unique")
        return tuple(sorted(capabilities, key=lambda item: item.capability_id))

    def normalize_requirements(
        self, requirements: tuple[BusinessRequirement, ...]
    ) -> tuple[BusinessRequirement, ...]:
        ids = [item.requirement_id for item in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def plan(
        self,
        workspace: BusinessWorkspace,
        capabilities: tuple[BusinessCapability, ...],
        requirements: tuple[BusinessRequirement, ...],
        max_capabilities: int = 8,
    ) -> BusinessPlan:
        if max_capabilities <= 0:
            raise ValueError("max_capabilities must be positive")

        workflows = self.normalize_workflows(workspace.workflows)
        normalized_capabilities = self.normalize_capabilities(capabilities)
        normalized_requirements = self.normalize_requirements(requirements)
        scope = set(workspace.business_kinds)
        selected: list[BusinessCapability] = []

        for requirement in normalized_requirements:
            if requirement.business_kind not in scope:
                raise ValueError("workspace lacks required business kind")
            compatible = [
                capability
                for capability in normalized_capabilities
                if capability.kind == requirement.capability_kind
                and requirement.business_kind in capability.business_kinds
                and set(requirement.required_capabilities).issubset(
                    set(capability.capabilities)
                )
            ]
            if not compatible:
                raise ValueError("no compatible business capability")
            selected.append(compatible[0])

        selected_ids = tuple(item.capability_id for item in selected)
        if len(set(selected_ids)) > max_capabilities:
            raise ValueError("business plan exceeds capability limit")

        return BusinessPlan(
            workspace_id=workspace.workspace_id,
            workflow_ids=tuple(workflow.workflow_id for workflow in workflows),
            capability_ids=selected_ids,
            requirement_ids=tuple(
                item.requirement_id for item in normalized_requirements
            ),
        )
