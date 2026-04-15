import os
import json
import folium

RAW_DIR = "data/raw"
OUTPUT_FILE = "data/exports/map.html"


def load_points():
    points = []

    for file in sorted(os.listdir(RAW_DIR)):
        if not file.endswith(".log"):
            continue

        with open(os.path.join(RAW_DIR, file), "r") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    lat = data["gps"]["lat"]
                    lon = data["gps"]["lon"]
                    points.append((lat, lon))
                except:
                    continue

    return points


def create_map(points):
    if not points:
        print("No data!")
        return

    # stred mapy = prvý bod
    m = folium.Map(location=points[0], zoom_start=13)

    # vykreslenie trasy
    folium.PolyLine(points, color="blue", weight=3).add_to(m)

    # začiatok
    folium.Marker(points[0], tooltip="Start").add_to(m)

    # koniec
    folium.Marker(points[-1], tooltip="End").add_to(m)

    # uloženie
    os.makedirs("data/exports", exist_ok=True)
    m.save(OUTPUT_FILE)

    print(f"Map saved to {OUTPUT_FILE}")


def main():
    points = load_points()
    create_map(points)


if __name__ == "__main__":
    main()