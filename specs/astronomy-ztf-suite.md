# Alpha Linux — Astronomy / ZTF Suite Specification

**Status:** Phase 0 normative specification
**Requirement:** AL-REQ-0020

## Purpose

Provide an integrated astronomy workflow for public survey data, machine-learning analysis and discovery workflows, including ZTF-oriented pipelines, without embedding a single scientific project into the operating-system foundation.

## Capabilities

Data acquisition/import → validation → preprocessing → scientific feature generation → ML inference/training → candidate inspection → provenance → visualization/reporting.

## Project isolation

Scientific environments MUST be reproducible and isolated from the base system. Datasets, models, generated features, predictions and reports MUST have distinct lifecycle metadata.

## AI integration

Astronomy agents may plan and execute authorized analysis steps, but scientific results MUST retain provenance, configuration and model identity. AI-generated interpretation MUST be distinguishable from measured or derived data.

## Recovery

Interrupted pipeline → resume from validated checkpoint where possible.
Corrupt derived artifacts → regenerate from declared inputs.
Environment failure → reconstruct from project manifest/lock information.

## Acceptance evidence

Dataset integrity, deterministic/reproducible feature generation where applicable, model provenance, checkpoint recovery, offline operation for local data, permission tests, and end-to-end sample workflow.
