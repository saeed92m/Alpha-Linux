# Changelog

All notable Alpha Linux changes will be documented here.

The project follows a release-oriented change history. Unreleased work is kept under the `Unreleased` section until it is assigned to a release.

## Unreleased

### Added

- Phase 2 reference-runtime surfaces covering system integration, Control Center, Software Center, Hardware Manager, Observatory, Profiles, update/recovery foundations, and the unified integration facade.
- Phase 3 desktop and interaction foundation covering deterministic desktop/session capability modeling.
- Phase 3 COSMIC integration boundary with deterministic, non-mutating reference binding.
- Phase 3 multitasking foundation with immutable workspace/window contracts and deterministic planning.
- Phase 3 touch and pen foundation with immutable input-device contracts and deterministic capability planning.
- Phase 3 HiDPI foundation with immutable display-scaling contracts and deterministic policy validation.
- Phase 3 multi-display foundation with immutable topology, primary-display semantics, and deterministic display selection.
- Phase 3 theme-system foundation with immutable theme contracts, token validation, deterministic overlays, and stable theme identity.
- Phase 4 Alpha AI Core foundation with immutable model descriptors, deterministic registry normalization, request validation, and capability contracts.
- Phase 4 AI Execution Runtime foundation with deterministic provider selection and explicit execution-plan contracts.
- Phase 4 Assistant foundation with immutable sessions and turns, deterministic normalization, context-budget validation, and an explicit AI request boundary.
- Phase 4 Memory foundation with immutable memory records, namespace-scoped bounded retrieval planning, and deterministic normalization.
- Phase 4 Knowledge Center foundation with immutable source/document contracts, explicit provenance, deterministic normalization, and namespace-scoped bounded planning.
- Phase 4 Command Bar foundation with immutable command contracts, deterministic normalization, availability enforcement, and bounded argument validation.
- Phase 4 Agent Runtime foundation with immutable agent contracts, explicit capability allowlists, deterministic planning, and bounded step budgets.
- Phase 4 Orchestrator foundation with immutable dependency graphs, deterministic topological planning, cycle rejection, and bounded workflow size.

### Changed

- Completed the Phase 2 reference-runtime baseline and activated Phase 3 — Desktop and Interaction.
- Completed the Phase 3 desktop and interaction reference-runtime foundation; Phase 4 — AI Platform became the active implementation phase.
- Phase 4 now has eight merged reference-runtime foundations: Alpha AI Core, AI Execution Runtime, Assistant, Memory, Knowledge Center, Command Bar, Agent Runtime, and Orchestrator.
- Continued CI/CD, reproducibility, security, package, SBOM, artifact, and documentation validation as mandatory engineering evidence.

### Notes

- The repository does not yet contain an installable Alpha Linux release.
- No stable, beta, or alpha product release is claimed by this changelog until release artifacts and the required release evidence exist.
- Phase 3 completion refers to the deterministic reference/runtime foundation. Privileged host mutation, production COSMIC runtime integration, installer/ISO delivery, and release-scoped validation remain governed by their respective roadmap phases.
- Phase 4 remains in implementation; completion will not be claimed until all roadmap slices and their required evidence are complete.
