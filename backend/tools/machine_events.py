import json
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "machine_events.json"
AI4I_PATH = Path(__file__).parent.parent / "data" / "ai4i_machine_events.json"


def load_json(path):
    if not path.exists():
        return []
    return json.loads(path.read_text())


def get_machine_events(line: str):
    events = load_json(DATA_PATH)

    if line.lower() == "ai4i demo line":
        events += load_json(AI4I_PATH)

    return [event for event in events if event["line"].lower() == line.lower()]
