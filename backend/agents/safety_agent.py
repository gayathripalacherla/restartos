from tools.safety import check_safety_requirements
from models.schemas import EvidenceItem


def run(machine: str):
    rules = check_safety_requirements(machine)

    evidence = []
    for rule in rules:
        requirements = "; ".join(rule["requirements"])
        evidence.append(
            EvidenceItem(
                source="safety_rules",
                summary=f"Restart requirements for {machine}: {requirements}",
                confidence=0.97,
                citation=f"safety_rules.json#{machine}",
            )
        )

    return evidence