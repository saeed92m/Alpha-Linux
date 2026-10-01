#!/usr/bin/env bash
set -euo pipefail

APP="Alpha Linux Installer"
TARGET=/target
LOG=/var/log/alpha-installer.log
mkdir -p /var/log
exec > >(tee -a "$LOG") 2>&1

fail() {
  echo "ERROR: $*" >&2
  zenity --error --title="$APP" --text="$*" 2>/dev/null || true
  exit 1
}

[ "$(id -u)" -eq 0 ] || fail "Run the installer as administrator."
[ -d /sys/firmware/efi ] || fail "This prototype installer requires UEFI firmware."
for t in lsblk sgdisk partprobe mkfs.vfat mkfs.ext4 mount umount rsync grub-install grub-mkconfig blkid findmnt zenity; do
  command -v "$t" >/dev/null || fail "Missing installer tool: $t"
done

DISK_ROWS="$(lsblk -dnpo NAME,TYPE | awk '$2=="disk"{print $1}' | while read -r d; do
  [ -b "$d" ] || continue
  [ "$(lsblk -dnbo SIZE "$d")" -ge 8589934592 ] || continue
  model="$(lsblk -dn -o MODEL "$d" | sed 's/[[:space:]]*$//')"
  [ -n "$model" ] || model="unknown model"
  size="$(lsblk -dnbo SIZE "$d" | numfmt --to=iec --suffix=B)"
  printf '%s\t%s\n' "$d" "$d — $model — $size"
done)"
[ -n "$DISK_ROWS" ] || fail "No suitable disk of at least 8 GiB was found."

TARGET_DISK="$(printf '%s\n' "$DISK_ROWS" | zenity --list --radiolist --width=900 --height=500   --title="$APP"   --text="Select an EMPTY dedicated disk. This prototype will erase the selected disk."   --column="" --column="Disk" --hide-header --print-column=2 2>/dev/null || true)"
[ -n "$TARGET_DISK" ] || fail "Installation cancelled."

CHILDREN="$(lsblk -lnpo NAME "$TARGET_DISK" | tail -n +2)"
[ -z "$CHILDREN" ] || fail "Selected disk already has partitions. Choose an empty dedicated disk."

if lsblk -lnpo NAME,FSTYPE,LABEL "$TARGET_DISK" | grep -Eiq 'ntfs|BitLocker|Windows|Microsoft|Recovery'; then
  fail "Windows/encryption/recovery indicators were detected; the prototype refuses this disk."
fi

if ! zenity --warning --title="$APP — DESTRUCTIVE OPERATION"   --text="EVERYTHING on $TARGET_DISK will be erased.\n\nAlpha-only installation requires a dedicated empty disk.\n\nContinue?"   --ok-label="ERASE AND INSTALL" --cancel-label="Cancel"; then
  fail "Installation cancelled before disk mutation."
fi

cleanup() {
  set +e
  umount -R "$TARGET" 2>/dev/null || true
}
trap cleanup EXIT

EFI_PART="$TARGET_DISK"1
ROOT_PART="$TARGET_DISK"2
if [[ "$TARGET_DISK" =~ nvme|mmcblk ]]; then
  EFI_PART="$TARGET_DISK"p1
  ROOT_PART="$TARGET_DISK"p2
fi

echo "Partitioning $TARGET_DISK"
sgdisk --zap-all "$TARGET_DISK"
sgdisk --clear   --new=1:2048:+512M --typecode=1:ef00 --change-name=1:Alpha-EFI   --new=2:0:0 --typecode=2:8300 --change-name=2:Alpha-Root   "$TARGET_DISK"
sgdisk --verify "$TARGET_DISK"
partprobe "$TARGET_DISK" || true
sleep 2
[ -b "$EFI_PART" ] || fail "EFI partition was not created."
[ -b "$ROOT_PART" ] || fail "Root partition was not created."

mkfs.vfat -F32 -n ALPHA-EFI "$EFI_PART"
mkfs.ext4 -F -L ALPHA-ROOT "$ROOT_PART"
mkdir -p "$TARGET/boot/efi"
mount "$ROOT_PART" "$TARGET"
mount "$EFI_PART" "$TARGET/boot/efi"

echo "Staging Live filesystem into the installed system"
rsync -aHAX --numeric-ids   --exclude=/dev/* --exclude=/proc/* --exclude=/sys/* --exclude=/run/*   --exclude=/tmp/* --exclude=/mnt/* --exclude=/media/* --exclude=/cdrom/*   --exclude=/target/* --exclude=/lost+found / "$TARGET/"

mkdir -p "$TARGET/dev" "$TARGET/proc" "$TARGET/sys" "$TARGET/run"
mount --bind /dev "$TARGET/dev"
mount --bind /dev/pts "$TARGET/dev/pts" 2>/dev/null || true
mount -t proc proc "$TARGET/proc"
mount -t sysfs sysfs "$TARGET/sys"
mount -t tmpfs tmpfs "$TARGET/run"

ROOT_UUID="$(blkid -s UUID -o value "$ROOT_PART")"
EFI_UUID="$(blkid -s UUID -o value "$EFI_PART")"
cat > "$TARGET/etc/fstab" <<EOF
UUID=$ROOT_UUID / ext4 defaults,errors=remount-ro 0 1
UUID=$EFI_UUID /boot/efi vfat umask=0077 0 1
EOF

cp -L /etc/resolv.conf "$TARGET/etc/resolv.conf" 2>/dev/null || true

echo "Installing UEFI bootloader"
chroot "$TARGET" /bin/bash -euxo pipefail <<'CHROOT'
if ! command -v grub-install >/dev/null 2>&1; then
  apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y grub-efi-amd64 efibootmgr
fi
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=AlphaLinux --recheck
grub-mkconfig -o /boot/grub/grub.cfg
touch /etc/alpha-linux-installed
rm -f /etc/alpha-live-installer-installed
CHROOT

[ -s "$TARGET/boot/grub/grub.cfg" ] || fail "GRUB configuration verification failed."
[ -d "$TARGET/boot/efi/EFI/AlphaLinux" ] || fail "Alpha UEFI bootloader verification failed."
[ -f "$TARGET/etc/alpha-linux-installed" ] || fail "Post-install health marker verification failed."

sync
echo "INSTALL_RESULT=PASS"
echo "ROOT_UUID=$ROOT_UUID"
echo "EFI_UUID=$EFI_UUID"
zenity --info --title="$APP — Installation complete"   --text="Alpha Linux installation completed. Remove the Live USB and reboot.\n\nThis prototype supports UEFI + Alpha-only installation on a dedicated empty disk." 2>/dev/null || true
