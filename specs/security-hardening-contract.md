# Phase 6 Security Hardening Contract

## Purpose

This foundation defines immutable security classifications, hardening controls, audit-event contracts, and deterministic bounded planning.

## Contracts

- SecurityClassification categorizes information sensitivity.
- SecurityControl maps a hardening control to supported actions.
- SecurityAuditEvent records a reference-only security disposition.
- SecurityHardeningPlan contains normalized selected controls and deterministic deny events.
- SecurityHardeningPlanner performs normalization and bounded compatibility planning.

## Security semantics

Controls are normalized by stable identifiers. Unknown actions are represented as deterministic deny events rather than being implicitly authorized. Duplicate identifiers and invalid bounds are rejected.

## Boundary

No live authorization enforcement, credential handling, secret storage, network access, filesystem mutation, subprocess execution, host mutation, or external security-tool execution occurs in this foundation.
