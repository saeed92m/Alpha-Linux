# Alpha Assistant Contract

The Phase 4 assistant layer is a declarative reference runtime.

## Responsibilities
- Represent assistant identity and session state.
- Represent ordered conversation turns.
- Normalize turns deterministically.
- Enforce a declared context budget.
- Construct an explicit request for the existing AI execution boundary.

## Invariants
- Session and assistant identifiers are non-empty.
- Turn sequences are contiguous and ordered.
- Turn content is non-empty.
- Context usage is non-negative and cannot exceed the session budget.
- Planning has no provider, network, credential, persistence, subprocess, autonomous-action, or host-mutation semantics.

Actual model execution remains outside this reference layer.
