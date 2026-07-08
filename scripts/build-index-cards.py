#!/usr/bin/env python3
"""Regenerate theme card grid in index.html with preview + template + download links."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "templates.json").read_text(encoding="utf-8"))
ORG = CONFIG["githubOrg"]
PREFIX = CONFIG["repoPrefix"]
ZIP = f"{CONFIG['projectRepo']}/raw/main/solo/zips"

THEMES = list(CONFIG["themes"].items())

CARDS = []
for slug, meta in THEMES:
    preview_num = {
        "document": "Doc", "classic": "02", "minimal": "03", "terminal": "&gt;_ ",
        "brutalist": "!", "deck": "▢", "editorial": "04", "bold": "05",
        "academic": "06", "creative": "07",
    }.get(slug, slug[:3])
    CARDS.append((slug, meta))

DESCRIPTIONS = {
    "document": "Plain single-column CV page — like a simple academic homepage. No sidebar, no hero. Easiest start.",
    "classic": "Sidebar CV: headshot, PDF download, project thumbnails, publications list.",
    "minimal": "Text-first statement. Inline thumbs, collapsible video, optional audio.",
    "terminal": "CLI window aesthetic — commands, green-on-black, developer vibe. Great for CS &amp; data science.",
    "brutalist": "Giant type, thick borders, raw energy. Anti-polish on purpose — loud and memorable.",
    "deck": "Full-screen scroll-snap slides — like a presentation. One idea per screen, slide numbers.",
    "editorial": "Magazine-style: full-width hero image, featured project + video, photo gallery.",
    "bold": "Split-screen hero, impact stats, image-forward cards, video highlight.",
    "academic": "Publications, research poster figure, talk video, ORCID, formal headshot.",
    "creative": "Visual mosaic, 6-image gallery, mixed image + video row, case-study tiles.",
}

TAGS = {
    "document": ["Text-first", "Bullet lists", "PDF link"],
    "classic": ["Sidebar photo", "CV PDF", "Project thumbs"],
    "minimal": ["Collapsible video", "PDF link", "Audio slot"],
    "terminal": ["CLI blocks", "Monospace", "Video slot"],
    "brutalist": ["Oversized type", "Hard edges", "PDF block"],
    "deck": ["Full-screen slides", "Scroll-snap", "Video + image"],
    "editorial": ["Hero image", "Video embed", "Gallery"],
    "bold": ["Split hero", "Stats row", "Video"],
    "academic": ["Poster figure", "Talk video", "PDFs"],
    "creative": ["Photo gallery", "Mosaic grid", "Video reel"],
}

SECTIONS = [
    ("Simple starters", "Plain, familiar layouts — great if you want something safe and fast.", 0, 3),
    ("Distinct layouts", "These look and feel very different — pick one that matches your personality or field.", 3, 10),
]


def card_html(slug: str, meta: dict) -> str:
    starter = meta.get("starter")
    cls = "theme-card theme-card--starter" if starter else "theme-card"
    label = meta["label"]
    preview = {
        "document": "Doc", "classic": "02", "minimal": "03", "terminal": "&gt;_ ",
        "brutalist": "!", "deck": "▢", "editorial": "04", "bold": "05",
        "academic": "06", "creative": "07",
    }[slug]
    tags_html = "".join(f"<li>{t}</li>" for t in TAGS[slug])
    repo = f"https://github.com/{ORG}/{PREFIX}-{slug}"
    return f"""          <article class="{cls}">
            <a class="theme-card-hit" href="./themes/{slug}.html">
              <div class="theme-preview theme-preview--{slug}">
                <span>{preview}</span>
              </div>
              <h2>{label}</h2>
              <p>{DESCRIPTIONS[slug]}</p>
              <ul class="theme-features">{tags_html}</ul>
            </a>
            <div class="theme-card-actions">
              <a class="theme-card-link" href="./themes/{slug}.html">Preview →</a>
              <a class="theme-card-template" href="{repo}" target="_blank" rel="noopener noreferrer">Use template</a>
              <a class="theme-card-download" href="{ZIP}/{slug}.zip" download>ZIP ↓</a>
            </div>
          </article>
"""


def main() -> None:
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    start = index.find('      <section class="theme-section">')
    end = index.find('      <section class="home-steps">')
    if start == -1 or end == -1:
        raise SystemExit("markers not found")

    items = list(CONFIG["themes"].items())
    blocks = []
    for sec_title, sec_desc, i0, i1 in SECTIONS:
        cards = "\n".join(card_html(slug, meta) for slug, meta in items[i0:i1])
        blocks.append(f"""      <section class="theme-section">
        <h2 class="theme-section-title">{sec_title}</h2>
        <p class="theme-section-desc">{sec_desc}</p>
        <div class="theme-grid">

{cards}
        </div>
      </section>
""")
    index = index[:start] + "\n".join(blocks) + "\n" + index[end:]
    (ROOT / "index.html").write_text(index, encoding="utf-8")
    print("Updated index.html theme grid")


if __name__ == "__main__":
    main()
