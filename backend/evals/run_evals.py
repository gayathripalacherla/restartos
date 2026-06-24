from agents.llm_brain_agent import parse_freeform_scenario
from models.schemas import IncidentRequest
from orchestrator import run_incident_workflow


CASES = [
    {
        "name": "verified_filler_restart",
        "incident": IncidentRequest(
            line="Line 3",
            machine="Filler",
            issue="Keeps faulting after 20 minutes",
            deadline="3:00 PM",
            product="Bottled Tea",
            operator_note="Bottles backed up near capper",
        ),
        "expected_recommendation": "restart_at_reduced_speed",
        "expected_verdict": "PASS",
        "expected_blocked": False,
    },
    {
        "name": "labeler_missing_asset_evidence",
        "incident": IncidentRequest(
            line="Line 2",
            machine="Labeler",
            issue="Labels keep drifting out of alignment",
            deadline="5:00 PM",
            product="Bottled Tea",
            operator_note="Labels started skewing after roll change",
        ),
        "expected_recommendation": "escalate_to_maintenance",
        "expected_verdict": "FAIL",
        "expected_blocked": True,
    },
    {
        "name": "missing_product_quality_rule",
        "incident": IncidentRequest(
            line="Line 3",
            machine="Filler",
            issue="Keeps faulting after 20 minutes",
            deadline="3:00 PM",
            product="Sparkling Water",
            operator_note="Same filler head issue, different product",
        ),
        "expected_recommendation": "restart_at_reduced_speed",
        "expected_verdict": "FAIL",
        "expected_blocked": True,
    },
    {
        "name": "unknown_line_missing_live_events",
        "incident": IncidentRequest(
            line="Line 9",
            machine="Filler",
            issue="Filler faulted during startup",
            deadline="4:00 PM",
            product="Bottled Tea",
            operator_note="No events are showing for the new line",
        ),
        "expected_recommendation": "escalate_to_maintenance",
        "expected_verdict": "FAIL",
        "expected_blocked": True,
    },
    {
        "name": "ai4i_imported_dataset_triage",
        "incident": IncidentRequest(
            line="AI4I Demo Line",
            machine="AI4I Machine Type L",
            issue="Predictive maintenance dataset indicates machine failure",
            deadline="N/A",
            product="Bottled Tea",
            operator_note="Imported from UCI AI4I failure rows",
        ),
        "expected_recommendation": "escalate_to_maintenance",
        "expected_verdict": "FAIL",
        "expected_blocked": True,
    },
]


def assert_equal(name, actual, expected):
    if actual != expected:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")


def run_case(case):
    result = run_incident_workflow(case["incident"])

    assert_equal(
        f"{case['name']} recommendation",
        result["decision"]["recommendation"],
        case["expected_recommendation"],
    )
    assert_equal(
        f"{case['name']} verifier",
        result["verification"]["verdict"],
        case["expected_verdict"],
    )
    assert_equal(
        f"{case['name']} blocked",
        result["decision_contract"]["blocked"],
        case["expected_blocked"],
    )

    return result


def run_brain_eval():
    parsed = parse_freeform_scenario(
        "Line 3 filler keeps faulting after 20 minutes. Need restart before 3 PM for Bottled Tea."
    )

    required = ["line", "machine", "issue", "deadline", "product"]
    for field in required:
        if not parsed.get(field):
            raise AssertionError(f"brain_parse missing {field}")

    return parsed


def main():
    passed = 0

    for case in CASES:
        run_case(case)
        print(f"PASS {case['name']}")
        passed += 1

    brain_result = run_brain_eval()
    print(f"PASS brain_parse llm_used={brain_result.get('llm_used')}")
    passed += 1

    print(f"\n{passed} evals passed")


if __name__ == "__main__":
    main()