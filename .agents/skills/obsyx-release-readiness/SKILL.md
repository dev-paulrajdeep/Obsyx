---
name: obsyx-release-readiness
description: Evaluate whether an ObsyxOS change or ISO candidate meets repository, test, VM, security, documentation, and release-evidence gates before a maintainer considers merging or publishing it.
---

# ObsyxOS Release Readiness Gate

Do not publish or claim a release. Produce a readiness assessment for the human maintainer.

## Gate A — Repository integrity

- Review the full diff and ensure changes stay within the task scope.
- Check package manifests, build inputs, dependency assumptions, file permissions, and licensing notes where applicable.
- Confirm no secrets, credentials, machine-specific paths, or unreviewed binary artifacts were added.

## Gate B — Automated checks

- Run only validation commands that exist in the repository or are specified in the task contract.
- Record exact command, exit code, and result.
- Verify failure paths are tested where relevant; do not hide or downgrade failing checks.

## Gate C — OS behavior evidence

Mark the following separately: `ISO BUILT`, `UEFI LIVE BOOT`, `LIVE SESSION`, `INSTALLER`, `INSTALLED SYSTEM FIRST BOOT`, `UPDATE/RECOVERY`, and `REAL HARDWARE`. Each must be `PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED` with evidence.

Any destructive test must follow `/obsyx-vm-safety` and use a disposable VM/disk only. Lack of a VM test is not a pass.

## Gate D — Distribution artifacts

For a release candidate, check ISO size/path, SHA-256 digest, release notes, build commit, source revision, licensing/attribution, and signature verification plan. Do not claim a signature is valid unless it was actually verified with the expected public key.

## Output

Return a concise table of gate, status, evidence, and blockers; list release-blocking defects; and recommend `READY FOR HUMAN REVIEW`, `NOT READY`, or `BLOCKED`. The maintainer owns all merge, tagging, signing, publishing, and release decisions.
