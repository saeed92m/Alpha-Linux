# SDR/RF Domain Contract

## Purpose

The SDR/RF domain foundation defines immutable frequency-band, SDR capability, and acquisition-requirement contracts and produces deterministic bounded device plans.

## Contracts

- RFMode identifies supported reference modulation/data modes.
- RFFrequencyBand declares a validated frequency range and supported modes.
- SDRDevice declares frequency coverage, maximum sample rate, supported modes, and enabled state.
- RFRequirement declares the required center frequency, sample rate, and mode.
- SDRPlan contains only requirement and selected device identifiers.
- SDRRFPlanner normalizes inputs deterministically and selects enabled devices satisfying frequency, sample-rate, and mode constraints.

## Rejection semantics

The planner rejects duplicate identifiers, invalid frequency/sample-rate contracts, disabled or incompatible devices, and invalid device bounds.

## Non-goals

This contract performs no SDR hardware access, RF capture/transmission, tuner control, DSP/GNU Radio execution, subprocess execution, network access, credential access, or host mutation.
