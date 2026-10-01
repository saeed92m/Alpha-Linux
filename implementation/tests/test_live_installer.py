from pathlib import Path
import subprocess

INSTALLER = Path("scripts/alpha-live-installer.sh")


def test_live_installer_passes_bash_syntax_check():
    result = subprocess.run(["bash", "-n", str(INSTALLER)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_live_installer_exists_and_is_bash_script():
    text = INSTALLER.read_text(encoding="utf-8")
    assert text.startswith("#!/usr/bin/env bash")
    assert "set -euo pipefail" in text


def test_live_installer_is_fail_closed_before_disk_mutation():
    text = INSTALLER.read_text(encoding="utf-8")
    assert '[ -d /sys/firmware/efi ]' in text
    assert 'CHILDREN="$(lsblk -lnpo NAME "$TARGET_DISK" | tail -n +2)"' in text
    assert '[ -z "$CHILDREN" ] || fail' in text
    assert "Windows|Microsoft|Recovery" in text
    assert '--ok-label="ERASE AND INSTALL"' in text


def test_live_installer_has_deterministic_partition_and_verification_steps():
    text = INSTALLER.read_text(encoding="utf-8")
    assert "sgdisk --zap-all" in text
    assert "--change-name=1:Alpha-EFI" in text
    assert "--change-name=2:Alpha-Root" in text
    assert "sgdisk --verify" in text
    assert "grub-install --target=x86_64-efi" in text
    assert 'INSTALL_RESULT=PASS' in text
    assert '/etc/alpha-linux-installed' in text
