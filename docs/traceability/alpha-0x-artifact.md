# Alpha 0.x Artifact Traceability

| Requirement | Implementation | Tests | Specification |
| --- | --- | --- | --- |
| Immutable artifact specification | implementation/alpha_core/alpha_artifacts.py | implementation/tests/test_alpha_artifacts.py | specs/alpha-0x-artifact-contract.md |
| Deterministic normalization | AlphaArtifactPlanner.normalize_* | test_specs_are_normalized | Semantics |
| Evidence validation | AlphaArtifactPlanner.plan | valid/missing/invalid tests | Semantics |
| Alpha version contract | AlphaArtifactSpec | test_alpha_version_required | Semantics |
| Bounded planning | AlphaArtifactPlanner.plan | test_plan_is_bounded | Semantics |
| Pure checksum helper | sha256_hex | test_sha256_helper_is_deterministic | Semantics |
| No publication side effects | planner | static security + full CI | Boundary |
