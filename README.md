# PortfolioTraining — Minimal HTML/CSS portfolio starter

This repository contains a minimal, accessible, and printable static portfolio built with plain HTML and CSS. It is intended as a starter you can customize for grad-school applications.

What I added in this commit
- assets/css/styles.css — main styles (responsive + accessible)
- assets/css/print.css — print stylesheet for resume printing
- projects/index.html and a sample project page
- blog/index.html and a sample blog post
- assets/resume.pdf (placeholder) — replace with your real PDF
- README.md (this file)

Suggested next steps
1. Replace /assets/resume.pdf with a PDF export of your resume (same filename).
2. Edit `index.html` to include your real contact details, education, and experience.
3. Add project case studies in `projects/` as `projects/<slug>/index.html` and link images from `assets/images/`.
4. Add blog posts to `blog/` as plain `.html` files (or adopt a tiny build step later to author in Markdown).

Deployment
- GitHub Pages (recommended for simplicity):
  - Repo settings → Pages → Source: `main` branch / `/ (root)` → Save.
  - Your site will be available at `https://<your-username>.github.io/<repo>` (it may take a minute to publish).
- Netlify or Vercel: drag-and-drop the site folder (build step not required for pure static HTML) or connect the GitHub repo and set the publish directory to `/`.

Accessibility & Performance
- All pages use semantic HTML and include a skip link.
- Images should include `alt` text and be optimized (srcset, WebP/AVIF preferred).
- Keep JS optional — this starter is zero-JS by default for best performance.

If you want, I can now:
- Replace the placeholder PDF with a generated one from the resume HTML (requires a small build step), or
- Add an optional tiny build script that converts Markdown -> HTML while still serving pure HTML, or
- Add a GitHub Action to validate HTML and build previews.

Tell me which of those (if any) you want next.