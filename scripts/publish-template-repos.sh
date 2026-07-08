#!/usr/bin/env bash
# Publish each solo/ folder as a separate GitHub template repository.
# Prerequisites: git, GitHub CLI (gh), and `gh auth login` (or GH_TOKEN in CI)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ORG="LoganMJones"
PREFIX="PortfolioTraining"
SOURCE_SHA="$(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo "local")"
SYNC_MSG="Sync from ${PREFIX}@${SOURCE_SHA}"

THEMES=(
  document classic minimal terminal brutalist deck
  editorial bold academic creative
)

if ! command -v gh >/dev/null 2>&1; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  LOCAL_GH="${SCRIPT_DIR}/../.tools/gh_2.96.0_macOS_arm64/bin/gh"
  if [[ -x "$LOCAL_GH" ]]; then
    gh() { "$LOCAL_GH" "$@"; }
  else
    echo "Error: GitHub CLI (gh) is required. Install: https://cli.github.com/"
    echo "Or run from repo root after downloading gh to .tools/"
    exit 1
  fi
fi

if [[ -z "${GH_TOKEN:-}" ]] && ! gh auth status >/dev/null 2>&1; then
  echo "Error: gh is not authenticated. Run: gh auth login"
  echo "In CI, set GH_TOKEN or repository secret TEMPLATE_PUBLISH_TOKEN."
  exit 1
fi

for theme in "${THEMES[@]}"; do
  REPO="${ORG}/${PREFIX}-${theme}"
  DIR="${ROOT}/solo/${theme}"
  echo "=== Publishing ${REPO} ==="

  if [[ ! -d "$DIR" ]]; then
    echo "Missing ${DIR} — run: ./scripts/regenerate-all.sh"
    exit 1
  fi

  rm -rf "${DIR}/.git"
  git -C "$DIR" init -b main
  git -C "$DIR" add -A
  git -C "$DIR" commit -m "${SYNC_MSG}"

  if gh repo view "$REPO" >/dev/null 2>&1; then
    echo "Repo exists — force pushing main"
    git -C "$DIR" remote add origin "https://github.com/${REPO}.git" 2>/dev/null || \
      git -C "$DIR" remote set-url origin "https://github.com/${REPO}.git"
    git -C "$DIR" push -u origin main --force
  else
    gh repo create "$REPO" --public --source="$DIR" --remote=origin --push \
      --description "Portfolio template — ${theme} layout (Portfolio Training)"
  fi

  gh repo edit "$REPO" --enable-issues=false --enable-wiki=false
  gh api -X PATCH "repos/${REPO}" -f is_template=true
  echo "✓ ${REPO} (template enabled)"
done

echo ""
echo "Done. Template repos synced from ${SYNC_MSG}."
echo "Main project: ${ORG}/${PREFIX}"
