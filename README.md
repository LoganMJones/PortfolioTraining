# Portfolio Template

A modern, minimal portfolio for graduate school and professional development. No build tools, no VS Code required — edit on GitHub, host free on GitHub Pages.

---

## Get your site live (no VS Code needed)

### Step 1 — Copy the template

On GitHub, click **Use this template** → create a new repo (e.g. `yourname-portfolio`).

### Step 2 — Turn on GitHub Pages

1. Open your repo on **github.com**
2. Go to **Settings** → **Pages**
3. Under **Build and deployment** → **Source**: choose **Deploy from a branch**
4. Branch: **main**, folder: **/ (root)**
5. Click **Save**
6. Wait 1–2 minutes

Your site URL will be:

```
https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
```

> If you name the repo `yourusername.github.io`, the URL is just `https://yourusername.github.io`

### Step 3 — Edit your content on GitHub

You do **not** need VS Code. Edit files directly in the browser:

1. Open your repo on github.com
2. Click `index.html` → click the **pencil icon** (Edit)
3. Replace placeholder text with your info
4. Scroll down → **Commit changes**

Do the same for `css/style.css` if you want to change colors.

### Step 4 — Check your live site

**Important:** Do not preview by clicking `index.html` inside the GitHub repo — that shows raw unstyled HTML.

Always open your **GitHub Pages URL** (from Settings → Pages). That's your real site.

---

## What to customize

| File | What to change |
|------|----------------|
| `index.html` | Your name, bio, education, experience, projects, contact links |
| `css/style.css` | `--accent` at the top for your brand color |
| `assets/` | Add your photo or CV (optional) |

---

## Project structure

```
├── index.html       ← your content (start here)
├── css/style.css    ← look and feel
├── js/main.js       ← menu + scroll animations
├── assets/          ← photos, CV
└── .nojekyll        ← required for GitHub Pages
```

---

## Using GitHub Copilot (in the browser)

1. Open your repo on github.com
2. Click the **Copilot** icon in the top bar (or use Copilot Chat if available)
3. Try prompts like:

- "Rewrite the About section for a PhD application in psychology"
- "Change the accent color in style.css to Northwestern purple"
- "Add a Publications section matching the existing design"

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Site looks like plain HTML | You're viewing the file on GitHub, not the Pages URL. Go to Settings → Pages for the correct link. |
| CSS not loading | Make sure `css/style.css` exists in your repo (not just on your computer). Check the file is committed and pushed. |
| Changes not showing | Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows). Wait 2 min for Pages to rebuild. |
| 404 error | Pages may still be deploying. Check Settings → Pages shows a green checkmark. |

---

## Design features

- Full-screen dark hero with grid texture
- Editorial numbered sections (01, 02, 03…)
- Bento-style project grid
- Scroll-reveal animations
- Mobile-friendly navigation
- Accessible (skip link, focus styles, semantic HTML)

---

## Workshop outline (60–90 min)

1. Copy template & enable GitHub Pages (15 min)
2. Edit `index.html` on github.com with your content (30 min)
3. Customize accent color in `css/style.css` (10 min)
4. Use Copilot to refine a section (15 min)
5. Share live URLs & troubleshoot (10 min)

---

MIT License — free to use and share with your cohort.
