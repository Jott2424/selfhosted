# SeaweedFS

### Self-hosted S3-compatible object store, replacing MinIO now that it's no longer receiving patches

- `p_seaweedfs` — single container running the master, volume server, filer and S3 gateway together (`weed server -filer -s3`). Fine for one node; split them into separate services if this ever grows to a cluster.

| Host port | What | Container port |
|---|---|---|
| 58333 | S3 API | 8333 |
| 58888 | Filer UI / HTTP file API | 8888 |
| 59333 | Master UI (cluster status, volumes) | 9333 |

The volume server port (8080) isn't published, since S3 clients only talk to the gateway.

## First-time setup

1. Pick a **local disk** path for the data and create it on the host. Don't put it on NFS: SeaweedFS's volume and filer stores want local-disk semantics and performance, which is the same NFS issue noted in [datalake](../datalake). Update the two volume paths in [docker-compose.yml](docker-compose.yml) if you don't use `/mnt/seaweedfs/prod`.
2. Create the S3 credentials file from the example, outside the repo, at the path the compose file mounts:

   ```sh
   cp s3.json.example /mnt/seaweedfs/prod/s3.json
   # edit it and set a real accessKey / secretKey
   ```

   Generate keys with something like `openssl rand -hex 16` (access key) and `openssl rand -base64 32` (secret key). Store them in [Vault](../vault) rather than in this repo.
3. Deploy the stack, then check `http://<host>:59333` to see the master and volume server up.

`s3.json` can hold several identities. Give each project its own with only the `actions` it needs (`Read`, `Write`, `List`, ...) instead of sharing the admin key. The server reads the file at startup, so restart the container after editing it.

## Using it

Create a bucket and use it with any S3 client:

```sh
export AWS_ACCESS_KEY_ID=<accessKey>
export AWS_SECRET_ACCESS_KEY=<secretKey>
aws --endpoint-url http://<host>:58333 s3 mb s3://datalake
aws --endpoint-url http://<host>:58333 s3 cp file.parquet s3://datalake/
```

For Spark (S3A), point it at the same endpoint and use path-style access:

```
spark.hadoop.fs.s3a.endpoint=http://<host>:58333
spark.hadoop.fs.s3a.path.style.access=true
spark.hadoop.fs.s3a.access.key=<accessKey>
spark.hadoop.fs.s3a.secret.key=<secretKey>
```

The listener is plain HTTP, so keep it on the LAN/Tailscale or behind a TLS reverse proxy.

## Migrating off MinIO

SeaweedFS doesn't read MinIO's on-disk format, so data has to be copied over the S3 API, e.g. `rclone sync minio:bucket seaweed:bucket` with an rclone remote for each. After that, change the endpoint and credentials in Spark and [Unity Catalog](../datalake/dev/infra/UnityCatalog) and retire `p_minio01`.
