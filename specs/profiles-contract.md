# Profiles Contract

## Status

Phase 2 implementation contract. Profiles are declarative configuration
presets and are not an authorization mechanism.

## Responsibilities

- Define stable profile identity and descriptive metadata.
- Store namespaced configuration values.
- Resolve multiple profiles deterministically in caller-specified order.
- Preserve explicit precedence: later selected profiles override earlier values.

## Invariants

- Profile identifiers are unique within a registry.
- Registry listing is deterministic.
- Configuration keys are non-empty namespaced strings.
- Unknown profiles are ignored without fabricated settings.
- Profile resolution never executes commands or mutates the host.
- Profile data cannot grant permissions or bypass Policy Engine/System Service controls.

## Future integration

Desktop/session integration may consume resolved settings, but any operation
that changes privileged system state must cross the existing authorization and
system-service boundaries.
