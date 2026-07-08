#!/usr/bin/env python3
"""Add solo-get download banner to each theme preview page."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = [
    "document", "classic", "minimal", "terminal", "brutalist", "deck",
    "editorial", "bold", "academic", "creative",
]
LABELS = {
    "document": "Document", "classic": "Classic", "minimal": "Minimal",
    "terminal": "Terminal", "brutalist": "Brutalist", "deck": "Deck",
    "editorial": "Editorial", "bold": "Bold", "academic": "Academic",
    "creative": "Creative",
}
RAW = "https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips"
GUIDE = "https://loganmjones.github.io/PortfolioTraining/guide.html#get-layout"

BANNER = """
  <div class="solo-get" role="note">
    <p><strong>Like this layout?</strong>
      <a href="{url}/{theme}.zip" download>Download {label} only</a> (ZIP — no other themes)
      · <a href="{guide}">Set it up on GitHub</a></p>
  </div>
"""

MARKER = '  <a class="skip-link" href="#main">Skip to content</a>\n'


def main() -> None:
    for theme in THEMES:
        path = ROOT / "themes" / f"{theme}.html"
        text = path.read_text(encoding="utf-8")
        banner = BANNER.format(url=RAW, theme=theme, label=LABELS[theme], guide=GUIDE)
        needle = MARKER + banner
        if "class=\"solo-get\"" in text:
            # replace existing banner
            import re
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
            print(f"skip {theme}: no skip-link")
            continue
        path.write_text(text, encoding="utf-8")
        print(f"Updated themes/{theme}.html")


if __name__ == "__main__":
    main()
