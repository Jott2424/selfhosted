# proxmox-vms

Terraform provisioning for VMs on the Dell R630, plus Python scripts to
configure them once they're up. Currently manages two VMs:

| VM | Role |
|---|---|
| `postgres` | Postgres server, open to the LAN |
| `pokemon-simulations` | Python (numpy/pandas/psycopg2) environment for running Pokémon battle simulations and writing results to `postgres` |

## How it fits together

1. **A cloud-init template** on the R630 (built once via `scripts/create-cloud-init-template.sh`) is the base image every VM clones from.
2. **Terraform** (`main.tf` / `variables.tf`) clones that template into right-sized VMs — CPU, memory, disk, and static IP all come from a `vms` map in `terraform.tfvars`, so resizing a VM is a one-line change and a `terraform apply`.
3. **Python scripts** (`scripts/`) handle everything Terraform doesn't — installing Postgres, setting up the simulation venv — by SSHing into the VM once it's running. They work identically from Windows, Mac, or Linux.

## Setup

Requires a Proxmox host reachable at the `endpoint` in `main.tf`, with a
cloud-init-enabled template already created (see
`scripts/create-cloud-init-template.sh` if you need to build one).

```bash
cp terraform.tfvars.example terraform.tfvars
# fill in your API token, template VM ID, SSH key, and per-VM sizing

terraform init
terraform plan
terraform apply
```

`terraform.tfvars` holds real secrets (API token, SSH key) and is
gitignored — never commit it.

## Configuring a VM after it's created

Set your SSH private key path once:

```bash
export PROXMOX_VMS_SSH_KEY=~/.ssh/your_key   # Mac/Linux
$env:PROXMOX_VMS_SSH_KEY = "C:\path\to\your_key"   # Windows PowerShell
```

Then run either script from `scripts/`:

```bash
python3 scripts/deploy.py postgres              # just one VM
python3 scripts/deploy.py all                   # both VMs
python3 scripts/redeploy.py                     # terraform apply, then configure both
```

`deploy.py` waits for SSH to come up before doing anything, so it's safe
to run right after starting a VM. Both scripts are idempotent — safe to
re-run any time.

## Notes

- VMs are created powered off (`started = false`) and don't start on host
  boot (`on_boot = false`) — start them manually (`qm start <vmid>` on the
  Proxmox host, or via the web UI) when you actually need them.
- The QEMU guest agent is intentionally disabled (`agent { enabled = false }`)
  since it's not installed in the template — leaving it enabled causes
  `terraform plan`/`apply` to hang for the provider's full 15-minute agent
  timeout during refresh.
