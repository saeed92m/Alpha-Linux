# Agent Runtime Contract

An agent request follows:

Understand → Inspect → Plan → Authorize → Execute → Verify → Report.

The runtime MUST keep planning separate from authorization.

Each action declares target, capability, risk class and expected effect. Verification is required before success is reported for state-changing operations.

## Verification

Mock tool tests, denied-action tests, approval-flow tests, failed-action tests and postcondition verification.
