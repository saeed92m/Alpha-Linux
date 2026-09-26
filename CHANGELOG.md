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
- Phase 5 Developer, AI/ML/HPC, Astronomy, Aerospace, Engineering, Motorsport, Electronics, SDR/RF, Creator, Music & Audio, Data/GIS, Business, Cloud/DevOps, and Education and research domain foundations.
- Phase 6 security hardening foundation with immutable security classification, control, audit-event, and hardening-plan contracts, deterministic bounded planning, and deny-by-default reference semantics.
- Phase 6 privacy hardening foundation with immutable classification, purpose, consent, retention, request, decision, and plan contracts.
- Phase 6 recovery and backup foundation with immutable recovery policy/request/decision contracts, deterministic normalization, bounded planning, verification and retention semantics.
- Phase 6 compatibility foundation with immutable target/requirement/decision/plan contracts, deterministic platform/version/capability evaluation, and bounded reference-only planning.
- Phase 6 performance foundation with immutable target/requirement/decision/plan contracts, deterministic latency/throughput/resource-budget evaluation, and bounded reference-only planning.
- Phase 6 hardware validation foundation with immutable capability/requirement/decision/plan contracts, deterministic declared-capability validation, and bounded reference-only planning.
- Phase 6 accessibility foundation with immutable capability/requirement/decision/plan contracts, deterministic declared-feature validation, and bounded reference-only planning.
- Phase 6 localization foundation with immutable locale/bundle/planning contracts, deterministic locale fallback and missing-bundle reporting, and bounded reference-only planning.
- Phase 6 release QA foundation with immutable gate/evidence/result contracts, deterministic required-evidence aggregation, and explicit pass/fail semantics.
- Phase 7 Alpha release foundation with immutable release manifest/evidence/readiness contracts and deterministic no-release-until-ready evaluation.

### Changed

- Phase 5 Domain Platform is complete and Phase 6 — Hardening is the active implementation phase.
- Phase 6 security hardening is complete; privacy hardening is complete; recovery and backup are complete; compatibility is complete; performance is complete; hardware validation is complete; accessibility is complete; localization is complete; release QA is complete. Phase 6 Hardening is complete and Phase 7 — Alpha releases is active. The repository currently contains release-readiness foundations only; no product release is claimed until an actual build artifact and independent evidence are present.
- Continued CI/CD, reproducibility, security, package, SBOM, artifact, and documentation validation as mandatory engineering evidence.

- Phase 7 Alpha 0.x artifact foundation: immutable artifact specifications, deterministic evidence validation, filename semantics, bounded planning, and pure SHA-256 support.

### Notes

- The repository does not yet contain an installable Alpha Linux release.
- No stable, beta, or alpha product release is claimed by this changelog until release artifacts and the required release evidence exist.
- Phase 3 completion refers to the deterministic reference/runtime foundation. Privileged host mutation, production COSMIC runtime integration, installer/ISO delivery, and release-scoped validation remain governed by their respective roadmap phases.
- Phase 4 reference-runtime implementation is complete. Production provider execution, persistent knowledge/memory backends, autonomous host actions, privileged integration, and release-scoped evidence remain outside these foundations and are governed by later implementation/release phases.
- Phase 5 and Phase 6 foundations remain reference contracts only unless their individual implementation evidence explicitly expands the boundary.
