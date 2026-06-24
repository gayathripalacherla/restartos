from agents.llm_brain_agent import parse_freeform_scenario
from audit.store import list_runs, save_run
from models.schemas import IncidentRequest
from orchestrator import run_incident_workflow


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_result(name, incident, result):
    decision = result["decision"]
    verification = result["verification"]
    contract = result["decision_contract"]

    print_section(name)
    print(f"Incident: {incident.line} / {incident.machine}")
    print(f"Issue: {incident.issue}")
    print(f"Recommendation: {decision['recommendation']}")
    print(f"Likely cause: {decision['likely_cause']}")
    print(f"Confidence: {round(decision['confidence'] * 100)}%")
    print(f"Verifier: {verification['verdict']}")
    print(f"Blocked: {contract['blocked']}")
    print(f"Allowed next action: {contract['allowed_next_action']}")
    print(f"Evidence found: {', '.join(contract['evidence_found'])}")
    print(f"Evidence missing: {', '.join(contract['evidence_missing']) or 'none'}")
    print(f"Trace steps: {len(result['trace'])}")
    print(f"Artifacts: {', '.join(result['artifacts'].keys())}")

    saved = save_run(incident, result)
    print(f"Saved audit run: {saved['run_id']}")


def run_structured_demos():
    pass_incident = IncidentRequest(
        line="Line 3",
        machine="Filler",
        issue="Keeps faulting after 20 minutes",
        deadline="3:00 PM",
        product="Bottled Tea",
        operator_note="Bottles backed up near capper",
    )
    pass_result = run_incident_workflow(pass_incident)
    print_result("PASS DEMO: Evidence-backed restart", pass_incident, pass_result)

    fail_incident = IncidentRequest(
        line="Line 2",
        machine="Labeler",
        issue="Labels keep drifting out of alignment",
        deadline="5:00 PM",
        product="Bottled Tea",
        operator_note="Labels started skewing after roll change",
    )
    fail_result = run_incident_workflow(fail_incident)
    print_result("FAIL DEMO: Missing evidence escalation", fail_incident, fail_result)

    ai4i_incident = IncidentRequest(
        line="AI4I Demo Line",
        machine="AI4I Machine Type L",
        issue="Predictive maintenance dataset indicates machine failure",
        deadline="N/A",
        product="Bottled Tea",
        operator_note="Imported from UCI AI4I failure rows",
    )
    ai4i_result = run_incident_workflow(ai4i_incident)
    print_result("DATASET DEMO: UCI AI4I imported failure evidence", ai4i_incident, ai4i_result)


def run_brain_demo():
    print_section("LLM BRAIN DEMO: Freeform scenario to structured incident")

    scenario = (
        "Line 3 filler keeps faulting after about 20 minutes. "
        "Bottles are backing up near the capper. "
        "We need to know if we can restart before 3 PM for Bottled Tea."
    )

    brain = parse_freeform_scenario(scenario)

    incident = IncidentRequest(
        line=brain["line"],
        machine=brain["machine"],
        issue=brain["issue"],
        deadline=brain["deadline"],
        product=brain["product"],
        operator_note=brain["operator_note"],
    )

    result = run_incident_workflow(incident)
    result["brain_parse"] = brain

    print(f"LLM used: {brain['llm_used']}")
    print(f"Brain confidence: {round(brain['brain_confidence'] * 100)}%")
    print(f"Brain assessment: {brain['brain_assessment']}")
    print_result("BRAIN WORKFLOW RESULT", incident, result)


def main():
    run_structured_demos()
    run_brain_demo()

    print_section("AUDIT HISTORY")
    runs = list_runs()
    print(f"Total saved runs: {len(runs)}")
    for run in runs[:5]:
        print(
            f"{run['run_id']} | "
            f"{run['incident']['line']} / {run['incident']['machine']} | "
            f"{run['decision']['recommendation']} | "
            f"{run['verification']['verdict']}"
        )


if __name__ == "__main__":
    main()