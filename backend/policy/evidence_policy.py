import json
from pathlib import Path


POLICY_PATH = Path(__file__).parent.parent / "config" / "evidence_policy.json"

DEFAULT_REQUIRED = {
    "machine_events",
    "maintenance_history",
    "manuals",
    "safety_rules",
    "quality_rules",
    "production_schedule",
}


def load_policy():
    if not POLICY_PATH.exists():
        return {
            "restart_recovery": {
                "required": sorted(DEFAULT_REQUIRED),
                "optional": [],
                "description": "Default RestartOS evidence policy.",
            }
        }

    return json.loads(POLICY_PATH.read_text())


def get_required_evidence(policy_name: str = "restart_recovery"):
    policy = load_policy()
    return set(policy.get(policy_name, {}).get("required", DEFAULT_REQUIRED))


def get_optional_evidence(policy_name: str = "restart_recovery"):
    policy = load_policy()
    return set(policy.get(policy_name, {}).get("optional", []))


def normalize_sources(evidence):
    sources = {item.source for item in evidence}

    if "ai4i_machine_events" in sources:
        sources.add("machine_events")

    return sources