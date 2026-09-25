# Alpha Linux — CI Gate to Job Mapping

**Status:** normative CI mapping; Phase 1 executable subset implemented

This document maps stable gate identifiers to implementation jobs. Job names are implementation details; gate IDs are normative.

| Gate | Required job | Blocks release? | Evidence |
|---|---|---:|---|
| CI-VAL-001 | validate | Yes | validation report |
| CI-DOC-001 | docs | Yes | documentation checks |
| CI-LINT-001 | lint | Yes | lint report |
| CI-TEST-001 | unit | Yes | unit test report |
| CI-TEST-002 | integration | Yes | integration report |
| CI-PKG-001 | package | Yes | package validation |
| CI-SEC-001 | security | Yes | security report |
| CI-BLD-001 | build | Yes | build manifest |
| CI-ART-001 | artifact | Yes | artifact manifest/digest |
| CI-REP-001 | reproducibility | Yes for release candidates | reproducibility evidence |
| CI-ISO-001 | iso | Yes for ISO releases | boot/live/install evidence |
| CI-REL-001 | release | Yes | promotion record |

## Execution policy

- Every required gate MUST produce machine-readable evidence.
- A skipped release-critical gate is a failure unless the gate definition explicitly marks it conditional.
- Conditional gates MUST state their applicability and reason.
- Evidence MUST identify source commit, environment, tool version and timestamp.
- Job implementation may evolve without changing gate semantics.


## Phase 1 applicability

For the current Phase 1 foundation, CI-VAL-001, CI-DOC-001, CI-LINT-001, CI-TEST-001, CI-TEST-002, CI-PKG-001 and CI-SEC-001 are executable and blocking. CI-BLD-001, CI-ART-001, CI-REP-001, CI-ISO-001 and CI-REL-001 remain release-scoped and are not represented as passed by the Phase 1 workflow. They become blocking when their corresponding release artifacts and promotion process are implemented.
