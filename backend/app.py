from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents.llm_brain_agent import parse_freeform_scenario
from audit.store import get_run, list_runs, save_run
from models.schemas import FreeformIncidentRequest, IncidentRequest
from orchestrator import run_incident_workflow

app = FastAPI(title="RestartOS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "RestartOS API"}


@app.post("/incident/run")
def run_incident(incident: IncidentRequest):
    result = run_incident_workflow(incident)
    audit_record = save_run(incident, result)
    result["run_id"] = audit_record["run_id"]
    result["created_at"] = audit_record["created_at"]
    return result


@app.post("/incident/brain-run")
def brain_run_incident(request: FreeformIncidentRequest):
    brain_parse = parse_freeform_scenario(request.scenario)

    incident = IncidentRequest(
        line=brain_parse["line"],
        machine=brain_parse["machine"],
        issue=brain_parse["issue"],
        deadline=brain_parse["deadline"],
        product=brain_parse["product"],
        operator_note=brain_parse["operator_note"],
    )

    result = run_incident_workflow(incident)
    result["brain_parse"] = brain_parse

    audit_record = save_run(incident, result)
    result["run_id"] = audit_record["run_id"]
    result["created_at"] = audit_record["created_at"]

    return result

@app.get("/runs/{run_id}")
def get_run_by_id(run_id: str):
    run = get_run(run_id)

    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    return run

@app.get("/runs")
def get_runs():
    return {"runs": list_runs()}