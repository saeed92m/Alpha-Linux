# Alpha Linux — Phase 0 Security Closure Matrix

**Status:** Phase 0 normative traceability supplement

This matrix closes the security areas identified as remaining Phase 0 gaps. It complements the threat model and security-control matrix; it does not replace them.

| Security area | Control requirement | Enforcement boundary | Verification |
|---|---|---|---|
| Plugin isolation | AL-SEC-0007 | Plugin capability broker / sandbox | denied-capability and isolation tests |
| Cloud integration | AL-SEC-0008, AL-SEC-0005 | explicit provider boundary + credential broker | consent, credential-scope, revocation tests |
| Firmware | AL-SEC-0005, AL-SEC-0009 | firmware/update service + authenticated metadata | provenance, signature, rollback tests |
| Physical access | AL-SEC-0001, AL-SEC-0009 | boot/authentication/encryption/recovery policy | locked-device and recovery-boundary tests |
| AI/tool authorization | AL-SEC-0001–0003 | policy engine outside model | adversarial authorization tests |
| Recovery | AL-SEC-0009 | recovery environment + authenticated state | security-preserving rollback tests |
| Observability | AL-SEC-0008 | telemetry policy / permission boundary | privacy and redaction tests |

## Non-negotiable invariants

1. A model output is never an authorization grant.
2. A plugin declaration is never proof of trust.
3. Secure Boot is not treated as proof that every runtime component is trusted.
4. Recovery MUST NOT create a privilege bypass.
5. Cloud credentials MUST be scoped and revocable.
6. Security-sensitive firmware transitions MUST be attributable to an authenticated source.
7. Sensitive telemetry MUST follow explicit policy and minimization.
8. Failure handling MUST preserve the strongest applicable security boundary.

## Phase 0 exit evidence

Each row requires an executable test identifier or an explicitly documented pre-implementation evidence plan. Missing evidence blocks Specification Freeze.
