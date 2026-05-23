"""Generate test ZIP archive containing multiple CSV files with random numeric data."""
import csv
import io
import os
import random
import zipfile

random.seed(42)

FILES = {
    "sensor_temperature.csv": {"mean": 25.0, "std": 3.5, "rows": 200},
    "sensor_pressure.csv":    {"mean": 1013.0, "std": 12.0, "rows": 150},
    "sensor_humidity.csv":    {"mean": 60.0, "std": 8.0, "rows": 180},
    "motor_vibration.csv":    {"mean": 0.5, "std": 0.15, "rows": 250},
    "power_consumption.csv":  {"mean": 220.0, "std": 18.5, "rows": 300},
}

COLUMNS = ["timestamp", "value_a", "value_b", "value_c"]


def generate_csv(mean: float, std: float, rows: int) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(COLUMNS)
    for i in range(rows):
        ts = f"2026-01-01 {i // 3600:02d}:{(i % 3600) // 60:02d}:{i % 60:02d}"
        va = round(random.gauss(mean, std), 6)
        vb = round(random.gauss(mean * 1.1, std * 0.8), 6)
        vc = round(random.gauss(mean * 0.9, std * 1.2), 6)
        writer.writerow([ts, va, vb, vc])
    return buf.getvalue()


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(out_dir, "test_data.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, params in FILES.items():
            csv_content = generate_csv(params["mean"], params["std"], params["rows"])
            zf.writestr(filename, csv_content)
            print(f"  Added {filename} ({params['rows']} rows, expected std ≈ {params['std']})")

    size_kb = os.path.getsize(zip_path) / 1024
    print(f"\n[OK] Created {zip_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
