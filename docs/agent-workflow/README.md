# ObsyxOS Agent Workflow (Gemini Antigravity)

This scaffold adds repository-local agent roles and repeatable task procedures without changing the desktop implementation. It is designed for the current Antigravity agent/skills format.

## Structure

```text
.agents/
├── AGENTS.md                         # Always-on project operating contract
├── agents/
│   ├── obsyx-architect/agent.md            # Architecture/contracts/manifest owner
│   ├── obsyx-os-builder/agent.md           # ISO/installer/system implementation owner
│   └── obsyx-verifier/agent.md             # Independent QA/OS CI/evidence owner
└── skills/
    ├── obsyx-task/SKILL.md           # /obsyx-task
    ├── obsyx-vm-safety/SKILL.md      # /obsyx-vm-safety
    └── obsyx-release-readiness/SKILL.md # /obsyx-release-readiness

docs/agent-workflow/
├── OWNERSHIP.md
├── ACCEPTANCE_GATES.md
├── templates/
└── examples/
```

The `os/**`, `.agents/contracts/**`, and `.github/workflows/os-ci.yml` entries in the ownership matrix describe reserved future ownership boundaries. They are not evidence that the actual OS implementation already exists.

## Install into the Obsyx repository

1. Create a working branch and inspect the archive.
2. Extract the archive's contents into the **Obsyx repository root**. Do not extract into `docs/agent-workflow/`.
3. Inspect the diff and keep the existing `README.md` and `ROADMAP.md` untouched unless a separate task explicitly requires editing them.
4. Open/reload the project in Antigravity. Confirm that the specialist agent files appear in the available custom-agent list and that the three skills can be invoked.
5. Run `python tools/validate_agent_workflow.py` from the repository root after copying the files. The validator checks this scaffold's required files and core metadata; it does not prove Antigravity runtime discovery.
6. Use the first task in `examples/` as a bounded smoke test. Ask the primary agent to plan before delegating; do not ask agents to modify OS implementation before the repository audit and interface contract are accepted.

If your Antigravity build exposes custom agents only in Antigravity 2.0/CLI rather than the IDE UI, the definitions remain repository-local and version-controlled; use the supported agent manager in the installed Antigravity version to verify discovery before relying on delegation. Skills provide the portable task procedures and slash-command workflow.

## Recommended first run

Invoke `/obsyx-task` with the example task `TASK-0001-repository-audit.md`. Its expected result is an evidence-based inventory and a proposed next task, not a bootable ISO or a claim of OS readiness.

## Working style

- One implementation owner per task; one writer per file at a time.
- Architect first when interfaces or package policy are unresolved.
- Builder implements only against an accepted contract.
- Verifier independently checks acceptance; it does not edit production implementation.
- Primary agent/human owns integration, roadmap changes, merge, signing, publishing, and release decisions.
- Destructive OS testing is VM-only, with a dedicated virtual disk whose identity is verified.
