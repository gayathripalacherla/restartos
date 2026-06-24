from models.schemas import Decision


def normalize_sources(evidence):
    sources = {item.source for item in evidence}

    if "ai4i_machine_events" in sources:
        sources.add("machine_events")

    return sources


def run(evidence):
    sources = normalize_sources(evidence)
    summaries = [item.summary.lower() for item in evidence]

    if "machine_events" not in sources:
        return Decision(
            recommendation="escalate_to_maintenance",
            confidence=0.45,
            likely_cause="No live machine event evidence found for this line",
            reasoning=[
                "The system cannot identify the failure origin without machine event evidence",
                "Historical machine evidence alone is not enough to approve a restart path",
            ],
            risks=[
                "Restart recommendation could be unsafe without current line fault evidence"
            ],
        )

    if "production_schedule" not in sources:
        return Decision(
            recommendation="escalate_to_maintenance",
            confidence=0.5,
            likely_cause="Production schedule is missing for this line",
            reasoning=[
                "The system found machine failure evidence but cannot evaluate restart timing or production impact",
                "A restart decision needs current schedule and remaining production context",
            ],
            risks=[
                "Restart could miss deadline, conflict with batch timing, or create downstream production risk"
            ],
        )

    if any("servo overload" in summary for summary in summaries):
        return Decision(
            recommendation="restart_at_reduced_speed",
            confidence=0.82,
            likely_cause="Filler head 4 servo overload after fill pressure instability",
            reasoning=[
                "First critical fault occurred at the filler",
                "Capper issue appeared after filler fault and is likely downstream",
                "Similar past incident was resolved by cleaning filler head 4 and recalibrating the servo",
                "Safety rules allow restart after inspection and dry cycle",
                "Quality rules require holding initial output for sampling",
            ],
            risks=[
                "Fault may recur if servo overheating or filler head resistance remains unresolved"
            ],
        )

    if any("ai4i predictive maintenance failure" in summary for summary in summaries):
        return Decision(
            recommendation="escalate_to_maintenance",
            confidence=0.68,
            likely_cause="Imported AI4I predictive-maintenance failure evidence requires plant-specific validation",
            reasoning=[
                "AI4I machine failure evidence indicates abnormal operating conditions",
                "The system still needs plant-specific safety, maintenance, manual, and schedule evidence before recovery artifacts can be generated",
            ],
            risks=[
                "Dataset-derived failure evidence should not directly authorize real plant recovery action"
            ],
        )

    return Decision(
        recommendation="escalate_to_maintenance",
        confidence=0.55,
        likely_cause="Insufficient evidence to identify failure origin",
        reasoning=["No clear first-fault pattern found"],
        risks=["Restart may be unsafe without additional inspection"],
    )