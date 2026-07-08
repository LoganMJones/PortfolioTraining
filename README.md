# Portfolio Template — 10 Layouts

Ten portfolio designs for graduate school and professional development — from plain CV pages to terminal windows and full-screen slides. **No coding tools required** — edit everything on github.com in your browser.

**Live demo:** [loganmjones.github.io/PortfolioTraining](https://loganmjones.github.io/PortfolioTraining/)

---

## Start here

1. **[Setup Guide](guide.html)** — step-by-step for non-technical users
2. **[Pick a layout](index.html)** — preview all 10 themes
3. **Customize one** — search your file for `EDIT HERE`

---

## The 10 layouts

### Simple starters

| Layout | File | Style |
|--------|------|-------|
| **Document** | `themes/document.html` | Plain single-column CV — easiest start |
| **Classic** | `themes/classic.html` | Sidebar + photo, resume-style |
| **Minimal** | `themes/minimal.html` | Black & white, text-first |

### Distinct layouts

| Layout | File | Style |
|--------|------|-------|
| **Terminal** | `themes/terminal.html` | CLI window, developer vibe |
| **Brutalist** | `themes/brutalist.html` | Giant type, thick borders, raw energy |
| **Deck** | `themes/deck.html` | Full-screen scroll-snap slides |
| **Editorial** | `themes/editorial.html` | Magazine hero, gallery, video |
| **Bold** | `themes/bold.html` | Gradients, colorful impact cards |
| **Academic** | `themes/academic.html` | Formal serif, publications, poster |
| **Creative** | `themes/creative.html` | Dark mosaic grid, playful |

Every layout shares a **black bar at the top** so you can switch between them like separate pages.

---

## Quick customization

### On GitHub (no VS Code, no Terminal)

1. Open your repo → click `themes/your-layout.html` → click the **pencil icon**
2. Press **Cmd+F** (Mac) or **Ctrl+F** (Windows)
3. Search these labels:

| Search for | What to change |
|------------|----------------|
| `EDIT HERE — NAME` | Your full name |
| `EDIT HERE — TAGLINE` | One-sentence description |
| `EDIT HERE — ABOUT` | Your bio |
| `EDIT HERE — EMAIL` | Your email |
| `ADD YOUR PHOTO HERE` | Instructions to add a headshot |
| `EDIT LINK HERE` | LinkedIn, GitHub, project URLs |

4. For colors: edit `css/[layout].css` — only change the hex codes in the **CHANGE YOUR COLORS HERE** section at the top
5. Click **Commit changes** at the bottom

### Delete when done

Search for `trainer-tip` and delete those yellow boxes — they're training helpers, not part of your final site.

---

## Add a photo

1. In your repo, go to the `assets` folder
2. **Add file** → **Upload files** → drag in `photo.jpg`
3. In your theme file, find `ADD YOUR PHOTO HERE` and follow the comment instructions

---

## GitHub Pages setup

1. Repo → **Settings** → **Pages**
2. Source: **Deploy from a branch** → `main` → `/ (root)`
3. Your site URL: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

**Don't** preview by clicking `index.html` in the repo — that shows unstyled HTML. Use your Pages URL.

---

## File structure

```
├── index.html              ← layout picker (homepage)
├── guide.html              ← detailed setup guide
├── themes/
│   ├── document.html
│   ├── classic.html
│   ├── minimal.html
│   ├── terminal.html
│   ├── brutalist.html
│   ├── deck.html
│   ├── editorial.html
│   ├── bold.html
│   ├── academic.html
│   └── creative.html
├── css/
│   ├── shared.css          ← theme switcher (don't edit)
│   ├── document.css        ← colors for Document
│   ├── classic.css
│   └── ...
├── js/main.js
└── assets/                 ← put photos here
```

---

## Workshop outline (90 min)

| Time | Activity |
|------|----------|
| 10 min | Why portfolios matter; demo the 10 layouts |
| 15 min | Copy template, enable GitHub Pages |
| 10 min | Walk through [guide.html](guide.html) together |
| 30 min | Students pick a layout, search `EDIT HERE`, fill in content |
| 15 min | Add photos, change accent color |
| 10 min | Share live URLs, delete trainer-tip boxes |

---

## GitHub Copilot prompts

- "Rewrite my about section for a PhD application in cognitive science"
- "Change the accent color in css/academic.css to Northwestern purple"
- "What does ADD YOUR PHOTO HERE mean in this file?"

---

MIT License · Kellogg REU Portfolio Training
