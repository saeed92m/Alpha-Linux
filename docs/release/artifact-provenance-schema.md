# Alpha Linux — Release Artifact Provenance Schema

**Status:** Phase 0 normative release metadata schema

## Purpose

Every release artifact must be attributable to immutable source, declared build inputs, validation evidence, and release identity.

## Required record

| Field | Required | Meaning |
|---|---|---|
| artifact_id | Yes | Stable artifact identifier |
| artifact_type | Yes | ISO, package, repository metadata, recovery image, etc. |
| version | Yes | Alpha release version |
| channel | Yes | Declared lifecycle channel |
| source_commit | Yes | Immutable Git commit |
| source_tree_digest | Yes | Digest of source/input tree |
| build_id | Yes | Unique build execution identity |
| build_timestamp | Yes | UTC build timestamp |
| builder_identity | Yes | Trusted builder identity |
| toolchain | Yes | Compiler/interpreter/build-tool versions |
| package_set | Yes | Package manifest or lock identity |
| configuration_digest | Yes | Relevant configuration identity |
| dependency_inventory | Yes | SBOM/dependency inventory reference |
| test_evidence | Yes | Validation/test references |
| artifact_digest | Yes | Digest of final artifact bytes |
| signature | Channel-dependent | Authenticated signature |
| promotion_record | Stable | Candidate-to-stable promotion evidence |

## Integrity rules

- Provenance is generated from trusted build context.
- Artifact digests are calculated from final bytes.
- Source identity is immutable.
- Provenance contains no secrets.
- Stable promotion requires successful release gates and recorded evidence.
- Records are retained for the defined release lifecycle.

## Release chain

**Source → Build Inputs → Build → Tests → Artifact → Digest/Signature → Promotion → Release Record**

A missing or unverifiable required field blocks stable release.

Concrete serialization and signing formats are implementation-phase decisions.
