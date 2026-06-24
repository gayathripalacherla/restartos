from tools.quality import check_quality_rules
from models.schemas import EvidenceItem


def run(product: str):
    rules = check_quality_rules(product)

    evidence = []
    for rule in rules:
        requirements = "; ".join(rule["requirements"])
        evidence.append(
            EvidenceItem(
                source="quality_rules",
                summary=f"Quality requirements for {product}: {requirements}",
                confidence=0.94,
                citation=f"quality_rules.json#{product}",
            )
        )

    return evidence