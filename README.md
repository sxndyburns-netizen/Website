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
assets/img/campuses/leighton-park/   drop food photos here (see below)
assets/img/favicon.svg  brand mark
```

The header and footer are repeated in each page. If you change navigation, update all six files.

## Leighton Park food photos

The food gallery on `campuses.html` shows illustrated placeholders until real photos are added. Save four images as:

```
assets/img/campuses/leighton-park/food-1.jpg   hot meals cooked fresh on site
assets/img/campuses/leighton-park/food-2.jpg   salad bar & seasonal produce
assets/img/campuses/leighton-park/food-3.jpg   homemade puddings
assets/img/campuses/leighton-park/food-4.jpg   mealtimes together
```

They appear automatically, with no code changes. Landscape images around 1200×900px work best. **Use only photos you have permission to use.** Ask Leighton Park's lettings/summer team or their caterer for marketing images.

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
