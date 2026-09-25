# Phase 1 Foundation Traceability

**Status:** normative implementation traceability

| Contract | Implementation | Verification | CI gate |
|---|---|---|---|
| System Service Contract | implementation/alpha_core/system_service.py | implementation/tests/test_system_service.py | CI-TEST-001, CI-TEST-002 |
| Policy Contract | implementation/alpha_core/policy.py | implementation/tests/test_policy.py | CI-TEST-001, CI-SEC-001 |
| Project Manifest Contract | implementation/alpha_core/manifest.py, implementation/schemas/project-manifest.schema.json | implementation/tests/test_manifest.py | CI-VAL-001, CI-TEST-001, CI-PKG-001 |
| Observability Contract | implementation/alpha_core/observability.py | implementation/tests/test_observability.py | CI-TEST-001, CI-SEC-001 |
| Agent Runtime Contract | implementation/alpha_core/agent.py | implementation/tests/test_agent.py | CI-TEST-001, CI-TEST-002, CI-SEC-001 |
| Artifact Provenance | implementation/alpha_core/provenance.py | implementation/tests/test_provenance.py | CI-BLD-001, CI-ART-001, CI-SEC-001 |

## Evidence rule

A contract is not considered implemented merely because source files exist. The implementation must have executable tests, applicable CI gates, and no unresolved contract contradiction. Release-critical claims additionally require successful machine-readable CI evidence for the target commit.
