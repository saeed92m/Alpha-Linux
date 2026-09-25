# Alpha Linux — Security Control Traceability Matrix

**Status:** Phase 0 normative control mapping

| Requirement | Threat / risk | Required control | Verification |
|---|---|---|---|
| AL-SEC-0001 | Privilege escalation / unauthorized action | Least privilege, scoped identities and policy enforcement outside UI/model | Security test |
| AL-SEC-0002 | AI-generated unauthorized action | Deterministic authorization boundary independent of model output | Adversarial agent test |
| AL-SEC-0003 | Destructive/admin AI action | Explicit approval or documented safe-policy exception | UX/security test |
| AL-SEC-0004 | Credential exposure | Secret scanning, protected storage, log redaction, no secrets in images/source | Security scan |
| AL-SEC-0005 | Package/artifact tampering | Authenticated metadata, signatures and verification before trusted use | Supply-chain test |
| AL-SEC-0006 | Dependency compromise | SBOM/software inventory, provenance and vulnerability tracking | Supply-chain audit |
| AL-SEC-0007 | Malicious plugin/agent | Trust classification, scoped permissions, isolation and revocation | Plugin security test |
| AL-SEC-0008 | Data exfiltration / excessive telemetry | Data minimization, explicit consent/control, local-first handling where practical | Privacy audit |
| AL-SEC-0009 | Recovery bypass | Recovery paths preserve authentication/encryption/security policy | Recovery security test |
| AL-SEC-0010 | Unreviewed security regression | Mandatory security review for security-critical changes | Release audit |

## Cross-cutting controls

- Secure Boot support must not be represented as proof that every component is trusted.
- The AI model is never the authorization authority.
- Package provenance must remain inspectable.
- Recovery must not create an undocumented privilege bypass.
- Cloud integrations are separate trust boundaries.
- Audit data must be protected against unauthorized modification where it is used as security evidence.

## Gate

Every AL-SEC requirement must have a mapped threat/risk, control and verification method before Specification Freeze.
