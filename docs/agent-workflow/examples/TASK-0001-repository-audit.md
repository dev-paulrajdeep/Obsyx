# Task Brief — TASK-0001: Repository and OS Readiness Audit

- **Status:** Ready
- **Milestone:** Repository-first workflow bootstrap
- **Primary owner:** obsyx-architect
- **Reviewer:** obsyx-verifier
- **Dependencies:** Agent scaffold installed; `ROADMAP.md` and `README.md` readable
- **Branch/worktree:** `chore/antigravity-agent-workflow` (suggested; maintainer may rename)

## Goal

Produce an evidence-based inventory of the existing Obsyx repository and a prioritized first OS engineering task. Do not implement the ISO or installer in this task.

## Current state and evidence

The roadmap describes Obsyx Desktop and Obsyx OS as separate deliverables and states that distro-specific engineering has not started. Verify this against the current checkout and identify any drift.

## In scope

- Read `README.md`, `ROADMAP.md`, existing CI, `tools/`, desktop module structure, and tests.
- Add or update only `docs/os-architecture/repository-audit.md` and `docs/os-architecture/decisions/` if needed, subject to the architect's ownership.
- Produce a list of existing build/test commands supported by repository files.
- Recommend one minimal next task and its acceptance criteria.

## Out of scope / forbidden paths

- Do not modify desktop production code.
- Do not create the live ISO or installer.
- Do not claim boot, installation, or hardware compatibility.
- Do not edit `ROADMAP.md` without primary-agent approval.

## Acceptance criteria

- [ ] Audit lists the actual top-level paths and relevant existing build/test commands with evidence.
- [ ] Existing desktop functionality is separated from missing OS layers.
- [ ] Missing prerequisites and open architecture decisions are explicit.
- [ ] A single next task is recommended with bounded paths and testable criteria.
- [ ] Verifier independently confirms audit claims against the repo.

## Verification plan

| Check | Exact command or procedure | Expected result | Status/evidence |
|---|---|---|---|
| Repository inventory | `find . -maxdepth 2 -type f -not -path './.git/*' | sort` | Actual list captured | NOT TESTED |
| Existing tests/build | Inspect repo docs and CI; run only commands documented by repo | Supported commands and outcomes recorded | NOT TESTED |
| Independent audit | Verifier checks cited paths and commands | No material unsupported claims | NOT TESTED |

## Safety and risk

- **Potential destructive/external actions:** None permitted
- **VM required?:** No
- **Host impact allowed:** No writes beyond architect-owned audit/ADR paths
- **Stop conditions:** Missing or conflicting project documentation; report conflict rather than silently reconciling it
