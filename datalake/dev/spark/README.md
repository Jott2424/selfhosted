# Apache Spark
### The open source compute we will be using for our datalake project

- `d_spark-master` — cluster master, web UI on port 18080
- `d_spark-worker` — a single worker (2 cores / 2GB), connects to the master over the host network

Both run with `network_mode: host` on the R720xd since they're addressed directly by IP (`192.168.1.3`) rather than through Docker's internal networking.