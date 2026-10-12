#!/usr/bin/env bash
# Obsyx - Automated Safe Installer Wrapper
# Direct executable script for installing Obsyx desktop configuration.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ "$#" -eq 0 ] && [ -t 0 ]; then
    exec "${REPO_ROOT}/bin/obsyx" install --interactive
else
    exec "${REPO_ROOT}/bin/obsyx" install "$@"
fi
