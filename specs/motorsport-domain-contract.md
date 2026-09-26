# Motorsport Domain Contract

## Purpose

The Motorsport domain foundation defines immutable vehicle, component, and setup-requirement contracts and produces deterministic bounded setup plans.

## Contracts

- MotorsportComponentKind identifies powertrain, drivetrain, chassis, or data components.
- MotorsportVehicle declares a vehicle identity and capabilities.
- MotorsportComponent declares an immutable component identity, kind, capabilities, and enabled state.
- SetupRequirement declares the component kind and capabilities required by a setup item.
- MotorsportSetupPlan contains only the selected component and requirement identifiers.
- MotorsportPlanner normalizes inputs deterministically and selects enabled components satisfying vehicle, kind, and capability requirements.

## Rejection semantics

The planner rejects duplicate identifiers, empty contracts, missing vehicle capabilities, disabled or incompatible components, and invalid component bounds.

## Non-goals

This contract performs no ECU writes, CAN access, telemetry I/O, hardware control, subprocess execution, network access, credential access, or host mutation.
