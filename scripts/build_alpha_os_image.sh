#!/usr/bin/env bash
set -euo pipefail

VERSION="${ALPHA_VERSION:-0.1.0a1}"
CHANNEL="${ALPHA_CHANNEL:-alpha}"
ARCH="${ALPHA_ARCH:-amd64}"
RELEASE_ID="${ALPHA_RELEASE_ID:-alpha-os-0-1-0a1}"
SOURCE_COMMIT="${GITHUB_SHA:?GITHUB_SHA is required}"
CI_RUN_ID="${GITHUB_RUN_ID:?GITHUB_RUN_ID is required}"
BUILD_ENVIRONMENT="${ALPHA_BUILD_ENVIRONMENT:-github-hosted-ubuntu-latest}"
REPRODUCIBILITY_RESULT="${ALPHA_REPRODUCIBILITY_RESULT:-not-run}"

BASE_URL="https://releases.ubuntu.com/resolute/"
BASE_ISO="ubuntu-26.04.1-desktop-amd64.iso"
BASE_SHA256="601e30fbf5d97759367c632e2c33630665039b7e2158fd068403da3ccf1bda1f"

OUT_DIR="${GITHUB_WORKSPACE:-.}/dist"
WORK_DIR="${RUNNER_TEMP:-/tmp}/alpha-os-image"
BASE_PATH="${WORK_DIR}/${BASE_ISO}"
OUTPUT_PATH="${OUT_DIR}/alpha-linux-${VERSION}-${CHANNEL}-${ARCH}.iso"
SEED_PATH="${WORK_DIR}/alpha-release.json"
MANIFEST_PATH="${OUT_DIR}/alpha-linux-${VERSION}-${CHANNEL}-${ARCH}.manifest.json"

mkdir -p "${OUT_DIR}" "${WORK_DIR}"
rm -f "${OUTPUT_PATH}" "${MANIFEST_PATH}" "${SEED_PATH}"

echo "Downloading Ubuntu base image: ${BASE_ISO}"
curl --fail --location --retry 3 --retry-delay 2 --output "${BASE_PATH}" "${BASE_URL}${BASE_ISO}"

echo "Verifying Ubuntu base SHA-256"
printf '%s  %s\n' "${BASE_SHA256}" "${BASE_PATH}" | sha256sum --check --strict -

python3 - "${SEED_PATH}" "${BASE_ISO}" "${BASE_SHA256}" "${VERSION}" "${CHANNEL}" "${ARCH}" "${RELEASE_ID}" "${SOURCE_COMMIT}" "${CI_RUN_ID}" "${BUILD_ENVIRONMENT}" "${REPRODUCIBILITY_RESULT}" <<'PY'
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
    reproducibility_result,
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
    "reproducibility_result": reproducibility_result,
    "builder": "alpha-linux-os-image-repack",
    "contract": "specs/alpha-os-image-artifact-contract.md",
}
Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

echo "Repacking bootable Ubuntu ISO while preserving original boot metadata"
xorriso   -indev "${BASE_PATH}"   -outdev "${OUTPUT_PATH}"   -map "${SEED_PATH}" /alpha-release.json   -boot_image any replay   -compliance no_emul_toc   -padding included

echo "Validating ISO structure and embedded Alpha metadata"
xorriso -indev "${OUTPUT_PATH}" -ls /alpha-release.json | grep -F 'alpha-release.json'
xorriso -indev "${OUTPUT_PATH}" -report_el_torito plain | tee "${OUT_DIR}/el-torito-report.txt"
grep -Eq 'BIOS|EFI|El Torito' "${OUT_DIR}/el-torito-report.txt"

IMAGE_SIZE="$(stat -c '%s' "${OUTPUT_PATH}")"
IMAGE_SHA256="$(sha256sum "${OUTPUT_PATH}" | awk '{print $1}')"

PYTHONPATH="${GITHUB_WORKSPACE:-.}/implementation" \
python3 - "${OUTPUT_PATH}" "${MANIFEST_PATH}" "${RELEASE_ID}" "${VERSION}" "${CHANNEL}" "${ARCH}" "${SOURCE_COMMIT}" "${CI_RUN_ID}" "${BUILD_ENVIRONMENT}" "${REPRODUCIBILITY_RESULT}" "${IMAGE_SIZE}" "${IMAGE_SHA256}" <<'PY'
import json
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
)
evidence.validate_filename()

payload = {
    **evidence.__dict__,
    "deterministic_filename": evidence.deterministic_filename,
}
Path(manifest).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

echo "IMAGE=${OUTPUT_PATH}"
echo "SIZE=${IMAGE_SIZE}"
echo "SHA256=${IMAGE_SHA256}"
echo "MANIFEST=${MANIFEST_PATH}"
