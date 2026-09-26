# Creator Domain Contract

## Purpose

The Creator domain foundation defines immutable creative-project, tool-capability, and production-requirement contracts and produces deterministic bounded tool plans.

## Contracts

- CreatorMediaKind identifies reference creative workload classes.
- CreatorProject declares the media kinds supported by a project.
- CreatorTool declares supported media kinds, capabilities, and enabled state.
- CreatorRequirement declares a required media kind and capability set.
- CreatorPlan contains only the selected tool and requirement identifiers.
- CreatorPlanner normalizes inputs deterministically and selects enabled tools compatible with project scope and production requirements.

## Rejection semantics

The planner rejects duplicate identifiers, empty contracts, project scope mismatches, disabled or incompatible tools, and invalid tool bounds.

## Non-goals

This contract performs no media editing, rendering, encoding, capture, filesystem mutation, subprocess execution, network access, credential access, or host mutation.
