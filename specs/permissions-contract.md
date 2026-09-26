# Alpha Permissions Contract

The Permissions layer is a declarative Phase 4 reference foundation.

## Responsibilities
- Represent immutable permission rules and requests.
- Normalize policy rules deterministically.
- Evaluate capability requests against explicit rules.
- Default-deny unknown capabilities.
- Produce a permission decision without performing the requested action.

## Invariants
- Rule IDs and capabilities are non-empty.
- Permission effects are explicit.
- Rule IDs are unique within an evaluated policy.
- Matching decisions are deterministic.
- Capabilities without a matching rule are denied.

## Security boundary

This foundation performs no action execution, credential access, subprocess execution, network access, autonomous action, or host mutation.
