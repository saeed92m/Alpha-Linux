# Alpha Linux — Adaptive Resource Intelligence Specification

**Status:** Phase 0 normative specification
**Requirements:** AL-REQ-0002, AL-NFR-0008

## Purpose

Coordinate CPU, GPU, RAM, VRAM, storage I/O, network, thermal and power behavior according to workload and explicit user policy.

## Operating modes

Adaptive (default), Performance, Maximum Compute, Power Saver, Quiet, AI Optimized, Gaming, Scientific Compute, Motorsport.

## Control model

Observe → Classify workload → Evaluate constraints → Select policy → Request bounded changes → Verify effect → Revert/escalate on failure.

The subsystem MUST never assume that a requested kernel/driver control succeeded; effective state must be measured when observable.

## Safety boundaries

- No unsafe thermal override.
- No disabling security controls to gain performance.
- User policy overrides automation where explicitly configured.
- Battery/thermal limits remain hard constraints.
- Administrative actions use privileged services, never direct model authority.

## Resource dimensions

CPU frequency/cores, GPU performance state, RAM pressure, VRAM pressure, storage I/O, network activity, thermal state, battery/AC state, background services, container/VM load, AI workload priority.

## Failure/recovery

Controller failure → preserve last known safe policy and disable automatic mutation.
Telemetry unavailable → degrade to conservative policy.
Thermal anomaly → prioritize protection over performance.

## Acceptance evidence

Mode transition tests, thermal-bound tests, AC/battery tests, workload classification tests, failed-actuation tests, rollback tests, and resource-budget measurements.
