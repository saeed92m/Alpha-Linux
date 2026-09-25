# Alpha Linux — Music & Audio Suite Specification

**Status:** Phase 0 normative specification
**Requirement:** AL-REQ-0020

## Scope

DAW, recording, mixing, mastering, MIDI, virtual instruments, synthesizers, samplers, effects, audio editing, sound design, notation, composition, arrangement, ear training, live performance, podcasting, voice, streaming and AI-assisted music workflows.

## Audio stack

PipeWire, JACK compatibility, ALSA and standards-based plugin/MIDI ecosystems are integration targets. Low-latency and multi-channel workflows MUST expose relevant buffer, sample-rate, device and routing state.

## Safety/recovery

Audio routing changes MUST be inspectable. Project sessions, presets and plugin state SHOULD be included in backup policies. Destructive edits MUST preserve source material when the application supports non-destructive workflows.

## Acceptance evidence

Device hotplug, low-latency playback/recording, MIDI routing, plugin discovery, multi-channel routing, session backup/restore, and recovery from audio-server failure.
