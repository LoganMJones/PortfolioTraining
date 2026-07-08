#!/usr/bin/env python3
"""Generate fill-checklist HTML blocks and inject into theme pages."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKLISTS = json.loads((ROOT / "theme-checklists.json").read_text(encoding="utf-8"))

MARKER_START = '    <div class="fill-checklist"'
MARKER_END = '    </div>\n\n'

AI_TIP = """      <p class="fill-checklist-ai"><strong>Using an AI coding assistant?</strong> Select and copy this entire blue box into Cursor or another agentic coding AI. Ask it to walk you through every item below — your text, photos, PDFs, and video — then implement the changes in <code>index.html</code> and tell you what to upload to <code>assets/</code>.</p>

"""

def image_rows(images: list) -> str:
    if not images:
        return "      <tr><td colspan=\"4\"><em>None — text and links only</em></td></tr>\n"
    rows = []
    for img in images:
        size = f"{img['minWidth']}×{img['minHeight']} px min"
        count = img["count"]
        file_hint = img["file"]
        if count > 1:
            base = file_hint.rsplit(".", 1)
            if len(base) == 2:
                file_hint = f"{base[0]}-1.{base[1]} … {base[0]}-{count}.{base[1]}"
        rows.append(
            f"      <tr><td>{count}× {img['subject']}</td>"
            f"<td><code>{file_hint}</code></td>"
            f"<td>{size}<br>{img['ratio']}</td>"
            f"<td>Search <code>{img['slot']}</code></td></tr>\n"
        )
    return "".join(rows)


def file_rows(files: list) -> str:
    if not files:
        return "      <tr><td colspan=\"3\"><em>None required</em></td></tr>\n"
    return "".join(
        f"      <tr><td>{f['label']}</td><td><code>{f['file']}</code></td>"
        f"<td>{f['notes']}</td></tr>\n"
        for f in files
    )


def video_rows(videos: list) -> str:
    if not videos:
        return ""
    items = "".join(
        f"<li><strong>{v['count']}× video</strong> — {v['notes']} "
        f"(search <code>{v['slot']}</code>)</li>\n"
        for v in videos
    )
    return f"    <p><strong>Video</strong></p>\n    <ul>{items}    </ul>\n"


def text_list(items: list) -> str:
    return "".join(f"      <li>{item}</li>\n" for item in items)


def build_html(theme: str, data: dict) -> str:
    label = data["label"]
    total_images = sum(i["count"] for i in data["images"])
    total_pdfs = len(data["files"])
    total_videos = sum(v["count"] for v in data["video"])

    summary_parts = [f"{total_images} photo{'s' if total_images != 1 else ''}" if total_images else None,
                     f"{total_pdfs} PDF{'s' if total_pdfs != 1 else ''}" if total_pdfs else None,
                     f"{total_videos} video embed{'s' if total_videos != 1 else ''}" if total_videos else None]
    summary = " · ".join(p for p in summary_parts if p) or "Text only"

    return f"""    <div class="fill-checklist" id="fill-checklist">
      <strong>📋 To fully fill out {label}</strong>
      <span class="fill-checklist-summary">Gather: {summary}</span>
      <p class="fill-checklist-intro">Replace every placeholder below — no extra sections needed. Delete this box when done.</p>
{AI_TIP}
      <p><strong>Text to write</strong> (search <code>EDIT HERE</code> or replace placeholder copy)</p>
      <ul class="fill-checklist-text">
{text_list(data['text'])}      </ul>

      <p><strong>Photos to upload</strong> (to <code>assets/</code> on GitHub — JPG recommended, compress to ~500 KB each)</p>
      <table class="fill-checklist-table">
        <thead><tr><th>Qty</th><th>Filename</th><th>Min size</th><th>Find in HTML</th></tr></thead>
        <tbody>
{image_rows(data['images'])}        </tbody>
      </table>

      <p><strong>PDFs to upload</strong></p>
      <table class="fill-checklist-table">
        <thead><tr><th>Document</th><th>Filename</th><th>Notes</th></tr></thead>
        <tbody>
{file_rows(data['files'])}        </tbody>
      </table>
{video_rows(data['video'])}    </div>

"""


def inject(html: str, block: str) -> str:
    if 'class="fill-checklist"' in html:
        pattern = re.compile(
            r'\n\s*<div class="fill-checklist".*?</div>\n\n',
            re.DOTALL,
        )
        return pattern.sub("\n" + block, html, count=1)
    if 'class="trainer-tip"' in html:
        return re.sub(
            r'(\n\s*<div class="trainer-tip[^"]*">.*?</div>\n)',
            r"\1\n" + block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    if 'class="privacy-notice"' in html:
        return re.sub(
            r'(\n\s*<div class="privacy-notice">.*?</div>\n)',
            r"\1\n" + block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    return html.replace("<main", "\n" + block + "    <main", 1)


def main() -> None:
    for theme, data in CHECKLISTS.items():
        path = ROOT / "themes" / f"{theme}.html"
        html = path.read_text(encoding="utf-8")
        block = build_html(theme, data)
        html = inject(html, block)
        path.write_text(html, encoding="utf-8")
        print(f"Updated themes/{theme}.html")


if __name__ == "__main__":
    main()
