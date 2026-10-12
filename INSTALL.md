# Install the ObsyxOS Antigravity Agent Workflow

1. From the Obsyx repository, create a clean branch, for example:
   ```bash
   git switch -c chore/antigravity-agent-workflow
   ```
2. Extract the archive contents into the repository root (the directory that contains `README.md` and `ROADMAP.md`). Use a no-overwrite extraction mode so existing files are not replaced.
3. Review the copied files and run:
   ```bash
   python tools/validate_agent_workflow.py
   ```
4. Reload the repository in Antigravity. Verify the three custom agents are discoverable in the agent manager and test `/obsyx-task`, `/obsyx-vm-safety`, and `/obsyx-release-readiness`.
5. Run the bounded repository-audit task in `docs/agent-workflow/examples/TASK-0001-repository-audit.md` before starting OS implementation.

The validator proves only structural completeness. Runtime discovery and real agent behavior must be checked in the installed Antigravity version. This package does not build an ISO, run an installer, install dependencies, or modify the host system.
