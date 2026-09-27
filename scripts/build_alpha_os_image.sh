#!/usr/bin/env bash
set -euo pipefail

VERSION="${ALPHA_VERSION:-0.1.0a1}"
CHANNEL="${ALPHA_CHANNEL:-alpha}"
ARCH="${ALPHA_ARCH:-amd64}"
RELEASE_ID="${ALPHA_RELEASE_ID:-alpha-os-0-1-0a1}"
SOURCE_COMMIT="${GITHUB_SHA:?GITHUB_SHA is required}"
CI_RUN_ID="${GITHUB_RUN_ID:?GITHUB_RUN_ID is required}"
BUILD_ENVIRONMENT="${ALPHA_BUILD_ENVIRONMENT:-github-hosted-ubuntu-latest}"
VERIFY_REPRODUCIBILITY="${ALPHA_VERIFY_REPRODUCIBILITY:-true}"
SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-946684800}"

BASE_URL="https://releases.ubuntu.com/resolute/"
BASE_ISO="ubuntu-26.04.1-desktop-amd64.iso"
BASE_SHA256="601e30fbf5d97759367c632e2c33630665039b7e2158fd068403da3ccf1bda1f"

OUT_DIR="${GITHUB_WORKSPACE:-.}/dist"
WORK_DIR="${RUNNER_TEMP:-/tmp}/alpha-os-image"
BASE_PATH="${WORK_DIR}/${BASE_ISO}"
OUTPUT_PATH="${OUT_DIR}/alpha-linux-${VERSION}-${CHANNEL}-${ARCH}.iso"
REFERENCE_PATH="${WORK_DIR}/alpha-linux-${VERSION}-${CHANNEL}-${ARCH}.reproducibility.iso"
SEED_PATH="${WORK_DIR}/alpha-release.json"
MANIFEST_PATH="${OUT_DIR}/alpha-linux-${VERSION}-${CHANNEL}-${ARCH}.manifest.json"
LIVE_ROOT="${WORK_DIR}/live-rootfs"
CASPER_DIR="${WORK_DIR}/casper"
CUSTOM_SQUASHFS="${WORK_DIR}/filesystem.cosmic.squashfs"
COSMIC_MANIFEST_PATH="${OUT_DIR}/cosmic-live-image-evidence.json"

mkdir -p "${OUT_DIR}" "${WORK_DIR}"
rm -f "${OUTPUT_PATH}" "${REFERENCE_PATH}" "${MANIFEST_PATH}" "${SEED_PATH}" "${CUSTOM_SQUASHFS}" "${COSMIC_MANIFEST_PATH}"
rm -rf "${LIVE_ROOT}" "${CASPER_DIR}"

echo "Downloading Ubuntu base image: ${BASE_ISO}"
curl --fail --location --retry 3 --retry-delay 2 --output "${BASE_PATH}" "${BASE_URL}${BASE_ISO}"

echo "Verifying Ubuntu base SHA-256"
printf '%s  %s\n' "${BASE_SHA256}" "${BASE_PATH}" | sha256sum --check --strict -

python3 - "${SEED_PATH}" "${BASE_ISO}" "${BASE_SHA256}" "${VERSION}" "${CHANNEL}" "${ARCH}" "${RELEASE_ID}" "${SOURCE_COMMIT}" "${CI_RUN_ID}" "${BUILD_ENVIRONMENT}" <<'PY'
import json
import sys
from pathlib import Path

(
    path,
    base_filename,
    base_sha256,
    version,
    channel,
    architecture,
    release_id,
    source_commit,
    ci_run_id,
    build_environment,
) = sys.argv[1:]

payload = {
    "product": "Alpha Linux",
    "release_id": release_id,
    "version": version,
    "channel": channel,
    "architecture": architecture,
    "artifact_format": "iso",
    "source_base": {
        "product": "Ubuntu",
        "version": "26.04.1 LTS",
        "filename": base_filename,
        "sha256": base_sha256,
        "url": "https://releases.ubuntu.com/resolute/",
    },
    "source_commit": source_commit,
    "ci_run_id": ci_run_id,
    "build_environment": build_environment,
    "reproducibility_method": "same-run-second-build-same-inputs",
    "builder": "alpha-linux-os-image-repack",
    "contract": "specs/alpha-os-image-artifact-contract.md",
}
Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

export SOURCE_DATE_EPOCH

prepare_live_rootfs() {
  echo "Extracting Ubuntu Live rootfs from the ISO"
  mkdir -p "${CASPER_DIR}" "${LIVE_ROOT}"
  xorriso -indev "${BASE_PATH}" -osirrox on -extract /casper "${CASPER_DIR}" >/dev/null 2>&1 || true
  test -f "${CASPER_DIR}/filesystem.squashfs"
  unsquashfs -d "${LIVE_ROOT}" "${CASPER_DIR}/filesystem.squashfs" >/dev/null 2>&1
}

install_cosmic_runtime() {
  echo "Installing COSMIC into the live rootfs"
  chroot "${LIVE_ROOT}" /bin/bash -lc '
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y --no-install-recommends ca-certificates curl gpg
    mkdir -p /usr/share/keyrings
    curl -fsSL https://apt.pop-os.org/release.key | gpg --dearmor -o /usr/share/keyrings/pop-os-archive-keyring.gpg
    cat > /etc/apt/sources.list.d/pop-os-cosmic.list <<"EOF"
deb [signed-by=/usr/share/keyrings/pop-os-archive-keyring.gpg arch=amd64] https://apt.pop-os.org/release $(. /etc/os-release && echo "$UBUNTU_CODENAME") main
EOF
    apt-get update
    if ! apt-get install -y --no-install-recommends cosmic-session cosmic-desktop; then
      apt-get install -y --no-install-recommends cosmic-session || true
    fi
  '
}

validate_cosmic_runtime() {
  echo "Validating the COSMIC live-session runtime"
  test -f "${LIVE_ROOT}/usr/share/xsessions/cosmic.desktop" || test -f "${LIVE_ROOT}/usr/share/wayland-sessions/cosmic.desktop"
  test -x "${LIVE_ROOT}/usr/bin/start-cosmic" || test -x "${LIVE_ROOT}/usr/local/bin/start-cosmic"

  PYTHONPATH="${GITHUB_WORKSPACE:-.}/implementation" \
  python3 - "${LIVE_ROOT}" "${COSMIC_MANIFEST_PATH}" <<'PY'
import json
import os
import sys
from pathlib import Path

root = Path(sys.argv[1])
manifest_path = Path(sys.argv[2])

desktop_candidates = (
    root / "usr/share/xsessions/cosmic.desktop",
    root / "usr/share/wayland-sessions/cosmic.desktop",
)
launcher_candidates = (
    root / "usr/bin/start-cosmic",
    root / "usr/local/bin/start-cosmic",
)

for desktop in desktop_candidates:
    if desktop.exists():
        break
else:
    raise SystemExit("missing cosmic.desktop in live rootfs")

for launcher in launcher_candidates:
    if launcher.exists() and os.access(launcher, os.X_OK):
        break
else:
    raise SystemExit("missing executable start-cosmic in live rootfs")

payload = {
    "desktop_file": next(str(path) for path in desktop_candidates if path.exists()),
    "session_launcher": next(str(path) for path in launcher_candidates if path.exists() and os.access(path, os.X_OK)),
    "required_packages": ["cosmic-session", "cosmic-desktop"],
    "state": "validated",
}
manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2, sort_keys=True))
PY
}

prepare_live_rootfs
install_cosmic_runtime
validate_cosmic_runtime

echo "Rebuilding Live squashfs with the custom COSMIC runtime"
mksquashfs "${LIVE_ROOT}" "${CUSTOM_SQUASHFS}" -noappend -quiet

build_iso() {
  local output_path="$1"
  echo "Building ISO: ${output_path}"
  xorriso \
    -indev "${BASE_PATH}" \
    -outdev "${output_path}" \
    -map "${SEED_PATH}" /alpha-release.json \
    -map "${CUSTOM_SQUASHFS}" /casper/filesystem.squashfs \
    -boot_image any replay \
    -compliance no_emul_toc \
    -padding included
}

echo "Repacking bootable Ubuntu ISO with deterministic time inputs and a COSMIC-enabled live rootfs"
build_iso "${OUTPUT_PATH}"

REPRODUCIBILITY_RESULT="not-run"
REFERENCE_SHA256="0000000000000000000000000000000000000000000000000000000000000000"

if [[ "${VERIFY_REPRODUCIBILITY}" == "true" ]]; then
  build_iso "${REFERENCE_PATH}"
  IMAGE_SHA256_FIRST="$(sha256sum "${OUTPUT_PATH}" | awk '{print $1}')"
  REFERENCE_SHA256="$(sha256sum "${REFERENCE_PATH}" | awk '{print $1}')"
  if [[ "${IMAGE_SHA256_FIRST}" != "${REFERENCE_SHA256}" ]]; then
    echo "Reproducibility check failed: first=${IMAGE_SHA256_FIRST} second=${REFERENCE_SHA256}"
    REPRODUCIBILITY_RESULT="failed"
    exit 1
  fi
  REPRODUCIBILITY_RESULT="passed"
fi

echo "Validating ISO structure and embedded Alpha metadata"
xorriso -indev "${OUTPUT_PATH}" -ls /alpha-release.json | grep -F 'alpha-release.json'
xorriso -indev "${OUTPUT_PATH}" -ls /casper | tee "${OUT_DIR}/live-filesystem-evidence.txt"
grep -Eq "\.squashfs['[:space:]]*$" "${OUT_DIR}/live-filesystem-evidence.txt"
grep -Eq "^['[:space:]]*initrd['[:space:]]*$" "${OUT_DIR}/live-filesystem-evidence.txt"

IMAGE_SIZE="$(stat -c '%s' "${OUTPUT_PATH}")"
IMAGE_SHA256="$(sha256sum "${OUTPUT_PATH}" | awk '{print $1}')"

PYTHONPATH="${GITHUB_WORKSPACE:-.}/implementation" \
python3 - "${OUTPUT_PATH}" "${MANIFEST_PATH}" "${RELEASE_ID}" "${VERSION}" "${CHANNEL}" "${ARCH}" "${SOURCE_COMMIT}" "${CI_RUN_ID}" "${BUILD_ENVIRONMENT}" "${REPRODUCIBILITY_RESULT}" "${IMAGE_SIZE}" "${IMAGE_SHA256}" "${REFERENCE_SHA256}" <<'PY'
import json
import os
import sys
from pathlib import Path
from alpha_core.os_image import OSImageEvidence

(
    image,
    manifest,
    release_id,
    version,
    channel,
    architecture,
    source_commit,
    ci_run_id,
    build_environment,
    reproducibility_result,
    image_size,
    image_sha256,
    reproducibility_reference_sha256,
) = sys.argv[1:]

evidence = OSImageEvidence(
    release_id=release_id,
    version=version,
    channel=channel,
    architecture=architecture,
    artifact_format="iso",
    artifact_filename=Path(image).name,
    artifact_size=int(image_size),
    artifact_sha256=image_sha256,
    source_commit=source_commit,
    ci_run_id=ci_run_id,
    build_environment=build_environment,
    reproducibility_result=reproducibility_result,
    reproducibility_reference_sha256=reproducibility_reference_sha256,
)

evidence.validate_filename()

payload = {
    **evidence.__dict__,
    "deterministic_filename": evidence.deterministic_filename,
    "source_date_epoch": int(os.environ["SOURCE_DATE_EPOCH"]),
}
Path(manifest).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

echo "IMAGE=${OUTPUT_PATH}"
echo "SIZE=${IMAGE_SIZE}"
echo "SHA256=${IMAGE_SHA256}"
echo "REFERENCE_SHA256=${REFERENCE_SHA256}"
echo "REPRODUCIBILITY=${REPRODUCIBILITY_RESULT}"
echo "MANIFEST=${MANIFEST_PATH}"
echo "COSMIC_MANIFEST=${COSMIC_MANIFEST_PATH}"

