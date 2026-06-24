from pydantic import BaseModel
from typing import List, Optional


class IncidentRequest(BaseModel):
    line: str
    machine: str
    issue: str
    deadline: str
    product: str
    operator_note: Optional[str] = None


class EvidenceItem(BaseModel):
    source: str
    summary: str
    confidence: float
    citation: str


class Decision(BaseModel):
    recommendation: str
    confidence: float
    likely_cause: str
    reasoning: List[str]
    risks: List[str]


class VerificationResult(BaseModel):
    verdict: str
    missing_evidence: List[str]
    safety_blockers: List[str]
    human_approval_required: bool
    notes: str

class FreeformIncidentRequest(BaseModel):
    scenario: str  