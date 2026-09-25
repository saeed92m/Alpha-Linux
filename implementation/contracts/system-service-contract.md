# System Service Contract

**Phase:** 1 Foundation

## Contract

A privileged Alpha system service MUST expose:
- explicit operation identity;
- caller identity;
- required capability;
- validated input;
- authorization decision;
- bounded execution;
- structured result;
- audit/evidence identity;
- failure state.

Services MUST NOT trust UI state or model output as authorization.

## Failure

Invalid input → reject without mutation.
Unauthorized request → reject and record policy result.
Execution failure → return structured failure; preserve safe state where possible.

## Verification

Unit tests for validation and authorization; integration tests for service lifecycle; negative tests for unauthorized and malformed requests.
