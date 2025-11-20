# CLAUDE.md — UAV RC xApp Policy Project

## What this repo is for

This repository is a **playground** for implementing O-RAN UAV use cases in a
RIC environment:

- **Use Case 2:** Flight Path Based Dynamic UAV Radio Resource Allocation.
- **Use Case 3:** Radio Resource Allocation for UAV Application Scenario.

The goal is **not** to implement an entire near-RT RIC or RC xApp, but to:

1. Define **clean data models** and **algorithms** for UAV-aware policies.
2. Implement these in a reusable Python package (`uav-policy`).
3. Provide a small RC client stub that can be wired to an existing RC xApp.
4. Make the project easy to extend using Claude Code (skills, commands,
   and subagents).

The use-case text lives in `spec/uav_oran_usecase.md`. Algorithm details are
in `docs/algorithms.md`.

## Repo layout (important for Claude Code)

- `spec/uav_oran_usecase.md` — textual O-RAN UAV use-case description.
- `docs/architecture.md` — high-level architecture: Non-RT RIC ↔ Near-RT RIC.
- `docs/algorithms.md` — path-aware + QoS-aware algorithm design.
- `xapps/uav-policy/`
  - `src/uav_policy/policy_engine.py` — core data classes and algorithms.
  - `src/uav_policy/main.py` — toy driver for local testing/logging.
  - `tests/test_policy_engine.py` — unit tests for the policies.
- `xapps/rc-grpc-client/`
  - `src/rc_grpc_client/client.py` — RcGrpcClient stub (to be wired to RC xApp).
- `skills/` — Claude skills (digest use-case, scaffold policy, sim operator).
- `subagents/` — Claude subagents (RIC architect, xApp dev, sim integration, QA).
- `commands/` — higher-level workflow commands.

When you (Claude) work on this repo, always start by reading:

1. `CLAUDE.md` (this file).
2. `spec/uav_oran_usecase.md`.
3. `docs/algorithms.md`.

## Ground rules for modifications

1. **Respect the O-RAN layers.**  
   - Non-RT RIC and rApps do offline planning and training.
   - Near-RT RIC xApps make per-UAV decisions on short timescales.
   - E2SM_RC / RC xApp handle the actual control messages to gNB/DU/RU.

2. **Keep algorithms and transport separated.**  
   - `uav-policy` should only compute `ResourceDecision`s.
   - Mapping to real RC / E2 messages belongs in `rc-grpc-client` or an
     integration module.

3. **Prefer TDD where possible.**  
   - For new policy behavior, first update `tests/test_policy_engine.py`.
   - Then update `policy_engine.py` to satisfy the tests.

4. **Make assumptions explicit.**  
   - If an algorithm depends on radio-map quality, path-position accuracy,
     or RC capabilities, write this in comments / docs.

## How to run tests (for humans and tools)

Assuming a virtual environment with pytest installed:

```bash
cd xapps/uav-policy
pytest
```

You can also write small scripts in `uav_policy/main.py` to play with the
policies in isolation.


## Project purpose

This repo is a *design + scaffolding* project for an O-RAN UAV use case:

- Map O-RAN WG1 use cases **“Flight path based dynamic UAV radio resource allocation”** and **“UAV application scenario”** onto:
  - Non-RT RIC rApps (ML model training on UAV flight-path + RAN KPIs)
  - Near-RT RIC xApps (KPM + UAV policy + RC actuator)
- Integrate with existing **RC xApp** implementations (e.g. `ric-app-rc`) instead of re‑implementing the full E2SM_RC stack.
- Provide a Claude-friendly layout (skills, subagents, commands) so Claude Code can gradually turn this into a working prototype.

You (Claude) should treat this repo as an *architecture + automation shell* around upstream O-RAN SC / FlexRIC components, not a fork of them.

## Ground rules for Claude

- Work in **small, reviewable steps**. Prefer “design → tests → code → docs”.
- Do *not* invent new O-RAN interfaces. Only use:
  - Non‑RT RIC ⇄ Near‑RT RIC: A1 / A1-EI, offline data channels
  - Near‑RT RIC ⇄ E2 Nodes: E2AP with E2SM_KPM and E2SM_RC
- Assume:
  - Simulation with srsRAN, ns-O-RAN, or OSC near‑RT RIC testbeds.
  - RC xApp implemented externally (e.g. `o-ran-sc/ric-app-rc`); this repo only talks to it via **gRPC + JSON configs**.

Always keep **UAV use cases** in `spec/uav_oran_usecase.md` as the source of truth for requirements.

## Repo layout

- `README.md` – high-level overview and getting-started instructions.
- `spec/uav_oran_usecase.md` – text version of the O-RAN UAV use-case sections (user-provided).
- `docs/architecture.md` – system architecture notes and data-flow between rApp/xApps.
- `xapps/rc-grpc-client/` – thin Python client that talks to the RC xApp’s gRPC API.
- `xapps/uav-policy/` – main near‑RT RIC policy logic for UAV resource allocation.
- `skills/` – Claude Skills tuned for O-RAN / UAV work.
- `subagents/` – role-specialized subagents (architect, xApp dev, simulation, QA).
- `commands/` – high-level workflows Claude can follow (init project, run sim, design policy).

When adding new files, please keep this list in sync.

## Recommended development workflow (for Claude Code)

1. **Orient**
   - Skim `spec/uav_oran_usecase.md` and `docs/architecture.md`.
   - Inspect `xapps/uav-policy/policy_engine.py` and `xapps/rc-grpc-client/client.py` to see current abstractions.
2. **Design before code**
   - For any new feature, first update `docs/architecture.md` (or add a new design doc) with:
     - goal, inputs/outputs, main data structures, and failure modes.
3. **Tests first**
   - Create or extend tests in `xapps/uav-policy/tests/` (they can be simple, synthetic unit tests).
   - Focus on *pure* logic: mapping UAV state + channel KPIs → abstract “resource allocation decisions”.
4. **Implement**
   - Modify `policy_engine.py` and `integration.py` to satisfy the tests.
   - Only touch `rc-grpc-client` when you really need new gRPC calls or control schemas.
5. **Wire to RC xApp**
   - Treat the RC xApp as a remote service:
     - Define a small, typed request/response schema in `xapps/rc-grpc-client/client.py`.
     - Map internal “resource allocation decisions” → one or more RC control messages.
   - Keep this mapping isolated so it can evolve with real E2SM_RC deployments.
6. **Run locally / in sim**
   - Provide simple CLI entry points in each xApp:
     - `python -m uav_policy.main` – runs policy loop in “dry-run” mode (no gRPC).
     - Later, add modes that talk to a live RC xApp instance or simulator.
7. **Document**
   - Update `README.md` and `docs/architecture.md` whenever the behavior or interfaces change.

## Coding conventions

- Language: **Python 3.11+** for glue/xApp scaffolding.
- Style:
  - Prefer `dataclasses` for value types.
  - Type-annotate public functions and key internal helpers.
  - Keep modules small and composable; avoid large God-classes.
- Dependencies:
  - Keep runtime deps minimal.
  - For gRPC, put generated code under `xapps/rc-grpc-client/proto/` or vendored from upstream.

## Domain model (simplified)

Core entities (in code):

- `UavState` – UAV id, 3D position, velocity, planned path segment id, slice id.
- `RadioSnapshot` – per-cell KPIs for this UAV (RSRP/RSRQ, PRB utilization, HO history).
- `ResourceDecision` – abstract decision from policy engine:
  - target cell / slice,
  - PRB quota / slice weight,
  - optional HO / measurement-config hints.

Core flows:

1. Non-RT RIC (out of scope here) trains ML model(s) and publishes model ids / policies.
2. `uav-policy` xApp:
   - fetches model or policy from non-RT RIC or config,
   - consumes `UavState` + `RadioSnapshot`,
   - produces `ResourceDecision`.
3. `rc-grpc-client`:
   - converts `ResourceDecision` into RC xApp gRPC requests,
   - RC xApp converts those into E2SM_RC messages towards DU/CU.

## How to use skills, subagents, and commands

- **Skills** in `skills/`:
  - Each skill focuses on one area (spec digestion, xApp scaffolding, simulation ops).
- **Subagents** in `subagents/`:
  - Use them when a task is big enough to split into roles.
- **Commands** in `commands/`:
  - Treat command docs as high-level playbooks.

## Safety / boundaries

- Do **not** include any real credentials, IPs, or proprietary operator configs in this repo.
- Keep this project focused on:
  - high-level RRM / policy logic,
  - public, open-source testbeds,
  - abstractions that can be implemented against multiple vendors.

---


## AI Patch Guardrails (for Claude Code)

You are Claude Code working on this repository.  
Your main responsibilities are:
- Help implement small, well-scoped changes.
- Respect existing architecture, tests, and maintainer feedback.
- Avoid over-engineering and premature abstraction.

**IMPORTANT: You MUST follow all rules in this section whenever you propose patches or edit files.**

---

### 0. General workflow

1. **Explore & understand before coding**
   - ALWAYS read the relevant files and existing tests first.
   - Summarize your understanding and planned changes before editing.
   - If anything is ambiguous, ask for clarification instead of guessing.

2. **Plan → Implement → Verify**
   - Make a short plan (“think hard”) before you start editing.
   - Keep changes minimal and focused on the requested task.
   - Always run the relevant tests or at least explain precisely how to run them.

3. **Respect project-local rules**
   - The rules below (imports, logging, Dockerfile, tests, etc.) come from real code review feedback.
   - Treat them as authoritative for this repository.

---

### 1. Function abstraction & structure

**IMPORTANT: DO NOT introduce premature abstractions.**

1. **No trivial wrapper functions**
   - If a function only:
     - has 1–2 lines, AND
     - just calls another function (e.g., `return compose_text_message(...)`),
     - and is used only 1–2 times,
   - THEN: DO NOT create a separate helper function for it.
   - Example: DO NOT create `create_error_message(lang_code: str)` that only wraps `compose_text_message(get_response(...))`.

2. **Rule of Three (YAGNI)**
   - 1st occurrence: write the code inline.
   - 2nd occurrence: copy-paste is acceptable.
   - 3rd occurrence: you MAY propose a helper.
   - 4th occurrence: you SHOULD refactor into a shared abstraction.
   - Any refactor MUST clearly improve readability and reduce real duplication, not just “cosmetic” wrapping.

3. **Handler vs implementation**
   - For public handlers, follow this pattern:
     - `handler()`:
       - Handles `try/except`.
       - Logs exceptions with `logger.exception(...)`.
       - Returns a standard error message.
     - `_handler_impl()`:
       - Contains business logic only.
   - DO NOT move complex business logic into the handler.

---

### 2. Python imports

**IMPORTANT: All imports MUST follow PEP 8 and be at module top-level.**

1. **Placement**
   - Place imports at the top of the file, after module comments/docstring.
   - DO NOT add imports inside functions or methods unless explicitly documented as an exception.

2. **Order**
   - Group imports as:
     1. Standard library
     2. Third-party libraries
     3. Local modules
   - Separate each group with a blank line.

3. **Example**

```python
# 1. Standard library
from typing import Dict, Optional

# 2. Third-party
from linebot.v3.messaging import TextMessage

# 3. Local modules
from src.modules.qna.constants import RESPONSE_DATA_PATH
from src.modules.utils import compose_text_message, get_response
```

---

### 3. Logging & error handling

1. **Use `logger.exception` in `except` blocks**
   - When catching unexpected errors in handlers, prefer:
     ```python
     except Exception as e:
         logger.exception(f"Error in qna_handler: {e}")
         return compose_text_message(
             get_response(RESPONSE_DATA_PATH, "error_message", lang_code)
         )
     ```
   - This captures the full stack trace at ERROR level.

2. **Separation of concerns**
   - Handlers:
     - Validate input.
     - Call `_impl`.
     - Catch and log unexpected errors.
   - `_impl` functions:
     - Contain business logic and can be unit-tested directly.

---

### 4. Dockerfile changes

**IMPORTANT: Keep runtime images slim and focused on runtime dependencies.**

1. **Base image**
   - Prefer minimal base images similar to:
     ```Dockerfile
     FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
     ```

2. **Dependency installation**
   - Copy only `pyproject.toml` and lockfiles before running the install command.
   - Install ONLY runtime dependencies inside the final image.
   - DO NOT install tools that are only required for:
     - type checking (e.g. pyright),
     - linters,
     - local development.
   - If such tools are needed, suggest:
     - a dev-only image, or
     - a separate `dev` target in the Dockerfile,
     - but DO NOT add them silently.

---

### 5. Code smell & refactoring

When you notice repetition:

1. **Do NOT refactor automatically just because you see repetition.**
   - First, check:
     - Is this “incidental” repetition (similar text but different semantics)?
     - Or “essential” repetition (same logic, same semantics)?

2. **Avoid shotgun surgery**
   - If a change requires modifying many different files and call sites for a small benefit, you are probably introducing a bad abstraction.
   - In that case:
     - Explain the tradeoffs.
     - Ask the user before proceeding with a large refactor.

---

### 6. Tests & TDD

**IMPORTANT: Tests must be meaningful, not just “green”.**

1. **Correct TDD order**
   - DO NOT follow:
     - “write tests → accept whatever output you get”.
   - Instead:
     - Read the existing implementation first.
     - Understand whether the feature is implemented or still TODO.
     - Design tests that match the intended behavior.
     - Then update implementation to satisfy those tests.

2. **Detect unimplemented features**
   - If you see any of the following:
     - `// TODO: implement this`
     - returning an **empty struct** (e.g., `Tracing: &SomeType{}`)
     - variables assigned but only used as `_ = variable`
     - golden files containing empty objects like `tracing: {}`
   - THEN:
     - Treat the feature as “NOT YET IMPLEMENTED”.
     - DO NOT write tests that pretend the feature is fully working.
     - Instead, you may:
       - Add clearly labeled placeholder tests, OR
       - Create a GitHub issue describing the missing implementation.

3. **Test naming**
   - Use precise names:
     - `valid-X` → tests the successful path.
     - `invalid-X` → tests error handling and validation failures.
     - `placeholder-X` → feature not yet fully implemented, placeholder coverage only.
   - DO NOT name a test `invalid-tracing` if it does not actually test invalid behavior.

4. **No skipped tests in new code**
   - DO NOT add tests with `t.Skip()` unless explicitly requested and clearly documented as a temporary measure.
   - All new tests you add SHOULD run and pass on CI.

5. **Avoid redundant tests**
   - Before adding a new test file:
     - Check existing E2E / integration tests.
     - If existing tests already cover the behavior, DO NOT add redundant tests.
   - Example: For minimal RBAC changes, prefer relying on existing E2E tests rather than adding new tests that just verify Kubernetes basics.

6. **Use standard library & project helpers**
   - In Go tests:
     - Prefer `strings.Contains` over custom substring checks.
     - Use existing helper packages (e.g. `ktesting/setup.go`) instead of building ad-hoc loggers or setups.

---

### 7. File selection & change scope

**IMPORTANT: Keep diffs minimal and focused.**

1. **Verify file usage before editing**
   - Before modifying a file:
     - Check if it is still used in the build/runtime.
     - For suspicious files (e.g., old generators like `kubebuilder-gen.go`):
       - Use `git grep` or build commands to confirm usage.
   - If a maintainer comment says “this file is not used anymore, better to delete it”:
     - DO NOT update the file.
     - Suggest deleting it instead, if appropriate for this PR.

2. **Minimal patch principle**
   - For tasks like “minimal RBAC fix”:
     - Focus only on the specific RBAC manifests mentioned by the issue or reviewer.
     - Avoid:
       - editing unrelated manifests,
       - adding new test suites,
       - touching generator files unless required.

3. **Respect project conventions**
   - Follow existing patterns in the codebase:
     - Same logging style.
     - Same error handling style.
     - Same file layout and naming conventions.

---

### 8. Human review & maintainer feedback

1. **Maintainer comments are authoritative**
   - When a reviewer (e.g. project maintainer) gives feedback like:
     - “These tests are unnecessary.”
     - “This file is unused; delete it instead of updating it.”
   - You MUST:
     - Treat this feedback as the source of truth for future edits.
     - Reflect these rules in your subsequent patches.

2. **Document learnings**
   - When you discover a new project-specific rule through review:
     - Propose an update to `CLAUDE.md` (or ask the user to add it).
     - Follow the updated rule consistently in future changes.

---

### 9. How to work with tests & golden files in this repo

1. **Golden files**
   - When adding or updating golden files (YAML, JSON, etc.):
     - Ensure they contain meaningful, non-empty configuration.
     - If the implementation is a placeholder, clearly mark the golden file as such with comments.
     - Question suspicious emptiness (e.g., `tracing: {}`) and check whether the feature is really implemented.

2. **Creating follow-up issues**
   - If you identify missing behavior (e.g., tracing translation not fully implemented):
     - Propose creating a GitHub issue with:
       - Title, e.g.: `"Implement tracing translation in AgentgatewayPolicy frontend"`.
       - Links to the relevant PR / tests / files.
       - A plan for implementation and test updates.

---

### 10. Claude Code behavior summary (TL;DR)

When generating patches in this repo, you MUST:

- **Understand before coding**: read implementation & tests first.
- **Keep changes minimal**: avoid editing unused files or adding redundant tests.
- **Avoid premature abstraction**: no one-line wrappers unless used ≥3 times AND more readable.
- **Follow local style**: imports at top, logging via `logger.exception`, handler + `_impl` split, slim Dockerfiles.
- **Design meaningful tests**: no fake “invalid” tests, no `t.Skip()` tests, no empty golden files unless clearly marked as placeholders.
- **Respect maintainers**: treat review comments as project rules and adjust your behavior accordingly.

If you are unsure which rule applies, you MUST stop, summarize the options, and ask the user for guidance before making large-scale or irreversible changes.
