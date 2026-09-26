# Alpha 0.1.0a1 Release Traceability

| Requirement | Implementation | Tests |
|---|---|---|
| Immutable release manifest | implementation/alpha_core/alpha_release.py | manifest tests |
| Artifact/checksum/source/CI binding | AlphaReleaseManifest | manifest fixture |
| Deterministic tag | AlphaReleasePlanner.tag_for | test_tag_is_deterministic |
| Gate completeness | AlphaReleasePlanner.plan | ready/missing/failed tests |
| No publication side effects | AlphaReleasePlanner | contract review + CI |
