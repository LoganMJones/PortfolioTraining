#!/usr/bin/env python3
"""Build solo/ layout packages — one self-contained zip per theme."""

import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = [
    "document",
    "classic",
    "minimal",
    "terminal",
    "brutalist",
    "deck",
    "editorial",
    "bold",
    "academic",
    "creative",
]

THEME_LABELS = {
    "document": "Document",
    "classic": "Classic",
    "minimal": "Minimal",
    "terminal": "Terminal",
    "brutalist": "Brutalist",
    "deck": "Deck",
    "editorial": "Editorial",
    "bold": "Bold",
    "academic": "Academic",
    "creative": "Creative",
}

GUIDE_URL = "https://loganmjones.github.io/PortfolioTraining/guide.html"
REPO_RAW = "https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips"

SWITCHER_RE = re.compile(
    r"\n  <nav class=\"theme-switcher\".*?</nav>\n",
    re.DOTALL,
)


def make_shared_solo() -> str:
    text = (ROOT / "css" / "shared.css").read_text(encoding="utf-8")
    start = text.find("/* ── Theme switcher ── */")
    end = text.find("/* ── Privacy notice")
    if start != -1 and end != -1:
        text = text[:start] + text[end:]
    text = text.replace(
        ":root {\n  --theme-switcher-height: 2.75rem;\n}",
        ":root {\n  --theme-switcher-height: 0;\n}",
        1,
    )
    if "--theme-switcher-height: 0" not in text:
        text = ":root {\n  --theme-switcher-height: 0;\n}\n\n" + text
    return text


def process_html(html: str, theme: str) -> str:
    html = SWITCHER_RE.sub("\n", html)
    html = re.sub(r'\n  <div class="solo-get".*?</div>\n', "\n", html, count=1, flags=re.DOTALL)
    html = html.replace("has-theme-switcher ", "")
    html = html.replace("../css/shared.css", "./css/shared.css")
    html = html.replace("../css/", "./css/")
    html = html.replace("../js/", "./js/")
    html = html.replace("../assets/", "./assets/")
    html = html.replace("../guide.html", f"{GUIDE_URL}")
    html = html.replace("../index.html", "./index.html")
    html = html.replace(f"themes/{theme}.html", "index.html")
    html = html.replace("themes/", "")
    return html


def solo_readme(theme: str) -> str:
    label = THEME_LABELS[theme]
    zip_url = f"{REPO_RAW}/{theme}.zip"
    return f"""# {label} Layout — Solo Package

This folder is **only** the {label} layout — no other themes, no layout picker.

## Quick start (no Terminal)

1. **Download:** [{label} layout ZIP]({zip_url})
2. **Unzip** the file on your computer (double-click the `.zip`).
3. On GitHub, create a new repository named `my-portfolio`.
4. Click **Add file** → **Upload files** → drag in everything from the unzipped folder (`index.html`, `css/`, `js/`, `assets/`).
5. **Settings** → **Pages** → Source: **main** branch, **/ (root)** folder → Save.
6. Edit `index.html` on GitHub — search for `EDIT HERE`.

**Full setup guide:** {GUIDE_URL}

## What's inside

```
index.html       ← your portfolio (homepage)
css/shared.css   ← media helpers
css/{theme}.css  ← colors & layout
js/main.js
assets/          ← put photos & PDFs here
```
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

        for name in (".gitkeep", "README.md"):
            src = ROOT / "assets" / name
            if src.exists():
                shutil.copy2(src, out / "assets" / name)

        (out / "README.md").write_text(solo_readme(theme), encoding="utf-8")
        zip_dir(out, zips_dir / f"{theme}.zip")
        print(f"Built solo/{theme}/ and solo/zips/{theme}.zip")

    (solo_root / "README.md").write_text(
        f"""# Solo layout packages

Each subfolder (and matching ZIP in `zips/`) is a **complete, single-layout** portfolio — ready to upload to a new GitHub repo.

**Students:** preview layouts on the [live demo](https://loganmjones.github.io/PortfolioTraining/), then download **only** the ZIP for the layout you chose.

| Layout | Download ZIP |
|--------|--------------|
"""
        + "\n".join(
            f"| {THEME_LABELS[t]} | [Download]({REPO_RAW}/{t}.zip) |"
            for t in THEMES
        )
        + f"""

See the [setup guide]({GUIDE_URL}#get-layout) for upload steps.

Regenerate after theme changes: `python3 scripts/build-solo.py`
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
