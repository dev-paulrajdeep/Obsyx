# Task Brief — <ID>: <short title>

- **Status:** Proposed | Ready | In Progress | Blocked | Review | Done
- **Milestone:** <roadmap phase / issue / milestone>
- **Primary owner:** <one agent or human>
- **Reviewer:** <usually obsyx-verifier for implementation>
- **Dependencies:** <accepted contract, prerequisite issue, tools>
- **Branch/worktree:** <name>

## Goal

<One measurable outcome and why it matters.>

## Current state and evidence

<Relevant paths, observed behavior, command output, or line references. Separate fact from assumption.>

## In scope

- `<exact/path/**>`

## Out of scope / forbidden paths

- `<paths that must not change>`
- No unrelated cleanup or broad refactor.

## Contract and assumptions

- **Accepted contract/ADR:** <path or “not required”; implementation must stop if required contract is missing>
- **Assumptions:** <explicit list>
- **Open decisions:** <questions to resolve before implementation>

## Acceptance criteria

- [ ] <Observable, objective result>
- [ ] <Expected failure/edge case behavior>
- [ ] <Documentation or handoff evidence>

## Verification plan

| Check | Exact command or procedure | Expected result | Status/evidence |
|---|---|---|---|
| Static | `<command that exists or will be introduced>` | `<expected>` | NOT TESTED |
| Unit/integration | `<command/procedure>` | `<expected>` | NOT TESTED |
| Runtime/VM (if applicable) | `<safe procedure>` | `<expected>` | NOT TESTED |

## Safety and risk

- **Potential destructive/external actions:** <none or detail>
- **VM required?:** Yes | No
- **Host impact allowed:** No by default; any exception requires explicit human approval.
- **Rollback/disposal:** <steps>
- **Stop conditions:** <conditions that require stopping and reporting>

## Handoff requirements

- Changed files and brief purpose
- Exact commands, exit codes, and actual results
- Acceptance criterion status with evidence
- Known risks, follow-up work, blocked/not-tested checks
- No merge/release claim unless the maintainer approved it
