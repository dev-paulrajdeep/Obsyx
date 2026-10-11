---
name: obsyx-task
description: Plan and execute a bounded ObsyxOS engineering task using single-writer ownership, architecture contracts, specialist handoffs, and evidence-based acceptance criteria. Use for new tasks, roadmap milestones, implementation requests, and multi-agent work.
---

# ObsyxOS Task Workflow

Run this sequence for each non-trivial request.

## 1. Inspect before planning

- Read `ROADMAP.md`, `README.md`, `.agents/AGENTS.md`, and `docs/agent-workflow/OWNERSHIP.md`.
- Inspect relevant paths and existing tests. Do not assume that roadmap checkboxes describe current code unless checked against the repository.
- Identify whether the request is for Obsyx Desktop or Obsyx OS.

## 2. Write a task brief

Copy `docs/agent-workflow/templates/TASK.md`. Fill in:

- measurable goal and motivation;
- current state with file/line evidence where available;
- one implementation owner;
- allowed and forbidden paths;
- dependencies and contract status;
- observable acceptance criteria;
- safe verification commands and safety constraints;
- explicit non-goals.

Do not dispatch implementation while a necessary interface is unresolved. Ask `obsyx-architect` to produce or revise the contract first.

## 3. Delegate by boundary

- Architecture, package manifest, or interface decision: `obsyx-architect`.
- ISO, installer, or system integration implementation: `obsyx-os-builder`, only after its contract is accepted.
- Tests, CI, safety review, or independent acceptance review: `obsyx-verifier`.

The primary agent remains the orchestrator. Prefer isolated branches/worktrees for parallel tasks. Never have two agents edit the same file concurrently. Use parallel work only after path ownership and interface contracts are stable.

## 4. Execute one owner at a time per file set

Give each agent the filled task brief and ask it to report with `docs/agent-workflow/templates/HANDOFF.md`. Require actual command output/status. When a task crosses boundaries, hand off the artifact and acceptance criteria explicitly.

## 5. Independently verify

Ask `obsyx-verifier` to compare the change with the brief and run the applicable checks. Follow `/obsyx-vm-safety` for destructive OS tests. If tests are unavailable, report `BLOCKED` or `NOT TESTED`; never silently skip them.

## 6. Integrate and report

Review the diff, task scope, tests, acceptance evidence, documentation, and safety implications. Only the primary agent/human maintainer approves merges, roadmap status changes, and releases. Summarize changed files, results, known risks, and the next smallest step.

## Required status vocabulary

- **PASS** — acceptance criteria were verified with evidence.
- **FAIL** — at least one criterion failed.
- **BLOCKED** — a prerequisite prevents a required check or implementation step.
- **NOT TESTED** — no evidence was produced for that check.

Never treat a successful static check as evidence of runtime boot or installation success.
