
I have chosen Redis as the database.

Because on exploring, I found out that Redis is more suitable for time-series like data. And I wanted to cover the bonus point of showing trends over real-time.

## Setup Script

The Redis key creation and ingestion logic is handled directly in [`data_ingest.py`](./data_ingest.py). For each location, a key is created with:

- A unique name like `aqi:downtown`
- A label: `location=Downtown`
- A duplicate policy (`last`) to avoid timestamp collisions
- A 2-day retention policy (`retention_msecs=172800000`)

If the key does not exist, it is created dynamically when the script runs.

## Credentials Management

Connection details are handled securely via environment variables:
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_PASSWORD`

These are injected by the deployment platform (Railway) and excluded from version control using `.gitignore`.
