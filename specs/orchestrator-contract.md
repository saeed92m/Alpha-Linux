# Alpha Orchestrator Contract

The Orchestrator is a declarative Phase 4 reference foundation.

## Responsibilities
- Represent immutable orchestration nodes and dependencies.
- Normalize graph definitions deterministically.
- Validate dependency references and node bounds.
- Produce a deterministic topological execution plan.
- Reject cyclic graphs without executing any node.

## Invariants
- Node IDs and kinds are non-empty.
- Dependencies are non-empty when supplied and unique.
- A node cannot depend on itself.
- All dependencies must resolve to known nodes.
- Workflow size is bounded by the request.
- Planned order is deterministic and dependency-respecting.

## Security boundary

This foundation performs no workflow/task execution, subprocess execution, network/provider access, credential handling, autonomous action, or host mutation.
