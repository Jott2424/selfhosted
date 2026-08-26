# Tailscale

### Subnet router so other Tailscale devices can reach the homelab LAN without installing Tailscale on every box

Runs with `network_mode: host`, `NET_ADMIN`/`NET_RAW` capabilities, and `/dev/net/tun` passed through, all required for it to route traffic. State persists under `/mnt/Vault/Homelab/Portainer/Stacks/Tailscale/prod/data` on the Truenas box.

`TS_AUTHKEY` must be set to a real auth key generated from the [Tailscale admin console](https://login.tailscale.com/admin/settings/keys) before deploying — never commit a real key here.
