from policy.evidence_policy import get_required_evidence, normalize_sources


def build_decision_contract(evidence, decision, verification):
    sources = normalize_sources(evidence)
    required_evidence = get_required_evidence("restart_recovery")

    evidence_found = sorted(sources)
    evidence_missing = sorted(required_evidence - sources)
    blocked = verification.verdict != "PASS"

    return {
        "recommendation": decision.recommendation,
        "confidence": decision.confidence,
        "evidence_required": sorted(required_evidence),
        "evidence_found": evidence_found,
        "evidence_missing": evidence_missing,
        "blocked": blocked,
        "block_reason": verification.notes if blocked else None,
        "human_approval_required": verification.human_approval_required,
        "allowed_next_action": (
            "generate_recovery_artifacts"
            if verification.verdict == "PASS"
            else "escalate_to_maintenance_lead"
        ),
        "artifact_policy": (
            "Recovery artifacts are generated only after verifier PASS under the configured evidence policy. "
            "Failed verification produces an escalation note instead."
        ),
    }