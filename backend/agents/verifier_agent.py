from models.schemas import VerificationResult
from policy.evidence_policy import get_required_evidence, normalize_sources


def run(evidence, decision):
    sources = normalize_sources(evidence)
    missing = []

    required_sources = get_required_evidence("restart_recovery")

    for source in required_sources:
        if source not in sources:
            missing.append(source)

    allowed_recommendations = {
        "restart_now",
        "restart_at_reduced_speed",
        "keep_line_down",
        "escalate_to_maintenance",
    }

    safety_blockers = []
    if decision.recommendation not in allowed_recommendations:
        safety_blockers.append("Decision recommendation is not an allowed action.")

    if missing or safety_blockers:
        return VerificationResult(
            verdict="FAIL",
            missing_evidence=sorted(missing),
            safety_blockers=safety_blockers,
            human_approval_required=True,
            notes="Decision needs more evidence or has safety blockers.",
        )

    return VerificationResult(
        verdict="PASS",
        missing_evidence=[],
        safety_blockers=[],
        human_approval_required=True,
        notes="Decision is supported by the configured evidence policy.",
    )