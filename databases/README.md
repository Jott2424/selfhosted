# databases
### Frequently, i use postgres, mysql, or some other database to store data for my projects. This includes a docker-compose.yml for deploying a few general purpose databases that can be used by any of my other microservices or projects

### I will number my databases because sometimes i will spin up a dedicated instance specifically to be used by one project or service, in which case i want to be able to easily refer to them by name and number

### Current instances
- `p_postgres01` (host port 17501) — general purpose, shared by other stacks (e.g. [envelopes](../envelopes))
- `p_postgres02` (host port 17502) — dedicated to analytics work

Note: [immich](../immich) runs its own dedicated Postgres container rather than using an instance from here, since it needs a specific pgvector-enabled image.