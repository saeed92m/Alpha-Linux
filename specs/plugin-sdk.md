# Alpha Linux — Plugin and SDK Specification

**Status:** Phase 0 normative specification
**Requirement:** AL-SEC-0007

## Purpose

Allow third-party and first-party extensions without granting implicit system-wide trust.

## Trust model

Plugin identity → declared capabilities → user/admin authorization → isolated execution → audited actions → revocation.

## Normative requirements

- Plugins MUST declare identity, version, publisher, capabilities, dependencies, data access, network access, and update source.
- Installation MUST verify package integrity and applicable signatures/provenance.
- Capability grants MUST be explicit and revocable.
- Plugins MUST NOT receive unrestricted root/system access by default.
- Untrusted plugins SHOULD run in a sandbox appropriate to their capability set.
- Plugin actions affecting system state MUST pass the same policy boundary used by Alpha agents.
- Revocation MUST prevent further use at an enforcement boundary and preserve recovery options.

## Threat coverage

Malicious plugin, compromised publisher, dependency substitution, capability escalation, data exfiltration, update hijack, and plugin-to-agent privilege confusion.

## Acceptance evidence

Install verification, capability denial, sandbox escape resistance where applicable, revocation, malicious update, dependency integrity, and audit tests.
