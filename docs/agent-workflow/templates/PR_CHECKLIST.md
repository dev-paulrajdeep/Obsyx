# ObsyxOS Pull Request Checklist

## Scope and ownership
- [ ] The task brief exists and acceptance criteria are measurable.
- [ ] Changes stay inside the assigned paths; cross-boundary changes have an explicit handoff.
- [ ] No two-agent concurrent writes occurred on the same file.
- [ ] Desktop behavior was not changed unintentionally.

## Engineering
- [ ] Architecture contract/ADR is accepted where required.
- [ ] Tests cover expected behavior and relevant failure cases.
- [ ] Exact commands and outcomes are reported; skipped checks are listed.
- [ ] No hardcoded secrets, personal data, or machine-specific credentials.
- [ ] Docs, package manifests, permissions, and licensing/attribution notes are updated as needed.

## OS safety and evidence
- [ ] No destructive host-disk or host boot configuration operation was performed.
- [ ] Any destructive OS installation test used a verified disposable VM and dedicated virtual disk.
- [ ] Static checks, ISO build, VM boot, installation, first boot, and real hardware are reported as separate statuses.
- [ ] Release claims have supporting logs/artifacts and checksums; signatures are only claimed as verified if actually verified.

## Review
- [ ] Independent verifier report is attached or explicitly marked not required.
- [ ] Remaining risks and follow-up tasks are described.
- [ ] Primary agent/human maintainer has reviewed the diff.
- [ ] No automatic merge, tag, signature, or publication without maintainer authorization.
