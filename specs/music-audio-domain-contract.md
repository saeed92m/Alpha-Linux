# Music & Audio Domain Contract

## Purpose

The Music & Audio foundation defines immutable audio-session, track, capability, and routing-requirement contracts and produces deterministic bounded routing plans.

## Contracts

- AudioKind identifies supported audio representations.
- TrackRole distinguishes source, processed, and rendered tracks.
- AudioCapability declares an input/output/processing/MIDI capability and supported audio kinds.
- AudioSession declares supported audio kinds and validates track scope.
- AudioRoutingRequirement declares a required capability kind, audio kind, and capability set.
- AudioPlan contains normalized session, track, capability, and requirement identifiers.
- MusicAudioPlanner performs deterministic normalization and compatibility planning.

## Rejection semantics

Invalid identifiers, empty capability sets, duplicate identifiers, session-scope mismatches, incompatible capabilities, and invalid planning bounds are rejected deterministically.

## Boundary

This foundation performs no recording, playback, DAW execution, MIDI/device I/O, filesystem mutation, subprocess execution, network access, credential access, or host mutation.
