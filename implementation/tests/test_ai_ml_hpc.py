from alpha_core.ai_ml_hpc import ComputeResource, MLHPCPlanner, MLWorkload, WorkloadKind


def resource(resource_id: str, *, cpu: int = 8, memory: int = 16384, gpu: int = 0, gpu_memory: int = 0, enabled: bool = True) -> ComputeResource:
    return ComputeResource(resource_id, resource_id, cpu, memory, gpu, gpu_memory, enabled)


def test_normalization_is_deterministic() -> None:
    planner = MLHPCPlanner()
    resources = (resource("gpu-b", gpu=1, gpu_memory=8192), resource("cpu-a"))
    assert tuple(r.resource_id for r in planner.normalize_resources(resources)) == ("cpu-a", "gpu-b")


def test_gpu_workload_selects_sufficient_resource() -> None:
    planner = MLHPCPlanner()
    workload = MLWorkload("train-1", WorkloadKind.TRAINING, 6, 12000, 1, 12000)
    plan = planner.plan(workload, (resource("small-gpu", cpu=8, memory=16000, gpu=1, gpu_memory=8192), resource("large-gpu", cpu=16, memory=32768, gpu=1, gpu_memory=16384)))
    assert plan.resource_ids == ("large-gpu",)


def test_disabled_resource_is_rejected() -> None:
    planner = MLHPCPlanner()
    workload = MLWorkload("infer-1", WorkloadKind.INFERENCE, 2, 4096)
    try:
        planner.plan(workload, (resource("offline", enabled=False),))
    except ValueError as exc:
        assert str(exc) == "no compatible compute resource"
    else:
        raise AssertionError("expected ValueError")


def test_insufficient_gpu_memory_is_rejected() -> None:
    planner = MLHPCPlanner()
    workload = MLWorkload("train-2", WorkloadKind.TRAINING, 4, 8192, 1, 16000)
    try:
        planner.plan(workload, (resource("gpu", cpu=8, memory=16384, gpu=1, gpu_memory=8192),))
    except ValueError as exc:
        assert str(exc) == "no compatible compute resource"
    else:
        raise AssertionError("expected ValueError")


def test_resource_limit_is_bounded() -> None:
    planner = MLHPCPlanner()
    workload = MLWorkload("infer-2", WorkloadKind.INFERENCE, 2, 4096)
    plan = planner.plan(workload, (resource("b"), resource("a")), max_resources=1)
    assert plan.resource_ids == ("a",)


def test_duplicate_resource_ids_are_rejected() -> None:
    planner = MLHPCPlanner()
    workload = MLWorkload("infer-3", WorkloadKind.INFERENCE, 2, 4096)
    try:
        planner.plan(workload, (resource("same"), resource("same")))
    except ValueError as exc:
        assert str(exc) == "resource IDs must be unique"
    else:
        raise AssertionError("expected ValueError")


def test_gpu_memory_requires_gpu() -> None:
    try:
        MLWorkload("bad", WorkloadKind.INFERENCE, 2, 4096, 0, 1024)
    except ValueError as exc:
        assert str(exc) == "gpu_memory_mib requires gpu_count"
    else:
        raise AssertionError("expected ValueError")
