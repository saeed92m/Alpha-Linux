# Alpha Command Bar Contract

The Command Bar is a declarative Phase 4 reference foundation.

## Responsibilities
- Represent typed command descriptors and invocations.
- Normalize commands deterministically.
- Resolve known and available commands.
- Enforce a bounded argument contract.
- Produce an execution plan without executing the command.

## Invariants
- Command identifiers and titles are non-empty.
- Argument limits are non-negative.
- Invocation identifiers are non-empty.
- Invocation arguments are non-empty when supplied.
- Command ordering is deterministic by command ID.
- Unknown, unavailable, and over-limit invocations are rejected.

## Security boundary

This foundation performs no shell or subprocess execution, network/provider access, credential handling, autonomous action, or host mutation.
