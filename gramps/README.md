# Gramps

### Self-hosted genealogy / family tree software (Gramps Web)

- `p_grampsweb` — main web app (UI + API), port 50380
- `p_grampsweb_celery` — background worker for reports/exports, shares the grampsweb image and config
- `p_grampsweb_redis` — Celery broker/result backend + rate-limit storage (Valkey), port 50381

Uses its own SQLite-based Gramps database and search index rather than the shared Postgres in [databases](../databases). Config, search index, thumbnails, and media all persist under `/mnt/Vault/Homelab/Portainer/Stacks/Gramps/prod` on the Truenas box.
