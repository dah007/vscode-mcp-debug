#!/usr/bin/env bash
set -euo pipefail

# Run quick CI-style checks for the development server
# Exits non-zero if any check fails

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

echo "Running endpoint checks..."
bash "$SCRIPT_DIR/check_endpoints.sh"
echo "All CI checks passed."
