# Agent Ownership and Interfaces

This matrix is the default boundary contract. Paths marked for future OS work may not exist yet; ownership does not imply implementation status.

| Role | Owns/writes | May inspect | Must not change without reassignment |
|---|---|---|---|
| Primary agent — Obsyx Lead / Orchestrator | `ROADMAP.md`; task assignment/integration decisions; cross-cutting changes explicitly assigned by the human | Entire repo | Must not claim tests passed without evidence; must not publish or merge without maintainer authorization |
| `obsyx-architect` | `.agents/contracts/**`; `docs/os-architecture/**`; `os/manifests/**` | Entire repo | ISO profiles, installer/system code, tests, CI, desktop runtime, roadmap |
| `obsyx-os-builder` | `os/iso/**`; `os/installer/**`; `os/system/**`; `os/scripts/**` | Contracts and current repo | Contracts/manifests/ADRs, `os/tests/**`, CI, desktop runtime, roadmap |
| `obsyx-verifier` | `os/tests/**`; `.github/workflows/os-ci.yml`; `docs/agent-workflow/reports/**`; verification artifacts explicitly assigned | Entire repo | Production implementation and architecture contracts; do not rewrite code to make tests pass |

## Interface sequence

1. **Architect → Builder:** accepted contract/ADR; manifest schema and assumptions; path ownership; commands/interfaces; error and rollback behavior; testable acceptance criteria.
2. **Builder → Verifier:** implementation commit/diff; exact build/test commands; expected behavior; known limits; no assertion without evidence.
3. **Verifier → Primary:** criterion-by-criterion status; exact commands/results; defects with paths and reproduction steps; blocked/not-tested cases.
4. **Primary → Maintainer:** diff summary, acceptance evidence, open risks, proposed merge/next task. The human maintainer keeps final control.

## Conflict protocol

- If a task needs files owned by another role, stop before editing and request a scoped handoff.
- If two tasks would edit one file, serialize them or create distinct files/interfaces first.
- Shared contracts are frozen during parallel implementation; proposed changes return to the architect and primary agent.
- Only change ownership by editing this matrix first and explicitly notifying affected task owners.

## Existing desktop paths

The current desktop paths (`core/`, `hypr/`, `waybar/`, `rofi/`, `swaync/`, `kitty/`, `wlogout/`, `profiles/`, `user/`, `tools/`) are outside the OS builder's default write scope. Desktop and OS integration work must state exactly which boundary it changes.
