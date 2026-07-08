#!/usr/bin/env python3
"""Add unobtrusive template credit + ZIP link to showcase theme pages."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "templates.json").read_text(encoding="utf-8"))
PROJECT_URL = CONFIG["projectUrl"]
PROJECT_REPO = CONFIG["projectRepo"]
THEMES = list(CONFIG["themes"].keys())

CREDIT_INNER_RE = re.compile(
    r'<p class="template-credit">.*?</p>',
    re.DOTALL,
)
ARCHITECT_CREDIT_RE = re.compile(
    r'<p class="architect-credit">.*?</p>',
    re.DOTALL,
)


def zip_url(theme: str) -> str:
    return f"{PROJECT_REPO}/raw/main/solo/zips/{theme}.zip"


def credit_inner(theme: str) -> str:
    return (
        f'<a href="{PROJECT_URL}" rel="noopener noreferrer">Portfolio Training</a>'
        f' · <a href="{zip_url(theme)}" download rel="noopener noreferrer">Download ZIP</a>'
    )


def architect_credit_inner() -> str:
    return (
        f"Entire project architected by "
        f'<a href="{CONFIG["architectUrl"]}" rel="noopener noreferrer">{CONFIG["architectName"]}</a> '
        f'with <a href="{CONFIG["cursorUrl"]}" target="_blank" rel="noopener noreferrer">'
        f'{CONFIG["cursorName"]}</a> assistance.'
    )


def credit_paragraph(theme: str, indent: str = "      ") -> str:
    return f'{indent}<p class="template-credit">{credit_inner(theme)}</p>\n'


def architect_credit_paragraph(indent: str = "  ") -> str:
    return f'{indent}<p class="architect-credit">{architect_credit_inner()}</p>\n'


def upsert_credit(html: str, theme: str) -> str:
    inner = credit_inner(theme)
    if CREDIT_INNER_RE.search(html):
        return CREDIT_INNER_RE.sub(
            f'<p class="template-credit">{inner}</p>',
            html,
            count=1,
        )
    return html


def upsert_architect_credit(html: str, indent: str = "  ") -> str:
    inner = architect_credit_inner()
    if ARCHITECT_CREDIT_RE.search(html):
        return ARCHITECT_CREDIT_RE.sub(
            f'<p class="architect-credit">{inner}</p>',
            html,
            count=1,
        )
    if CREDIT_INNER_RE.search(html):
        match = CREDIT_INNER_RE.search(html)
        if match:
            return (
                html[: match.end()]
                + f'\n{indent}<p class="architect-credit">{inner}</p>'
                + html[match.end() :]
            )
    return html + architect_credit_paragraph(indent)


def showcase_footer_block(theme: str, indent: str = "  ") -> str:
    return (
        f'{indent}<p class="template-credit">{credit_inner(theme)}</p>\n'
        f"{architect_credit_paragraph(indent)}"
    )


def add_credit_to_footer(html: str, theme: str) -> str:
    html = upsert_credit(html, theme)
    html = upsert_architect_credit(html)
    if "template-credit" in html:
        return html

    footer_re = re.compile(
        r"(?P<indent>^[ \t]*)<footer class=\"(?P<cls>site-footer|footer|doc-footer)[^\"]*\"[^>]*>"
        r"(?P<body>.*?)</footer>",
        re.MULTILINE | re.DOTALL,
    )

    def repl(match: re.Match[str]) -> str:
        if "template-credit" in match.group("body"):
            return match.group(0)
        indent = match.group("indent")
        cls_match = re.search(
            r'<footer class="([^"]+)"',
            match.group(0),
        )
        cls = cls_match.group(1) if cls_match else match.group("cls")
        body = match.group("body").rstrip()
        credits = showcase_footer_block(theme, indent + "  ").rstrip()
        return (
            f'{indent}<footer class="{cls}">{body}\n'
            f"{credits}\n"
            f"{indent}</footer>"
        )

    updated, count = footer_re.subn(repl, html, count=1)
    return updated if count else html


def add_terminal_footer(html: str, theme: str) -> str:
    html = upsert_credit(html, theme)
    html = upsert_architect_credit(html, indent="    ")
    if "template-credit-footer" in html:
        return html
    marker = '  <script src="../js/main.js"></script>'
    footer = (
        "\n  <footer class=\"template-credit-footer\">\n"
        f"    <p class=\"template-credit\">{credit_inner(theme)}</p>\n"
        f"    <p class=\"architect-credit\">{architect_credit_inner()}</p>\n"
        "  </footer>\n"
    )
    if marker in html:
        return html.replace(marker, footer + marker, 1)
    return html


def add_deck_footer(html: str, theme: str) -> str:
    html = upsert_credit(html, theme)
    html = upsert_architect_credit(html, indent="    ")
    if "template-credit-footer" in html:
        return html
    marker = "  </main>\n\n  <script"
    replacement = (
        "  </main>\n\n"
        "  <footer class=\"template-credit-footer\">\n"
        f"    <p class=\"template-credit\">{credit_inner(theme)}</p>\n"
        f"    <p class=\"architect-credit\">{architect_credit_inner()}</p>\n"
        "  </footer>\n\n  <script"
    )
    return html.replace(marker, replacement, 1)


def main() -> None:
    for theme in THEMES:
        path = ROOT / "themes" / f"{theme}.html"
        html = path.read_text(encoding="utf-8")
        if theme == "terminal":
            html = add_terminal_footer(html, theme)
        elif theme == "deck":
            html = add_deck_footer(html, theme)
        else:
            html = add_credit_to_footer(html, theme)
        path.write_text(html, encoding="utf-8")
        print(f"Credited themes/{theme}.html")


if __name__ == "__main__":
    main()
