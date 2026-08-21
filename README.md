# selfhosted
### A repo for all of my self hosted projects

## Stacks
| Folder | What it runs |
|---|---|
| [calibre](calibre) | Calibre + Calibre-Web — ebook library and web reader |
| [databases](databases) | Shared Postgres instances used by other stacks below |
| [datalake](datalake) | Data lake / warehouse infra (MinIO, Unity Catalog, Spark) on the R720xd |
| [envelopes](envelopes) | My own envelope-budgeting app |
| [immich](immich) | Self-hosted photo/video backup |
| [plex](plex) | Plex media server |
| [project_management](project_management) | Kanboard, for personal project tracking |

Each folder has its own `docker-compose.yml` and is deployed as an independent stack (mostly through Portainer on the boxes below).

### As of November 2025, my homelab includes
- Custom Built Truenas Box
    - Used for NAS, Plex, Immich, and a variety of other selfhosted applications, including my own development projects.
    - Hardware
        - Ryzen 5 5600G
        - 32GB Ram
        - 4 Storage pools totaling 24TB
        - GTX 1070

- Dell R720xd
    - Runs proxmox to host VMs for spark, ML development & training, minio, etc.
    - Hardware
        - (2) Xeon E5-2697 V2 (12C/24T each)
        - (24) 32 GB DDR3 Ram (768 total)
        - (2) 480 GB SSD (boot - raid 1 - 120GB usable)
        - (8) 1 TB HDD (vm storage space - raid 10 - 4TB usable)

- Dell R630
    - Hardware
        - (2) Xeon E5-2697A V4 (16C/32T each)
        - (24) 32 GB DDR4 Ram (768 total)
        - (2) 480 GB SSD (boot - raid 1 - 120GB usable)
        - (8) 1 TB HDD (vm storage space - raid 10 - 4TB usable)

- Spare Linux PC
    - Runs Omarchy (for now) for daily driving a linux desktop experience
    1. Ryzen 5 5600G
    2. 32GB Ram