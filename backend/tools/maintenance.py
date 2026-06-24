import json
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "maintenance_history.json"


def get_maintenance_history(asset: str):
    records = json.loads(DATA_PATH.read_text())
    return [record for record in records if record["asset"].lower() == asset.lower()]