# Software Center Traceability

| Area | Contract | Implementation | Tests |
|---|---|---|---|
| Catalog model | specs/software-center-contract.md | implementation/alpha_core/software_center.py | implementation/tests/test_software_center.py |
| Local catalog loading | specs/software-center-contract.md | implementation/alpha_core/software_center.py | implementation/tests/test_software_center.py |
| Install/remove planning | specs/software-center-contract.md | implementation/alpha_core/software_center.py | implementation/tests/test_software_center.py |

## Security trace

Software Center is not an authorization authority. Catalog loading is read-only,
transaction planning is dry-run only, and future privileged package operations
must cross the existing Policy Engine/System Service boundary.
