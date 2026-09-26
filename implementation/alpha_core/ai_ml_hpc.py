from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class WorkloadKind(str, Enum):
    TRAINING = "training"
    INFERENCE = "inference"


@dataclass(frozen=True)
class MLWorkload:
    workload_id: str
    kind: WorkloadKind
    cpu_cores: int
    memory_mib: int
    gpu_count: int = 0
    gpu_memory_mib: int = 0

    def __post_init__(self) -> None:
        if not self.workload_id.strip(): raise ValueError("workload_id is required")
        if self.cpu_cores <= 0: raise ValueError("cpu_cores must be positive")
        if self.memory_mib <= 0: raise ValueError("memory_mib must be positive")
        if self.gpu_count < 0: raise ValueError("gpu_count must be non-negative")
        if self.gpu_memory_mib < 0: raise ValueError("gpu_memory_mib must be non-negative")
        if self.gpu_count == 0 and self.gpu_memory_mib: raise ValueError("gpu_memory_mib requires gpu_count")


@dataclass(frozen=True)
class ComputeResource:
    resource_id: str
    name: str
    cpu_cores: int
    memory_mib: int
    gpu_count: int = 0
    gpu_memory_mib: int = 0
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.resource_id.strip(): raise ValueError("resource_id is required")
        if not self.name.strip(): raise ValueError("name is required")
        if self.cpu_cores <= 0: raise ValueError("cpu_cores must be positive")
        if self.memory_mib <= 0: raise ValueError("memory_mib must be positive")
        if self.gpu_count < 0: raise ValueError("gpu_count must be non-negative")
        if self.gpu_memory_mib < 0: raise ValueError("gpu_memory_mib must be non-negative")
        if self.gpu_count == 0 and self.gpu_memory_mib: raise ValueError("gpu_memory_mib requires gpu_count")


@dataclass(frozen=True)
class MLHPCPlan:
    workload: MLWorkload
    resource_ids: tuple[str, ...]


class MLHPCPlanner:
    """Deterministic AI/ML/HPC workload-resource planning only."""

    def normalize_resources(self, resources: tuple[ComputeResource, ...]) -> tuple[ComputeResource, ...]:
        return tuple(sorted(resources, key=lambda item: item.resource_id))

    def plan(self, workload: MLWorkload, resources: tuple[ComputeResource, ...], max_resources: int = 1) -> MLHPCPlan:
        if max_resources <= 0: raise ValueError("max_resources must be positive")
        normalized = self.normalize_resources(resources)
        ids = [resource.resource_id for resource in normalized]
        if len(set(ids)) != len(ids): raise ValueError("resource IDs must be unique")
        compatible = [
            resource for resource in normalized
            if resource.enabled
            and resource.cpu_cores >= workload.cpu_cores
            and resource.memory_mib >= workload.memory_mib
            and resource.gpu_count >= workload.gpu_count
            and resource.gpu_memory_mib >= workload.gpu_memory_mib
        ]
        if not compatible: raise ValueError("no compatible compute resource")
        selected = compatible[:max_resources]
        return MLHPCPlan(workload=workload, resource_ids=tuple(r.resource_id for r in selected))
