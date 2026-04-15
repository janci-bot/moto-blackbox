import os
import json
from statistics import mean

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"


def ensure_dirs():
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def process_file(filename):
    speeds = []
    temps = []
    count = 0

    with open(filename, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                speeds.append(data.get("speed", 0))
                temps.append(data.get("temp", 0))
                count += 1
            except Exception:
                continue

    if count == 0:
        return None

    return {
        "records": count,
        "avg_speed": round(mean(speeds), 2),
        "max_speed": max(speeds),
        "avg_temp": round(mean(temps), 2)
    }


def get_output_filename(input_file):
    base = os.path.basename(input_file).replace(".log", ".json")
    return os.path.join(PROCESSED_DIR, base)


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
