#!/usr/bin/env bash
# Publish each solo/ folder as a separate GitHub template repository.
# Prerequisites: git, GitHub CLI (gh), and `gh auth login`
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ORG="LoganMJones"
PREFIX="PortfolioTraining"

THEMES=(
  document classic minimal terminal brutalist deck
  editorial bold academic creative
)

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: GitHub CLI (gh) is required. Install: https://cli.github.com/"
  exit 1
fi

for theme in "${THEMES[@]}"; do
  REPO="${ORG}/${PREFIX}-${theme}"
  DIR="${ROOT}/solo/${theme}"
  echo "=== Publishing ${REPO} ==="

  if [[ ! -d "$DIR" ]]; then
    echo "Missing ${DIR} — run: python3 scripts/build-solo.py"
    exit 1
  fi

  rm -rf "${DIR}/.git"
  git -C "$DIR" init -b main
  git -C "$DIR" add -A
  git -C "$DIR" commit -m "Initial commit: ${theme} portfolio template"

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
echo "Done. Update templates.json / guide links if repo names changed."
echo "Main project: ${ORG}/${PREFIX}"
