import random
import time
from datetime import datetime, timezone
import redis
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=True  # Redis Cloud requires SSL
)

# List of locations
LOCATIONS = ["Downtown", "Industrial Zone", "Residential Area", "Airport"]

# Initial AQI values
city_aqi_state = {
    "Downtown": 60,
    "Industrial Zone": 120,
    "Residential Area": 40,
    "Airport": 80
}

# AQI categories
AQI_CATEGORIES = [
    (0, 50, "Good", False),
    (51, 100, "Moderate", False),
    (101, 150, "Unhealthy for Sensitive Groups", False),
    (151, 200, "Unhealthy", True),
    (201, 300, "Very Unhealthy", True),
    (301, 500, "Hazardous", True)
]

def map_aqi_to_status_and_alert(aqi_value):
    for lower, upper, status, alert in AQI_CATEGORIES:
        if lower <= aqi_value <= upper:
            return status, alert
    return "Unknown", False

def clamp(value, min_val=0, max_val=500):
    return max(min(value, max_val), min_val)

def unix_ms():
    # Add small jitter to prevent duplicate timestamps
    return int(datetime.now(timezone.utc).timestamp() * 1000) + random.randint(0, 5)

def push_to_timeseries(city, aqi_value):
    key = f"aqi:{city.replace(' ', '_').lower()}"
    timestamp = unix_ms()

    # If the key doesn't exist, create with labels and duplicate policy
    if not r.exists(key):
        r.ts().create(
            key,
            labels={"location": city},
            duplicate_policy="last"  # This allows safe upserts
        )

    # Add the value to time series
    r.ts().add(key, timestamp, aqi_value)
    print(f"[{city}] -> AQI {aqi_value} @ {timestamp}")

def main():
    while True:
        for city in LOCATIONS:
            drift = random.randint(-30, 30)
            new_aqi = clamp(city_aqi_state[city] + drift)
            city_aqi_state[city] = new_aqi
            push_to_timeseries(city, new_aqi)
        time.sleep(10)

if __name__ == "__main__":
    main()