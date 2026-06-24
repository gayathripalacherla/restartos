import json
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "quality_rules.json"


def check_quality_rules(product: str):
    rules = json.loads(DATA_PATH.read_text())
    return [rule for rule in rules if rule["product"].lower() == product.lower()]