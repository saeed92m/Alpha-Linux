# COSMIC Integration Traceability

| Area | Contract | Implementation | Tests |
|---|---|---|---|
| COSMIC integration metadata | specs/cosmic-integration-contract.md | implementation/alpha_core/cosmic.py | implementation/tests/test_cosmic.py |
| Session binding | specs/cosmic-integration-contract.md | implementation/alpha_core/cosmic.py | implementation/tests/test_cosmic.py |
| Compatibility state | specs/cosmic-integration-contract.md | implementation/alpha_core/cosmic.py | implementation/tests/test_cosmic.py |

## Security trace

The COSMIC reference adapter is read/describe-only. It does not authorize,
install, launch, replace, or mutate privileged desktop components.
