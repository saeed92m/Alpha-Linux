# AI/ML/HPC Domain Contract

## Purpose

The AI/ML/HPC domain foundation defines immutable contracts for describing machine-learning workloads and available compute resources, then produces deterministic resource plans.

## Contracts

- WorkloadKind distinguishes training from inference.
- MLWorkload declares CPU, memory, GPU-count, and GPU-memory requirements.
- ComputeResource declares available CPU, memory, GPU-count, and GPU-memory capacity.
- MLHPCPlan contains only selected resource identifiers.
- MLHPCPlanner normalizes resources deterministically and selects enabled resources whose capacity satisfies the workload.

## Determinism and bounds

Resources are normalized by resource_id. Selection preserves that order and is bounded by max_resources.

## Rejection semantics

The planner rejects invalid dimensions, duplicate resource identifiers, non-positive resource bounds, disabled or insufficient resources, and workloads requesting GPU memory without GPUs.

## Non-goals

This contract does not execute workloads, allocate physical devices, start containers or processes, invoke schedulers, install packages, access networks or credentials, or mutate the host.
