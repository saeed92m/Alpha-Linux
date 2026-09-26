# Business Domain Contract

## Purpose

The Business foundation defines immutable workspace, workflow, capability, and requirement contracts and produces deterministic bounded business plans.

## Contracts

- BusinessKind identifies supported business workflow domains.
- WorkflowRole distinguishes input, process, and output workflow stages.
- BusinessCapability declares a planning, analysis, reporting, or automation capability.
- BusinessWorkspace declares supported business kinds and validates workflow scope.
- BusinessRequirement declares a required capability kind, business kind, and capability set.
- BusinessPlan contains normalized workspace, workflow, capability, and requirement identifiers.
- BusinessPlanner performs deterministic normalization and compatibility planning.

## Rejection semantics

Invalid identifiers, empty capability sets, duplicate identifiers, workspace-scope mismatches, incompatible capabilities, and invalid planning bounds are rejected deterministically.

## Boundary

This foundation performs no ERP/CRM execution, transaction processing, payments, filesystem mutation, subprocess execution, network access, credential access, or host mutation.
