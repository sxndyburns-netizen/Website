# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Marketing site for **Sandbox English** (trading as **Sandbox English Summer School**), a residential English summer school for ages 8–18 in London or the area around London, as the family or agent chooses. The first summer is **2028**. The domain is **sandboxenglish.co.uk**. The audience is **parents, agents and group leaders**. It's a small static site (three main pages: `index.html`, `agents.html` and `consultation.html`, plus `privacy.html`, `terms.html`, `cookies.html`, `credits.html` and `404.html`) with plain HTML, one CSS file and one vanilla JS file. A small Python generator assembles the pages. There are no dependencies, package manager, linter or tests.

```bash
python3 src/build.py          # regenerate root *.html, credits.html, sitemap.xml, robots.txt (Python 3.11+, stdlib only)
python3 src/images.py         # after adding/replacing a photo: make its 800px version (needs Pillow)
python3 -m http.server 8000   # preview at http://localhost:8000
```

The generated HTML is committed and served as-is, so any static host works (GitHub Pages is the intended option). **Edit `src/`, never the root `*.html` files, then run the build and commit both.** A rebuild with no source changes should produce no git diff, which is a quick way to check the build is sound.

**Never push to `main` without the user's explicit instruction for that change.** Commit and push to the working branch; `main` is what the live site publishes from.

## Business rules that shape every edit

- **The site exists to book free consultations.** Never add prices, fees, calculators or "from £…" copy. Every call to action leads to `consultation.html`. Pre-fill links use `?type=parent|agent|group` and `?area=london|around-london`.
- **Keep it to about three pages.** The home page holds everything for families, in anchored sections (`#programme`, `#about`, `#safety`, `#summer-life`, `#locations`, `#faq`…) that the nav links to, in page order. About us sits between the programme and safety. Add sections rather than new pages. The legal pages are the only exception.
- **Only state confirmed facts as facts.** The README's "Confirmed facts" section lists them: 15 hours of English a week; small classes (never a number); two excursions a week, tailored to parents' and agents' wishes, each with free time and a packed lunch; 24/7 staff on site and emergency line; first-aid trained staff; at least one member of staff for every 10 students (a 1:10 staff-to-student ratio, not a class size); **one programme**, with students grouped on site by age and level; complete beginners welcome; stays of one to six weeks.
- **Not accredited yet.** Never claim or imply accreditation or membership (British Council, English UK or others) until the user confirms it's granted. The README's "Accreditation and visas" section explains why it matters.
- **No bookings or payments yet.** Don't mention payment protection, trust accounts, deposits or online booking steps on the site until the arrangement in the README's "Bookings and payments" section is live and the user confirms it.
- **Company details are placeholders.** `COMPANY` in `src/build.py` holds the legal name, company number, registered office and ICO number, shown in the footer, privacy policy and terms (via `{{company:key}}`). Values in `[brackets]` are placeholders. Don't invent real-looking values, and keep them out of the JSON-LD until they're real.
- **No venues are confirmed.** Never name a venue in copy, alt text, captions, file names or photo credit links, and don't use photos of potential venues. Describe "the area around London" and "London" as regions only, and never state venue features (e.g. "close to Heathrow") as fact.
- **Location is the customer's choice.** Both options are available: London, or the area around London. Present them side by side as equal options and word it as the parent's or agent's decision ("choose London or the area around London"), never as the school's choice, and never mark either as "on request". Only one site operates in 2028, but don't say so on the site.
- **Founder:** Alexander Burns, a student with several years' experience delivering enjoyable summer programmes, who founded the school to offer a better experience at a reasonable price. He is also the **Designated Safeguarding Lead**. The school is founder-led (not family-run) and teaches English only. Don't invent quotes attributed to him, or state safeguarding training or qualifications he hasn't confirmed.
- **Tone:** professional and warm.
- **Photos:** always prefer real photos to illustrations. **No child's face may ever be visible.** Show children from behind, as silhouettes, or as hands only.
- **Accessibility:** keep text contrast at WCAG AA. White text goes on `--coral-700` (not the brand coral `#f2603d`), and small coral text uses `--coral-text`. Headings must not skip levels (use `.h3`/`.h4` classes to change size).
- **Brand:** navy `#14213d` and coral `#f2603d` are the core pair. The logo is a speech bubble holding a sandcastle with a flag, a sun and a wave, beside the "Sandbox" wordmark. There is no stamp or year, and the header uses the simple mark. It must keep working in one colour for shirts and lanyards. Print logos are in `assets/brand/`, regenerated by `src/brand.py` (fonts can be instanced from `assets/fonts/`). The website's copy is `MARK` in `src/build.py`, so change both together, copy `mark-full-colour.svg` to `assets/img/favicon.svg`, and re-render `favicon.ico`, `assets/img/favicon-32.png` and `assets/img/apple-touch-icon.png` from it (older Safari ignores the SVG icon). Icon links and the `og:image` share image get a content-hash `?v=` from `versioned()` in `src/build.py`, which busts Safari's sticky icon cache and WhatsApp/social preview caches; keep using it. The share image (`assets/img/share.jpg`) has the age range and location line drawn into it, so redraw it when those change.

## Architecture

**The generator (`src/build.py`).** Each `src/pages/*.html` file starts with front matter (`title:`, `description:`, optional `robots: noindex`), then `---`, then the page body. The build wraps each body with the shared `<head>` (meta, Open Graph and share image, font preloads, JSON-LD on the home page), the header/nav (`NAV`) and the footer (`footer()`), so a nav or footer change is made once. It also writes `credits.html` from `assets/img/photos/credits.json`, plus `sitemap.xml` and `robots.txt`. Shortcodes:
- `{{photo:slug|alt|variant|caption}}` becomes a `<figure class="photo">` with `srcset` (the 1600px and `-800` files), `width`/`height`, and lazy loading (`tall` = the hero, loaded first).
- `{{trips}}` becomes the excursion cards from `TRIPS`, used on the home and agents pages.
- `{{icon:name}}` becomes an inline SVG from `ICON`.
- `{{founder}}` becomes Alexander's portrait (`assets/img/photos/founder.jpg`, 4:5) with his name and roles, or a navy "AB" monogram if that file is missing. The current portrait is temporary (a bin bag fashion show photo). When a professional headshot arrives, follow the README's "Temporary portrait" steps: the old photo moves to Summer life, captioned "Bin bag fashion show".
- `{{company:key}}` becomes a value from `COMPANY` (`name`, `number`, `office`, `ico`).

Link to the home page as `./` (and its sections as `./#faq`), never `index.html`, so the home page has one address. Browsers, Safari in particular, remember tab icons per address.

The build fails on unknown shortcodes, icons or company keys, missing photo files, or photos without a `credits.json` entry, and warns while company details are placeholders. Text is read and written as UTF-8, and attribute values are HTML-escaped.

**Photos** live in `assets/img/photos/<slug>.jpg` (pre-cropped: 16:10 wide, 4:5 tall hero, 4:3 default, about 1600px wide) with `<slug>-800.jpg` made by `src/images.py`. Every photo needs a `credits.json` entry (description, artist, licence, licence URL, source), and the README's photo table lists them. For images used with permission (e.g. Alexander's photo), leave `license_url` and `source` empty and the credits page shows "—". Write alt text that describes what the photo actually shows.

**Getting photos in the cloud environment:**
- **Pexels:** full images download directly from `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&cs=tinysrgb&w=2000`. The pexels.com site itself is blocked, so find photo IDs with web search.
- **Wikimedia Commons:** the API works but is rate-limited. `upload.wikimedia.org` only serves standard thumbnail widths (`/thumb/…/1280px-<name>`), and full-size originals return 429. Send a descriptive User-Agent.
- **Blocked:** the Unsplash site (bot challenge) and some venue websites.

**CSS (`assets/css/styles.css`):**
- It starts with the self-hosted `@font-face` rules (`assets/fonts/`, Fraunces and DM Sans woff2). Don't add Google Fonts or any other third-party request: the cookie policy promises there are none apart from form submissions to Formspree.
- Design tokens (palette, fonts, radii, spacing) live on `:root`.
- Sections are `.section`, with `--alt` for a sand background, `--navy` for dark and `--tight-top` to remove top padding. There are also layout helpers (`.split`, `.split--top`, `.grid-2/3/4/tiles`, `.photo-grid`, `.mt-sm`/`.mt-md`/`.mt-lg`), cards, `.faq` (`<details>`), `.prose` (legal pages) and `.form-layout`.
- The site is light-only. Below 1240px the nav collapses into a menu button, but only when JavaScript runs. Layouts must not scroll horizontally at 390px width.

**JS (`assets/js/main.js`)** is one IIFE that wires up:
- the sticky header and mobile nav (Esc closes it)
- `.reveal` scroll-in. Content is only hidden once `html.reveal-ready` is set, so it stays visible if JS fails
- validation for `form[data-validate]`. Each field's error element is found through its `aria-describedby`, and hidden or disabled fields are skipped
- consultation-form logic: `data-show-for="agent group"` fields appear for the chosen enquirer type, the phone number becomes required for phone or WhatsApp, and `?type=` / `?area=` pre-fill the form

Both forms post to Formspree (`FORM_ENDPOINT` in `src/build.py`, `{{form_endpoint}}` in page sources). With JavaScript, `main.js` sends readable JSON in the background (skipping empty and hidden-for-this-enquirer fields), then shows the element named by `data-success`. On failure it shows the element named by `data-status` (or the newsletter message) instead. Each form has a hidden `_gotcha` spam trap and hidden `form`/`_subject` fields. Newsletter sign-ups go to the same Formspree form for now. See the README's "Forms" section.

## Launch checklist

The README's **Launch checklist** is the single list of what is left, in priority order:
1. **Blocking before go-live:** test the forms (connected to Formspree), the mailbox, the registered address, naming providers in the privacy policy, a legal review, the ICO fee, and social accounts. The domain (`https://sandboxenglish.co.uk`, GitHub Pages with HTTPS enforced) and `main` as the default branch are done. Keep the root `CNAME` file.
2. **Before promoting:** accreditation, founder headshot, DSL training, written policies, a phone/WhatsApp number, booking and agent terms, and insurance. Google Search Console and Bing Webmaster Tools are done (keep the `google-site-verification` TXT record in DNS).
3. **Before taking the first booking or payment:** accreditation first, package-travel wording in the booking terms, a trust arrangement for customer money, working capital, bank accounts, VAT advice, booking form and e-signature tools, a data protection impact assessment, privacy policy updates, and an end-to-end test. The plan is in the README's "Bookings and payments" section.
4. **When venues and dates are confirmed:** name them, swap in venue photos, add dates, and update the rules in this file.
5. **After the first summer:** real photos (with consent), testimonials, and removing "new school" wording.

When you finish an item, tick it in the README (`- [x]`) in the same commit. If a change affects an item (e.g. connecting a form provider), update the related pages too: the privacy policy's providers and the cookie policy if the provider sets cookies or loads scripts. Don't mark legal or business items (insurance, ICO fee, legal review) as done unless the user confirms them.
