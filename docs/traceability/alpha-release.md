# Alpha Release Traceability

| Requirement | Implementation | Tests | Specification |
| --- | --- | --- | --- |
| Immutable release contracts | implementation/alpha_core/release.py | implementation/tests/test_release.py | specs/alpha-release-contract.md |
| Deterministic evidence normalization | ReleasePlanner.normalize_evidence | test_evidence_normalization_is_deterministic | Semantics |
| Readiness evaluation | ReleasePlanner.evaluate | ready/missing/failed tests | Semantics |
| Artifact requirement | ReleaseManifest | test_release_manifest_requires_artifacts | Semantics |
| Reference-only boundary | release planner | full CI + static security | Boundary |
