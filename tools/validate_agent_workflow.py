#!/usr/bin/env python3
"""Validate that the ObsyxOS Antigravity agent scaffold is structurally complete.

This uses only the Python standard library. It validates file presence and key
metadata but does not prove that Antigravity discovers or executes the agents.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ".agents/AGENTS.md",
    ".agents/agents/obsyx-architect/agent.md",
    ".agents/agents/obsyx-os-builder/agent.md",
    ".agents/agents/obsyx-verifier/agent.md",
    ".agents/skills/obsyx-task/SKILL.md",
    ".agents/skills/obsyx-vm-safety/SKILL.md",
    ".agents/skills/obsyx-release-readiness/SKILL.md",
    "docs/agent-workflow/OWNERSHIP.md",
    "docs/agent-workflow/ACCEPTANCE_GATES.md",
    "docs/agent-workflow/templates/TASK.md",
    "docs/agent-workflow/templates/HANDOFF.md",
    "docs/agent-workflow/templates/VM_TEST_REPORT.md",
    "docs/agent-workflow/templates/PR_CHECKLIST.md",
    "docs/agent-workflow/examples/TASK-0001-repository-audit.md",
]


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Missing or malformed YAML frontmatter: {path.relative_to(ROOT)}")
    return match.group(1)


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing required file: {relative}")

    agent_names: set[str] = set()
    agent_paths = [
        ".agents/agents/obsyx-architect/agent.md",
        ".agents/agents/obsyx-os-builder/agent.md",
        ".agents/agents/obsyx-verifier/agent.md",
    ]
    for rel in agent_paths:
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            fm = frontmatter(path)
            required_markers = ["name:", "description:", "subagent:", "mainAgent:", "model:", "commandExecutionPolicy:"]
            for marker in required_markers:
                if marker not in fm:
                    errors.append(f"{rel}: missing frontmatter marker {marker}")
            name_match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", fm)
            if name_match:
                name = name_match.group(1)
                if name in agent_names:
                    errors.append(f"Duplicate agent name: {name}")
                agent_names.add(name)
            if "commandExecutionPolicy: sandbox" not in fm:
                errors.append(f"{rel}: expected commandExecutionPolicy: sandbox")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))

    skill_paths = [
        ".agents/skills/obsyx-task/SKILL.md",
        ".agents/skills/obsyx-vm-safety/SKILL.md",
        ".agents/skills/obsyx-release-readiness/SKILL.md",
    ]
    for rel in skill_paths:
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            fm = frontmatter(path)
            if not re.search(r"(?m)^name:\s*obsyx-[a-z0-9-]+\s*$", fm):
                errors.append(f"{rel}: missing valid skill name")
            if not re.search(r"(?m)^description:\s*.+$", fm):
                errors.append(f"{rel}: missing skill description")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))

    safety = ROOT / ".agents/skills/obsyx-vm-safety/SKILL.md"
    if safety.exists():
        content = safety.read_text(encoding="utf-8")
        for phrase in ["disposable VM", "dedicated virtual disk", "stop", "host"]:
            if phrase.lower() not in content.lower():
                errors.append(f"VM safety skill: expected safety phrase {phrase!r}")

    if errors:
        print("Agent workflow validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Agent workflow validation: PASS")
    print(f"- {len(REQUIRED_FILES)} required files present")
    print(f"- {len(agent_names)} unique custom agent definitions have core metadata")
    print(f"- {len(skill_paths)} skill definitions have core metadata")
    print("- VM safety guardrails present")
    print("Note: Antigravity discovery must be verified in the installed app/version.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
