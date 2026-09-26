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
- Phase 4 Permissions foundation with immutable rules/requests, deterministic policy evaluation, explicit allow/deny decisions, and default-deny behavior.
- Phase 4 Verification foundation with immutable evidence contracts, deterministic normalization, bounded reports, and explicit pass/fail aggregation.
- Phase 5 Developer domain foundation with immutable workspace/toolchain contracts, deterministic normalization, compatibility selection, and bounded toolchain planning.
- Phase 5 AI/ML/HPC domain foundation with immutable training/inference workload contracts, compute-resource capability contracts, deterministic compatibility planning, and bounded resource selection.
- Phase 5 Astronomy domain foundation with immutable sky-position, photometry, and observation contracts, deterministic normalization, and bounded object-specific planning.
- Phase 5 Aerospace domain foundation with immutable vehicle capability and mission-phase contracts, deterministic capability validation, ordered sequencing, and bounded mission planning.
- Phase 5 Engineering domain foundation with immutable engineering project/analysis contracts, explicit unit-bearing values, deterministic resource compatibility planning, and bounded analysis planning.
- Phase 5 Motorsport domain foundation with immutable vehicle/component/setup contracts, deterministic compatibility planning, and bounded setup selection.
- Phase 5 Electronics domain foundation with immutable board/interface/component/circuit contracts, deterministic compatibility planning, and bounded component selection.
- Phase 5 SDR/RF domain foundation with immutable frequency-band, SDR capability, and acquisition-requirement contracts, deterministic compatibility planning, and bounded device selection.
- Phase 5 Creator domain foundation with immutable project, media-asset lifecycle, tool-capability, and production-requirement contracts, deterministic normalization, bounded planning, and explicit source/proxy/cache/generated-output separation.
- Phase 5 Music & Audio domain foundation with immutable session, track, capability, and routing-requirement contracts, deterministic normalization, bounded routing planning, and explicit source/processed/rendered track separation.
- Phase 5 Data/GIS domain foundation with immutable project, layer, spatial-reference, tool, and analysis-requirement contracts, deterministic normalization, bounded compatibility planning, and explicit source/derived/output layer separation.
- Phase 5 Business domain foundation with immutable workspace, workflow, capability, and requirement contracts, deterministic normalization, bounded compatibility planning, and explicit input/process/output workflow roles.
- Phase 5 Cloud/DevOps domain foundation with immutable environment, service, and requirement contracts, deterministic normalization, bounded compatibility planning, and explicit reference-only cloud execution boundaries.
- Phase 5 Education and research domain foundation with immutable workspace, workflow, capability, and requirement contracts, deterministic normalization, bounded compatibility planning, and explicit reference-only education/research execution boundaries.
- Phase 6 security hardening foundation with immutable security classification, control, audit-event, and hardening-plan contracts, deterministic bounded planning, and deny-by-default reference semantics.
- Phase 6 privacy hardening foundation with immutable classification, purpose, consent, retention, request, decision, and plan contracts.
- Phase 6 recovery and backup foundation with immutable recovery policy/request/decision contracts, deterministic normalization, bounded planning, verification and retention semantics.

### Changed

- Completed the Phase 2 reference-runtime baseline and activated Phase 3 — Desktop and Interaction.
- Completed the Phase 3 desktop and interaction reference-runtime foundation; Phase 4 — AI Platform became the active implementation phase.
- Phase 4 now has ten merged reference-runtime foundations: Alpha AI Core, AI Execution Runtime, Assistant, Memory, Knowledge Center, Command Bar, Agent Runtime, Orchestrator, Permissions, and Verification.
- Phase 5 Developer domain foundation is complete; AI/ML/HPC became the active domain slice.
- Phase 5 AI/ML/HPC domain foundation is complete; Astronomy became the active domain slice.
- Phase 5 Astronomy domain foundation is complete; Aerospace became the active domain slice.
- Phase 5 Aerospace domain foundation is complete; Engineering became the active domain slice.
- Phase 5 Engineering domain foundation is complete; Motorsport became the active domain slice.
- Phase 5 Motorsport domain foundation is complete; Electronics became the active domain slice.
- Phase 5 Electronics domain foundation is complete; SDR/RF became the active domain slice.
- Phase 5 SDR/RF foundation is complete; Creator became the active domain slice.
- Phase 5 Creator foundation is complete; Music & Audio became the active domain slice.
- Phase 5 Music & Audio foundation is complete; Data/GIS became the active domain slice.
- Phase 5 Data/GIS foundation is complete; Business became the active domain slice.
- Phase 5 Business foundation is complete; Cloud/DevOps became the active domain slice.
- Phase 5 Cloud/DevOps foundation is complete; Education and research became the active domain slice.
- Phase 5 Education and research foundation is complete; Phase 5 Domain Platform is complete and Phase 6 — Hardening became the active implementation phase.
- Phase 6 security hardening foundation is complete; privacy hardening is complete; recovery and backup became the active Phase 6 slice.
- Continued CI/CD, reproducibility, security, package, SBOM, artifact, and documentation validation as mandatory engineering evidence.

### Notes

- The repository does not yet contain an installable Alpha Linux release.
- No stable, beta, or alpha product release is claimed by this changelog until release artifacts and the required release evidence exist.
- Phase 3 completion refers to the deterministic reference/runtime foundation. Privileged host mutation, production COSMIC runtime integration, installer/ISO delivery, and release-scoped validation remain governed by their respective roadmap phases.
- Phase 4 reference-runtime implementation is complete. Production provider execution, persistent knowledge/memory backends, autonomous host actions, privileged integration, and release-scoped evidence remain outside these foundations and are governed by later implementation/release phases.
- Phase 5 domain foundations remain reference-domain contracts only unless their individual implementation evidence explicitly expands the boundary.
