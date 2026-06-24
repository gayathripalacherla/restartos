from tools.schedule import get_production_schedule
from models.schemas import EvidenceItem


def run(line: str):
    schedules = get_production_schedule(line)

    evidence = []
    for schedule in schedules:
        evidence.append(
            EvidenceItem(
                source="production_schedule",
                summary=(
                    f"{line} has {schedule['remaining_units']} units remaining by "
                    f"{schedule['deadline']}; normal rate {schedule['normal_units_per_minute']}/min, "
                    f"reduced rate {schedule['reduced_speed_units_per_minute']}/min"
                ),
                confidence=0.92,
                citation=f"production_schedule.json#{line}",
            )
        )

    return evidence