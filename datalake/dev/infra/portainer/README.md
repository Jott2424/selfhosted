# Portainer stack (dev)
### The version of the dev datalake stack actually deployed through Portainer

Same services as [`datalake/dev/docker-compose.yml`](../../docker-compose.yml) (MinIO + Unity Catalog), just with volumes pointed at the NFS share (`/mnt/nfs/files/...`) instead of a local mount — see the note in the [datalake README](../../../README.md) about the proxmox nfs-kernel-server issue.
