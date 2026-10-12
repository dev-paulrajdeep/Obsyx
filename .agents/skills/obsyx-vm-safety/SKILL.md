---
name: obsyx-vm-safety
description: Plan and validate safe ObsyxOS ISO boot and installer tests using disposable virtual machines and virtual disks only. Use before any partitioning, filesystem formatting, installation, bootloader, or target-root test.
---

# VM-Only Destructive Test Safety

This skill is a hard gate for every destructive OS test. If any precondition is uncertain, stop and report `BLOCKED`.

## Forbidden on the host

Never execute destructive or target-system commands against the workstation, including but not limited to `mkfs.*`, `wipefs`, `dd` targeting a block device, `fdisk`, `parted`, `sgdisk`, `sfdisk`, `cryptsetup luksFormat`, installer partitioning, bootloader installation, or writes to the host's `/boot`, EFI System Partition, or root filesystem. Do not run the target installer using host privileges. Do not use host `sudo` for installer testing.

A device named `/dev/vda`, `/dev/sda`, or `/dev/nvme0n1` is not proof that it is disposable.

## Required preconditions

Before a destructive command is even proposed for execution, establish and record all of the following:

1. The test runs inside a disposable VM, not on the workstation.
2. The VM's configuration identifies its attached target as a dedicated virtual disk created for this test.
3. The virtual disk contains no user data and can be discarded after the test.
4. The target device identity has been confirmed from inside the VM using read-only inspection, and it matches the VM configuration.
5. The test plan states the exact target device, expected destructive effect, restore/disposal method, and stop conditions.
6. The operator has the required explicit approval where the environment prompts for it.

If the agent cannot independently confirm the VM boundary and disk identity, do not run the command. Request a human-provided test environment or provide a non-destructive test plan instead.

## Safe testing sequence

1. Run static validation and unit tests first.
2. Build the ISO without modifying host disks.
3. Record the ISO path and SHA-256 digest.
4. Boot the ISO in a disposable UEFI VM without installing.
5. Test installer UI/logic with mock or dry-run fixtures where available.
6. Only then consider installation to the verified disposable virtual disk.
7. After installation, verify reboot and basic system/session startup inside that VM.
8. Dispose of the virtual disk/VM and record evidence.

## Evidence and status

Use `docs/agent-workflow/templates/VM_TEST_REPORT.md`. Record hypervisor, VM firmware mode, memory/CPU, virtual disk size/identity, ISO digest, steps, outcomes, logs/screenshots, and cleanup. Never include secrets. Distinguish ISO build, live boot, installation, reboot, and hardware compatibility claims.
