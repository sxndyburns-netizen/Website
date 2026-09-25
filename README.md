# Sandbox English Summer School — website

Marketing website for **Sandbox English** (trading as **Sandbox English Summer School**), a residential English summer school for young people aged 8–17 in London and the Thames Valley. **The first summer is 2028.** The site will live at **sandboxenglish.co.uk**.

The site is for **parents, agents and group leaders**. Its job is to get them to **book a free consultation**. No prices are published: every quote is tailored after the consultation.

It's a fast, dependency-free static site (HTML + CSS + vanilla JS) that can be hosted anywhere (GitHub Pages, Netlify, Cloudflare Pages…).

## Editing and building

The pages in the repo root are **generated**. Edit the sources in `src/pages/`, then rebuild:

```bash
python3 src/build.py            # regenerates the root *.html files and credits.html
python3 -m http.server 8000     # preview at http://localhost:8000
```

The build needs only Python 3.11+, with no packages. It adds the shared `<head>`, header, navigation and footer to every page and expands a few shortcodes. The site URL, email address and social links are set once at the top of `src/build.py` (`SITE_URL`, `EMAIL`, `SOCIAL`).

| Shortcode | Output |
| --- | --- |
| `{{photo:slug\|alt\|variant\|caption}}` | A photo slot for `assets/img/photos/<slug>.jpg` (`variant` is empty, `wide` or `tall`) |
| `{{trips}}` | The excursion option cards (defined in `TRIPS`) |
| `{{icon:name}}` | An inline SVG icon (defined in `ICON`) |

Commit both the sources and the regenerated HTML, because the host serves the HTML as-is.

## Pages

The site is deliberately small: three main pages, plus a photo credits page linked from the footer.

| File | Purpose |
| --- | --- |
| `index.html` | Everything families need, in sections the nav links to: who we work with, the programme (`#programme`), a typical day (`#day`), summer life (`#summer-life`), excursions (`#excursions`), food (`#food`), locations (`#locations`), safety and welfare (`#safety`), about the founder (`#about`), FAQs (`#faq`) |
| `agents.html` | For agents (`#agents`) and group leaders (`#groups`) |
| `consultation.html` | Consultation form. Pre-fills from `?type=parent\|agent\|group` and `?area=london\|thames-valley` |
| `credits.html` | Photo credits, generated from `assets/img/photos/credits.json` |

```
src/build.py            page generator (header, footer, icons, photo and trip markup)
src/pages/*.html        page sources
src/brand.py            regenerates the logo files in assets/brand/
assets/css/styles.css   design tokens + all components
assets/js/main.js       nav, tabs, scroll reveal, form validation, form pre-fill
assets/brand/           print-ready logos for shirts, lanyards and documents
assets/img/photos/      photos (one file per slot) + credits.json
```

## Brand

- **Name:** Sandbox English, trading as Sandbox English Summer School. Web: sandboxenglish.co.uk. Email: `hello@sandboxenglish.co.uk`. Social: @sandboxenglish.
- **Logo:** a speech bubble containing a wave and a sun (English, summer and the seaside). It uses two colours only, so it prints cleanly on shirts and lanyards, and every version also works in a single colour.
- **Colours:** navy `#14213d` and coral `#f2603d` are the core brand pair. Sand `#fdf9f1`/`#f8efdc` is the web background. Sea `#2a9d8f`, sun `#f7b733` and sky `#4a7fd6` are web accents only. Ask your printer to match navy and coral to the nearest Pantone.
- **Type:** Fraunces (bold display serif) for "Sandbox", and DM Sans (bold, spaced capitals) for "ENGLISH SUMMER SCHOOL". Both are free Google Fonts.

**Logo files** (`assets/brand/`, text already converted to outlines for print):

| File | Use |
| --- | --- |
| `logo-full-colour.svg` | Website, documents, white or light shirts |
| `logo-navy.svg` | One-colour print on light fabric or paper |
| `logo-white.svg` | Navy or coral shirts, dark backgrounds |
| `logo-stacked-*.svg` | Shirt chest or back prints, square spaces (full colour, navy, white) |
| `mark-*.svg` | The bubble on its own: sleeves, social avatars, favicons |
| `lanyard-navy.svg`, `lanyard-coral.svg` | One repeat of the lanyard design (20mm high). The printer tiles it along the strap |

## Photos

Every photo has a fixed slot: `assets/img/photos/<slug>.jpg`. If a file is missing, a tinted placeholder shows instead, so replacing a photo is just a matter of saving a new file with the same name.

Sandbox English has no photos of its own yet. The current photos are free stock photos from [Pexels](https://www.pexels.com/license/) (no credit required) and openly licensed photos from [Wikimedia Commons](https://commons.wikimedia.org) (CC BY-SA, which requires credit). The location photos show real potential sites, but captions describe them only in general terms. Every photo's photographer, licence and source is recorded in `assets/img/photos/credits.json`, and the build turns that into `credits.html`. When you add, replace or remove a photo, update its entry and rebuild.

**Rules for every photo**
- Children's faces must never be visible. Show them from behind, as silhouettes, or as hands only.
- Don't name venues in captions or alt text until they are confirmed.
- Use only images you're licensed to use.
- Crop to the slot's shape before saving: 16:10 for `wide` slots, 4:5 for the hero, and 4:3 for everything else. Save around 1600px wide, or 1200px for the hero.

| File | What it shows | Source | Used on |
| --- | --- | --- | --- |
| `activities-arts.jpg` | A student painting with a brush | Pexels | index.html |
| `activities-drama.jpg` | A theatre stage with red curtains | Pexels | index.html |
| `activities-evening.jpg` | Friends silhouetted around a bonfire | Pexels | index.html |
| `activities-sport.jpg` | A football on a floodlit pitch | Pexels | index.html |
| `food-1.jpg` | Roast chicken with vegetables | Pexels | index.html |
| `food-2.jpg` | Fresh salad at a buffet counter | Pexels | index.html |
| `food-3.jpg` | A selection of desserts | Pexels | index.html |
| `food-5.jpg` | Croissants and strawberries for breakfast | Pexels | index.html |
| `hero-students.jpg` | Students of different ages walking into school, seen from behind | Pexels | index.html |
| `lessons.jpg` | Students seated at desks in a classroom | Pexels | index.html |
| `location-arts-centre.jpg` | A modern music and arts centre on a school campus | Wikimedia Commons (CC BY-SA 4.0) | index.html |
| `location-campus-buildings.jpg` | Modern buildings and green space on a university campus in west London | Wikimedia Commons (CC BY-SA 4.0) | index.html |
| `location-campus-walkway.jpg` | A tree-lined walkway on a university campus in west London | Wikimedia Commons (CC BY-SA 4.0) | index.html |
| `location-modern-campus.jpg` | A curved glass building on a university campus in west London | Wikimedia Commons (CC BY-SA 4.0) | index.html |
| `location-parkland.jpg` | A historic school building across open parkland in the Thames Valley | Wikimedia Commons (CC BY-SA 4.0) | index.html |
| `location-parkland-hall.jpg` | A school hall framed by autumn trees in parkland | Wikimedia Commons (CC BY-SA 4.0) | index.html |
| `students-corridor.jpg` | Students with backpacks walking along a school corridor | Pexels | agents.html, index.html |
| `students-park.jpg` | Children running across a park with balloons | Pexels | index.html |
| `students-seminar.jpg` | Older students raising their hands in a seminar | Pexels | agents.html, index.html |
| `trip-cambridge.jpg` | A historic college in Cambridge | Pexels | agents.html, index.html |
| `trip-harry-potter.jpg` | The Great Hall set at the Warner Bros. Studio Tour London | Wikimedia Commons (CC BY-SA 4.0) | agents.html, index.html |
| `trip-london.jpg` | Westminster Bridge and the Houses of Parliament | Pexels | agents.html, index.html |
| `trip-madame-tussauds.jpg` | The exterior of Madame Tussauds London | Wikimedia Commons (CC BY-SA 4.0) | agents.html, index.html |
| `trip-oxford.jpg` | The Radcliffe Camera, Oxford | Pexels | agents.html, index.html |

## Confirmed facts (use freely)

- First summer: **2028**. Ages **8–17**. Residential. Stays of **one to six weeks**.
- **One programme**, with students grouped on site by age and English level. **Small classes** (no fixed number is published). A placement test before arrival and a speaking check on day one. Groups are reviewed during the course.
- **15 hours of English lessons a week.**
- **Two excursions a week**, chosen from many options and tailored to what parents and agents want. Every trip includes free time and a packed lunch.
- **Staff on site 24/7**, a **24/7 emergency line**, and **first-aid trained staff**. Safer recruitment and DBS checks for all staff. Safeguarding, anti-bullying, online safety and code-of-conduct policies.
- Three meals a day, with dietary needs catered for. Rooms separated by age and gender. Airport meet-and-greet and transfers available.
- Locations: **London and the Thames Valley** (no venues named).
- Founder: **Alexander Burns**, a student with several years' experience delivering enjoyable summer programmes, who founded Sandbox English to offer a better experience at a reasonable price.
- Contact: `hello@sandboxenglish.co.uk`, @sandboxenglish on Instagram, Facebook and YouTube.

## ⚠️ Still to do before launch

- Privacy policy, terms and cookie pages (currently `#`)
- Connect the consultation form and newsletter to real services (see below)
- Name the venues once they are confirmed

## Wiring up the forms

Both forms work front-end only right now. They validate input, then show a success message without sending anything. To make them live:

1. **Consultation form** (`src/pages/consultation.html`, `#consultation-form`): set `action` to a form endpoint (e.g. Formspree or Netlify Forms). Once `action` is not `#`, the form submits normally after validation.
2. **Newsletter** (footer, in `src/build.py`): connect the submit handler in `main.js` to your email provider.

## Going live on sandboxenglish.co.uk

With GitHub Pages: go to Settings → Pages, publish from `main` / root, then add the custom domain `sandboxenglish.co.uk` and follow GitHub's DNS instructions at your domain registrar. Canonical links in every page already point to `https://sandboxenglish.co.uk`.

## Suggested next steps

- Real photos from the first summer (with parental consent), testimonials, and venue photos once venues are confirmed
- Let people book a consultation slot directly (e.g. a Calendly or Microsoft Bookings link)
- Translated landing pages for key markets
- Analytics and cookie consent, sitemap.xml, robots.txt and structured data (`EducationalOrganization`)
