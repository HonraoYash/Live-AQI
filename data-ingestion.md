The data_ingest.py script simulates real-time Air Quality Index data and inserts it into the Redis datastore.

Using the python random library, I generated the AQI values.

For each of 4 locations:
- `"Downtown"`
- `"Industrial Zone"`
- `"Residential Area"`
- `"Airport"`

The script generates the following fields:
- `AQI_value` – a realistic air quality reading (int: 0–500)
- `timestamp` – the current UTC time in milliseconds
- `status` – a human-readable category (e.g., "Good", "Unhealthy")
- `temperature` – simulated ambient temperature in °C
- `alert` – boolean flag indicating if AQI is in a dangerous zone

### 2. **Applied Transformations**
- Applies a small ±30 drift to simulate gradual change in AQI
- Maps AQI to its category + alert level (e.g., AQI 205 → `"Very Unhealthy", alert=True`)
- Converts Fahrenheit to Celsius for temperature

### 3. **Store in RedisTimeSeries**
- Creates a time-series key per location (e.g., `aqi:downtown`)
- Attaches a label (`location="Downtown"`) for Grafana filtering
- Adds a **2-day retention policy** so old data is automatically deleted
- Uses a **duplicate_policy** of `"last"` to avoid timestamp conflicts

---

## Environment Variables Used

All Redis connection settings are stored securely using environment variables:
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_PASSWORD`

These are loaded at runtime and injected in production (via Railway or `.env` locally).

---

## Data Ingestion Frequency

- The script runs continuously
- Every **10 seconds**, new data is pushed for all 4 locations

---

## Example Output (Console)

[Downtown] -> AQI 93 @ 1747130034532

[Industrial Zone] -> AQI 162 @ 1747130034754

[Residential Area] -> AQI 49 @ 1747130034970

[Airport] -> AQI 75 @ 1747130035191