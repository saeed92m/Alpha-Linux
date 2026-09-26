# Astronomy Domain Contract

## Purpose

The Astronomy domain foundation defines immutable contracts for sky positions, photometric measurements, observations, and deterministic bounded selection for downstream analysis.

## Contracts

- SkyPosition represents right ascension and declination in degrees.
- Photometry represents a finite magnitude measurement.
- AstronomyObservation binds an object, source, timestamp, sky position, and optional photometry.
- AstronomyObservationPlan contains only selected observation identifiers.
- AstronomyPlanner normalizes observations deterministically and plans a bounded object-specific observation set.

## Scientific validation

Right ascension is constrained to [0, 360) degrees and declination to [-90, 90] degrees. Photometric magnitude must be finite. Observation identifiers must be unique within a planning input.

## Non-goals

This contract performs no telescope control, archive access, network I/O, FITS parsing, catalog download, model execution, filesystem mutation, subprocess execution, or host operation.
