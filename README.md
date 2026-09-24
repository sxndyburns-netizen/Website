# Sandbox Languages — website

Marketing website for **Sandbox Languages**, a family-run residential English language summer school in the UK for students aged 8–17.

The site's job is to get families to **book a free consultation**. No prices are published: every quote is tailored after the consultation.

It's a fast, dependency-free static site (HTML + CSS + vanilla JS). There's no build step: open `index.html` in a browser, or host the folder on any static host (GitHub Pages, Netlify, Cloudflare Pages, S3…).

```bash
# local preview
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home: hero, key stats, programmes, family-run story, campuses, a day at Sandbox, excursions, consultation CTA |
| `programmes.html` | Tabbed detail for Junior Explorers (8–12), Teen Discovery (13–15), Young Leaders (16–17); teaching approach, sample timetable, inclusions. Tabs deep-link (`programmes.html#teens`) |
| `campuses.html` | Leighton Park School (`#leighton-park`: Quaker ethos, private parkland, food gallery, travel links) and Brunel University of London (`#brunel`), plus a comparison table (`#compare`) |
| `summer-life.html` | Activities, excursions, accommodation, food, welfare |
| `about.html` | Our story (family-run, how we keep costs low), safeguarding (`#safeguarding`), team, FAQs (`#faq`) |
| `consultation.html` | Book-a-consultation form (pre-fills from `?programme=`, `?campus=`, `?type=group`) and what to expect |

```
assets/css/styles.css   design tokens + all components
assets/js/main.js       nav, tabs, scroll reveal, form validation, form pre-fill
assets/img/photos/      real photos, one file per slot (see Photos below)
assets/img/favicon.svg  brand mark
```

The header and footer are repeated in each page. If you change navigation, update all six files.

## Photos

The site is built around real photography. Every photo has a fixed slot: save a JPG at `assets/img/photos/<name>.jpg` and it appears automatically. Until then, a tinted placeholder (or, for a few slots, an illustration) shows instead.

**Current photos** come from [Wikimedia Commons](https://commons.wikimedia.org) under open licences (mostly CC BY-SA and CC0). Those licences require credit, so every photo is listed with its photographer, licence and source in `assets/img/photos/credits.json`. The build turns that file into `credits.html`, linked from the footer. If you replace a photo with your own, delete its entry from `credits.json`.

The Leighton Park **food** photos are representative stock images, not Leighton Park's own dining. Replace them with photos from the school or its caterer (Thomas Franks) when you can.

**Rules for every photo**
- Children must never be identifiable. Show them from behind, at a distance, as silhouettes, or show hands only.
- Use only images you're licensed to use: your own photos, images supplied by the venues, or stock photos whose licence allows commercial use (e.g. Unsplash or Pexels). Photos of Warner Bros. Studio Tour and Madame Tussauds are usually licensed for editorial use only, so check the licence or ask the venue for press images.
- Landscape images around 1600px wide work best (the hero is portrait, around 1200×1500px).

| File | What it should show | Used on |
| --- | --- | --- |
| `activities-arts.jpg` | Hands painting at an art table | summer-life.html |
| `activities-drama.jpg` | Students on a stage facing an audience, seen from behind | summer-life.html |
| `activities-evening.jpg` | Students gathered around a campfire at dusk, seen from behind | summer-life.html |
| `activities-sport.jpg` | Students playing football on a sunny playing field, seen from behind | summer-life.html |
| `brunel-campus.jpg` | Modern buildings on the Brunel University of London campus in Uxbridge | campuses.html, index.html |
| `brunel-grounds.jpg` | Green spaces between buildings on the Brunel campus | campuses.html |
| `brunel-halls.jpg` | A modern single en-suite bedroom in Brunel's halls of residence | campuses.html |
| `brunel-sports.jpg` | Brunel's indoor sports and athletics facilities | campuses.html |
| `hero-students.jpg` | Students walking together across a sunny school campus, seen from behind | index.html |
| `leighton-park-classroom.jpg` | A bright classroom at Leighton Park | campuses.html |
| `leighton-park-fields.jpg` | Open playing fields in the Leighton Park grounds | campuses.html |
| `leighton-park-food-1.jpg` | A freshly cooked hot lunch served in the Leighton Park dining hall | campuses.html, index.html |
| `leighton-park-food-2.jpg` | A salad bar with fresh seasonal vegetables | campuses.html, index.html |
| `leighton-park-food-3.jpg` | Homemade desserts laid out for service | campuses.html, index.html |
| `leighton-park-food-4.jpg` | Students eating together in the dining hall, seen from behind | campuses.html |
| `leighton-park-food-5.jpg` | A breakfast spread with fresh fruit, pastries and hot options | campuses.html |
| `leighton-park-food-6.jpg` | Fresh seasonal fruit ready for students | campuses.html |
| `leighton-park-grounds.jpg` | Leighton Park School's main building set in green parkland | campuses.html, index.html |
| `leighton-park-oaks.jpg` | Mature oak trees in the Leighton Park grounds | campuses.html |
| `leighton-park-pool.jpg` | The covered swimming pool at Leighton Park | campuses.html |
| `lessons.jpg` | Students raising their hands in a bright classroom, seen from behind | index.html |
| `programme-juniors.jpg` | Young students working on a craft project at a table, seen from behind | index.html, programmes.html |
| `programme-leaders.jpg` | Older students in a seminar room facing a presentation screen, seen from behind | index.html, programmes.html |
| `programme-teens.jpg` | Teenagers sitting on the grass on a sunny day, seen from behind | index.html, programmes.html |
| `trip-cambridge.jpg` | King's College Chapel and the River Cam in Cambridge | index.html, summer-life.html |
| `trip-harry-potter.jpg` | The Warner Bros. Studio Tour London, home of the Harry Potter film sets | index.html, summer-life.html |
| `trip-london.jpg` | Students on a guided walking tour in central London | index.html, summer-life.html |
| `trip-madame-tussauds.jpg` | The entrance to Madame Tussauds London | index.html, summer-life.html |
| `trip-oxford.jpg` | Historic college buildings in Oxford | index.html, summer-life.html |

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
- **Staff ratios, class sizes, bedtimes, excursions and facilities.**
- **Contact details:** `hello@sandboxlanguages.co.uk`, `+44 (0)1234 567890`.
- **Social links, privacy policy, T&Cs and cookie pages** currently point to `#`.
- **Team:** role cards only. Add the family's names and photos.
- **Accreditation:** none is claimed. Add logos only if held.

## Wiring up the forms

Both forms work front-end only right now. They validate input, then show a success message without sending anything. To make them live:

1. **Consultation form** (`consultation.html`, `#consultation-form`): set `action` to a form endpoint (e.g. Formspree, Netlify Forms with `data-netlify="true"`, or your CRM). Once `action` is not `#`, the form submits normally after validation.
2. **Newsletter** (footer): hook the submit handler in `main.js` up to your email provider (Mailchimp, Brevo, etc.).

## Suggested next steps

- Real photography, testimonials and accreditation logos
- Let families pick a consultation slot directly (e.g. embed a Calendly or Microsoft Bookings link)
- Translated landing pages for key markets (ES, IT, FR, TR, ZH…)
- Analytics + cookie consent, sitemap.xml, robots.txt and structured data (`EducationalOrganization`)
