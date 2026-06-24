import csv
import json
from pathlib import Path


SOURCE = Path("data/external/ai4i/ai4i2020.csv")
OUTPUT = Path("data/ai4i_machine_events.json")


def clean_row(row):
    return {
        (key or "").replace("\ufeff", "").strip(): (value or "").strip()
        for key, value in row.items()
    }


def detect_failure_modes(row):
    modes = []

    if row["TWF"] == "1":
        modes.append("tool wear failure")
    if row["HDF"] == "1":
        modes.append("heat dissipation failure")
    if row["PWF"] == "1":
        modes.append("power failure")
    if row["OSF"] == "1":
        modes.append("overstrain failure")
    if row["RNF"] == "1":
        modes.append("random failure")

    return modes


def make_event(row):
    uid = int(row["UDI"])
    machine_type = row["Type"]
    machine_id = row["Product ID"]
    failure_modes = detect_failure_modes(row)

    if row["Machine failure"] == "1":
        level = "FAULT"
        message = (
            f"AI4I predictive maintenance failure on asset {machine_id}. "
            f"Failure modes: {', '.join(failure_modes) or 'unspecified'}. "
            f"Air temp {row['Air temperature [K]']}K, process temp {row['Process temperature [K]']}K, "
            f"rotational speed {row['Rotational speed [rpm]']} rpm, torque {row['Torque [Nm]']} Nm, "
            f"tool wear {row['Tool wear [min]']} min."
        )
    else:
        level = "CONDITION"
        message = (
            f"AI4I normal operating sample for asset {machine_id}. "
            f"Air temp {row['Air temperature [K]']}K, process temp {row['Process temperature [K]']}K, "
            f"rotational speed {row['Rotational speed [rpm]']} rpm, torque {row['Torque [Nm]']} Nm, "
            f"tool wear {row['Tool wear [min]']} min."
        )

    return {
        "timestamp": f"AI4I-{uid:05d}",
        "line": "AI4I Demo Line",
        "machine": f"AI4I Machine Type {machine_type}",
        "level": level,
        "message": message,
        "source_dataset": "UCI AI4I 2020 Predictive Maintenance Dataset",
        "product_id": machine_id,
        "machine_failure": int(row["Machine failure"]),
        "failure_modes": failure_modes,
    }


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing source dataset: {SOURCE}")

    events = []

    with SOURCE.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for raw_row in reader:
            row = clean_row(raw_row)
            event = make_event(row)

            if event["machine_failure"] == 1:
                events.append(event)

    OUTPUT.write_text(json.dumps(events, indent=2))
    print(f"Wrote {len(events)} AI4I failure events to {OUTPUT}")


if __name__ == "__main__":
    main()