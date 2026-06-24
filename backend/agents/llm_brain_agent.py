import json
import os
import re


def fallback_parse(scenario: str):
    lower = scenario.lower()

    line_match = re.search(r"line\s*(\d+)", lower)
    line = f"Line {line_match.group(1)}" if line_match else "Unknown Line"

    machine = "Unknown Machine"
    for candidate in ["filler", "labeler", "capper", "conveyor", "compressor"]:
        if candidate in lower:
            machine = candidate.title()
            break

    product = "Bottled Tea"
    if "sparkling water" in lower:
        product = "Sparkling Water"
    elif "bottled tea" in lower:
        product = "Bottled Tea"
    elif "ai4i" in lower:
        line = "AI4I Demo Line"
        machine = "AI4I Machine Type L"

    time_match = re.search(r"(\d{1,2}\s*(:\d{2})?\s*(am|pm))", lower)
    deadline = time_match.group(1).upper().replace(" ", "") if time_match else "N/A"

    return {
        "line": line,
        "machine": machine,
        "issue": scenario,
        "deadline": deadline,
        "product": product,
        "operator_note": scenario,
        "brain_confidence": 0.45,
        "brain_assessment": "Fallback parser used because LLM was unavailable.",
        "missing_fields": [],
        "llm_used": False,
    }


def parse_freeform_scenario(scenario: str):
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if not api_key:
        return fallback_parse(scenario)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are the RestartOS intake brain for manufacturing operations. "
                        "Convert messy real-life incident reports into structured incident fields. "
                        "Do not invent evidence. If a field is missing, use a conservative default. "
                        "The downstream verifier will decide whether action is allowed."
                    ),
                },
                {
                    "role": "user",
                    "content": scenario,
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "restartos_incident_intake",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "line": {"type": "string"},
                            "machine": {"type": "string"},
                            "issue": {"type": "string"},
                            "deadline": {"type": "string"},
                            "product": {"type": "string"},
                            "operator_note": {"type": "string"},
                            "brain_confidence": {"type": "number"},
                            "brain_assessment": {"type": "string"},
                            "missing_fields": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                        "required": [
                            "line",
                            "machine",
                            "issue",
                            "deadline",
                            "product",
                            "operator_note",
                            "brain_confidence",
                            "brain_assessment",
                            "missing_fields",
                        ],
                    },
                }
            },
        )

        parsed = json.loads(response.output_text)
        parsed["llm_used"] = True
        return parsed

    except Exception as exc:
        parsed = fallback_parse(scenario)
        parsed["brain_assessment"] = f"Fallback parser used after LLM error: {exc}"
        return parsed