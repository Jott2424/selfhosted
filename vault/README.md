# Vault

### Self-hosted secrets manager (HashiCorp Vault) for my other projects to pull credentials, URLs, etc. from over an HTTP API

- `p_vault` — Vault server (UI + API), port 58200. Single node, file storage backend, persisted under `/mnt/Vault/Homelab/Portainer/Stacks/Vault/prod` on the Truenas box.

Config is passed inline via `VAULT_LOCAL_CONFIG` in the compose file, so no config file needs to exist on the host. The listener is plain HTTP, so keep it on the LAN/Tailscale or put a TLS reverse proxy in front of it.

## First-time setup

Vault starts **sealed and uninitialized**. Do this once:

```sh
docker exec -it p_vault vault operator init -key-shares=5 -key-threshold=3
```

Save the 5 unseal keys and the initial root token somewhere safe (not in this repo). Losing the unseal keys means losing the data. Then unseal (3 different keys):

```sh
docker exec -it p_vault vault operator unseal   # repeat 3x
```

**Vault re-seals every time the container restarts**, so repeat the unseal step after reboots/redeploys.

## Storing and reading secrets

Enable a KV v2 engine and add a secret:

```sh
export VAULT_ADDR=http://<truenas-ip>:58200
export VAULT_TOKEN=<root token>
vault secrets enable -path=secret kv-v2
vault kv put secret/myapp/db username=app password=hunter2 url=postgres://...
```

Read it from any project over the HTTP API:

```sh
curl -H "X-Vault-Token: $VAULT_TOKEN" $VAULT_ADDR/v1/secret/data/myapp/db
# -> {"data": {"data": {"username": "app", "password": "...", "url": "..."}, "metadata": {...}}}
```

Python: `hvac` (`hvac.Client(url=..., token=...).secrets.kv.v2.read_secret_version(path="myapp/db")`).

## Per-project access (don't use the root token in apps)

Create a policy scoped to one path and a token or AppRole for each project:

```sh
vault policy write myapp - <<'POLICY'
path "secret/data/myapp/*" { capabilities = ["read"] }
POLICY
vault token create -policy=myapp
```

Use AppRole (`vault auth enable approle`) for long-lived services, since tokens expire.
