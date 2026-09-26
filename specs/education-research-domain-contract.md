# Education and Research Domain Contract

## Purpose

The Education and research foundation defines immutable learning/research workspaces, workflow roles, capability and requirement contracts, and deterministic bounded plans.

## Contracts

- EducationKind identifies study, research, teaching, and training contexts.
- ResearchRole distinguishes input, investigation, and output workflow stages.
- EducationCapability declares a learning, analysis, experiment, or publication capability.
- EducationWorkspace declares supported education contexts and validates workflow scope.
- EducationRequirement declares a required capability kind, education context, and capability set.
- EducationPlan contains normalized workspace, workflow, capability, and requirement identifiers.
- EducationResearchPlanner performs deterministic normalization and compatibility planning.

## Rejection semantics

Invalid identifiers, empty capability sets, duplicate identifiers, workspace-scope mismatches, incompatible capabilities, and invalid planning bounds are rejected deterministically.

## Boundary

This foundation performs no LMS/ERP execution, credential access, payments, external service execution, filesystem mutation, subprocess execution, network access, or host mutation.
