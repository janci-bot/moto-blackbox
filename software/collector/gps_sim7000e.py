import serial


def nmea_to_decimal(coord, direction):
    if not coord:
        return None

    # rozdelenie: DDMM.MMMM
    degrees = int(float(coord) / 100)
    minutes = float(coord) - degrees * 100
    decimal = degrees + minutes / 60

    if direction in ['S', 'W']:
        decimal *= -1

    return decimal


def parse_rmc(line):
    parts = line.split(',')

    if len(parts) < 12:
        return None

    status = parts[2]
    if status != 'A':
        return None

    lat = nmea_to_decimal(parts[3], parts[4])
    lon = nmea_to_decimal(parts[5], parts[6])
    speed = float(parts[7]) * 1.852  # knots → km/h
    heading = float(parts[8]) if parts[8] else None

    return {
        "lat": lat,
        "lon": lon,
        "speed": round(speed, 2),
        "heading": heading
    }


def read_gps(port="/dev/ttyUSB1"):
    ser = serial.Serial(port, 115200, timeout=1)

    while True:
        line = ser.readline().decode(errors='ignore').strip()

        if line.startswith("$GNRMC") or line.startswith("$GPRMC"):
            data = parse_rmc(line)
            if data:
                return data