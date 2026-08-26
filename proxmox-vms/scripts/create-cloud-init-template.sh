#!/usr/bin/env bash
# Run this ON THE PROXMOX HOST (r630) via SSH or the web shell, as root.
# Builds a cloud-init-enabled VM template that Terraform can clone.
#
# Usage:
#   VMID=9000 STORAGE=local-lvm ./create-cloud-init-template.sh
#
# Re-run with a different VMID to build another template (e.g. Debian vs Ubuntu)
# without touching an existing one.

set -euo pipefail

VMID="${VMID:-9000}"
STORAGE="${STORAGE:-local-lvm}"
BRIDGE="${BRIDGE:-vmbr0}"
VM_NAME="${VM_NAME:-ubuntu-cloudinit-template}"
CORES="${CORES:-2}"
MEMORY="${MEMORY:-2048}"

# Ubuntu 24.04 LTS cloud image. Swap the URL for Debian 12, etc. if you prefer:
#   https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-amd64.qcow2
IMAGE_URL="${IMAGE_URL:-https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img}"
IMAGE_FILE="/var/lib/vz/template/iso/$(basename "$IMAGE_URL")"

if qm status "$VMID" &>/dev/null; then
  echo "VMID $VMID already exists. Choose a different VMID or remove it first (qm destroy $VMID)." >&2
  exit 1
fi

echo "==> Downloading cloud image"
mkdir -p "$(dirname "$IMAGE_FILE")"
if [ ! -f "$IMAGE_FILE" ]; then
  curl -fL -o "$IMAGE_FILE" "$IMAGE_URL"
else
  echo "Image already downloaded, skipping."
fi

echo "==> Creating base VM $VMID"
qm create "$VMID" \
  --name "$VM_NAME" \
  --memory "$MEMORY" \
  --cores "$CORES" \
  --cpu host \
  --net0 "virtio,bridge=$BRIDGE" \
  --ostype l26

echo "==> Importing disk into $STORAGE"
qm importdisk "$VMID" "$IMAGE_FILE" "$STORAGE"

echo "==> Attaching disk, cloud-init drive, boot/console config"
qm set "$VMID" --scsihw virtio-scsi-pci --scsi0 "$STORAGE:vm-$VMID-disk-0"
qm set "$VMID" --ide2 "$STORAGE:cloudinit"
qm set "$VMID" --boot order=scsi0
qm set "$VMID" --serial0 socket --vga serial0
qm set "$VMID" --agent enabled=1

echo "==> Converting to template"
qm template "$VMID"

echo
echo "Template $VMID ($VM_NAME) ready. Set template_vm_id = $VMID in terraform.tfvars."
