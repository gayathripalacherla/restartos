import json
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "production_schedule.json"


def get_production_schedule(line: str):
    schedules = json.loads(DATA_PATH.read_text())
    return [schedule for schedule in schedules if schedule["line"].lower() == line.lower()]