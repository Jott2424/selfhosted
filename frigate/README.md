# Frigate

### Self-hosted NVR with local AI object detection

Runs with `privileged: true` and a 512 MB `/dev/shm`. Ports are published in the 5xxxx range:

| Service | Host port | Container port |
|---|---|---|
| Web UI (authenticated) | `58971` | 8971 |
| RTSP restream | `58554` | 8554 |
| WebRTC (TCP/UDP) | `58555` | 8555 |

The unauthenticated UI (container port 5000) is left disabled. Config and recordings persist under `/mnt/Vault/Homelab/Portainer/Stacks/Frigate/prod/` (`config` and `storage`) on the Truenas box.

Camera, MQTT, and detector settings live in `config.yml` inside the config volume and are managed through the Frigate web UI, so they are not stored in this repo. Camera streams, RTSP credentials, and the MQTT password stay out of git.
