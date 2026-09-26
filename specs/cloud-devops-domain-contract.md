# Cloud/DevOps Domain Contract

## Purpose

The Cloud/DevOps foundation models immutable environments, services, requirements, and deterministic bounded compatibility plans.

## Contracts

- EnvironmentKind identifies development, staging, production, and lab environments.
- ServiceKind identifies compute, storage, database, and network services.
- CloudCapabilityKind identifies provisioning, observability, security, and delivery capabilities.
- CloudService declares supported environment kinds and capabilities.
- CloudEnvironment defines supported environment scope and validates service membership.
- CloudRequirement declares required capability, environment kind, and capability set.
- CloudPlan contains normalized environment, service, and requirement identifiers.
- CloudDevOpsPlanner performs deterministic normalization and compatibility planning.

## Rejection semantics

Invalid identifiers, empty capability sets, duplicate identifiers, environment-scope mismatches, incompatible services, and invalid planning bounds are rejected deterministically.

## Boundary

This foundation performs no cloud API execution, deployment, credential access, filesystem mutation, subprocess execution, network access, or host mutation.
