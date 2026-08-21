# Immich
### Self-hosted photo/video backup and management (Google Photos alternative)

- `p_immich01` — main server (web UI + API), port 50100
- `p_immich-machine-learning` — handles face/object recognition, CLIP search, etc.
- `p_immich-redis` — job queue / cache
- `p_immich-postgres` — dedicated Postgres with the pgvector extension (needed for ML search), separate from the shared instances in [databases](../databases)

Photos and the ML model cache live under `/mnt/Vault/Media/Pictures/Immich` on the Truenas box.
