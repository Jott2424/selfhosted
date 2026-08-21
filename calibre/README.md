# Calibre
### Ebook library management + web reader, for my personal book collection

- `calibre` — the full Calibre server/GUI, accessed via browser (ports 8080/8081)
- `calibre-web` — a lighter web frontend for browsing and reading the same library (port 8083)

Both containers point at the same library and Calibre config, so books added through either one show up in both.
