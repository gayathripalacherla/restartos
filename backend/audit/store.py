import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "run_history.json"


def _load_runs():
    if not DATA_PATH.exists():
        return []

    try:
        return json.loads(DATA_PATH.read_text())
    except json.JSONDecodeError:
        return []


def _save_runs(runs):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(runs, indent=2) + "\n")


def save_run(incident, result):
    runs = _load_runs()

    run_record = {
        "run_id": f"run_{uuid4().hex[:8]}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "incident": incident.model_dump(),
        "brain_parse": result.get("brain_parse"),
        "decision": result["decision"],
        "verification": result["verification"],
        "decision_contract": result.get("decision_contract"),
        "timeline": result["timeline"],
        "trace": result.get("trace", []),
        "artifact_keys": sorted(result.get("artifacts", {}).keys()),
    }

    runs.insert(0, run_record)
    _save_runs(runs)
    return run_record


def list_runs():
    return _load_runs()


def get_run(run_id):
    for run in _load_runs():
        if run["run_id"] == run_id:
            return run
    return None