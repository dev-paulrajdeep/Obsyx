#!/usr/bin/env python3
"""Obsyx Release Packaging Tool.

Bundles release source tarball and generates SHA256 checksum in dist/.
Usage:
    python3 tools/package_release.py [--version VERSION] [--out-dir DIR]
"""

import argparse
import hashlib
import os
import tarfile
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_version_from_cli():
    """Extract version from bin/obsyx."""
    cli_path = os.path.join(REPO_ROOT, "bin", "obsyx")
    if os.path.isfile(cli_path):
        with open(cli_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("VERSION ="):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "0.1.0"


def should_exclude(tarinfo):
    """Filter out git, pycache, dist, and local override files."""
    excluded_names = {
        ".git",
        ".github",
        "__pycache__",
        ".cache",
        "dist",
        "build",
        "tmp",
        ".obsyx_profile",
        "profile.lua",
    }
    parts = tarinfo.name.split("/")
    for part in parts:
        if part in excluded_names or part.endswith(".pyc") or part.endswith(".swp"):
            return None
    return tarinfo


def build_release_archive(version: str, out_dir: str):
    """Create tar.gz archive and sha256 checksum."""
    os.makedirs(out_dir, exist_ok=True)
    archive_name = f"obsyx-v{version}.tar.gz"
    archive_path = os.path.join(out_dir, archive_name)
    checksum_path = f"{archive_path}.sha256"

    prefix = f"obsyx-v{version}"

    with tarfile.open(archive_path, "w:gz") as tar:
        for item in sorted(os.listdir(REPO_ROOT)):
            if item in {".git", "dist", "__pycache__", ".cache", "tmp", ".obsyx_profile"}:
                continue
            full_path = os.path.join(REPO_ROOT, item)
            arcname = f"{prefix}/{item}"
            tar.add(full_path, arcname=arcname, filter=should_exclude)

    # Compute SHA256
    sha256 = hashlib.sha256()
    with open(archive_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    digest = sha256.hexdigest()

    with open(checksum_path, "w", encoding="utf-8") as f:
        f.write(f"{digest}  {archive_name}\n")

    return archive_path, checksum_path, digest


def main():
    parser = argparse.ArgumentParser(description="Obsyx Release Archive Packager")
    parser.add_argument("--version", default=get_version_from_cli(), help="Release version (e.g. 0.1.0)")
    parser.add_argument("--out-dir", default=os.path.join(REPO_ROOT, "dist"), help="Output directory")
    args = parser.parse_args()

    print(f"==> Packaging Obsyx v{args.version}...")
    archive_path, checksum_path, digest = build_release_archive(args.version, args.out_dir)

    size_mb = os.path.getsize(archive_path) / (1024 * 1024)
    print(f"[+] Archive:  {archive_path} ({size_mb:.2f} MB)")
    print(f"[+] Checksum: {checksum_path}")
    print(f"[+] SHA256:   {digest}")


if __name__ == "__main__":
    main()
