# Sandbox Languages — website

Marketing website for **Sandbox Languages**, a residential English language summer school in the UK for students aged 8–17.

It's a fast, dependency-free static site (HTML + CSS + vanilla JS). There's no build step: open `index.html` in a browser, or host the folder on any static host (GitHub Pages, Netlify, Cloudflare Pages, S3…).

```bash
# local preview
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home: hero, key stats, programme cards, approach, a day at Sandbox, excursions, CTA |
| `programmes.html` | Tabbed detail for Junior Explorers (8–12), Teen Discovery (13–15), Young Leaders (16–17); teaching approach, sample timetable, inclusions. Tabs deep-link (`programmes.html#teens`) |
| `summer-life.html` | Campus, activities, excursions, accommodation, food, welfare |
| `dates-fees.html` | 2027 start dates and availability, **interactive fee calculator**, inclusions, booking steps, offers |
| `about.html` | Story, values, safeguarding (`#safeguarding`), team, FAQs (`#faq`) |
| `contact.html` | Validated enquiry form (pre-fills from `?programme=` and `?type=`), contact details |

```
assets/css/styles.css   design tokens + all components
assets/js/main.js       nav, tabs, scroll reveal, fee calculator, form validation
assets/img/favicon.svg  brand mark
```

The header and footer are repeated in each page. If you change navigation, update all six files.

## Design system

- **Concept:** a "sandbox" is where children build, experiment and play without fear of mistakes. That's the brand's teaching philosophy, so the look is warm, sunny and playful but trustworthy for parents.
- **Palette** (CSS custom properties in `:root`): sand `#fdf9f1`/`#f8efdc`, navy `#14213d` (text, trust), coral `#f2603d` (primary action), sea `#2a9d8f`, sun `#f7b733`, sky `#4a7fd6`.
- **Type:** Fraunces (display serif, soft and friendly) + DM Sans (body), via Google Fonts.
- **Logo:** a speech bubble over a strip of sand in a rounded navy tile (inline SVG, plus `favicon.svg`).
- **Accessibility:** skip link, semantic landmarks, keyboard-operable tabs and menu (Esc closes), visible focus rings, `aria-live` form errors, `prefers-reduced-motion` support, no horizontal scroll at 390px.

## ⚠️ Placeholder content to confirm before launch

The copy is realistic but **these details are assumptions and must be checked or replaced**:

- **Prices:** £1,190 / £1,290 / £1,390 per week; £95 registration; £350 deposit; extras (£260 transfer, £120 UM, £160/wk extra English, £90 theatre); 5% 3+ week saving; early-bird, sibling and group offers. These values live in `dates-fees.html` (calculator `data-rate` / `data-price` attributes), `index.html` and `programmes.html`.
- **Dates & availability:** Sundays 4 July – 8 August 2027, Young Leaders 11 July – 7 August; all "Open".
- **Campus & location:** described generically as a boarding-school campus in the English countryside. The excursions (London, Oxford, Cambridge, Brighton, Windsor, Canterbury) assume the south-east of England.
- **Staff ratios, class sizes, bedtimes and facilities** (pool, theatre, nurse, etc.).
- **Contact details:** `hello@sandboxlanguages.co.uk`, `+44 (0)1234 567890`, head-office address.
- **Social links, privacy policy, T&Cs and cookie pages** currently point to `#`.
- **Team:** role cards only. Add real names and photos.
- **Accreditation:** none is claimed. Add British Council / English UK / etc. logos only if held.
- **Imagery:** the site uses SVG illustrations. Swap in real campus photography when available.

## Wiring up the forms

Both forms work front-end only right now. They validate input, then show a success message without sending anything. To make them live:

1. **Enquiry form** (`contact.html`, `#enquiry-form`): set `action` to a form endpoint (e.g. Formspree, Netlify Forms with `data-netlify="true"`, or your CRM). Once `action` is not `#`, the form submits normally after validation.
2. **Newsletter** (footer): hook the submit handler in `main.js` up to your email provider (Mailchimp, Brevo, etc.).

## Suggested next steps

- Real photography, testimonials and accreditation logos
- Booking form with online deposit payment
- Translated landing pages for key markets (ES, IT, FR, TR, ZH…)
- Analytics + cookie consent, sitemap.xml, robots.txt and structured data (`EducationalOrganization`)
