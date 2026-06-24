from tools.maintenance import get_maintenance_history
from tools.manuals import search_manuals
from models.schemas import EvidenceItem


def run(machine: str):
    evidence = []

    history = get_maintenance_history(machine)
    for record in history:
        evidence.append(
            EvidenceItem(
                source="maintenance_history",
                summary=f"{record['date']}: {record['issue']} resolved by {record['resolution']}",
                confidence=0.9,
                citation=f"maintenance_history.json#{record['date']}",
            )
        )

    manuals = search_manuals(machine)
    for manual in manuals:
        evidence.append(
            EvidenceItem(
                source="manuals",
                summary=f"{manual['section']}: {manual['content']}",
                confidence=0.88,
                citation=f"manuals.json#{manual['section']}",
            )
        )

    return evidence