# Electronics Domain Contract

## Purpose

The Electronics domain foundation defines immutable board, interface, component, and circuit-requirement contracts and produces deterministic bounded component plans.

## Contracts

- ElectronicsInterface defines an interface kind and capability set.
- ElectronicsBoard declares the board-level interface capabilities available to a circuit plan.
- ElectronicsComponent declares immutable component interfaces and enabled state.
- CircuitRequirement declares an interface kind and required capabilities.
- ElectronicsPlan contains only selected component and requirement identifiers.
- ElectronicsPlanner normalizes inputs deterministically and selects enabled components compatible with both board and circuit requirements.

## Rejection semantics

The planner rejects duplicate identifiers, empty contracts, missing board capabilities, disabled or incompatible components, and invalid component bounds.

## Non-goals

This contract performs no GPIO/I2C/SPI/serial I/O, device flashing, instrument control, subprocess execution, network access, credential access, or host mutation.
