# Branching Strategy

## Permanent branch

`main` is the primary integration branch.

## Working branches

Use focused branches for changes:

- `feature/*`
- `fix/*`
- `docs/*`
- `build/*`
- `ci/*`
- `security/*`
- `release/*`

## Rules

- Do not develop directly on `main` for substantial changes.
- Keep branches focused and reviewable.
- Every material change must remain traceable to a requirement, issue or approved change request.
- Release commits are identified by immutable tags.
