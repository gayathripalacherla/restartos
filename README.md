# RestartOS

RestartOS is an agent-orchestrated manufacturing recovery system. It turns a messy production-line fault report into an evidence-backed restart decision, verifier result, decision contract, audit trace, and operational handoff artifacts.

Instead of acting like a generic chat UI, RestartOS behaves like a coordinated recovery workflow: it gathers evidence, checks safety and quality policy, verifies whether action is allowed, and either generates recovery artifacts or escalates the incident.

## Why It Matters

Manufacturing downtime decisions are high-pressure and evidence-sensitive. A technician may report:

```text
Line 3 filler keeps faulting after about 20 minutes.
Bottles backed up near the capper.
We need restart before 3 PM for Bottled Tea.