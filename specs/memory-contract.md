# Alpha Memory Contract

The Phase 4 memory layer is a declarative reference contract.

## Responsibilities
- Represent typed memory records and namespaces.
- Normalize records deterministically.
- Define bounded retrieval queries.
- Produce a retrieval plan without performing persistence or I/O.

## Invariants
- Memory IDs, namespaces and content are non-empty.
- Priority is non-negative.
- Retrieval limits are positive and bounded by the query.
- Records are ordered deterministically by priority and memory ID.
- Retrieval is namespace-scoped.

## Security boundary

This layer does not persist data, access a database/filesystem, create embeddings, access networks/providers, execute subprocesses, authorize actions, or mutate the host.
