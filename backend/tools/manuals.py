import json
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "manuals.json"


def search_manuals(machine: str):
    manuals = json.loads(DATA_PATH.read_text())
    return [manual for manual in manuals if manual["machine"].lower() == machine.lower()]