# Policy Contract

**Phase:** 1 Foundation

Policy evaluation is the authoritative boundary for privileged Alpha actions.

## Inputs

Identity, requested action, target, capabilities, risk class, current system state and explicit user grants.

## Output

Allow, deny or require approval, with machine-readable reason and evidence identity.

## Invariants

- Model output is never authorization.
- UI is not the authorization authority.
- Grants are scoped and revocable.
- Destructive/admin operations default to explicit approval unless a documented safe policy applies.

## Verification

Positive, negative, expired-grant, revoked-grant and adversarial-input tests.
