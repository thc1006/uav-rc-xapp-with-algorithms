# Skill: UAV Policy xApp Scaffolder

## Purpose

Use this skill when you need to add or modify policy behavior in
`xapps/uav-policy`.

## Instructions

1. Start by reading:
   - `CLAUDE.md`
   - `docs/algorithms.md`
   - `xapps/uav-policy/README.md`
2. When adding behavior:
   - **First** update or add tests in `xapps/uav-policy/tests/test_policy_engine.py`.
   - **Then** modify `xapps/uav-policy/src/uav_policy/policy_engine.py`.
   - Keep algorithms pure (no network I/O, no logging); integration belongs
     elsewhere.
3. Ensure any new data fields are documented in both the dataclasses and
   `docs/algorithms.md` if relevant.
