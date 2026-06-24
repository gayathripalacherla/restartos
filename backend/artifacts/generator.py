def generate_artifacts(incident, decision):
    return {
        "restart_checklist": [
            "Inspect filler head 4",
            "Verify all guards are closed",
            "Clear bottle accumulation around filler and capper",
            "Confirm emergency stop circuit is reset",
            "Run 10-minute dry cycle",
            "Restart at 60% speed",
            "Monitor fill pressure for 20 minutes",
        ],
        "work_order": {
            "asset": f"{incident.line} {incident.machine}",
            "priority": "High",
            "problem": incident.issue,
            "likely_cause": decision.likely_cause,
            "recommended_action": "Inspect filler head 4, clean if needed, and recalibrate servo assembly",
        },
        "qc_plan": [
            "Hold first 180 bottles after restart",
            "Check fill volume every 15 minutes for first hour",
            "Inspect caps and seals before release",
            "Release held product only after QA approval",
        ],
        "shift_handoff": (
            f"{incident.line} {incident.machine} faulted before the {incident.deadline} deadline. "
            f"Recommendation: {decision.recommendation}. Likely cause: {decision.likely_cause}. "
            "Monitor fill pressure and filler head 4 after restart."
        ),
    }


def generate_escalation_note(incident, decision, verification):
    missing = ", ".join(verification.missing_evidence)

    return {
        "escalation_note": (
            f"Escalation required for {incident.line} {incident.machine}. "
            f"Reported issue: {incident.issue}. "
            f"Operator note: {incident.operator_note or 'No operator note provided'}. "
            f"Restart was blocked because the verifier returned {verification.verdict}. "
            f"Missing evidence: {missing}. "
            f"Current recommendation: {decision.recommendation}. "
            f"Reason: {decision.likely_cause}. "
            "Maintenance lead should collect the missing evidence before approving restart or repair."
        )
    }