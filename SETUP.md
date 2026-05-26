# MGM Laboratory — Org Profile README setup

Everything in this folder is ready to drop into a special `.github`
repository on the **MGM-Laboratory** GitHub organization. Once it's
there, GitHub will render `profile/README.md` as the front page of
<https://github.com/MGM-Laboratory>.

---

## 1. File layout to publish

The repo must be named exactly `.github` and the README must live at
`profile/README.md`. Final structure:

```
.github/                                       ← repo name (public)
└── profile/
    ├── README.md
    └── assets/
        ├── hero.svg
        ├── divider-strip.svg
        ├── grid-3x3.svg
        ├── focus-pillars.svg
        ├── signals.svg
        ├── footer.svg
        ├── logo.svg
        ├── banner.png
        └── patterns/                          ← all 80 source tiles
            ├── p-1.svg
            ├── ...
            └── p-80.svg
```

The `output/profile/` folder in this delivery matches that tree exactly —
copy its contents into the new repo's root.

---

## 2. One-time publish (CLI)

```bash
# 1. create the repo on GitHub UI: https://github.com/organizations/MGM-Laboratory/repositories/new
#    name: .github   |   visibility: Public

# 2. from this folder:
cd output
git init -b main
git add profile
git commit -m "chore: add organization profile readme"
git remote add origin git@github.com:MGM-Laboratory/.github.git
git push -u origin main
```

Within ~30 seconds <https://github.com/MGM-Laboratory> will render the
new front page.

---

## 3. Things to find-and-replace before you push

| Placeholder | Where | Replace with |
|---|---|---|
| `hello@mgmlab.id` | README.md `mailto:` links | Your real lab contact email |
| `https://discord.gg/` | README.md | Your real Discord invite URL |
| `https://www.linkedin.com/` | README.md | Your LinkedIn company page URL |
| `https://www.instagram.com/` | README.md | Your IG profile URL |

The four highlighted repos at the top (atlas, asset-library, domain,
keycloak-theme) are already wired in. To swap one, edit the
`<!-- FEATURED WORK (top showcase) -->` block in `profile/README.md`
and change the `&repo=` parameter on the pin-card URL.

A quick sweep for stale placeholders:

```bash
grep -n "hello@mgmlab.id\|discord.gg/\"\|linkedin.com/\"\|instagram.com/\"" profile/README.md
```

---

## 4. How the animations work

Everything animated lives in **standalone SVG files** under
`profile/assets/`. They use **SMIL** (`<animate>`, `<animateTransform>`),
which GitHub renders inside `<img>` tags but strips when SVGs are inlined
through markdown's `![]()` syntax. So the README uses raw `<img>` tags
with `raw.githubusercontent.com/...` URLs — keep it that way when you
edit.

| Animation | File | Effect |
|---|---|---|
| Wordmark drop-in, drifting pattern field, bottom marquee | `hero.svg` | Plays once on load, marquee loops forever |
| Tiles scale-in left-to-right | `divider-strip.svg` | One-shot cascade |
| 9 tiles fade in diagonally | `grid-3x3.svg` | One-shot, ~1s |
| 5 discipline cards slide-up + sigil idle motion | `focus-pillars.svg` | Cards stagger in, glyphs idle forever |
| Discipline bars grow, "EST. 2025" lifts in | `signals.svg` | One-shot, ~2.3s; edit percentages inline to update |
| Brand dots breathe, reverse marquee | `footer.svg` | Loops forever |
| Typed tagline | `readme-typing-svg.demolab.com` | Re-renders on every page load |

If a particular animation feels too busy or too slow once it's live,
open the SVG and tweak the `dur="..."` values — that's the only thing
you usually need to touch.

---

## 5. Third-party badges & widgets used

All third-party services are read-only image endpoints — no auth needed.

- `img.shields.io` — top-link badges, contact buttons, and the four
  live org signal badges in section 03. The signal badges hit
  `api.github.com/orgs/MGM-Laboratory` through shields' `dynamic/json`
  endpoint, so the follower count, public-repo count and founding date
  stay current automatically.
- `readme-typing-svg.demolab.com` — typed tagline.
- `komarev.com/ghpvc` — visitor counter.
- `github-readme-stats.vercel.app` — **only** the four repo pin cards
  at the top of the page. Pin cards work for org-owned repos; the full
  stats card, top-langs donut, and activity graph are user-only (they
  404 for org slugs), which is why section 03 uses a self-hosted SVG
  instead.

If any of those go down, the README still renders — only the affected
images break. Everything visual-system-defining (hero, dividers, grid,
focus pillars, signals, footer) is hosted from your own repo.

---

## 6. Accessibility & contrast (per DESIGN_SYSTEM.md)

- All text uses `--ink` (#0E1116) or `--ink-3` (#6B7280) on white.
- Brand red `#F94141` is used only as a fill behind white text (`for-the-badge` style passes AA Large).
- Brand yellow `#F7BF33` is used as a fill with dark text (`logoColor=0E1116`), never as text on white.
- The hero & footer use the inverse surface `#0E1116` exactly once each — same rule the design system asks for ("at most once per long page").
- The pattern grids never place two same-color tiles or same-shape tiles next to each other (horizontally or vertically), as required.

---

## 7. Testing the README before going public

You can preview the rendered README locally with any GitHub-flavored
markdown renderer. The simplest path:

```bash
# install once
brew install gh
gh extension install yusukebe/gh-markdown-preview

# then from output/
gh markdown-preview profile/README.md
```

Note that SVG animations only animate when fetched over HTTP from the
actual `raw.githubusercontent.com` URL — local previews show static
first frames. Push to a private fork first if you want a true preview.
