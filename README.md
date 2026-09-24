# Sandbox Languages — website

Marketing website for **Sandbox Languages**, a family-run residential English language summer school in the UK for students aged 8–17.

The site's job is to get families to **book a free consultation**. No prices are published: every quote is tailored after the consultation.

It's a fast, dependency-free static site (HTML + CSS + vanilla JS) that can be hosted anywhere (GitHub Pages, Netlify, Cloudflare Pages, S3…).

## Editing and building

The pages in the repo root are **generated**. Edit the sources in `src/pages/`, then rebuild:

```bash
python3 src/build.py            # regenerates the root *.html files and credits.html
python3 -m http.server 8000     # preview at http://localhost:8000
```

The build needs only Python 3.11+, with no packages. It adds the shared header, navigation and footer to every page and expands a few shortcodes, so a change to the nav or footer is made once in `src/build.py`:

| Shortcode | Output |
| --- | --- |
| `{{photo:slug\|alt\|variant\|caption}}` | A photo slot for `assets/img/photos/<slug>.jpg` (`variant` is empty, `wide` or `tall`) |
| `{{trips}}` | The five excursion cards (defined in `TRIPS`) |
| `{{icon:name}}` | An inline SVG icon (defined in `ICON`) |

Commit both the sources and the regenerated HTML, because the host serves the HTML as-is.

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home: hero, key stats, programmes, family-run story, campuses, Leighton Park dining, a typical day, excursions, consultation CTA |
| `programmes.html` | Tabbed detail for Junior Explorers (8–12), Teen Discovery (13–15), Young Leaders (16–17); teaching approach, sample timetable, inclusions. Tabs deep-link (`programmes.html#teens`) |
| `campuses.html` | Leighton Park School (`#leighton-park`: Quaker ethos, private parkland, food gallery, travel links) and Brunel University of London (`#brunel`), plus a comparison table (`#compare`) |
| `summer-life.html` | Activities, excursions, accommodation, food, welfare |
| `about.html` | Our story (family-run, how we keep costs low), safeguarding (`#safeguarding`), team, FAQs (`#faq`) |
| `consultation.html` | Book-a-consultation form (pre-fills from `?programme=`, `?campus=`, `?type=group`) and what to expect |
| `credits.html` | Photo credits, generated from `assets/img/photos/credits.json` |

```
src/build.py            page generator (header, footer, icons, photo and trip markup)
src/pages/*.html        page sources
assets/css/styles.css   design tokens + all components
assets/js/main.js       nav, tabs, scroll reveal, form validation, form pre-fill
assets/img/photos/      photos (one file per slot) + credits.json
assets/img/favicon.svg  brand mark
```

## Photos

Every photo has a fixed slot: `assets/img/photos/<slug>.jpg`. If a file is missing, a tinted placeholder shows instead, so replacing a photo is just a matter of saving a new file with the same name.

**Sources.** The current photos are free stock photos from [Pexels](https://www.pexels.com/license/) (no credit required), plus openly licensed photos from [Wikimedia Commons](https://commons.wikimedia.org) of the campuses, the Harry Potter Studio Tour and Madame Tussauds. The Commons licences (CC BY-SA) require credit. Every photo's photographer, licence and source is recorded in `assets/img/photos/credits.json`, and the build turns that into `credits.html`, linked from the footer. When you add, replace or remove a photo, update its entry and rebuild.

**Rules for every photo**
- Children's faces must never be visible. Show them from behind, as silhouettes, or as hands only.
- Use only images you're licensed to use: your own photos, images supplied by the venues, or stock photos whose licence allows commercial use.
- Crop to the slot's shape before saving: 16:10 for `wide` slots, 4:5 for the hero, and 4:3 for everything else. Save around 1600px wide, or 1200px for the hero.

**To replace when possible**
- The six **Leighton Park food** photos are representative stock images, not Leighton Park's own dining. Ask the school or its caterer (Thomas Franks) for real ones.
- The **Harry Potter Studio Tour** and **Madame Tussauds** photos are CC BY-SA community photos. The venues' official press images would be the more cautious choice for advertising.
- Real photos of **Leighton Park's** playing fields, pool and boarding houses, and **Brunel's** en-suite rooms and sports facilities, would strengthen the Campuses page. There were none available to use.

| File | What it shows | Source | Used on |
| --- | --- | --- | --- |
| `activities-arts.jpg` | A student painting with a brush | Pexels | summer-life.html |
| `activities-drama.jpg` | A theatre stage with red curtains | Pexels | summer-life.html |
| `activities-evening.jpg` | Friends silhouetted around a bonfire | Pexels | summer-life.html |
| `activities-sport.jpg` | A football on a floodlit pitch | Pexels | summer-life.html |
| `brunel-buildings.jpg` | Modern buildings and green space on the Brunel campus | Wikimedia Commons (CC BY-SA 4.0) | campuses.html |
| `brunel-campus.jpg` | A curved glass building on the Brunel University of London campus | Wikimedia Commons (CC BY-SA 4.0) | campuses.html, index.html |
| `brunel-grounds.jpg` | A tree-lined walkway on the Brunel campus | Wikimedia Commons (CC BY-SA 4.0) | campuses.html |
| `hero-students.jpg` | Children walking hand in hand, seen from behind | Pexels | index.html |
| `leighton-park-food-1.jpg` | Roast chicken with vegetables | Pexels | campuses.html, index.html |
| `leighton-park-food-2.jpg` | Fresh salad at a buffet counter | Pexels | campuses.html, index.html |
| `leighton-park-food-3.jpg` | A selection of desserts | Pexels | campuses.html, index.html |
| `leighton-park-food-4.jpg` | A dining hall with tables set out | Pexels | campuses.html |
| `leighton-park-food-5.jpg` | Croissants and strawberries for breakfast | Pexels | campuses.html |
| `leighton-park-food-6.jpg` | Fresh oranges and melons | Pexels | campuses.html |
| `leighton-park-grounds.jpg` | The Old School building across parkland at Leighton Park School | Wikimedia Commons (CC BY-SA 4.0) | campuses.html, index.html |
| `leighton-park-music.jpg` | The Michael Malnick Centre for music and media at Leighton Park | Wikimedia Commons (CC BY-SA 4.0) | campuses.html |
| `leighton-park-oaks.jpg` | Peckover Hall at Leighton Park framed by autumn trees | Wikimedia Commons (CC BY-SA 4.0) | campuses.html |
| `lessons.jpg` | Students seated at desks in a classroom | Pexels | index.html |
| `programme-juniors.jpg` | Children running across a park with balloons | Pexels | index.html, programmes.html |
| `programme-leaders.jpg` | Older students raising their hands in a seminar | Pexels | index.html, programmes.html |
| `programme-teens.jpg` | Students with backpacks walking along a school corridor | Pexels | index.html, programmes.html |
| `trip-cambridge.jpg` | A historic college in Cambridge | Pexels | index.html, summer-life.html |
| `trip-harry-potter.jpg` | The Great Hall set at the Warner Bros. Studio Tour London | Wikimedia Commons (CC BY-SA 4.0) | index.html, summer-life.html |
| `trip-london.jpg` | Westminster Bridge and the Houses of Parliament | Pexels | index.html, summer-life.html |
| `trip-madame-tussauds.jpg` | The exterior of Madame Tussauds London | Wikimedia Commons (CC BY-SA 4.0) | index.html, summer-life.html |
| `trip-oxford.jpg` | The Radcliffe Camera, Oxford | Pexels | index.html, summer-life.html |

## Design system

- **Concept:** a "sandbox" is where children build, experiment and play without fear of mistakes. That's the brand's teaching philosophy, so the look is warm, sunny and playful but trustworthy for parents.
- **Palette** (CSS custom properties in `:root`): sand `#fdf9f1`/`#f8efdc`, navy `#14213d` (text, trust), coral `#f2603d` (primary action), sea `#2a9d8f`, sun `#f7b733`, sky `#4a7fd6`.
- **Type:** Fraunces (display serif, soft and friendly) + DM Sans (body), via Google Fonts.
- **Logo:** a speech bubble over a strip of sand in a rounded navy tile (inline SVG, plus `favicon.svg`).
- **Accessibility:** skip link, semantic landmarks, keyboard-operable tabs and menu (Esc closes), visible focus rings, `aria-live` form errors, `prefers-reduced-motion` support, no horizontal scroll at 390px.

## ⚠️ Content to confirm before launch

- **Campuses:** both are described as Sandbox campuses. Confirm the agreements with each venue before launch. Venue facts came from public sources in September 2026:
  - Leighton Park: Quaker school founded 1890, 65 acres of parkland, ~30 min to Heathrow by road, ~25 min to Paddington by train, Elizabeth line from Reading, catering by Thomas Franks.
  - Brunel: single-site campus in Uxbridge, en-suite halls, ~20 min to Heathrow, ~40 min to central London by tube.
  Check that summer catering and rooms match what the venues will provide for your groups.
- **"Discounted rate" claims** about Leighton Park catering and campus partnerships. Make sure these reflect your actual agreements.
- **Staff ratios, class sizes, bedtimes and facilities.** Excursions are fixed: London walking tour, Oxford, Cambridge, Harry Potter Studio Tour and Madame Tussauds, each with free time and a packed lunch.
- **Contact details:** `hello@sandboxlanguages.co.uk`, `+44 (0)1234 567890`.
- **Social links, privacy policy, T&Cs and cookie pages** currently point to `#`.
- **Team:** role cards only. Add the family's names and photos.
- **Accreditation:** none is claimed. Add logos only if held.

## Wiring up the forms

Both forms work front-end only right now. They validate input, then show a success message without sending anything. To make them live:

1. **Consultation form** (`consultation.html`, `#consultation-form`): set `action` to a form endpoint (e.g. Formspree, Netlify Forms with `data-netlify="true"`, or your CRM). Once `action` is not `#`, the form submits normally after validation.
2. **Newsletter** (footer): hook the submit handler in `main.js` up to your email provider (Mailchimp, Brevo, etc.).

## Suggested next steps

- Leighton Park's own food and campus photos, testimonials and accreditation logos
- Let families pick a consultation slot directly (e.g. embed a Calendly or Microsoft Bookings link)
- Translated landing pages for key markets (ES, IT, FR, TR, ZH…)
- Analytics + cookie consent, sitemap.xml, robots.txt and structured data (`EducationalOrganization`)
