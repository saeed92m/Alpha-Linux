from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EducationKind(str, Enum):
    STUDY = "study"
    RESEARCH = "research"
    TEACHING = "teaching"
    TRAINING = "training"


class ResearchRole(str, Enum):
    INPUT = "input"
    INVESTIGATE = "investigate"
    OUTPUT = "output"


class EducationCapabilityKind(str, Enum):
    LEARNING = "learning"
    ANALYSIS = "analysis"
    EXPERIMENT = "experiment"
    PUBLICATION = "publication"


@dataclass(frozen=True)
class EducationCapability:
    capability_id: str
    kind: EducationCapabilityKind
    education_kinds: tuple[EducationKind, ...]
    capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("capability_id is required")
        if not self.education_kinds:
            raise ValueError("education_kinds must be non-empty")
        if len(set(self.education_kinds)) != len(self.education_kinds):
            raise ValueError("education_kinds must be unique")
        if not self.capabilities:
            raise ValueError("capabilities must be non-empty")
        if len(set(self.capabilities)) != len(self.capabilities):
            raise ValueError("capabilities must be unique")
        if any(not item.strip() for item in self.capabilities):
            raise ValueError("capabilities must be non-empty")


@dataclass(frozen=True)
class EducationWorkflow:
    workflow_id: str
    name: str
    education_kind: EducationKind
    role: ResearchRole

    def __post_init__(self) -> None:
        if not self.workflow_id.strip():
            raise ValueError("workflow_id is required")
        if not self.name.strip():
            raise ValueError("name is required")


@dataclass(frozen=True)
class EducationWorkspace:
    workspace_id: str
    name: str
    education_kinds: tuple[EducationKind, ...]
    workflows: tuple[EducationWorkflow, ...] = ()

    def __post_init__(self) -> None:
        if not self.workspace_id.strip():
            raise ValueError("workspace_id is required")
        if not self.name.strip():
            raise ValueError("name is required")
        if not self.education_kinds:
            raise ValueError("education_kinds must be non-empty")
        if len(set(self.education_kinds)) != len(self.education_kinds):
            raise ValueError("education_kinds must be unique")
        workflow_ids = [workflow.workflow_id for workflow in self.workflows]
        if len(set(workflow_ids)) != len(workflow_ids):
            raise ValueError("workflow IDs must be unique")
        scope = set(self.education_kinds)
        if any(workflow.education_kind not in scope for workflow in self.workflows):
            raise ValueError("workflow education kind is outside workspace scope")


@dataclass(frozen=True)
class EducationRequirement:
    requirement_id: str
    capability_kind: EducationCapabilityKind
    education_kind: EducationKind
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
class EducationPlan:
    workspace_id: str
    workflow_ids: tuple[str, ...]
    capability_ids: tuple[str, ...]
    requirement_ids: tuple[str, ...]


class EducationResearchPlanner:
    """Deterministic education and research planning only."""

    def normalize_workflows(
        self, workflows: tuple[EducationWorkflow, ...]
    ) -> tuple[EducationWorkflow, ...]:
        ids = [workflow.workflow_id for workflow in workflows]
        if len(set(ids)) != len(ids):
            raise ValueError("workflow IDs must be unique")
        return tuple(sorted(workflows, key=lambda item: item.workflow_id))

    def normalize_capabilities(
        self, capabilities: tuple[EducationCapability, ...]
    ) -> tuple[EducationCapability, ...]:
        ids = [item.capability_id for item in capabilities]
        if len(set(ids)) != len(ids):
            raise ValueError("capability IDs must be unique")
        return tuple(sorted(capabilities, key=lambda item: item.capability_id))

    def normalize_requirements(
        self, requirements: tuple[EducationRequirement, ...]
    ) -> tuple[EducationRequirement, ...]:
        ids = [item.requirement_id for item in requirements]
        if len(set(ids)) != len(ids):
            raise ValueError("requirement IDs must be unique")
        return tuple(sorted(requirements, key=lambda item: item.requirement_id))

    def plan(
        self,
        workspace: EducationWorkspace,
        capabilities: tuple[EducationCapability, ...],
        requirements: tuple[EducationRequirement, ...],
        max_capabilities: int = 8,
    ) -> EducationPlan:
        if max_capabilities <= 0:
            raise ValueError("max_capabilities must be positive")

        workflows = self.normalize_workflows(workspace.workflows)
        normalized_capabilities = self.normalize_capabilities(capabilities)
        normalized_requirements = self.normalize_requirements(requirements)
        scope = set(workspace.education_kinds)
        selected: list[EducationCapability] = []

        for requirement in normalized_requirements:
            if requirement.education_kind not in scope:
                raise ValueError("workspace lacks required education kind")
            compatible = [
                capability
                for capability in normalized_capabilities
                if capability.kind == requirement.capability_kind
                and requirement.education_kind in capability.education_kinds
                and set(requirement.required_capabilities).issubset(
                    set(capability.capabilities)
                )
            ]
            if not compatible:
                raise ValueError("no compatible education capability")
            selected.append(compatible[0])

        selected_ids = tuple(item.capability_id for item in selected)
        if len(set(selected_ids)) > max_capabilities:
            raise ValueError("education plan exceeds capability limit")

        return EducationPlan(
            workspace_id=workspace.workspace_id,
            workflow_ids=tuple(workflow.workflow_id for workflow in workflows),
            capability_ids=selected_ids,
            requirement_ids=tuple(
                item.requirement_id for item in normalized_requirements
            ),
        )
