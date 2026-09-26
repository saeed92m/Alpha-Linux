# Alpha Knowledge Center Contract

The Knowledge Center is a declarative reference foundation.

## Responsibilities
- Represent typed knowledge sources and documents.
- Preserve explicit provenance.
- Normalize documents deterministically.
- Scope plans by knowledge namespace.
- Produce bounded document-selection plans without external retrieval.

## Invariants
- Source, namespace, document, title, content, and provenance identifiers are non-empty.
- Query limits are positive.
- Document selection is deterministic.
- Only sources belonging to the requested namespace may contribute documents.
- Provenance is explicit and carried by each document.

## Security boundary

This foundation performs no web/network retrieval, database/vector-store access, embedding generation, subprocess execution, autonomous action, or host mutation.
