# RestartOS

RestartOS is an agent-orchestrated manufacturing recovery system. It turns a messy production-line fault report into an evidence-backed restart decision, verifier result, decision contract, audit trace, and operational handoff artifacts.

Instead of acting like a generic chat UI, RestartOS behaves like a coordinated recovery workflow: it gathers evidence, checks safety and quality policy, verifies whether action is allowed, and either generates recovery artifacts or escalates the incident.

## Live Project

- Live app: [restartos-367orq73n-gayathri-palacherla.vercel.app](https://restartos-367orq73n-gayathri-palacherla.vercel.app)
- Backend API: [restartos.onrender.com](https://restartos.onrender.com)
- GitHub repo: [github.com/gayathripalacherla/restartos](https://github.com/gayathripalacherla/restartos)

## Why It Matters

Manufacturing downtime decisions are high-pressure and evidence-sensitive. A technician may report:

```text
Line 3 filler keeps faulting after about 20 minutes.
Bottles backed up near the capper.
We need restart before 3 PM for Bottled Tea.
```

RestartOS converts that into:

- likely failure cause
- evidence board
- verifier result
- decision contract
- restart checklist
- work order
- QC plan
- shift handoff
- persistent audit record

## What It Demonstrates

- LLM-powered freeform incident intake
- Multi-agent orchestration across maintenance, safety, quality, production, decision, verifier, and artifact agents
- Tool-backed evidence retrieval from machine events, manuals, maintenance history, safety rules, quality rules, and production schedule
- Policy-driven verifier gate
- Explicit decision contracts for allowed next actions
- Persistent audit history with run-level trace inspection
- UCI AI4I predictive-maintenance dataset integration
- Eval suite covering PASS, FAIL, missing evidence, unknown line, dataset, and LLM parser scenarios
- React frontend for running and inspecting recovery workflows

## Architecture

```text
Freeform Operator Report
        |
        v
LLM Brain Parser
        |
        v
Structured IncidentRequest
        |
        v
Specialist Agents
  - Event Timeline Agent
  - Maintenance Agent
  - Safety Agent
  - Quality Agent
  - Production Agent
        |
        v
Evidence Board
        |
        v
Decision Agent
        |
        v
Verifier Agent
        |
        v
Decision Contract Agent
        |
        v
Artifact Agent
        |
        v
Persistent Audit Store
```

Full architecture details: [ARCHITECTURE.md](ARCHITECTURE.md)

## Example Output

```text
Recommendation: restart_at_reduced_speed
Likely cause: Filler head 4 servo overload after fill pressure instability
Confidence: 82%
Verifier: PASS
Blocked: False
Allowed next action: generate_recovery_artifacts
Artifacts: restart_checklist, work_order, qc_plan, shift_handoff
```

If evidence is missing:

```text
Recommendation: escalate_to_maintenance
Verifier: FAIL
Blocked: True
Allowed next action: escalate_to_maintenance_lead
Artifacts: escalation_note
```

## Project Structure

```text
restartos/
  backend/
    agents/          specialist agents and orchestration logic
    artifacts/       generated checklist, work order, QC plan, handoff, escalation note
    audit/           persistent run history and run detail lookup
    config/          evidence policy
    data/            sample machine, maintenance, safety, quality, and schedule data
    evals/           regression evals
    models/          Pydantic schemas
    policy/          evidence policy loader
    scripts/         dataset import and demo scripts
    tools/           data access tools
    app.py           FastAPI app
    orchestrator.py  main workflow
  frontend/
    src/             React UI
  ARCHITECTURE.md
  README.md
```

## Setup

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Run the API:

```bash
uvicorn app:app --reload --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173/
```

For deployed frontends, set:

```bash
VITE_API_BASE_URL=https://your-backend-url
```

## API Usage

Run a freeform LLM workflow:

```bash
curl -X POST http://127.0.0.1:8000/incident/brain-run \
  -H "Content-Type: application/json" \
  -d '{"scenario":"Line 3 filler keeps faulting after about 20 minutes. Bottles backed up near the capper. We need restart before 3 PM for Bottled Tea."}'
```

Get audit history:

```bash
curl http://127.0.0.1:8000/runs
```

Get one audit run:

```bash
curl http://127.0.0.1:8000/runs/run_b00080f1
```

## Demo Script

Run four end-to-end demos from one command:

```bash
cd backend
PYTHONPATH=. python3 scripts/demo_restartos.py
```

The demo covers:

- evidence-backed restart PASS
- missing-evidence escalation FAIL
- UCI AI4I dataset triage
- LLM brain freeform intake

## Evals

```bash
cd backend
PYTHONPATH=. python3 evals/run_evals.py
```

Expected result:

```text
6 evals passed
```

## Deployment

One simple deployment path:

- Deploy `backend/` as a Python web service.
- Deploy `frontend/` as a Vite static site.
- Set the frontend environment variable `VITE_API_BASE_URL` to the deployed backend URL.
- Set the backend environment variable `OPENAI_API_KEY` if you want live LLM parsing.

Backend settings:

```text
Root directory: backend
Build command: pip install -r requirements.txt
Start command: uvicorn app:app --host 0.0.0.0 --port $PORT
```

Frontend settings:

```text
Root directory: frontend
Build command: npm run build
Output directory: dist
Environment variable: VITE_API_BASE_URL=<backend service URL>
```

## Dataset Integration

RestartOS imports failure rows from the UCI AI4I 2020 Predictive Maintenance dataset into machine-event format.

The dataset-backed scenario intentionally demonstrates a realistic safety behavior: imported failure evidence alone is not enough to approve restart. If maintenance history, manuals, production schedule, or safety rules are missing, RestartOS blocks the recovery path and escalates.

## Safety Design

RestartOS does not blindly generate restart instructions.

Recovery artifacts are generated only after verifier PASS under the configured evidence policy. Failed verification produces an escalation note instead.

## Why This Is Agent Orchestration

RestartOS coordinates multiple specialized agents with separate responsibilities and traceable outputs. Each run records:

- agent name
- tool used
- action taken
- evidence count
- decision impact
- verifier result
- allowed next action

That makes the system inspectable, auditable, and safer than a single prompt-based assistant.
