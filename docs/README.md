# Alpha Linux Documentation

## Authority hierarchy

1. Master Specification — normative product requirements.
2. Architecture — intended system design.
3. Requirements — traceable requirements and constraints.
4. Master Feature Matrix — status and traceability index.
5. Handbook — educational and operational knowledge.
6. Roadmap — sequencing and milestones.
7. Planning — decisions, assumptions, risks and change control.
8. Implementation — executable system and source.
9. Testing — evidence that requirements are satisfied.
10. Release documentation — evidence and metadata for distributed artifacts.

## Current phase

**Phase 2 — System Integration and Core Runtime**

Phase 0 provides the frozen normative foundation. Phase 1 established executable engineering contracts and CI evidence. Phase 2 is implementing Alpha Core and system-integration vertical slices, while CI/CD continuously verifies the executable implementation boundary.

## Working rule

If implementation reveals a missing requirement or architectural assumption, stop and update the appropriate authoritative document before silently encoding the assumption in code.

The CI/CD workflow is executable engineering policy: its runtime results are evidence, while specifications and architecture remain the authoritative sources for required behavior.
