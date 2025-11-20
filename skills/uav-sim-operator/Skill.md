# Skill: UAV Simulation Operator

## Purpose

Use this skill to think about how the policy would behave in realistic
scenarios and how to integrate it with simulators (ns-O-RAN, srsRAN, etc.).

## Instructions

1. Read `docs/architecture.md` and `docs/algorithms.md`.
2. Propose concrete simulation scenarios, including:
   - UAV flight paths (altitude, speed, path length).
   - Cell layout and slices.
   - Traffic profiles (video vs control).
3. For each scenario, specify:
   - What KPM subscriptions are needed.
   - What metrics to log (handover count, throughput, latency, impact on
     ground UEs).
   - How `ResourceDecision`s should be translated into RC actions.
