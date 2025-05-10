import random
import time
import json
from datetime import datetime, timezone
import redis

# Redis Cloud connection (replace with your credentials)
r = redis.Redis(
    host='redis-16499.c284.us-east1-2.gce.redns.redis-cloud.com',
    port=16499,
    password='WcbZdb1D88FovliZTCSPcB2GPJZ9owqD',
    ssl=False  # <--- Must be False since you're using redis://
)


# List of locations
LOCATIONS = ["Downtown", "Industrial Zone", "Residential Area", "Airport"]

# Initial AQI values (realistic starting points)
city_aqi_state = {
    "Downtown": 60,
    "Industrial Zone": 120,
    "Residential Area": 40,
    "Airport": 80
}

# AQI status thresholds
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

# def generate_data_for_city(city):
#     # Drift AQI by ±30
#     last_aqi = city_aqi_state[city]
#     drift = random.randint(-30, 30)
#     new_aqi = clamp(last_aqi + drift)

#     # Update global state
#     city_aqi_state[city] = new_aqi

#     # Transformations
#     status, alert = map_aqi_to_status_and_alert(new_aqi)
#     temp_f = random.uniform(60, 100)
#     temperature_c = round((temp_f - 32) * 5 / 9, 2)
#     timestamp = datetime.utcnow().isoformat() + "Z"

#     return {
#         "location": city,
#         "timestamp": timestamp,
#         "AQI_value": new_aqi,
#         "status": status,
#         "temperature": temperature_c,
#         "alert": alert
#     }

def unix_ms():
    return int(datetime.now(timezone.utc).timestamp() * 1000)

def push_to_timeseries(city, aqi_value):
    key = f"aqi:{city.replace(' ', '_').lower()}"
    timestamp = unix_ms()

    # Check and create key if it doesn't exist
    if not r.exists(key):
        r.ts().create(key, labels={"location": city})

    # Add value to time-series
    r.ts().add(key, timestamp, aqi_value)
    print(f"[{city}] -> AQI {aqi_value} @ {timestamp}")


# def main():
#     while True:
#         for city in LOCATIONS:
#             data_point = generate_data_for_city(city)
#             print(data_point)  # Replace with Redis push later
#         time.sleep(10)  # simulate every 10 seconds (or use 60 for real minute)

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
