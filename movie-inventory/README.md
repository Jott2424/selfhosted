# Movie Inventory

### My own self-built app for cataloguing my movie & show collection

Tracks the collection with metadata/poster art pulled from TMDb, uses Claude to OCR case photos when adding titles, and cross-references the Plex library. Browses the Truenas media shares read-only for reference. Connects to a dedicated database on the shared `p_postgres01` instance from [databases](../databases). Runs on port 55000.
