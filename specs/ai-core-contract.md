# Alpha AI Core Contract

## Status

Phase 4 implementation contract. The current AI core is a deterministic, immutable, declarative reference layer.

## Responsibilities

- Represent validated model/provider identity.
- Represent model kind and capabilities.
- Normalize model registration deterministically.
- Validate model selection and execution requests.
- Keep provider execution outside this reference layer.

## Invariants

- Model and provider identifiers are non-empty.
- Model identifiers are unique and deterministically ordered.
- Model capabilities are unique and ordered.
- Execution requests reference registered models.
- Planning has no network, credential, authorization, or host-mutation semantics.

## Runtime boundary

A production provider adapter may execute a validated request. Provider credentials, network access, sandboxing, authorization, and execution must remain behind explicit runtime/service boundaries with verification evidence.
