# Alpha Linux Threat Model

Security architecture starts from explicit threats rather than isolated features.

## Assets

- user data
- credentials and secrets
- AI memory
- AI tool permissions
- source code and projects
- package signing keys
- build infrastructure
- release artifacts
- system configuration
- telemetry and logs
- backups
- network identity
- recovery media

## Threat classes

- malicious software;
- supply-chain compromise;
- repository/package tampering;
- credential theft;
- privilege escalation;
- destructive AI actions;
- prompt/tool abuse;
- malicious plugins;
- compromised cloud integrations;
- unsafe updates;
- boot-chain attacks;
- unauthorized physical access;
- data exfiltration;
- backup compromise;
- denial of service.

## Security controls

Controls must include least privilege, authenticated sources, signed artifacts, sandboxing where appropriate, explicit AI permissions, secrets isolation, encryption, secure boot support, auditability, recovery and rollback.

## AI-specific rule

An AI model is not a security authority. Authorization must be enforced outside the model by deterministic policy controls.

## Lifecycle

Threat modeling is repeated when architecture, trust boundaries, package sources, AI capabilities, privileged operations or release infrastructure materially change.
