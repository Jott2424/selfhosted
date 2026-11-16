# Mosquitto

### MQTT message broker (used by Frigate, Home Assistant, etc.)

Ports are published in the 5xxxx range:

| Service | Host port | Container port |
|---|---|---|
| MQTT | `51883` | 1883 |
| MQTT over WebSockets | `59001` | 9001 |

Config, persistence data, and logs live under `/mnt/Vault/Homelab/Portainer/Stacks/Mosquitto/prod/` (`config`, `data`, `log`) on the Truenas box.

## First-time setup

Mosquitto 2.x only listens locally and refuses remote clients without a config file, so create these on the Truenas box before starting the stack.

`config/mosquitto.conf`:

```
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log

listener 1883
listener 9001
protocol websockets

allow_anonymous false
password_file /mosquitto/config/passwd
```

Then create the password file (run once the container is up, and again for each additional user), and restart the container:

```
docker exec -it p_mosquitto mosquitto_passwd -c /mosquitto/config/passwd <user>   # -c creates the file; omit it to add more users
docker restart p_mosquitto
```

Usernames and passwords live only in the `passwd` file in the config volume, so they are not stored in this repo.

## Clients

Point clients at `<host-ip>` port `51883` with the user and password above. For example, in Frigate's web UI set the MQTT host to the Truenas IP and the port to `51883`.
