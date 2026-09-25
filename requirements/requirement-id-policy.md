# Requirement ID Policy

Stable requirement identifiers are mandatory before Specification Freeze.

## ID families

| Prefix | Meaning |
|---|---|
| AL-REQ | Functional requirement |
| AL-NFR | Non-functional requirement |
| AL-SEC | Security/privacy requirement |
| AL-HW | Hardware/firmware requirement |
| AL-UX | UI/UX/accessibility requirement |
| AL-COMP | Compatibility requirement |
| AL-PKG | Packaging/repository requirement |
| AL-BLD | Build/reproducibility requirement |
| AL-REL | Release/lifecycle requirement |
| AL-REC | Recovery/rollback requirement |
| AL-AI | AI/agent requirement |
| AL-TEST | Test requirement |

Identifiers are stable once published. Text may evolve through controlled change.

## Requirement quality

Every requirement should be:

- atomic where practical;
- unambiguous;
- testable;
- traceable;
- prioritized;
- assigned to a subsystem;
- associated with validation evidence;
- explicit about dependencies and constraints.

A requirement that cannot be tested must be refined or its validation method explicitly documented.
