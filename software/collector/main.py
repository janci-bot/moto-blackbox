import os
import json
import time
import random
import math
from datetime import datetime

DATA_DIR = "data/raw"

MIN_SPEED = 5       # km/h
MIN_DISTANCE = 5    # metre
SMOOTH_ALPHA = 0.2


# =========================
# UTILS
# =========================

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def get_filename():
    date_str = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DATA_DIR, f"{date_str}.log")


# =========================
# GEO FUNCTIONS
# =========================

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # meters

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def calculate_heading(lat1, lon1, lat2, lon2):
    d_lon = math.radians(lon2 - lon1)

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - \
        math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)

    heading = math.degrees(math.atan2(x, y))
    return (heading + 360) % 360


def smooth_heading(prev, new, alpha=0.2):
    if prev is None:
        return new

    prev_rad = math.radians(prev)
    new_rad = math.radians(new)

    x = (1 - alpha) * math.cos(prev_rad) + alpha * math.cos(new_rad)
    y = (1 - alpha) * math.sin(prev_rad) + alpha * math.sin(new_rad)

    smoothed = math.degrees(math.atan2(y, x))
    return (smoothed + 360) % 360


# =========================
# COLLECTOR LOGIC
# =========================

last_point = None
last_heading = None


def generate_data():
    global last_point, last_heading

    # simulácia GPS pohybu
    lat = 48.736277 + random.uniform(-0.001, 0.001)
    lon = 19.146191 + random.uniform(-0.001, 0.001)

    speed = round(random.uniform(0, 120), 2)

    heading = None

    if last_point and speed > MIN_SPEED:
        distance = calculate_distance(
            last_point["lat"],
            last_point["lon"],
            lat,
            lon
        )

        if distance > MIN_DISTANCE:
            raw_heading = calculate_heading(
                last_point["lat"],
                last_point["lon"],
                lat,
                lon
            )

            heading = smooth_heading(last_heading, raw_heading, SMOOTH_ALPHA)
            last_heading = heading

    last_point = {"lat": lat, "lon": lon}

    return {
        "timestamp": datetime.now().isoformat(),
        "gps": {"lat": lat, "lon": lon},
        "speed": speed,
        "heading": round(heading, 2) if heading is not None else None,
        "temp": round(random.uniform(15, 35), 2),
        "pressure": round(random.uniform(990, 1025), 2),
        "accel": round(random.uniform(-2, 2), 2)
    }


def write_data(data):
    filename = get_filename()
    with open(filename, "a") as f:
        f.write(json.dumps(data) + "\n")


def main():
    print("Collector started...")
    ensure_data_dir()

    while True:
        data = generate_data()
        write_data(data)

        print(f"Logged: {data}")

        time.sleep(2)


if __name__ == "__main__":
    main()