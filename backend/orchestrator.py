from agents import (
    event_timeline_agent,
    maintenance_agent,
    safety_agent,
    quality_agent,
    production_agent,
)
from agents.decision_agent import run as decide
from agents.decision_contract_agent import build_decision_contract
from agents.verifier_agent import run as verify
from artifacts.generator import generate_artifacts, generate_escalation_note


def add_trace(trace, agent, tool, action, evidence_count, impact, status="completed"):
    trace.append(
        {
            "agent": agent,
            "tool": tool,
            "action": action,
            "status": status,
            "evidence_count": evidence_count,
            "impact": impact,
        }
    )


def run_incident_workflow(incident):
    timeline = []
    evidence = []
    trace = []

    timeline.append("Parsing incident goal")
    add_trace(
        trace,
        agent="Intake Parser",
        tool="IncidentRequest",
        action="Normalize structured incident fields",
        evidence_count=0,
        impact=f"Incident scoped to {incident.line} / {incident.machine}",
    )

    timeline.append("Checking machine event timeline")
    event_evidence = event_timeline_agent.run(incident.line)
    evidence += event_evidence
    add_trace(
        trace,
        agent="Event Timeline Agent",
        tool="get_machine_events",
        action=f"Fetch machine events for {incident.line}",
        evidence_count=len(event_evidence),
        impact="Identifies live fault sequence and failure origin evidence",
    )

    timeline.append("Checking maintenance history and manuals")
    maintenance_evidence = maintenance_agent.run(incident.machine)
    evidence += maintenance_evidence
    add_trace(
        trace,
        agent="Maintenance Agent",
        tool="get_maintenance_history + search_manuals",
        action=f"Retrieve history and SOP context for {incident.machine}",
        evidence_count=len(maintenance_evidence),
        impact="Adds prior repairs and troubleshooting procedures",
    )

    timeline.append("Checking safety requirements")
    safety_evidence = safety_agent.run(incident.machine)
    evidence += safety_evidence
    add_trace(
        trace,
        agent="Safety Agent",
        tool="check_safety_requirements",
        action=f"Check restart safety policy for {incident.machine}",
        evidence_count=len(safety_evidence),
        impact="Determines required safety checks before action",
    )

    timeline.append("Checking quality rules")
    quality_evidence = quality_agent.run(incident.product)
    evidence += quality_evidence
    add_trace(
        trace,
        agent="Quality Agent",
        tool="check_quality_rules",
        action=f"Check quality policy for {incident.product}",
        evidence_count=len(quality_evidence),
        impact="Determines hold, sampling, and release requirements",
    )

    timeline.append("Checking production schedule")
    production_evidence = production_agent.run(incident.line)
    evidence += production_evidence
    add_trace(
        trace,
        agent="Production Agent",
        tool="get_production_schedule",
        action=f"Fetch schedule context for {incident.line}",
        evidence_count=len(production_evidence),
        impact="Evaluates restart timing and production impact",
    )

    timeline.append("Creating recovery decision")
    decision = decide(evidence)
    add_trace(
        trace,
        agent="Decision Agent",
        tool="evidence_board",
        action="Generate proposed recovery recommendation",
        evidence_count=len(evidence),
        impact=f"Proposed action: {decision.recommendation}",
    )

    timeline.append("Verifying decision against evidence and safety requirements")
    verification = verify(evidence, decision)
    add_trace(
        trace,
        agent="Verifier Agent",
        tool="configured_evidence_policy",
        action="Check evidence sufficiency and allowed action",
        evidence_count=len(evidence),
        impact=f"Verifier result: {verification.verdict}",
    )

    timeline.append("Building decision contract")
    decision_contract = build_decision_contract(evidence, decision, verification)
    add_trace(
        trace,
        agent="Decision Contract Agent",
        tool="evidence_policy",
        action="Build explicit action contract",
        evidence_count=len(evidence),
        impact=(
            "Action allowed"
            if not decision_contract["blocked"]
            else "Action blocked pending evidence or review"
        ),
    )

    artifacts = {}
    if verification.verdict == "PASS":
        timeline.append("Generating restart checklist, work order, QC plan, and shift handoff")
        artifacts = generate_artifacts(incident, decision)
        add_trace(
            trace,
            agent="Artifact Agent",
            tool="generate_artifacts",
            action="Generate operational recovery artifacts",
            evidence_count=len(evidence),
            impact="Produced restart checklist, work order, QC plan, and shift handoff",
        )
    else:
        timeline.append("Generating escalation note for maintenance lead")
        artifacts = generate_escalation_note(incident, decision, verification)
        add_trace(
            trace,
            agent="Artifact Agent",
            tool="generate_escalation_note",
            action="Generate blocked-run escalation note",
            evidence_count=len(evidence),
            impact="Produced escalation note instead of recovery artifacts",
        )

    return {
        "timeline": timeline,
        "trace": trace,
        "evidence": [item.model_dump() for item in evidence],
        "decision": decision.model_dump(),
        "verification": verification.model_dump(),
        "decision_contract": decision_contract,
        "artifacts": artifacts,
    }