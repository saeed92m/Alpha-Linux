# Alpha Linux — Specification Freeze Checklist

**Status:** Phase 0 gate definition

Specification Freeze is a controlled milestone; it does not mean implementation is complete.

## A. Scope
- [ ] Product definition approved
- [ ] In-scope capabilities mapped
- [ ] Non-goals documented
- [ ] Scope-completeness audit passed
- [ ] Open scope decisions recorded

## B. Requirements
- [ ] Stable ID policy approved
- [ ] All P0 requirements have acceptance criteria
- [ ] Security, compatibility, recovery, build/release and UX families covered
- [ ] Requirement changes are traceable

## C. Specification
- [ ] Every P0 subsystem has a normative specification
- [ ] No conflicting duplicate authority exists
- [ ] Deferred behavior is explicitly marked

## D. Architecture
- [ ] Dependency boundaries approved
- [ ] Critical contract ownership defined
- [ ] Trust boundaries documented
- [ ] Circular/prohibited dependencies audited
- [ ] Failure/recovery boundaries documented

## E. Security / Privacy
- [ ] Threat model covers critical assets and attack classes
- [ ] P0 controls map to requirements
- [ ] AI authorization is enforced outside the model
- [ ] Secret handling is testable
- [ ] Plugin/integration trust boundaries are explicit

## F. Compatibility / Recovery
- [ ] Ubuntu point-release policy is explicit
- [ ] Hardware taxonomy is defined
- [ ] Dual-boot safety states are defined
- [ ] WSL/bare-metal boundary is defined
- [ ] Recovery and rollback states are defined

## G. Build / Release
- [ ] Build inputs and provenance are defined
- [ ] CI/CD gates have executable implementation plans
- [ ] ISO/package promotion flow is defined
- [ ] Artifact verification is defined
- [ ] Channels/versioning are defined

## H. UX / Accessibility / Localization
- [ ] Semantic design tokens are defined
- [ ] Critical input modalities are covered
- [ ] AI state/permission/verification UX is defined
- [ ] Accessibility is testable
- [ ] Localization and RTL/LTR behavior are defined

## I. Consistency
- [ ] Master Specification ↔ Requirements audited
- [ ] Requirements ↔ Architecture audited
- [ ] Architecture ↔ Roadmap audited
- [ ] Feature Matrix ↔ authoritative docs audited
- [ ] Handbook ↔ normative docs cross-referenced
- [ ] No stale paths or missing references remain

## J. Decision
- [ ] Assumptions explicitly listed
- [ ] Risks have mitigation/ownership
- [ ] Change Request process is operational
- [ ] Freeze approval is recorded
- [ ] Phase 1 entry criteria are satisfied

## Decision states

- **BLOCKED** — mandatory gate fails.
- **READY FOR REVIEW** — evidence assembled; formal review pending.
- **FROZEN** — baseline approved; new scope requires Change Requests.
- **SUPERSEDED** — replaced by a later approved baseline.

No document may mark Phase 0 frozen while a mandatory gate remains unchecked.
