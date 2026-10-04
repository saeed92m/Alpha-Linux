from pathlib import Path

MATRIX = Path("docs/release/media-compatibility-matrix.md")

REQUIRED_ROWS = (
    "| UEFI | GPT | GPT |",
    "| UEFI | MBR | GPT |",
    "| Legacy BIOS | MBR | MBR |",
    "| Legacy BIOS | GPT | MBR |",
)

def test_media_matrix_exists_and_is_fail_closed():
    text = MATRIX.read_text(encoding="utf-8")
    for row in REQUIRED_ROWS:
        assert row in text
    assert "Current status" in text
    assert "Evidence required" in text

def test_media_matrix_does_not_infer_physical_success_from_qemu():
    text = MATRIX.read_text(encoding="utf-8")
    assert "QEMU evidence closes only the virtual-boot rows" in text
    assert "no physical validation is claimed" in text

def test_media_matrix_requires_concrete_evidence_fields():
    text = MATRIX.read_text(encoding="utf-8")
    for field in (
        "exact ISO SHA-256",
        "USB-writing tool and version",
        "USB device model/capacity",
        "Firmware mode and firmware version",
        "Boot result and timestamp",
        "Hardware model",
        "Evidence artifact",
    ):
        assert field in text
