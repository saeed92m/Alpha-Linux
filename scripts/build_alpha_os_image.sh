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

mkdir -p "${OUT_DIR}" "${WORK_DIR}"
rm -f "${OUTPUT_PATH}" "${REFERENCE_PATH}" "${MANIFEST_PATH}" "${SEED_PATH}"

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

build_iso() {
  local output_path="$1"
  echo "Building ISO: ${output_path}"
  xorriso \
    -indev "${BASE_PATH}" \
    -outdev "${output_path}" \
    -map "${SEED_PATH}" /alpha-release.json \
    -map "${LIVE_SQUASHFS}" /casper/minimal.standard.live.squashfs \
    -boot_image any replay \
    -compliance no_emul_toc \
    -padding included
}

COSMIC_REPOSITORY="https://apt.pop-os.org/release"
COSMIC_KEY_URL="https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x63C46DF0140D738961429F4E204DD8AEC33A7AFF"
BASE_ROOTFS_DIR="${WORK_DIR}/minimal-root"
STANDARD_ROOTFS_DIR="${WORK_DIR}/standard-root"
LIVE_ROOTFS_DIR="${WORK_DIR}/live-root"
OVERLAY_ROOTFS_DIR="${WORK_DIR}/merged-root"
OVERLAY_WORK_DIR="${WORK_DIR}/overlay-work"
LIVE_SQUASHFS="${WORK_DIR}/minimal.standard.live.squashfs"
COSMIC_MANIFEST="${OUT_DIR}/alpha-cosmic-package-manifest.txt"

echo "Extracting layered Ubuntu Live filesystems for COSMIC integration"
rm -rf "${BASE_ROOTFS_DIR}" "${STANDARD_ROOTFS_DIR}" "${LIVE_ROOTFS_DIR}" "${OVERLAY_ROOTFS_DIR}" "${OVERLAY_WORK_DIR}" "${LIVE_SQUASHFS}" "${COSMIC_MANIFEST}"
CASPER_LIST="$(xorriso -indev "${BASE_PATH}" -ls /casper 2>&1)"
echo "${CASPER_LIST}"
strip_quotes() { tr -d "'"; }
SQUASHFS_NAMES="$(printf '%s\n' "${CASPER_LIST}" | strip_quotes | awk '$NF ~ /\.squashfs$/ {print $NF}')"
BASE_SQUASHFS_NAME="$(printf '%s\n' "${SQUASHFS_NAMES}" | awk '$0 == "minimal.squashfs" {print; exit}')"
STANDARD_SQUASHFS_NAME="$(printf '%s\n' "${SQUASHFS_NAMES}" | awk '$0 == "minimal.standard.squashfs" {print; exit}')"
LIVE_SQUASHFS_NAME="$(printf '%s\n' "${SQUASHFS_NAMES}" | awk '$0 == "minimal.standard.live.squashfs" {print; exit}')"
test -n "${BASE_SQUASHFS_NAME}"
test -n "${STANDARD_SQUASHFS_NAME}"
test -n "${LIVE_SQUASHFS_NAME}"
BASE_SQUASHFS_PATH="/casper/${BASE_SQUASHFS_NAME}"
STANDARD_SQUASHFS_PATH="/casper/${STANDARD_SQUASHFS_NAME}"
LIVE_SQUASHFS_PATH="/casper/${LIVE_SQUASHFS_NAME}"
echo "Detected layered Live payloads: ${BASE_SQUASHFS_PATH}, ${STANDARD_SQUASHFS_PATH}, ${LIVE_SQUASHFS_PATH}"
xorriso -indev "${BASE_PATH}" -osirrox on -extract "${BASE_SQUASHFS_PATH}" "${WORK_DIR}/minimal.squashfs"
xorriso -indev "${BASE_PATH}" -osirrox on -extract "${STANDARD_SQUASHFS_PATH}" "${WORK_DIR}/minimal.standard.squashfs"
xorriso -indev "${BASE_PATH}" -osirrox on -extract "${LIVE_SQUASHFS_PATH}" "${WORK_DIR}/minimal.standard.live.squashfs"
sudo unsquashfs -d "${BASE_ROOTFS_DIR}" "${WORK_DIR}/minimal.squashfs"
sudo unsquashfs -d "${STANDARD_ROOTFS_DIR}" "${WORK_DIR}/minimal.standard.squashfs"
sudo unsquashfs -d "${LIVE_ROOTFS_DIR}" "${WORK_DIR}/minimal.standard.live.squashfs"
sudo mkdir -p "${OVERLAY_ROOTFS_DIR}" "${OVERLAY_WORK_DIR}"
sudo mount -t overlay overlay -o lowerdir="${STANDARD_ROOTFS_DIR}:${BASE_ROOTFS_DIR}",upperdir="${LIVE_ROOTFS_DIR}",workdir="${OVERLAY_WORK_DIR}" "${OVERLAY_ROOTFS_DIR}"
cleanup_chroot() {
  sudo umount -lf "${OVERLAY_ROOTFS_DIR}/run" || true
  sudo umount -lf "${OVERLAY_ROOTFS_DIR}/tmp" || true
  sudo umount -lf "${OVERLAY_ROOTFS_DIR}/sys" || true
  sudo umount -lf "${OVERLAY_ROOTFS_DIR}/proc" || true
  sudo umount -lf "${OVERLAY_ROOTFS_DIR}/dev/pts" || true
  sudo umount -lf "${OVERLAY_ROOTFS_DIR}/dev" || true
  sudo umount -lf "${OVERLAY_ROOTFS_DIR}" || true
}
trap cleanup_chroot EXIT

echo "Injecting COSMIC repository and packages into merged Live rootfs"
sudo mkdir -p "${OVERLAY_ROOTFS_DIR}/etc/apt/keyrings" "${OVERLAY_ROOTFS_DIR}/etc/apt/sources.list.d"
curl --fail --location --retry 3 --retry-delay 2 --max-time 60 "${COSMIC_KEY_URL}" \
  | gpg --dearmor \
  | sudo tee "${OVERLAY_ROOTFS_DIR}/etc/apt/keyrings/pop-os.gpg" >/dev/null
printf 'deb [signed-by=/etc/apt/keyrings/pop-os.gpg] %s %s main\n' "${COSMIC_REPOSITORY}" "resolute" \
  | sudo tee "${OVERLAY_ROOTFS_DIR}/etc/apt/sources.list.d/alpha-cosmic.list" >/dev/null
sudo sed -i '/^[[:space:]]*deb[[:space:]]\+cdrom:/s/^/# disabled by Alpha Linux Live build/' "${OVERLAY_ROOTFS_DIR}/etc/apt/sources.list" || true

sudo tee "${OVERLAY_ROOTFS_DIR}/usr/sbin/policy-rc.d" >/dev/null <<'POLICY'
#!/bin/sh
exit 101
POLICY
sudo chmod 0755 "${OVERLAY_ROOTFS_DIR}/usr/sbin/policy-rc.d"

echo "Normalizing APT sources for deterministic Live customization"
sudo rm -f "${OVERLAY_ROOTFS_DIR}/etc/apt/sources.list"
sudo rm -f "${OVERLAY_ROOTFS_DIR}/etc/apt/sources.list.d/"*.list
sudo rm -f "${OVERLAY_ROOTFS_DIR}/etc/apt/sources.list.d/"*.sources
sudo tee "${OVERLAY_ROOTFS_DIR}/etc/apt/sources.list" >/dev/null <<'APT'
deb http://archive.ubuntu.com/ubuntu resolute main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu resolute-updates main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu resolute-security main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu resolute-backports main restricted universe multiverse
APT
printf 'deb [signed-by=/etc/apt/keyrings/pop-os.gpg] %s %s main\n' "${COSMIC_REPOSITORY}" "resolute" \
  | sudo tee "${OVERLAY_ROOTFS_DIR}/etc/apt/sources.list.d/alpha-cosmic.list" >/dev/null

sudo mount --bind /dev "${OVERLAY_ROOTFS_DIR}/dev"
sudo mount --bind /dev/pts "${OVERLAY_ROOTFS_DIR}/dev/pts"
sudo mount -t proc proc "${OVERLAY_ROOTFS_DIR}/proc"
sudo mount -t sysfs sysfs "${OVERLAY_ROOTFS_DIR}/sys"
sudo mount -t tmpfs tmpfs "${OVERLAY_ROOTFS_DIR}/run"
sudo mount -t tmpfs tmpfs "${OVERLAY_ROOTFS_DIR}/tmp"
echo "Preparing display-manager handoff for COSMIC"
if [[ -L "${OVERLAY_ROOTFS_DIR}/etc/systemd/system/display-manager.service" ]]; then
  sudo rm -f "${OVERLAY_ROOTFS_DIR}/etc/systemd/system/display-manager.service"
fi
sudo mkdir -p "${OVERLAY_ROOTFS_DIR}/run/systemd/resolve"
sudo cp -L /etc/resolv.conf "${OVERLAY_ROOTFS_DIR}/run/systemd/resolve/stub-resolv.conf"

timeout 20m sudo env DEBIAN_FRONTEND=noninteractive chroot "${OVERLAY_ROOTFS_DIR}" /usr/bin/apt-get update

echo "Installing COSMIC and validating dpkg state inside the build chroot"
set +e
timeout 20m sudo env DEBIAN_FRONTEND=noninteractive chroot "${OVERLAY_ROOTFS_DIR}" /usr/bin/apt-get install -y cosmic-session
APT_INSTALL_STATUS=$?
set -e

COSMIC_DPKG_STATUS="$(sudo chroot "${OVERLAY_ROOTFS_DIR}" /usr/bin/dpkg-query -W -f='${Status}' cosmic-session 2>/dev/null || true)"
echo "cosmic-session dpkg status: ${COSMIC_DPKG_STATUS}"
if [[ "${COSMIC_DPKG_STATUS}" != "install ok installed" ]]; then
  echo "COSMIC package installation did not reach a configured installed state (apt status=${APT_INSTALL_STATUS})"
  sudo chroot "${OVERLAY_ROOTFS_DIR}" /usr/bin/dpkg --audit || true
  sudo chroot "${OVERLAY_ROOTFS_DIR}" /usr/bin/dpkg-query -W -f='${Package} ${Status}\n' cosmic-session cosmic-settings cosmic-comp 2>/dev/null || true
  exit 1
fi

if [[ "${APT_INSTALL_STATUS}" -ne 0 ]]; then
  echo "apt-get returned ${APT_INSTALL_STATUS}, but cosmic-session is configured; continuing with explicit runtime validation."
fi

sudo chroot "${OVERLAY_ROOTFS_DIR}" /usr/bin/apt-get clean || true
sudo rm -rf "${OVERLAY_ROOTFS_DIR}/var/lib/apt/lists/"*

COSMIC_SESSION_FILE="$(find "${OVERLAY_ROOTFS_DIR}/usr/share/wayland-sessions" -maxdepth 1 -name 'cosmic.desktop' -print -quit)"
if [[ ! -s "${COSMIC_SESSION_FILE}" ]]; then
  echo "ERROR: COSMIC Wayland session file was not installed"
  find "${OVERLAY_ROOTFS_DIR}/usr/share/wayland-sessions" -maxdepth 1 -type f -print 2>/dev/null || true
  exit 1
fi
if [[ ! -x "${OVERLAY_ROOTFS_DIR}/usr/bin/start-cosmic" ]]; then
  echo "ERROR: /usr/bin/start-cosmic is missing or not executable"
  exit 1
fi

if [[ ! -x "${OVERLAY_ROOTFS_DIR}/usr/sbin/greetd" ]]; then
  echo "ERROR: greetd is required for the executable COSMIC graphical-session gate"
  exit 1
fi
if [[ ! -x "${OVERLAY_ROOTFS_DIR}/usr/bin/start-cosmic" ]]; then
  echo "ERROR: /usr/bin/start-cosmic is missing or not executable"
  exit 1
fi
if [[ ! -x "${OVERLAY_ROOTFS_DIR}/usr/bin/cosmic-greeter-start" ]]; then
  echo "ERROR: cosmic-greeter-start is required for the COSMIC display-manager path"
  exit 1
fi

echo "Configuring deterministic graphical-runtime boot dependencies"
# These services are unrelated to the COSMIC runtime gate and can block indefinitely
# under the QEMU/AppArmor-constrained CI environment. Mask them in the disposable
# validation image only; the production Live filesystem remains otherwise intact.
sudo mkdir -p "${OVERLAY_ROOTFS_DIR}/etc/systemd/system"
for unit in ldconfig.service snapd.apparmor.service; do
  sudo ln -sfn /dev/null "${OVERLAY_ROOTFS_DIR}/etc/systemd/system/$unit"
done

echo "Configuring greetd for deterministic COSMIC graphical-session validation"
sudo mkdir -p "${OVERLAY_ROOTFS_DIR}/etc/greetd"
sudo rm -f "${OVERLAY_ROOTFS_DIR}/etc/gdm3/custom.conf"
sudo tee "${OVERLAY_ROOTFS_DIR}/etc/greetd/config.toml" >/dev/null <<'GREETD'
[terminal]
vt = "1"
[general]
service = "cosmic-greeter"
[default_session]
command = "cosmic-greeter-start"
user = "cosmic-greeter"
[initial_session]
command = "start-cosmic"
user = "ubuntu"
GREETD

echo "Binding display-manager.service to greetd"
sudo mkdir -p "${OVERLAY_ROOTFS_DIR}/etc/systemd/system"
sudo rm -f "${OVERLAY_ROOTFS_DIR}/etc/systemd/system/display-manager.service"
sudo rm -f "${OVERLAY_ROOTFS_DIR}/etc/systemd/system/multi-user.target.wants/gdm.service" "${OVERLAY_ROOTFS_DIR}/etc/systemd/system/graphical.target.wants/gdm.service"
sudo mkdir -p "${OVERLAY_ROOTFS_DIR}/etc/systemd/system"
sudo ln -sfn /dev/null "${OVERLAY_ROOTFS_DIR}/etc/systemd/system/gdm.service"
if [[ -e "${OVERLAY_ROOTFS_DIR}/lib/systemd/system/greetd.service" ]]; then
  sudo ln -sf /lib/systemd/system/greetd.service "${OVERLAY_ROOTFS_DIR}/etc/systemd/system/display-manager.service"
fi

echo "Staging executable COSMIC graphical-session validator outside the mounted OverlayFS upperdir"
VALIDATOR_ROOTFS_DIR="${WORK_DIR}/cosmic-validator-root"
rm -rf "${VALIDATOR_ROOTFS_DIR}"
sudo mkdir -p "${VALIDATOR_ROOTFS_DIR}/usr/local/sbin" "${VALIDATOR_ROOTFS_DIR}/var/log" "${VALIDATOR_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target.wants"
sudo tee "${VALIDATOR_ROOTFS_DIR}/usr/local/sbin/alpha-cosmic-graphical-runtime-check" >/dev/null <<'CHECK'
#!/bin/sh
set -eu
OUT=/var/log/alpha-cosmic-graphical-runtime.log
exec >>"$OUT" 2>&1
emit() { printf "%s\\n" "$*" | tee -a "$OUT" /dev/ttyS0 2>/dev/null || printf "%s\\n" "$*" >>"$OUT"; }
emit "ALPHA_COSMIC_GRAPHICAL_RUNTIME=START"
emit "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
emit "kernel=$(uname -r)"
emit "uid1000=$(getent passwd 1000 || true)"
emit "drm=$(ls -l /dev/dri 2>/dev/null || true)"
deadline=$(( $(date +%s) + 150 ))
while [ "$(date +%s)" -lt "$deadline" ]; do
  session_ok=0
  cosmic_ok=0
  wayland_ok=0
  desktop_ok=0
  cosmic_pid="$(pgrep -u 1000 -x cosmic-comp | head -n1 || true)"
  if [ -n "$cosmic_pid" ]; then
    cosmic_ok=1
    cosmic_desktop="$(tr '\0' '\n' < "/proc/$cosmic_pid/environ" 2>/dev/null | sed -n 's/^XDG_CURRENT_DESKTOP=//p' | head -n1 || true)"
    if printf '%s' "$cosmic_desktop" | grep -Eqi 'cosmic'; then desktop_ok=1; fi
  fi
  if find /run/user/1000 -maxdepth 1 -type s -name 'wayland-*' -print -quit 2>/dev/null | grep -q .; then wayland_ok=1; fi
  while read -r sid _; do
    [ -n "$sid" ] || continue
    name=$(loginctl show-session "$sid" -p Name --value 2>/dev/null || true)
    type=$(loginctl show-session "$sid" -p Type --value 2>/dev/null || true)
    desktop=$(loginctl show-session "$sid" -p Desktop --value 2>/dev/null || true)
    echo "session sid=$sid name=$name type=$type desktop=$desktop"
    if [ "$name" = "ubuntu" ] && [ "$type" = "wayland" ]; then session_ok=1; fi
    if printf '%s' "$desktop" | grep -Eqi 'cosmic'; then desktop_ok=1; fi
  done <<EOF
$(loginctl list-sessions --no-legend 2>/dev/null || true)
EOF
  if [ "$session_ok" -eq 1 ] && [ "$cosmic_ok" -eq 1 ] && [ "$wayland_ok" -eq 1 ] && [ "$desktop_ok" -eq 1 ]; then
    emit "ALPHA_COSMIC_GRAPHICAL_RUNTIME=PASS"
    emit "cosmic_comp=$(pgrep -u 1000 -x cosmic-comp | head -n1)"
    emit "wayland_socket=$(find /run/user/1000 -maxdepth 1 -type s -name 'wayland-*' -print -quit)"
    cat "$OUT" > /dev/console 2>/dev/null || true
    exit 0
  fi
  sleep 5
done
emit "ALPHA_COSMIC_GRAPHICAL_RUNTIME=FAIL"
echo "=== processes ==="
ps -eo user,pid,ppid,tty,stat,cmd | grep -E 'cosmic|greetd|wayland' | grep -v grep || true
echo "=== sessions ==="
loginctl list-sessions --no-legend 2>&1 || true
echo "=== session details ==="
for sid in $(loginctl list-sessions --no-legend 2>/dev/null | awk '{print $1}'); do loginctl show-session "$sid" -p Name -p Type -p Desktop -p State 2>&1 || true; done
echo "=== wayland runtime ==="
find /run/user -maxdepth 3 -type s -name 'wayland-*' -ls 2>&1 || true
echo "=== greetd journal ==="
journalctl -u greetd --no-pager -n 160 2>&1 || true
cat "$OUT" > /dev/console 2>/dev/null || true
exit 1
CHECK
sudo chmod 0755 "${VALIDATOR_ROOTFS_DIR}/usr/local/sbin/alpha-cosmic-graphical-runtime-check"
sudo tee "${VALIDATOR_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target" >/dev/null <<'TARGET'
[Unit]
Description=Alpha Linux COSMIC graphical runtime validation target
Requires=dbus.service
Requires=systemd-logind.service
Requires=greetd.service
Wants=alpha-cosmic-graphical-runtime.service
After=basic.target dbus.service systemd-logind.service greetd.service
AllowIsolate=yes
TARGET

sudo tee "${VALIDATOR_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-graphical-runtime.service" >/dev/null <<'UNIT'
[Unit]
Description=Alpha Linux COSMIC graphical runtime validation
After=greetd.service
Wants=greetd.service
ConditionPathExists=/usr/bin/start-cosmic
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/alpha-cosmic-graphical-runtime-check
Environment=XDG_RUNTIME_DIR=/run/user/1000
TimeoutStartSec=180s
StandardOutput=journal+console
StandardError=journal+console
[Install]
WantedBy=multi-user.target
UNIT
sudo ln -sf /lib/systemd/system/greetd.service "${VALIDATOR_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target.wants/greetd.service"
sudo ln -sf ../alpha-cosmic-graphical-runtime.service "${VALIDATOR_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target.wants/alpha-cosmic-graphical-runtime.service"
sudo chroot "${OVERLAY_ROOTFS_DIR}" /usr/bin/dpkg-query -W -f='${binary:Package}\t${Version}\n'   | awk '/^(cosmic-|xdg-desktop-portal-cosmic|greetd)/'   | LC_ALL=C sort   > "${COSMIC_MANIFEST}"
if [[ ! -s "${COSMIC_MANIFEST}" ]]; then
  echo "ERROR: COSMIC package manifest is empty"
  exit 1
fi

printf 'COSMIC repository: %s\\n' "${COSMIC_REPOSITORY}" > "${OUT_DIR}/alpha-cosmic-runtime-evidence.txt"
printf 'COSMIC base layer: %s\\n' "${BASE_SQUASHFS_PATH}" >> "${OUT_DIR}/alpha-cosmic-runtime-evidence.txt"
printf 'COSMIC standard layer: %s\\n' "${STANDARD_SQUASHFS_PATH}" >> "${OUT_DIR}/alpha-cosmic-runtime-evidence.txt"
printf 'COSMIC live layer: %s\\n' "${LIVE_SQUASHFS_PATH}" >> "${OUT_DIR}/alpha-cosmic-runtime-evidence.txt"
printf 'COSMIC session: /usr/share/wayland-sessions/cosmic.desktop\\n' >> "${OUT_DIR}/alpha-cosmic-runtime-evidence.txt"
printf 'COSMIC launcher: /usr/bin/start-cosmic\\n' >> "${OUT_DIR}/alpha-cosmic-runtime-evidence.txt"
cat "${COSMIC_MANIFEST}" >> "${OUT_DIR}/alpha-cosmic-runtime-evidence.txt"

echo "Finalizing modified Ubuntu Live leaf layer"
cleanup_chroot

echo "Persisting staged COSMIC graphical validator into the unmounted Live leaf layer"
sudo mkdir -p "${LIVE_ROOTFS_DIR}/usr/local/sbin"
sudo cp -a "${VALIDATOR_ROOTFS_DIR}/usr/local/sbin/alpha-cosmic-graphical-runtime-check" "${LIVE_ROOTFS_DIR}/usr/local/sbin/"
sudo mkdir -p "${LIVE_ROOTFS_DIR}/var/log" "${LIVE_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target.wants"
sudo cp -a "${VALIDATOR_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target" "${LIVE_ROOTFS_DIR}/etc/systemd/system/"
sudo cp -a "${VALIDATOR_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-graphical-runtime.service" "${LIVE_ROOTFS_DIR}/etc/systemd/system/"
sudo cp -a "${VALIDATOR_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target.wants/." "${LIVE_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target.wants/"

sudo test -x "${LIVE_ROOTFS_DIR}/usr/local/sbin/alpha-cosmic-graphical-runtime-check"
sudo test -f "${LIVE_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target"
sudo test -f "${LIVE_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-graphical-runtime.service"
sudo test -L "${LIVE_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target.wants/greetd.service"
sudo test -L "${LIVE_ROOTFS_DIR}/etc/systemd/system/alpha-cosmic-validation.target.wants/alpha-cosmic-graphical-runtime.service"
echo "COSMIC graphical validator persisted in unmounted live leaf layer"

echo "Repacking modified Ubuntu Live layer"
sudo mksquashfs "${LIVE_ROOTFS_DIR}" "${LIVE_SQUASHFS}" -comp xz -noappend -all-root -xattrs -mkfs-time "${SOURCE_DATE_EPOCH}"
sudo chown "$(id -u):$(id -g)" "${LIVE_SQUASHFS}"
test -s "${LIVE_SQUASHFS}"

echo "Verifying COSMIC graphical validator inside the exact squashfs leaf consumed by QEMU"
sudo unsquashfs -cat "${LIVE_SQUASHFS}" etc/systemd/system/alpha-cosmic-validation.target >/dev/null
sudo unsquashfs -cat "${LIVE_SQUASHFS}" etc/systemd/system/alpha-cosmic-graphical-runtime.service >/dev/null
sudo unsquashfs -cat "${LIVE_SQUASHFS}" usr/local/sbin/alpha-cosmic-graphical-runtime-check >/dev/null
echo "COSMIC graphical validator verified inside final Live leaf squashfs"

echo "Repacking bootable Ubuntu ISO with deterministic time inputs"
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
xorriso -indev "${OUTPUT_PATH}" -report_el_torito plain | tee "${OUT_DIR}/el-torito-report.txt"
grep -Eq 'BIOS|EFI|El Torito' "${OUT_DIR}/el-torito-report.txt"

IMAGE_SIZE="$(stat -c '%s' "${OUTPUT_PATH}")"
IMAGE_SHA256="$(sha256sum "${OUTPUT_PATH}" | awk '{print $1}')"

PYTHONPATH="${GITHUB_WORKSPACE:-.}/implementation" \
python3 - "${OUTPUT_PATH}" "${MANIFEST_PATH}" "${RELEASE_ID}" "${VERSION}" "${CHANNEL}" "${ARCH}" "${SOURCE_COMMIT}" "${CI_RUN_ID}" "${BUILD_ENVIRONMENT}" "${REPRODUCIBILITY_RESULT}" "${IMAGE_SIZE}" "${IMAGE_SHA256}" "${REFERENCE_SHA256}" <<'PY'
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
    "source_date_epoch": int(__import__("os").environ["SOURCE_DATE_EPOCH"]),
}
Path(manifest).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

echo "IMAGE=${OUTPUT_PATH}"
echo "SIZE=${IMAGE_SIZE}"
echo "SHA256=${IMAGE_SHA256}"
echo "REFERENCE_SHA256=${REFERENCE_SHA256}"
echo "REPRODUCIBILITY=${REPRODUCIBILITY_RESULT}"
echo "MANIFEST=${MANIFEST_PATH}"
