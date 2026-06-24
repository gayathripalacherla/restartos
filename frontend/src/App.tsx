import { useState } from 'react'
import './App.css'

type TraceStep = {
  agent: string
  tool: string
  action: string
  status: string
  evidence_count: number
  impact: string
}

type RunRecord = {
  run_id: string
  created_at: string
  incident: {
    line: string
    machine: string
    issue: string
    deadline: string
    product: string
    operator_note?: string
  }
  decision: {
    recommendation: string
    confidence: number
    likely_cause: string
    reasoning: string[]
    risks: string[]
  }
  verification: {
    verdict: string
    missing_evidence: string[]
    safety_blockers: string[]
    human_approval_required: boolean
    notes: string
  }
  timeline: string[]
}

type Result = {
  run_id?: string
  created_at?: string
  brain_parse?: {
    line: string
    machine: string
    issue: string
    deadline: string
    product: string
    operator_note: string
    brain_confidence: number
    brain_assessment: string
    missing_fields: string[]
    llm_used: boolean
  }
  timeline: string[]
  trace?: TraceStep[]
  evidence: {
    source: string
    summary: string
    confidence: number
    citation: string
  }[]
  decision: {
    recommendation: string
    confidence: number
    likely_cause: string
    reasoning: string[]
    risks: string[]
  }
  verification: {
    verdict: string
    missing_evidence: string[]
    safety_blockers: string[]
    human_approval_required: boolean
    notes: string
  }
  decision_contract: {
    recommendation: string
    confidence: number
    evidence_required: string[]
    evidence_found: string[]
    evidence_missing: string[]
    blocked: boolean
    block_reason: string | null
    human_approval_required: boolean
    allowed_next_action: string
    artifact_policy: string
  }
  artifacts: {
    restart_checklist?: string[]
    work_order?: Record<string, string>
    qc_plan?: string[]
    shift_handoff?: string
    escalation_note?: string
  }
}

function App() {
  const [result, setResult] = useState<Result | null>(null)
  const [runs, setRuns] = useState<RunRecord[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [scenario, setScenario] = useState(
    'Line 3 filler keeps faulting after about 20 minutes. Bottles backed up near the capper. We need to know if we can restart before 3 PM for Bottled Tea.',
  )

  const [form, setForm] = useState({
    line: 'Line 3',
    machine: 'Filler',
    issue: 'Keeps faulting after 20 minutes',
    deadline: '3:00 PM',
    product: 'Bottled Tea',
    operator_note: 'Bottles backed up near capper',
  })

  async function loadRuns() {
    const response = await fetch('http://127.0.0.1:8000/runs')
    const data = await response.json()
    setRuns(data.runs)
  }

  async function runIncident() {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/incident/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
      loadRuns()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to run recovery')
    } finally {
      setLoading(false)
    }
  }

  async function runBrainIncident() {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/incident/brain-run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario }),
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
      loadRuns()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to run brain recovery')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">Agent Orchestration Track</p>
          <h1>RestartOS</h1>
          <p className="subtitle">
            Agentic line recovery for manufacturing faults. Converts messy
            production reports into evidence-backed decisions, verifier-gated
            actions, and operational artifacts.
          </p>
        </div>

        <form
          className="incident-form"
          onSubmit={(event) => {
            event.preventDefault()
            runIncident()
          }}
        >
          <input
            value={form.line}
            onChange={(event) => setForm({ ...form, line: event.target.value })}
            placeholder="Line"
          />
          <input
            value={form.machine}
            onChange={(event) =>
              setForm({ ...form, machine: event.target.value })
            }
            placeholder="Machine"
          />
          <input
            value={form.issue}
            onChange={(event) =>
              setForm({ ...form, issue: event.target.value })
            }
            placeholder="Issue"
          />
          <input
            value={form.deadline}
            onChange={(event) =>
              setForm({ ...form, deadline: event.target.value })
            }
            placeholder="Deadline"
          />
          <input
            value={form.product}
            onChange={(event) =>
              setForm({ ...form, product: event.target.value })
            }
            placeholder="Product"
          />
          <textarea
            value={form.operator_note}
            onChange={(event) =>
              setForm({ ...form, operator_note: event.target.value })
            }
            placeholder="Operator note"
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Running agents...' : 'Run Structured Recovery'}
          </button>
        </form>
      </section>

      <section className="panel">
        <h2>LLM Brain Intake</h2>
        <p>
          Paste a messy real-life technician or supervisor report. The brain
          extracts incident fields, then the verifier-gated workflow runs.
        </p>
        <textarea
          value={scenario}
          onChange={(event) => setScenario(event.target.value)}
          style={{ width: '100%', minHeight: '100px' }}
        />
        <button onClick={runBrainIncident} disabled={loading}>
          {loading ? 'Running brain...' : 'Run Brain Assessment'}
        </button>
      </section>

      {error && (
        <section className="panel">
          <h2>Request Failed</h2>
          <p>{error}</p>
        </section>
      )}

      <section className="panel">
        <h2>Run History</h2>
        <button onClick={loadRuns}>Refresh History</button>

        {runs.length === 0 && <p>No runs loaded yet.</p>}

        {runs.map((run) => (
          <article key={run.run_id} className="evidence-card">
            <span>{run.run_id}</span>
            <p>
              {run.incident.line} / {run.incident.machine} —{' '}
              {run.decision.recommendation}
            </p>
            <small>
              Verifier: {run.verification.verdict} · {run.created_at}
            </small>
          </article>
        ))}
      </section>

      {result && (
        <section className="grid">
          {result.brain_parse && (
            <div className="panel wide">
              <h2>Brain Parse</h2>
              <p>
                <strong>LLM used: </strong>
                {result.brain_parse.llm_used ? 'Yes' : 'No'}
              </p>
              <p>
                <strong>Parsed incident: </strong>
                {result.brain_parse.line} / {result.brain_parse.machine} /{' '}
                {result.brain_parse.product}
              </p>
              <p>
                <strong>Deadline: </strong>
                {result.brain_parse.deadline}
              </p>
              <p>
                <strong>Brain confidence: </strong>
                {Math.round(result.brain_parse.brain_confidence * 100)}%
              </p>
              <p>{result.brain_parse.brain_assessment}</p>
            </div>
          )}

          <div className="panel">
            <h2>Agent Timeline</h2>
            <ol>
              {result.timeline.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ol>
          </div>

          <div className="panel decision">
            <h2>Decision</h2>
            <strong>{result.decision.recommendation}</strong>
            <p>{result.decision.likely_cause}</p>
            <p>Confidence: {Math.round(result.decision.confidence * 100)}%</p>
            <p>Verifier: {result.verification.verdict}</p>
            {result.run_id && <p>Run ID: {result.run_id}</p>}
          </div>

          {result.trace && (
            <div className="panel wide">
              <h2>Agent Trace Inspector</h2>
              {result.trace.map((step, index) => (
                <article key={index} className="evidence-card">
                  <span>{step.agent}</span>
                  <p>
                    <strong>Tool: </strong>
                    {step.tool}
                  </p>
                  <p>
                    <strong>Action: </strong>
                    {step.action}
                  </p>
                  <p>
                    <strong>Evidence count: </strong>
                    {step.evidence_count}
                  </p>
                  <p>
                    <strong>Impact: </strong>
                    {step.impact}
                  </p>
                </article>
              ))}
            </div>
          )}

          <div className="panel wide">
            <h2>Decision Contract</h2>
            <p>
              <strong>Blocked: </strong>
              {result.decision_contract.blocked ? 'Yes' : 'No'}
            </p>
            <p>
              <strong>Allowed next action: </strong>
              {result.decision_contract.allowed_next_action}
            </p>
            <p>
              <strong>Evidence found: </strong>
              {result.decision_contract.evidence_found.join(', ')}
            </p>
            <p>
              <strong>Evidence missing: </strong>
              {result.decision_contract.evidence_missing.length > 0
                ? result.decision_contract.evidence_missing.join(', ')
                : 'None'}
            </p>
            {result.decision_contract.block_reason && (
              <p>
                <strong>Block reason: </strong>
                {result.decision_contract.block_reason}
              </p>
            )}
            <p>{result.decision_contract.artifact_policy}</p>
          </div>

          <div className="panel wide">
            <h2>Evidence Board</h2>
            <div className="evidence-list">
              {result.evidence.map((item, index) => (
                <article key={index} className="evidence-card">
                  <span>{item.source}</span>
                  <p>{item.summary}</p>
                  <small>{item.citation}</small>
                </article>
              ))}
            </div>
          </div>

          {result.verification.verdict === 'FAIL' && (
            <div className="panel wide">
              <h2>Human Review Required</h2>
              <p>{result.verification.notes}</p>
              <p>
                <strong>Missing evidence: </strong>
                {result.verification.missing_evidence.join(', ')}
              </p>
              {result.artifacts.escalation_note && (
                <>
                  <h2>Escalation Note</h2>
                  <p>{result.artifacts.escalation_note}</p>
                </>
              )}
            </div>
          )}

          {result.verification.verdict === 'PASS' && (
            <>
              <div className="panel">
                <h2>Restart Checklist</h2>
                <ul>
                  {result.artifacts.restart_checklist?.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="panel">
                <h2>Work Order</h2>
                {Object.entries(result.artifacts.work_order ?? {}).map(
                  ([key, value]) => (
                    <p key={key}>
                      <strong>{key}: </strong>
                      {value}
                    </p>
                  ),
                )}
              </div>

              <div className="panel">
                <h2>QC Plan</h2>
                <ul>
                  {result.artifacts.qc_plan?.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="panel">
                <h2>Shift Handoff</h2>
                <p>{result.artifacts.shift_handoff}</p>
              </div>
            </>
          )}
        </section>
      )}
    </main>
  )
}

export default App