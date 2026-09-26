# Alpha Agent Runtime Contract

The Agent Runtime is a declarative Phase 4 reference foundation.

## Responsibilities
- Represent immutable agent descriptors and bounded requests.
- Normalize agent and capability ordering deterministically.
- Enforce explicit capability allowlists.
- Enforce bounded step budgets.
- Produce an agent execution plan without executing the agent.

## Invariants
- Agent IDs, names, and task text are non-empty.
- Capability identifiers are non-empty and unique.
- Step budgets are positive and bounded by the selected agent.
- Disabled or unknown agents are rejected.
- Requested capabilities must be explicitly allowed by the selected agent.
- Planned capabilities are deterministic.

## Security boundary

This foundation performs no autonomous execution, subprocess execution, network/provider access, credential handling, or host mutation.
