# Alpha AI Safety and Permission Architecture

## Permission levels

| Level | Capability |
|---|---|
| 0 | Explain |
| 1 | Read |
| 2 | Suggest |
| 3 | Execute safe actions |
| 4 | Execute with approval |
| 5 | Restricted/admin |

## Enforcement

Permission enforcement must exist outside the language model and tool planner.

## Required controls

- explicit identity/context;
- scoped permissions;
- action preview where appropriate;
- confirmation for destructive/admin operations;
- audit log;
- timeout/cancellation;
- rollback where possible;
- post-action verification;
- user-visible result.

## Agent loop

```
Understand
→ Inspect
→ Plan
→ Authorize
→ Execute
→ Test
→ Verify
→ Report
```

An agent must not report success solely because a tool invocation returned without an error.
