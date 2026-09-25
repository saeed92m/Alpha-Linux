# Alpha Linux — Decision Log

## Purpose

Record architectural and product decisions so the project remains understandable and reproducible.

## Decision format

- Decision
- Context
- Alternatives
- Chosen approach
- Reason
- Trade-offs
- Consequences
- Date
- Status

## D-001 — Product name

**Decision:** The product is named **Alpha Linux**.

**Status:** Accepted

## D-002 — Base distribution

**Decision:** Use **Ubuntu 26.04 LTS** as the foundation, targeting the latest supported 26.04 point release during implementation.

**Status:** Accepted

## D-003 — Desktop

**Decision:** Use **COSMIC Desktop** as the primary desktop environment.

**Status:** Accepted

## D-004 — Architectural philosophy

**Decision:** Own the experience, integrate the ecosystem, and avoid reinventing foundational components when mature upstream solutions are appropriate.

**Status:** Accepted

## D-005 — AI architecture

**Decision:** AI is a first-class system layer rather than a standalone chatbot application.

**Status:** Accepted

## D-006 — Multi-agent architecture

**Decision:** Alpha includes a dedicated multi-agent orchestration layer with specialized agents, tool permissions, verification and user approval for sensitive actions.

**Status:** Accepted

## D-007 — Continuous learning

**Decision:** Continuous learning and personalization are core capabilities and must remain user-controlled, inspectable and reversible.

**Status:** Accepted

## D-008 — Themes

**Decision:** Light, Dark, System/Auto and extensible custom themes are first-class requirements.

**Status:** Accepted

## D-009 — Product branding

**Decision:** The project owner's supplied logo is the product-logo reference for Alpha Linux. The reference palette includes `#003C91` and `#8A8A8A`.

**Status:** Accepted

## D-010 — Documentation-first development

**Decision:** Implementation begins only after the specification and architecture baseline are reviewed and frozen.

**Status:** Accepted
