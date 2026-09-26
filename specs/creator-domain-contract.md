# Creator Domain Contract

## Purpose

The Creator domain foundation defines immutable creative-project, media-asset, tool-capability, and production-requirement contracts and produces deterministic bounded tool plans.

## Contracts

- CreatorMediaKind identifies reference creative workload classes.
- CreatorAssetRole explicitly distinguishes source assets, proxies, caches, and generated outputs.
- CreatorAsset identifies a media asset and its lifecycle role.
- CreatorProject declares supported media kinds and validates that its assets remain within project scope.
- CreatorTool declares supported media kinds, capabilities, and enabled state.
- CreatorRequirement declares a required media kind and capability set.
- CreatorPlan contains only normalized project, asset, tool, and requirement identifiers.
- CreatorPlanner normalizes assets, tools, and requirements deterministically and selects enabled tools compatible with project scope and production requirements.

## Rejection semantics

The planner and value objects reject duplicate identifiers, empty contracts, project-scope mismatches, disabled or incompatible tools, invalid asset scope, and invalid tool bounds.

## Data lifecycle boundary

Source assets remain distinguishable from proxies, caches, and generated outputs at the contract level. This foundation does not authorize deletion, replacement, mutation, or execution of any asset.

## Non-goals

This contract performs no media editing, rendering, encoding, capture, GPU/device control, filesystem mutation, subprocess execution, network access, credential access, or host mutation.
