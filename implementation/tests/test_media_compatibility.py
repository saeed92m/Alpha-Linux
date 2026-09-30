from alpha_core.media_compatibility import (
    BootMode,
    MediaCase,
    PartitionScheme,
    validate_media_matrix,
)


def case(mode, scheme, *, bootable=True, evidence="ci-evidence"):
    return MediaCase(mode, scheme, bootable, evidence)


def test_complete_declared_matrix_passes():
    cases = tuple(
        case(mode, scheme)
        for mode in BootMode
        for scheme in PartitionScheme
    )
    report = validate_media_matrix(cases)
    assert report.complete_for_declared_matrix is True
    assert report.missing_required_cases == ()
    assert report.unsupported_claims == ()


def test_missing_case_fails_closed():
    cases = (
        case(BootMode.UEFI, PartitionScheme.GPT),
        case(BootMode.LEGACY_BIOS, PartitionScheme.GPT),
        case(BootMode.UEFI, PartitionScheme.MBR),
    )
    report = validate_media_matrix(cases)
    assert report.complete_for_declared_matrix is False
    assert (BootMode.LEGACY_BIOS, PartitionScheme.MBR) in report.missing_required_cases


def test_nonbootable_case_is_not_accepted_as_evidence():
    cases = tuple(
        case(mode, scheme, bootable=not (mode is BootMode.UEFI and scheme is PartitionScheme.MBR))
        for mode in BootMode
        for scheme in PartitionScheme
    )
    report = validate_media_matrix(cases)
    assert report.complete_for_declared_matrix is False
    assert "uefi/mbr is declared but not bootable" in report.unsupported_claims


def test_empty_evidence_is_fail_closed():
    cases = tuple(
        case(mode, scheme, evidence="" if scheme is PartitionScheme.MBR else "qemu")
        for mode in BootMode
        for scheme in PartitionScheme
    )
    report = validate_media_matrix(cases)
    assert report.complete_for_declared_matrix is False
    assert "uefi/mbr has no evidence reference" in report.unsupported_claims


def test_matrix_can_be_scoped_to_uefi_gpt():
    report = validate_media_matrix(
        (case(BootMode.UEFI, PartitionScheme.GPT),),
        require_legacy=False,
        require_mbr=False,
    )
    assert report.complete_for_declared_matrix is True
