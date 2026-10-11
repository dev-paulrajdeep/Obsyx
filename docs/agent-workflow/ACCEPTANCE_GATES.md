# Acceptance Gates

A status is meaningful only with evidence. Use `PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED` for every applicable gate.

## Repository-first workflow gate

- [ ] Required agent, skill, template, and ownership files exist.
- [ ] Each custom agent has valid-looking YAML frontmatter with unique `name`, `description`, `subagent`, `mainAgent`, model, execution policy, and only documented tool identifiers.
- [ ] Every agent has a single write boundary and explicit forbidden paths.
- [ ] Task template requires one owner, scope boundaries, testable criteria, exact verification commands, and handoff evidence.
- [ ] Safety instructions prohibit host-disk destructive tests and require verified disposable VM/disk boundaries.
- [ ] No OS implementation status is implied by the existence of these definitions.
- [ ] Local scaffold validator passes.
- [ ] Antigravity runtime discovery is manually checked in the installed version.

## OS milestone gates (future; not satisfied by the scaffold)

1. **Contract gate:** base package policy and manifest schema reviewed; interfaces frozen.
2. **ISO build gate:** image is built from a documented profile; build logs and digest recorded.
3. **UEFI boot gate:** ISO boots in a clean, disposable UEFI VM; evidence recorded.
4. **Live-session gate:** networking and desktop session work sufficiently for the milestone; failures are logged.
5. **Install gate:** installer targets a dedicated virtual disk only; destructive operations and failure behavior are tested.
6. **First-boot gate:** installed VM reboots successfully and reaches a usable session; basic service/network checks pass.
7. **Release gate:** source revision, artifacts, checksum, release notes, licensing review, and signature policy are present; human maintainer approves release.

Passing an earlier gate never implies a later gate passed.
