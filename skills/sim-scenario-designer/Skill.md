# Skill: Simulation Scenario Designer

## Purpose

Use this skill to evolve the `sim/` directory into a concrete experiment
for ns-O-RAN or similar platforms.

## Instructions

1. Inspect the current YAML files in `sim/nsoran/` and scripts in
   `sim/scripts/`.
2. When the user describes a target experiment:
   - Update or extend `scenario.yaml`, `uav_paths.yaml`,
     `kpm_subscriptions.yaml`, or `rc_pipeline.yaml`.
   - Keep them high-level and platform-agnostic where possible.
3. Suggest how an ns-3/ns-O-RAN launcher or orchestration tool would:
   - Parse these files.
   - Configure the simulation.
   - Wire KPM reports and RC actions to/from the RIC and xApps.
