# Aerospace Domain Contract

## Purpose

The Aerospace domain foundation defines immutable vehicle capability and mission-phase contracts, then produces deterministic bounded mission plans.

## Contracts

- AerospaceVehicle declares the capabilities available to a vehicle.
- MissionPhase declares an ordered mission phase and its required capabilities.
- AerospaceMissionPlan contains the vehicle identifier and normalized phase identifiers.
- AerospacePlanner validates uniqueness, capability compatibility, deterministic sequencing, and phase bounds.

## Rejection semantics

The planner rejects duplicate phase identifiers or sequences, missing vehicle capabilities, non-positive bounds, and missions exceeding the configured phase limit.

## Non-goals

This contract performs no flight control, telemetry I/O, hardware access, propulsion or actuator control, network access, subprocess execution, credential access, or host mutation.
