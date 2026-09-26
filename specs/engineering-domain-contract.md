# Engineering Domain Contract

## Purpose

The Engineering domain foundation defines immutable analysis, project, unit-value, and compute-resource contracts and produces deterministic bounded analysis plans.

## Contracts

- AnalysisKind identifies structural, thermal, or fluid analysis.
- EngineeringValue carries a numeric value with an explicit unit label.
- EngineeringProject declares a project and its required analysis kinds.
- EngineeringResource declares compute capacity and supported solver kinds.
- EngineeringPlan contains only selected resource identifiers.
- EngineeringPlanner normalizes resources deterministically and selects enabled resources satisfying project and capacity requirements.

## Rejection semantics

The planner rejects duplicate identifiers, unsupported analysis kinds, disabled or undersized resources, invalid positive bounds, and empty contracts.

## Non-goals

This contract performs no CAD/CAE execution, solver invocation, filesystem mutation, subprocess execution, network access, credential access, or host mutation.
