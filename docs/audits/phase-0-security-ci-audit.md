# Alpha Linux — Phase 0 Security and CI Audit

**Status:** In progress

## Completed in this pass

- Security requirements are mapped to threat/risk classes, controls and verification.
- AI authorization is explicitly separated from model planning.
- Package/artifact integrity and provenance are treated as release controls.
- CI/CD now has stable gate IDs and explicit blocking semantics.
- Manual approvals are distinguished from automated verification.

## Remaining work

1. Expand threat controls for plugin isolation, cloud integrations, firmware and physical-access scenarios.
2. Map every P0 recovery path to security-preserving tests.
3. Define concrete CI job implementation only after build architecture is selected.
4. Define artifact signing implementation and key-management architecture.
5. Add adversarial AI/tool authorization test cases.
6. Reconcile all security/release assumptions during final Specification Freeze audit.

## Current decision

**Phase 0 remains BLOCKED / NOT FROZEN.**

No production security infrastructure, signing keys or privileged AI runtime should be introduced by this documentation change.
