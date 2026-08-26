variable "proxmox_api_token" {
  description = "Proxmox API token, format: user@realm!tokenid=uuid"
  type        = string
  sensitive   = true
}

variable "target_node" {
  description = "Proxmox node name to deploy on"
  type        = string
  default     = "r630"
}

variable "template_vm_id" {
  description = "VM ID of the cloud-init template to clone"
  type        = number
}

variable "storage_pool" {
  description = "Proxmox storage pool for VM disk and cloud-init drive"
  type        = string
  default     = "datalake"
}

variable "network_bridge" {
  description = "Proxmox network bridge to attach the VM to"
  type        = string
  default     = "vmbr0"
}

variable "ssh_public_key" {
  description = "SSH public key to inject via cloud-init"
  type        = string
}

variable "vms" {
  description = "Map of VMs to create, keyed by a short identifier"
  type = map(object({
    name       = string
    cpu_cores  = number
    memory     = number # MB
    disk_size  = number # GB
    ip_address = string # CIDR, e.g. "192.168.1.51/24", or "dhcp"
  }))
}

variable "vm_gateway" {
  description = "Gateway IP, required for VMs with a static ip_address"
  type        = string
  default     = "192.168.1.1"
}
