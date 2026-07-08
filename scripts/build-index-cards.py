#!/usr/bin/env python3
"""Regenerate theme card grid in index.html with preview + download links."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIP = "https://github.com/LoganMJones/PortfolioTraining/raw/main/solo/zips"

CARDS = [
    ("starter", "document", "Doc", "Document",
     "Plain single-column CV page — like a simple academic homepage. No sidebar, no hero. Easiest start.",
     ["Text-first", "Bullet lists", "PDF link"]),
    ("starter", "classic", "02", "Classic",
     "Sidebar CV: headshot, PDF download, project thumbnails, publications list.",
     ["Sidebar photo", "CV PDF", "Project thumbs"]),
    ("starter", "minimal", "03", "Minimal",
     "Text-first statement. Inline thumbs, collapsible video, optional audio.",
     ["Collapsible video", "PDF link", "Audio slot"]),
    ("", "terminal", "&gt;_ ", "Terminal",
     "CLI window aesthetic — commands, green-on-black, developer vibe. Great for CS &amp; data science.",
     ["CLI blocks", "Monospace", "Video slot"]),
    ("", "brutalist", "!", "Brutalist",
     "Giant type, thick borders, raw energy. Anti-polish on purpose — loud and memorable.",
     ["Oversized type", "Hard edges", "PDF block"]),
    ("", "deck", "▢", "Deck",
     "Full-screen scroll-snap slides — like a presentation. One idea per screen, slide numbers.",
     ["Full-screen slides", "Scroll-snap", "Video + image"]),
    ("", "editorial", "04", "Editorial",
     "Magazine-style: full-width hero image, featured project + video, photo gallery.",
     ["Hero image", "Video embed", "Gallery"]),
    ("", "bold", "05", "Bold",
     "Split-screen hero, impact stats, image-forward cards, video highlight.",
     ["Split hero", "Stats row", "Video"]),
    ("", "academic", "06", "Academic",
     "Publications, research poster figure, talk video, ORCID, formal headshot.",
     ["Poster figure", "Talk video", "PDFs"]),
    ("", "creative", "07", "Creative",
     "Visual mosaic, 6-image gallery, mixed image + video row, case-study tiles.",
     ["Photo gallery", "Mosaic grid", "Video reel"]),
]

SECTIONS = [
    ("Simple starters", "Plain, familiar layouts — great if you want something safe and fast. Only customize one.", 0, 3),
    ("Distinct layouts", "These look and feel very different — pick one that matches your personality or field.", 3, 10),
]


def card_html(starter: str, slug: str, preview: str, title: str, desc: str, tags: list) -> str:
    cls = f'theme-card theme-card--starter' if starter else "theme-card"
    tags_html = "".join(f"<li>{t}</li>" for t in tags)
    return f"""          <article class="{cls}">
            <a class="theme-card-hit" href="./themes/{slug}.html">
              <div class="theme-preview theme-preview--{slug}">
                <span>{preview}</span>
              </div>
              <h2>{title}</h2>
              <p>{desc}</p>
              <ul class="theme-features">{tags_html}</ul>
            </a>
            <div class="theme-card-actions">
              <a class="theme-card-link" href="./themes/{slug}.html">Preview →</a>
              <a class="theme-card-download" href="{ZIP}/{slug}.zip" download>Download only ↓</a>
            </div>
          </article>
"""


def main() -> None:
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    start = index.find('      <section class="theme-section">')
    end = index.find('      <section class="home-steps">')
    if start == -1 or end == -1:
        raise SystemExit("markers not found")

    blocks = []
    for sec_title, sec_desc, i0, i1 in SECTIONS:
        cards = "\n".join(card_html(*c) for c in CARDS[i0:i1])
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
