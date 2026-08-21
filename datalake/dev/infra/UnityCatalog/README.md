# Unity Catalog
### Data/model catalog for the datalake — tracks schemas, tables, and model versions on top of MinIO storage

- `server/` — the catalog server itself
  - `conf/` — server config (auth, S3/storage-root settings, logging) — mostly left at defaults/disabled for now
  - `db/` — the server's embedded H2 database (metadata only, not the actual data)
- `ui/` — optional web UI for browsing the catalog; see its [README](ui/README.md) for the custom build steps (the upstream image needs a CRLF→LF fix before it'll build cleanly)
