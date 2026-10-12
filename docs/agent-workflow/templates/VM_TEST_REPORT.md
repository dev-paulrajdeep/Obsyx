# ObsyxOS VM Test Report — <task/release ID>

## Environment

- **Tester/agent:**
- **Date/time:**
- **Hypervisor/version:**
- **Host OS:** <record only necessary version details; no secrets>
- **VM firmware:** UEFI | BIOS
- **VM vCPU / RAM:**
- **Target virtual disk size and configured identifier:**
- **Evidence the target is a dedicated disposable virtual disk:** <VM configuration path/screenshot and read-only in-guest device output>
- **ISO path and SHA-256:**
- **Test branch/commit:**

## Safety preflight

- [ ] Test is inside a disposable VM; no target-disk operations are being run on the host.
- [ ] VM configuration shows a dedicated virtual disk for this test.
- [ ] Target device identity has been checked read-only inside the VM.
- [ ] The disk can be discarded after the test; cleanup plan is known.
- [ ] No secrets or personal data are included in evidence.

If any safety box cannot be checked, stop. Set the result to `BLOCKED` and do not run destructive steps.

## Results

| Check | Status | Exact steps/command | Evidence | Notes |
|---|---|---|---|---|
| ISO build | NOT TESTED | | | |
| UEFI ISO boot | NOT TESTED | | | |
| Live session reaches usable desktop | NOT TESTED | | | |
| Networking | NOT TESTED | | | |
| Installer dry-run/mock path | NOT TESTED | | | |
| Install to dedicated virtual disk | NOT TESTED | | | |
| First reboot into installed system | NOT TESTED | | | |
| Basic session/services after reboot | NOT TESTED | | | |
| Cleanup/disposal | NOT TESTED | | | |

## Failures and recovery

<Failure details, logs, rollback/disposal, and whether the VM was reset.>

## Overall result

**PASS | FAIL | BLOCKED | NOT TESTED** — <evidence-based reason>
