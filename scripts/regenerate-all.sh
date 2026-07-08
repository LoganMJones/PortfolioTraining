#!/usr/bin/env bash
# Regenerate theme injections and solo/ packages from source themes.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT"
python3 scripts/add-fill-checklists.py
python3 scripts/add-template-credit.py
python3 scripts/build-solo.py

echo ""
echo "Done. solo/ packages rebuilt."
echo "Publish template repos: ./scripts/publish-template-repos.sh"
echo "Or push to main — GitHub Actions can publish automatically if configured."
