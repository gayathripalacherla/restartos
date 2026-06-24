from tools.machine_events import get_machine_events
from models.schemas import EvidenceItem


def run(line: str):
    events = get_machine_events(line)

    evidence = []
    for event in events:
        source = "machine_events"
        citation = f"machine_events.json#{event['timestamp']}"

        if event.get("source_dataset"):
            source = "ai4i_machine_events"
            citation = f"{event['source_dataset']}#{event['timestamp']}"

        evidence.append(
            EvidenceItem(
                source=source,
                summary=f"{event['machine']} {event['level']}: {event['message']} at {event['timestamp']}",
                confidence=0.95,
                citation=citation,
            )
        )

    return evidence