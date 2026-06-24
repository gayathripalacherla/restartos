# RestartOS Architecture

RestartOS is an agent-orchestrated manufacturing recovery system. It converts a messy line-fault report into an evidence-backed restart decision, verifier result, decision contract, audit trace, and operational artifacts.

## System Goal

A maintenance technician reports a real production issue, for example:

```text
Line 3 filler keeps faulting after about 20 minutes.
Bottles backed up near the capper.
We need restart before 3 PM for Bottled Tea.