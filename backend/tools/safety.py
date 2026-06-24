import json
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "safety_rules.json"


def check_safety_requirements(machine: str):
    rules = json.loads(DATA_PATH.read_text())
    return [rule for rule in rules if rule["machine"].lower() == machine.lower()]