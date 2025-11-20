# Skill: UAV O-RAN Use-Case Digest

## Purpose

Before making any code changes, use this skill to:

- Read `spec/uav_oran_usecase.md`.
- Summarize the background, goals, actors, data flows, and constraints for
  Use Case 2 and Use Case 3.
- Produce a checklist of requirements that the `uav-policy` xApp should
  respect.

## Instructions

1. Open and read `spec/uav_oran_usecase.md` carefully.
2. Extract:
   - Goals (what KPI to improve / protect).
   - Roles (Non-RT RIC, Near-RT RIC, Application servers, UAV, gNB/DU/RU).
   - Input data (flight path, radio KPIs, application QoS).
   - Output decisions (resource allocation hints, handover hints, slice usage).
3. Emit a short markdown document (`docs/usecase_digest.md`) with:
   - A high-level narrative.
   - A bullet-list of requirements that future code must not violate.
