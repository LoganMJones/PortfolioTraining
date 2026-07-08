# Portfolio Template — 10 Layouts

Ten portfolio designs for graduate school and professional development. **Preview on the demo site, then use the template for your chosen layout.**

**Live demo:** [loganmjones.github.io/PortfolioTraining](https://loganmjones.github.io/PortfolioTraining/)

---

## Start here

1. **[Preview layouts](index.html)** on the live demo
2. **[Use your layout's template](guide.html#get-layout)** on GitHub — one repo per layout
3. **Enable GitHub Pages** — follow the setup guide
4. **Edit `index.html`** — search for `EDIT HERE`

| Layout | Template repository | ZIP |
|--------|---------------------|-----|
| Document | [PortfolioTraining-document](https://github.com/LoganMJones/PortfolioTraining-document) | [document.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/document.zip) |
| Classic | [PortfolioTraining-classic](https://github.com/LoganMJones/PortfolioTraining-classic) | [classic.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/classic.zip) |
| Minimal | [PortfolioTraining-minimal](https://github.com/LoganMJones/PortfolioTraining-minimal) | [minimal.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/minimal.zip) |
| Terminal | [PortfolioTraining-terminal](https://github.com/LoganMJones/PortfolioTraining-terminal) | [terminal.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/terminal.zip) |
| Brutalist | [PortfolioTraining-brutalist](https://github.com/LoganMJones/PortfolioTraining-brutalist) | [brutalist.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/brutalist.zip) |
| Deck | [PortfolioTraining-deck](https://github.com/LoganMJones/PortfolioTraining-deck) | [deck.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/deck.zip) |
| Editorial | [PortfolioTraining-editorial](https://github.com/LoganMJones/PortfolioTraining-editorial) | [editorial.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/editorial.zip) |
| Bold | [PortfolioTraining-bold](https://github.com/LoganMJones/PortfolioTraining-bold) | [bold.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/bold.zip) |
| Academic | [PortfolioTraining-academic](https://github.com/LoganMJones/PortfolioTraining-academic) | [academic.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/academic.zip) |
| Creative | [PortfolioTraining-creative](https://github.com/LoganMJones/PortfolioTraining-creative) | [creative.zip](https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips/creative.zip) |

> **Instructors:** use [PortfolioTraining](https://github.com/LoganMJones/PortfolioTraining) (this repo) to demo all 10 layouts.  
> **Students:** preview here, then **Use this template** on the single layout you chose.

**Contact the architect:** [Logan Jones](https://www.loganjones.org/)

**Built with:** This entire project was architected by Logan Jones with [Cursor AI](https://cursor.com/) assistance.

---

## Maintainer: publish template repos

**Do changes reach the individual template repos automatically?** Not by default. The flow is:

1. Edit `themes/`, `css/`, scripts, or `theme-checklists.json` in this repo
2. Regenerate packages: `./scripts/regenerate-all.sh`
3. Sync to `PortfolioTraining-{layout}` repos: `./scripts/publish-template-repos.sh`

**Automatic option:** A GitHub Actions workflow (`.github/workflows/publish-templates.yml`) can run steps 2–3 on every push to `main`. One-time setup:

1. Create a [fine-grained personal access token](https://github.com/settings/tokens?type=beta) with **Contents: Read and write** on this repo and all `PortfolioTraining-*` template repos.
2. In this repo go to **Settings → Secrets and variables → Actions** and add `TEMPLATE_PUBLISH_TOKEN` with that PAT.
3. Push to `main` — the workflow regenerates `solo/`, commits ZIPs, and force-pushes each layout repo.

You can also trigger it manually from the **Actions** tab → **Publish template repos** → **Run workflow**.

Manual commands (same as CI):

```bash
./scripts/regenerate-all.sh
./scripts/publish-template-repos.sh   # requires GitHub CLI (gh auth login)
```

This creates/updates `LoganMJones/PortfolioTraining-{layout}` as GitHub template repositories.

---

MIT License · Kellogg REU Portfolio Training
