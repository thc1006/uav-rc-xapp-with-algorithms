# UAV-aware RAN Control (RC xApp) — Project Skeleton

This repository is a **Claude Code–friendly** scaffold for experimenting with
O-RAN WG1 UAV use cases using a UAV-aware policy xApp plus an RC gRPC client.

See `docs/architecture.md` for an overview.

This repository is a **skeleton** for experimenting with O-RAN UAV use cases
(Flight Path Based Dynamic UAV Radio Resource Allocation and Radio Resource
Allocation for UAV Application Scenario) using:

- A **UAV policy xApp** (`xapps/uav-policy`) that implements path-aware
  and QoS-aware resource control logic.
- A **RC gRPC client** (`xapps/rc-grpc-client`) that would forward
  `ResourceDecision`s to an RC xApp in a real deployment.
- **Claude Code configuration** (CLAUDE.md, skills, subagents, commands)
  to develop and iterate on the logic with Anthropic tooling.
