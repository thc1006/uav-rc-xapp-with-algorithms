# Skill: UAV Path Planner (Non-RT)

## Purpose

Use this skill to work on the DP-based Non-RT planner in
`nonrt/uav-path-planner`.

## Instructions

1. Read:
   - `CLAUDE.md`
   - `docs/architecture.md`
   - `nonrt/uav-path-planner/README.md`
2. For planner changes:
   - Start from `nonrt/uav-path-planner/tests/test_planner.py`.
   - Modify or add tests to express the new behavior.
   - Update `nonrt/uav-path-planner/src/uav_path_planner/planner.py`.
3. Keep the planner decoupled from any specific RIC / ns-3 interface.
4. Ensure the output remains a valid `FlightPlanPolicy` for
   `uav-policy` to consume.
