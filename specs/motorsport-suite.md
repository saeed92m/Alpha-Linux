# Alpha Linux — Motorsport Suite Specification

**Status:** Phase 0 normative specification
**Requirement:** AL-REQ-0020

## Scope

Vehicle diagnostics, ECU calibration workflows, data logging, analysis, simulation, telemetry, CAN/OBD tooling and engineering documentation.

## Safety

Vehicle-control actions are safety-sensitive. Any write/programming operation MUST identify target ECU/device, expected effect, prerequisites, authorization state, and recovery path. Automated agents MUST NOT silently perform safety-sensitive writes.

## Data integrity

Raw logs MUST be preserved separately from derived analysis. Calibration files MUST carry identity/version metadata and MUST support backup before modification.

## Recovery

Interrupted programming → device-specific recovery procedure; do not claim success without device verification.
Corrupt calibration → restore last known-good backup.

## Acceptance evidence

Read-only diagnostics, log integrity, calibration diff/backup, authorization gates, device verification, and failure-recovery tests.
