# Datalake

## This is my repo for all things running on my dell poweredge r720xd, as of writting this is only used for hosting my own cloud, which i use for data projects (datalake, data warehouse, cloud compute, etc...)

#### Note, i am having trouble getting nfs-kernel-server to run on proxmox so for now i am routing all of my files to the truenas server nfs share, but i will migrate this back over to the machine all of this is running on eventually.

## Structure
- `dev/` — [MinIO](dev/infra/Minio), [Unity Catalog](dev/infra/UnityCatalog), [Spark](dev/spark), and a code-server, all still being iterated on
- `dev/infra/portainer/` — the copy of the dev stack actually deployed through Portainer; volumes point at the NFS share instead of a local mount, per the note above
- `prod/` — MinIO only so far, promoted here once dev is stable