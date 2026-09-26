# Alpha 0.1.0a1 Release Traceability

| Requirement | Implementation | Tests |
|---|---|---|
| Immutable release manifest | implementation/alpha_core/alpha_release.py | manifest tests |
| Artifact/checksum/source/CI binding | AlphaReleaseManifest | manifest fixture |
| Deterministic tag | AlphaReleasePlanner.tag_for | test_tag_is_deterministic |
| Gate completeness | AlphaReleasePlanner.plan | ready/missing/failed tests |
| No publication side effects | AlphaReleasePlanner | contract review + CI |


## Current CI evidence binding

The release workflow records the machine-readable publication evidence in the `alpha-release-evidence` workflow artifact through `CI-REL-001 Release Evidence`. The evidence binds the actual wheel filename and SHA-256 digest to the workflow source commit, CI run ID, Alpha version, and deterministic tag intent.

The release remains unpublished until the release evidence is present and all required gates are independently successful. The workflow does not create tags or publish GitHub releases.
