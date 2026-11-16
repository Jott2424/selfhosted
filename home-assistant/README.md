# Home Assistant

### Home automation platform

Web UI is published on host port `58123` (container port 8123). Runs with `privileged: true` for USB/Bluetooth device access. It no longer uses `network_mode: host`, so LAN auto-discovery (mDNS/SSDP) won't work; add devices by IP instead. Config persists under `/mnt/Vault/Homelab/Portainer/Stacks/HomeAssistant/dev/config` on the Truenas box.
