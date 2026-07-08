#!/usr/bin/env python3
"""Build solo/ layout packages — one self-contained zip per theme."""

import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "templates.json").read_text(encoding="utf-8"))
THEMES = list(CONFIG["themes"].keys())
LABELS = {k: v["label"] for k, v in CONFIG["themes"].items()}
GUIDE_URL = f"{CONFIG['projectUrl']}guide.html"
PROJECT_URL = CONFIG["projectUrl"]
ORG = CONFIG["githubOrg"]
PREFIX = CONFIG["repoPrefix"]
REPO_RAW = f"{CONFIG['projectRepo']}/raw/main/solo/zips"

SWITCHER_RE = re.compile(
    r"\n  <nav class=\"theme-switcher\".*?</nav>\n",
    re.DOTALL,
)


def template_repo_url(theme: str) -> str:
    return f"https://github.com/{ORG}/{PREFIX}-{theme}"


def make_shared_solo() -> str:
    text = (ROOT / "css" / "shared.css").read_text(encoding="utf-8")
    start = text.find("/* ── Theme switcher ── */")
    end = text.find("/* ── Solo layout download banner")
    if end == -1:
        end = text.find("/* ── Privacy notice")
    if start != -1 and end != -1:
        solo_start = text.find("/* ── Solo layout download banner")
        if solo_start != -1 and solo_start < end:
            end = solo_start
        text = text[:start] + text[end:]
    text = text.replace(
        ":root {\n  --theme-switcher-height: 2.75rem;\n}",
        ":root {\n  --theme-switcher-height: 0;\n}",
        1,
    )
    if "--theme-switcher-height: 0" not in text:
        text = ":root {\n  --theme-switcher-height: 0;\n}\n\n" + text
    # Remove solo-get banner styles from solo packages
    solo_banner_start = text.find("/* ── Solo layout download banner")
    solo_banner_end = text.find("/* ── Template attribution")
    if solo_banner_start != -1 and solo_banner_end != -1:
        text = text[:solo_banner_start] + text[solo_banner_end:]
    return text


def process_html(html: str, theme: str) -> str:
    html = SWITCHER_RE.sub("\n", html)
    html = re.sub(r'\n  <div class="solo-get".*?</div>\n', "\n", html, count=1, flags=re.DOTALL)
    html = html.replace("has-theme-switcher ", "")
    html = html.replace("../css/shared.css", "./css/shared.css")
    html = html.replace("../css/", "./css/")
    html = html.replace("../js/", "./js/")
    html = html.replace("../assets/", "./assets/")
    html = html.replace("../guide.html", GUIDE_URL)
    html = html.replace("../index.html", PROJECT_URL)
    html = html.replace(f"themes/{theme}.html", "index.html")
    html = html.replace("themes/", "")
    return html


def template_readme(theme: str) -> str:
    label = LABELS[theme]
    repo = template_repo_url(theme)
    zip_url = f"{REPO_RAW}/{theme}.zip"
    architect = CONFIG["architectName"]
    architect_url = CONFIG["architectUrl"]
    return f"""# {label} Portfolio Template

A single-layout portfolio starter for graduate school and professional development. **No coding tools required** — edit everything on github.com in your browser.

**Preview this layout:** [{label} demo]({PROJECT_URL}themes/{theme}.html)

---

## Start here

1. Click the green **Use this template** button above → create a repo named `my-portfolio`.
2. **Settings** → **Pages** → Source: **main** branch, **/ (root)** → Save.
3. Edit `index.html` on GitHub — search for `EDIT HERE`.
4. Colors: edit `css/{theme}.css` — only the hex codes at the top.

**Full setup guide:** [{GUIDE_URL}]({GUIDE_URL})

**Other layouts:** [{PROJECT_URL}]({PROJECT_URL})

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Your portfolio — edit this |
| `css/{theme}.css` | Colors and layout |
| `css/shared.css` | Media helpers (rarely edit) |
| `js/main.js` | Mobile menu (optional) |
| `assets/` | Your photos and PDFs |

---

## No template button?

Download the [ZIP]({zip_url}) and upload files to a new repo manually.

---

Part of [Portfolio Training]({PROJECT_URL}) · Template by [{architect}]({architect_url})
"""


def zip_dir(source: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(source))


def main() -> None:
    solo_root = ROOT / "solo"
    zips_dir = solo_root / "zips"
    shared_solo = make_shared_solo()
    gitignore = ".DS_Store\n"
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")

    if solo_root.exists():
        for child in solo_root.iterdir():
            if child.name != "README.md":
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()

    zips_dir.mkdir(parents=True, exist_ok=True)

    for theme in THEMES:
        out = solo_root / theme
        (out / "css").mkdir(parents=True)
        (out / "js").mkdir(parents=True)
        (out / "assets").mkdir(parents=True)

        html = (ROOT / "themes" / f"{theme}.html").read_text(encoding="utf-8")
        (out / "index.html").write_text(process_html(html, theme), encoding="utf-8")
        (out / "css" / "shared.css").write_text(shared_solo, encoding="utf-8")
        shutil.copy2(ROOT / "css" / f"{theme}.css", out / "css" / f"{theme}.css")
        shutil.copy2(ROOT / "js" / "main.js", out / "js" / "main.js")
        (out / ".gitignore").write_text(gitignore, encoding="utf-8")
        (out / ".nojekyll").write_text("", encoding="utf-8")
        (out / "LICENSE").write_text(license_text, encoding="utf-8")

        for name in (".gitkeep", "README.md"):
            src = ROOT / "assets" / name
            if src.exists():
                shutil.copy2(src, out / "assets" / name)

        (out / "README.md").write_text(template_readme(theme), encoding="utf-8")
        zip_dir(out, zips_dir / f"{theme}.zip")
        print(f"Built solo/{theme}/")

    table_rows = "\n".join(
        f"| {LABELS[t]} | [Use template]({template_repo_url(t)}) | [ZIP]({REPO_RAW}/{t}.zip) |"
        for t in THEMES
    )
    (solo_root / "README.md").write_text(
        f"""# Solo layout packages

Source builds for **10 separate GitHub template repositories**. Students preview on the [live demo]({PROJECT_URL}), then use **Use this template** on the repo for their chosen layout.

| Layout | Template repo | ZIP fallback |
|--------|---------------|--------------|
{table_rows}

Regenerate: `python3 scripts/build-solo.py` · Publish repos: `scripts/publish-template-repos.sh`
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
