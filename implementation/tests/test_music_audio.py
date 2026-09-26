from alpha_core.music_audio import (
    AudioCapability, AudioCapabilityKind, AudioKind, AudioRoutingRequirement,
    AudioSession, AudioTrack, MusicAudioPlanner, TrackRole,
)


def track(track_id: str, kind=AudioKind.MONO, role=TrackRole.SOURCE):
    return AudioTrack(track_id, track_id, kind, role)


def capability(capability_id, kind=AudioCapabilityKind.INPUT,
               audio_kinds=(AudioKind.MONO,), capabilities=("capture",)):
    return AudioCapability(capability_id, kind, audio_kinds, capabilities)


def requirement(requirement_id="req-1", kind=AudioCapabilityKind.INPUT,
                 audio_kind=AudioKind.MONO, capabilities=("capture",)):
    return AudioRoutingRequirement(requirement_id, kind, audio_kind, capabilities)


def session(kinds=(AudioKind.MONO,), tracks=()):
    return AudioSession("session-1", "Alpha Audio Session", kinds, tracks)


def test_track_roles_and_normalization_are_deterministic():
    planner = MusicAudioPlanner()
    result = planner.normalize_tracks((
        track("rendered", role=TrackRole.RENDERED),
        track("source"),
        track("processed", role=TrackRole.PROCESSED),
    ))
    assert tuple(item.track_id for item in result) == ("processed", "rendered", "source")
    assert {item.role for item in result} == set(TrackRole)


def test_capability_and_requirement_normalization():
    planner = MusicAudioPlanner()
    assert tuple(item.capability_id for item in planner.normalize_capabilities(
        (capability("b"), capability("a"))
    )) == ("a", "b")
    assert tuple(item.requirement_id for item in planner.normalize_requirements(
        (requirement("b"), requirement("a"))
    )) == ("a", "b")


def test_planning_enforces_audio_kind_and_capability():
    planner = MusicAudioPlanner()
    result = planner.plan(session(tracks=(track("source"),)), (capability("mic"),), (requirement(),))
    assert result.session_id == "session-1"
    assert result.track_ids == ("source",)
    assert result.capability_ids == ("mic",)
    assert result.requirement_ids == ("req-1",)

    try:
        planner.plan(session(), (capability("mic", capabilities=("monitor",)),),
                     (requirement(capabilities=("capture", "low-latency")),))
    except ValueError as exc:
        assert str(exc) == "no compatible audio capability"
    else:
        raise AssertionError("expected ValueError")


def test_session_scope_is_enforced():
    try:
        MusicAudioPlanner().plan(session(), (capability("line", audio_kinds=(AudioKind.STEREO,)),),
                                 (requirement(audio_kind=AudioKind.STEREO),))
    except ValueError as exc:
        assert str(exc) == "session lacks required audio kind"
    else:
        raise AssertionError("expected ValueError")


def test_capability_kind_is_enforced():
    try:
        MusicAudioPlanner().plan(session(), (capability("out", kind=AudioCapabilityKind.OUTPUT),),
                                 (requirement(kind=AudioCapabilityKind.INPUT),))
    except ValueError as exc:
        assert str(exc) == "no compatible audio capability"
    else:
        raise AssertionError("expected ValueError")


def test_bounded_plan():
    planner = MusicAudioPlanner()
    result = planner.plan(session(), (capability("mic"), capability("mic-2")),
                          (requirement("a"), requirement("b")), max_capabilities=2)
    assert result.capability_ids == ("mic", "mic")
    try:
        planner.plan(session(), (capability("mic"),), (requirement(),), max_capabilities=0)
    except ValueError as exc:
        assert str(exc) == "max_capabilities must be positive"
    else:
        raise AssertionError("expected ValueError")


def test_invalid_contracts_are_rejected():
    try:
        AudioSession("s", "Alpha", ())
    except ValueError as exc:
        assert str(exc) == "audio_kinds must be non-empty"
    else:
        raise AssertionError("expected ValueError")

    try:
        AudioSession("s", "Alpha", (AudioKind.MONO,), (track("stereo", AudioKind.STEREO),))
    except ValueError as exc:
        assert str(exc) == "track audio kind is outside session scope"
    else:
        raise AssertionError("expected ValueError")

    try:
        capability("invalid", capabilities=())
    except ValueError as exc:
        assert str(exc) == "capabilities must be non-empty"
    else:
        raise AssertionError("expected ValueError")
