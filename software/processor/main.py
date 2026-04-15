import os
import json
import math
from statistics import mean

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"


# =========================
# UTILS
# =========================

def ensure_dirs():
    os.makedirs(PROCESSED_DIR, exist_ok=True)


# =========================
# HEADING CALCULATION
# =========================

def average_heading(headings):
    # odstráni None hodnoty
    headings = [h for h in headings if h is not None]

    if not headings:
        return None

    x = sum(math.cos(math.radians(h)) for h in headings)
    y = sum(math.sin(math.radians(h)) for h in headings)

    avg = math.degrees(math.atan2(y, x))
    return (avg + 360) % 360


# =========================
# PROCESSING
# =========================

def process_file(filename):
    speeds = []
    temps = []
    headings = []
    count = 0

    with open(filename, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())

                speeds.append(data.get("speed", 0))
                temps.append(data.get("temp", 0))
                headings.append(data.get("heading"))

                count += 1

            except Exception:
                continue

    if count == 0:
        return None

    avg_heading = average_heading(headings)

    return {
        "records": count,
        "avg_speed": round(mean(speeds), 2),
        "max_speed": max(speeds),
        "avg_temp": round(mean(temps), 2),
        "avg_heading": round(avg_heading, 2) if avg_heading is not None else None
    }


def get_output_filename(input_file):
    base = os.path.basename(input_file).replace(".log", ".json")
    return os.path.join(PROCESSED_DIR, base)


# =========================
# MAIN
# =========================

def main():
    print("Processor started...")
    ensure_dirs()

    for file in os.listdir(RAW_DIR):
        if not file.endswith(".log"):
            continue

        input_path = os.path.join(RAW_DIR, file)
        output_path = get_output_filename(input_path)

        result = process_file(input_path)

        if result:
            with open(output_path, "w") as f:
                json.dump(result, f, indent=2)

            print(f"Processed: {file} → {output_path}")


if __name__ == "__main__":
    main()