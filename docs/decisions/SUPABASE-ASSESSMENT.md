# Supabase Assessment and Architecture Decision

**Status:** Not part of the core operating-system architecture  
**Reviewed:** 2026-10-12  
**Scope:** Alpha-Linux

## Decision summary

Do not make Supabase a dependency of boot, live-session startup, installation, disk operations, recovery, package installation, or other critical/offline paths. Alpha-Linux prioritizes reproducible builds, offline-first behavior, safety boundaries, and reliable boot/install behavior; a hosted backend cannot be allowed to block these paths.

The connected Supabase account currently lists no projects. No project, deployment, or OS configuration was changed.

## Possible optional future uses

Only after the core OS is stable, an opt-in online service might support a software/catalog index, user-requested settings synchronization, or metadata for a companion service. Such features must degrade gracefully offline, minimize telemetry, make data collection explicit, and never hold credentials or elevated disk privileges in a cloud client.

## Acceptance gate

Require a specific user benefit, privacy/threat review, offline/failure tests, supply-chain review, cost comparison, and confirmation that boot/install and reproducible-build tests remain unchanged. No Supabase SDK or network requirement should enter the base image without a separate approved decision.

## Changelog

- 2026-10-12: Added initial assessment; no OS, build, installer, or infrastructure changes.
