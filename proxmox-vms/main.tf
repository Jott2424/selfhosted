terraform {
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "0.66.0"  # check the latest on the Terraform Registry
    }
  }
}

provider "proxmox" {
  endpoint  = "https://192.168.1.225:8006/api2/json"
  api_token = var.proxmox_api_token
  insecure  = true
}

resource "proxmox_virtual_environment_vm" "vm" {
  for_each = var.vms

  name      = each.value.name
  node_name = var.target_node

  started = false
  on_boot = false

  agent {
    enabled = false
  }

  clone {
    vm_id = var.template_vm_id
    full  = true
  }

  cpu {
    cores = each.value.cpu_cores
    type  = "host"
  }

  memory {
    dedicated = each.value.memory
  }

  disk {
    datastore_id = var.storage_pool
    interface    = "scsi0"
    size         = each.value.disk_size
  }

  network_device {
    bridge = var.network_bridge
  }

  initialization {
    datastore_id = var.storage_pool
    interface    = "ide2"

    ip_config {
      ipv4 {
        address = each.value.ip_address
        gateway = each.value.ip_address == "dhcp" ? null : var.vm_gateway
      }
    }

    user_account {
      username = " "
      keys     = [var.ssh_public_key]
    }
  }

  operating_system {
    type = "l26"
  }

  vga {
    type   = "serial0"
    memory = 16
  }
}

output "vm_ips" {
  description = "IP addresses reported by the QEMU guest agent, keyed by VM"
  value       = { for k, v in proxmox_virtual_environment_vm.vm : k => v.ipv4_addresses }
}
