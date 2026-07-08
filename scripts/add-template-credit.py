#!/usr/bin/env python3
"""Add unobtrusive template credit footer to all theme pages."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "templates.json").read_text(encoding="utf-8"))
PROJECT_URL = CONFIG["projectUrl"]

CREDIT_LINE = (
    f'      <p class="template-credit">'
    f'<a href="{PROJECT_URL}" rel="noopener noreferrer">Portfolio Training template</a></p>\n'
)

TERMINAL_FOOTER = (
    f'\n  <footer class="template-credit-footer">\n'
    f'    <p class="template-credit">'
    f'<a href="{PROJECT_URL}" rel="noopener noreferrer">Portfolio Training template</a></p>\n'
    f'  </footer>\n'
)

THEMES = list(CONFIG["themes"].keys())


def add_credit_to_footer(html: str) -> str:
    if "template-credit" in html:
        return html
    return re.sub(
        r"(  </footer>)",
        CREDIT_LINE + r"\1",
        html,
        count=1,
    )


def add_terminal_footer(html: str) -> str:
    if "template-credit" in html:
        return html
    marker = "  <script src=\"../js/main.js\"></script>"
    if marker in html:
        return html.replace(marker, TERMINAL_FOOTER + marker, 1)
    return html


def add_deck_footer(html: str) -> str:
    if "template-credit-footer" in html:
        return html
    marker = "  </main>\n\n  <script"
    replacement = (
        "  </main>\n\n"
        "  <footer class=\"template-credit-footer\">\n"
        f"    <p class=\"template-credit\">"
        f"<a href=\"{PROJECT_URL}\" rel=\"noopener noreferrer\">Portfolio Training template</a></p>\n"
        "  </footer>\n\n  <script"
    )
    return html.replace(marker, replacement, 1)


def main() -> None:
    for theme in THEMES:
        path = ROOT / "themes" / f"{theme}.html"
        html = path.read_text(encoding="utf-8")
        if theme == "terminal":
            html = add_terminal_footer(html)
        elif theme == "deck":
            html = add_deck_footer(html)
        else:
            html = add_credit_to_footer(html)
        path.write_text(html, encoding="utf-8")
        print(f"Credited themes/{theme}.html")


if __name__ == "__main__":
    main()
