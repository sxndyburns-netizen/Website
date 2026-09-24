# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Marketing site for **Sandbox Languages**, a family-run residential English summer school in the UK (ages 8–17). It's a static site with plain HTML, one CSS file and one vanilla JS file. It has no dependencies, package manager, build step, linter or tests.

```bash
python3 -m http.server 8000   # preview at http://localhost:8000 (opening index.html directly also works)
```

The branch is deployed as-is, so any static host works (GitHub Pages is the intended option).

## Business rules that shape every edit

- **The site exists to book free consultations.** Never add prices, fees, calculators or "from £…" copy. Every call to action leads to `consultation.html`. Pre-fill links use `?programme=juniors|teens|leaders`, `?campus=leighton-park|brunel` and `?type=group`.
- **Tone:** professional and warm. Emphasise that the school is family-run, founded by summer-school workers, and more fun and engaging while keeping costs low.
- **Campuses:** Leighton Park School in Reading gets the most emphasis: its Quaker ethos, 65-acre enclosed parkland, links to Heathrow and London, and premium meals at a discounted rate. The other campus is Brunel University of London in Uxbridge.
- **Excursions:** a London walking tour, Oxford tour, Cambridge tour, Harry Potter Studio Tour (officially "Warner Bros. Studio Tour London") and Madame Tussauds London. Every trip includes free time and a packed lunch.
- **Photos:** always prefer real photos to illustrations. **No child's face may ever be visible.** Show children from behind, as silhouettes, or as hands only.

## Architecture

**Pages repeat their shared markup.** The seven HTML pages were generated from shared templates, but that generator isn't in the repo. So the header/nav, footer, inline SVG icons and the photo and trip-card markup are copied into every page. When you change the nav, the footer or a repeated component, update **all** pages: `index`, `programmes`, `campuses`, `summer-life`, `about`, `consultation` and `credits`. The excursion cards appear in both `index.html` and `summer-life.html`.

**Photo slots** (`assets/img/photos/<slug>.jpg`) use one pattern everywhere:
```html
<figure class="photo photo--wide">            <!-- --wide 16:10, --tall 4:5, default 4:3 -->
  <div class="photo__placeholder" aria-hidden="true">…icon or SVG…</div>
  <img src="assets/img/photos/<slug>.jpg" alt="…" loading="lazy" onerror="this.remove()">
  <figcaption>…</figcaption>                  <!-- optional -->
</figure>
```
If the file is missing, the `<img>` removes itself and the placeholder shows. To add a photo, save a pre-cropped JPG to that aspect ratio at about 1600px wide (1200px for the portrait hero). Write alt text that describes what the photo actually shows.

**Photo credits:** `assets/img/photos/credits.json` records the source and licence of every photo. Pexels photos use the Pexels License. Wikimedia Commons photos are CC BY-SA and require attribution. `credits.html` renders that data as a table, and there is no generator in the repo. If you add, replace or remove a photo, update **both** files by hand.

**Getting photos in the cloud environment:**
- **Pexels:** full images download directly from `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&cs=tinysrgb&w=2000`. The pexels.com site itself is blocked, so find photo IDs with web search.
- **Wikimedia Commons:** the API works but is rate-limited. `upload.wikimedia.org` only serves standard thumbnail widths (`/thumb/…/1280px-<name>`), and full-size originals return 429. Send a descriptive User-Agent.
- **Blocked:** leightonpark.com (bot challenge), the Unsplash site and thomasfranks.com.

**CSS (`assets/css/styles.css`):**
- Design tokens (palette, fonts, radii, spacing) live on `:root`. The palette is sand, navy, coral, sea, sun and sky, with Fraunces for display type and DM Sans for body text (Google Fonts).
- Sections are `.section`, with `--alt` for a sand background and `--navy` for dark. `.container`, `.split`, `.grid-2/3/4/tiles`, cards, `.tabs` and `.faq` (`<details>`) provide layout and components.
- The site is light-only; there is no dark mode.
- Layouts must not scroll horizontally at 390px width.

**JS (`assets/js/main.js`)** is one IIFE that adds `.js` to `<html>` and then wires up:
- the sticky header and mobile nav (Esc closes it)
- `.reveal` scroll-in via IntersectionObserver
- ARIA tabs with hash deep links (`programmes.html#teens` via `data-hash`)
- validation for any `form[data-validate]`
- query-string pre-fill of the consultation form

Forms have `action="#"` and no backend. After validation, the element named by `data-success` is shown instead of the form. To make a form live, set a real `action` (Formspree, Netlify Forms or similar) and it will submit normally.

## Content still to confirm before launch

These are placeholders:
- contact details (`hello@sandboxlanguages.co.uk`, `+44 (0)1234 567890`)
- social, privacy, terms and cookie links, which currently point to `#`
- team names
- staff ratios

The six Leighton Park food photos are representative stock, not the school's own. Replace them with real photos when available.
