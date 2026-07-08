#!/usr/bin/env python3
"""Add solo-get download banner to each theme preview page."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "templates.json").read_text(encoding="utf-8"))
ORG = CONFIG["githubOrg"]
PREFIX = CONFIG["repoPrefix"]
RAW = f"{CONFIG['projectRepo']}/raw/main/solo/zips"
GUIDE = f"{CONFIG['projectUrl']}guide.html#get-layout"

THEMES = list(CONFIG["themes"].keys())
LABELS = {k: v["label"] for k, v in CONFIG["themes"].items()}

BANNER = """
  <div class="solo-get" role="note">
    <p><strong>Like this layout?</strong>
      <a href="https://github.com/{org}/{prefix}-{theme}" target="_blank" rel="noopener noreferrer">Use template</a>
      · <a href="{raw}/{theme}.zip" download>Download ZIP</a>
      · <a href="{guide}">Setup guide</a></p>
  </div>
"""

MARKER = '  <a class="skip-link" href="#main">Skip to content</a>\n'


def main() -> None:
    for theme in THEMES:
        path = ROOT / "themes" / f"{theme}.html"
        text = path.read_text(encoding="utf-8")
        banner = BANNER.format(org=ORG, prefix=PREFIX, theme=theme, raw=RAW, guide=GUIDE)
        if "class=\"solo-get\"" in text:
            text = re.sub(
                r'\n  <div class="solo-get".*?</div>\n',
                "\n" + banner,
                text,
                count=1,
                flags=re.DOTALL,
            )
        elif MARKER in text:
            text = text.replace(MARKER, MARKER + banner, 1)
        else:
            print(f"skip {theme}")
            continue
        path.write_text(text, encoding="utf-8")
        print(f"Updated themes/{theme}.html")


if __name__ == "__main__":
    main()
