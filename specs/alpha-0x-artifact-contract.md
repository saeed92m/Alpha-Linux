# Alpha 0.x Artifact Contract

## Purpose

Define release-scoped artifact specifications and evidence validation for Alpha 0.x.

## Semantics

- Artifact specifications are immutable and uniquely identified.
- Alpha versions use `0.x` or `0.x.y` format.
- Evidence requires a lowercase SHA-256 digest and positive artifact size.
- Expected filenames encode version, platform, architecture, and artifact type.
- Missing or filename-invalid evidence is reported deterministically.
- Planning is bounded.

## Boundary

The planner does not build, upload, publish, tag, download, or mutate release artifacts. The SHA-256 helper is a pure computation over supplied bytes.
