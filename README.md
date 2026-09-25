# Sandbox English Summer School — website

Marketing website for **Sandbox English** (trading as **Sandbox English Summer School**), a residential English summer school for young people aged 8–17 in London and the Thames Valley. **The first summer is 2028.** The site will live at **sandboxenglish.co.uk**.

The site is for **parents, agents and group leaders**. Its job is to get them to **book a free consultation**. No prices are published: every quote is tailored after the consultation.

It's a fast, dependency-free static site (HTML + CSS + vanilla JS) that can be hosted anywhere (GitHub Pages, Netlify, Cloudflare Pages…).

## Editing and building

The pages in the repo root are **generated**. Edit the sources in `src/pages/`, then rebuild:

```bash
python3 src/build.py            # regenerates the root *.html files, credits.html, sitemap.xml and robots.txt
python3 -m http.server 8000     # preview at http://localhost:8000
```

The build needs only Python 3.11+, with no packages. It adds the shared `<head>`, header, navigation and footer to every page and expands a few shortcodes. The site URL, email address and social links are set once at the top of `src/build.py` (`SITE_URL`, `EMAIL`, `SOCIAL`).

The build stops with an error if a shortcode is mistyped, a photo file is missing, or a photo has no entry in `credits.json`. Running it twice gives identical output.

| Shortcode | Output |
| --- | --- |
| `{{photo:slug\|alt\|variant\|caption}}` | A photo for `assets/img/photos/<slug>.jpg` with a smaller version for phones (`variant` is empty, `wide`, or `tall` for the hero, which loads first) |
| `{{trips}}` | The excursion option cards (defined in `TRIPS`) |
| `{{icon:name}}` | An inline SVG icon (defined in `ICON`) |

Page front matter is `title:`, `description:` and optionally `robots: noindex`.

Commit both the sources and the regenerated HTML, because the host serves the HTML as-is.

## Pages

The site is deliberately small: three main pages, plus legal and utility pages linked from the footer.

| File | Purpose |
| --- | --- |
| `index.html` | Everything families need, in sections the nav links to: who we work with, the programme (`#programme`), safety and welfare (`#safety`), a typical day (`#day`), summer life (`#summer-life`), excursions (`#excursions`), food (`#food`), locations (`#locations`), about the founder (`#about`), FAQs (`#faq`) |
| `agents.html` | For agents (`#agents`) and group leaders (`#groups`), plus an FAQ for partners (`#agent-faq`) |
| `consultation.html` | Consultation form. It shows extra questions for agents and group leaders, and needs a phone number when phone or WhatsApp is chosen. Pre-fills from `?type=parent\|agent\|group` and `?area=london\|thames-valley` |
| `privacy.html`, `terms.html`, `cookies.html` | Privacy policy, terms of use and cookie policy |
| `credits.html` | Photo credits, generated from `assets/img/photos/credits.json` (not indexed by search engines) |
| `404.html` | "Page not found" (GitHub Pages serves it automatically) |

```
src/build.py            page generator (head, header, footer, icons, photos, trips, sitemap)
src/pages/*.html        page sources
src/images.py           makes the 800px photo versions (needs Pillow)
src/brand.py            regenerates the logo files in assets/brand/ (needs fonttools)
assets/css/styles.css   self-hosted fonts, design tokens and all components
assets/js/main.js       nav, scroll reveal, form validation and form logic, pre-fill
assets/fonts/           Fraunces and DM Sans (woff2, SIL Open Font License)
assets/brand/           print-ready logos for shirts, lanyards and documents
assets/img/share.jpg    1200×630 preview image shown when the site is shared
assets/img/photos/      photos (one file per slot, plus <slug>-800.jpg) + credits.json
```

## Brand

- **Name:** Sandbox English, trading as Sandbox English Summer School. Web: sandboxenglish.co.uk. Email: `hello@sandboxenglish.co.uk`. Social: @sandboxenglish.
- **Logo:** a speech bubble containing a wave and a sun (English, summer and the seaside). It uses two colours only, so it prints cleanly on shirts and lanyards, and every version also works in a single colour.
- **Colours:** navy `#14213d` and coral `#f2603d` are the core brand pair. On the website, buttons and banners use a deeper coral `#c2412d` so white text is readable, and small coral text uses `#b83a22`. Sand `#fdf9f1`/`#f8efdc` is the web background. Sea `#2a9d8f`, sun `#f7b733` and sky `#4a7fd6` are web accents only. Ask your printer to match navy and coral to the nearest Pantone.
- **Type:** Fraunces (bold display serif) for "Sandbox", and DM Sans (bold, spaced capitals) for "ENGLISH SUMMER SCHOOL". Both are free Google Fonts. The website serves its own copies from `assets/fonts/`, so no request goes to Google.

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

Every photo has a fixed slot: `assets/img/photos/<slug>.jpg`, plus a smaller `<slug>-800.jpg` that phones download instead. To add or replace a photo:

1. Save it pre-cropped to the slot's shape: 16:10 for `wide` slots, 4:5 for the hero, and 4:3 for everything else. Save around 1600px wide, or 1200px for the hero.
2. Add or update its entry in `assets/img/photos/credits.json`.
3. Run `python3 src/images.py`, then `python3 src/build.py`.

Sandbox English has no photos of its own yet. The current photos are free stock photos from [Pexels](https://www.pexels.com/license/) (no credit required), apart from two from [Wikimedia Commons](https://commons.wikimedia.org) (CC BY-SA, which requires credit). Every photo's photographer, licence and source is recorded in `credits.json`, and the build turns that into `credits.html`.

**Rules for every photo**
- Children's faces must never be visible. Show them from behind, as silhouettes, or as hands only.
- Don't use photos of possible venues, or name venues anywhere (captions, alt text, file names or credit links), until they are confirmed.
- Use only images you're licensed to use.

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
| `location-campus.jpg` | A modern glass building among trees | Pexels | index.html |
| `location-grounds.jpg` | A large tree on a sunny green lawn | Pexels | index.html |
| `location-london.jpg` | London and the River Thames from above, at dawn | Pexels | index.html |
| `location-thames-valley.jpg` | A riverside meadow under a summer sky | Pexels | index.html |
| `location-windsor.jpg` | The Round Tower at Windsor Castle | Pexels | index.html |
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
- Three meals a day and a packed lunch on excursion days, with dietary needs catered for. Rooms separated by age and gender. Daily time to call home and phone-free lessons. Airport meet-and-greet and transfers available.
- Locations: **London and the Thames Valley** (no venues named).
- Founder: **Alexander Burns**, a student with several years' experience delivering enjoyable summer programmes, who founded Sandbox English to offer a better experience at a reasonable price.
- Contact: `hello@sandboxenglish.co.uk`, @sandboxenglish on Instagram, Facebook and YouTube.

## ⚠️ Launch checklist

Work through these in order. Tick items off by editing this file, so the next session knows where things stand.

### 1. Must be done before the site goes live

These are blocking. Launching without them would lose enquiries or break UK law.

- [ ] **Connect the consultation form** to a form service (e.g. Formspree or Netlify Forms). Until then, every enquiry is silently lost. See [Wiring up the forms](#wiring-up-the-forms).
- [ ] **Connect the newsletter sign-up** to an email provider (e.g. Mailchimp, Brevo or Buttondown), or remove the form from the footer in `src/build.py`.
- [ ] **Send a test submission** of both forms from a phone and a computer, and check they arrive.
- [ ] **Set up the mailbox** `hello@sandboxenglish.co.uk` and check it receives mail.
- [ ] **Add the registered address** (and company number, if Sandbox English is a limited company) to `src/pages/privacy.html` ("Who we are") and to the footer in `src/build.py`.
- [ ] **Name the form and email providers in the privacy policy** ("Who we share it with"), with where they store data.
- [ ] **Have the legal pages reviewed** by a solicitor or a reputable template service. `privacy.html`, `terms.html` and `cookies.html` are careful first drafts, not legal advice.
- [ ] **Register with the ICO and pay the data protection fee**, unless exempt. Most organisations that handle personal data must do this. Check at [ico.org.uk/fee](https://ico.org.uk/for-organisations/data-protection-fee/).
- [ ] **Check the cookie policy is still true** once the forms are connected. If a provider sets cookies or loads scripts, update `cookies.html` and add a consent banner for anything non-essential.
- [ ] **Create the social accounts** @sandboxenglish on Instagram, Facebook and YouTube (the footer links to them), or remove any you won't use from `SOCIAL` in `src/build.py`.
- [ ] **Point the domain at the site.** See [Going live](#going-live-on-sandboxenglishcouk). Then check `https://sandboxenglish.co.uk` loads with the padlock (HTTPS).
- [ ] **Make `main` the default branch** on GitHub (Settings → General). GitHub Pages should publish from `main`.

### 2. Strongly recommended before promoting the site

These build trust with parents and agents.

- [ ] **Add a photo of Alexander** to the About section (`#about` in `src/pages/index.html`). Adult faces are fine.
- [ ] **Name the Designated Safeguarding Lead** in the Safety section. Have the safeguarding, anti-bullying, online safety and code-of-conduct policies written and ready to send, since the site promises them on request.
- [ ] **Add a contact phone or WhatsApp number**, at least for agents and group leaders. Add it to the footer in `src/build.py` and the consultation page's sidebar.
- [ ] **Have booking terms and conditions ready.** The terms of use say every booking has separate booking terms, sent with the quote.
- [ ] **Write the agent terms** (commission, booking deadlines, payment schedule) so they can be confirmed in writing after a consultation, as the agents page promises.
- [ ] **Arrange insurance** (public liability and any other cover a residential course for children needs) before quoting.
- [ ] **State accreditation or membership honestly** once you have it (e.g. British Council, English UK). Don't add logos until they're granted.
- [ ] **Replace the Harry Potter Studio Tour and Madame Tussauds photos** with the venues' official press images, or confirm the current CC BY-SA photos are acceptable for advertising.
- [ ] **Set up Google Search Console** (and Bing Webmaster Tools) and submit `https://sandboxenglish.co.uk/sitemap.xml`.
- [ ] **Check the share preview** by pasting the site link into WhatsApp and a social network. The 1200×630 image is `assets/img/share.jpg`.

### 3. When venues and dates are confirmed

- [ ] **Name the venues** on the home page (`#locations`) and in the FAQs, and replace the regional location photos with real photos of the venues (with permission).
- [ ] **Add course dates** and update the "When does it start?" and "Where will the course take place?" FAQs.
- [ ] **Update `CLAUDE.md` and the "Confirmed facts" section** of this README, so the no-venue rule is lifted and new facts can be used.
- [ ] **Add location pre-fill links** for the confirmed venues, and update the consultation form's "Preferred area" options if needed.

### 4. After the first summer

- [ ] **Replace stock photos with real ones** from the first summer. Get written parental consent, and keep to the rule that no child's face is visible.
- [ ] **Add testimonials** from parents, agents and group leaders, with their permission.
- [ ] **Remove "new school" wording** such as the "Why choose a new summer school?" FAQ.

## Wiring up the forms

Both forms work front-end only right now. They validate input, then show a success message without sending anything. To make them live:

1. **Consultation form** (`src/pages/consultation.html`, `#consultation-form`): set `action` to the form service's endpoint (e.g. `https://formspree.io/f/xxxx`). Once `action` is not `#`, the form submits normally after validation. Most services then show their own thank-you page, or redirect back to a page you choose.
2. **Newsletter** (footer, in `src/build.py`): set the form's `action` to your email provider's sign-up URL, and rename the input's `name` if the provider needs a different field name. It then submits normally.
3. Run `python3 src/build.py`, commit, and send a test from each form.

Don't embed a provider's script or iframe without updating `cookies.html`. The site currently makes no third-party requests, and the cookie policy says so.

## Going live on sandboxenglish.co.uk

1. On GitHub, go to Settings → Pages and publish from `main`, root folder.
2. In the same screen, add the custom domain `sandboxenglish.co.uk` and follow GitHub's DNS instructions at your domain registrar (A records for the bare domain, a CNAME for `www`).
3. Once the certificate is issued, tick **Enforce HTTPS**.

Canonical links, the sitemap, `robots.txt` and the share image already use `https://sandboxenglish.co.uk`.

GitHub Pages serves `404.html` automatically. Its links are relative, so it works for mistyped top-level addresses (e.g. `/wrong-page`). Deeper mistyped paths may show it without styling.

## Recommendations and next steps

**For conversions**
- Let people pick a consultation time directly, for example with a Calendly or Microsoft Bookings link on the thank-you message. Check the tool's cookies first.
- Offer a downloadable one-page **fact sheet** (PDF) for agents to share with families. It could also be offered to parents.
- Add a short **"For parents" summary**: who to contact during the course, how updates work, and what happens after booking.

**For reach**
- **Translated landing sections** for key markets (e.g. Spanish, Italian, Chinese), starting with a translated summary and the consultation form.
- **Structured data** could be extended with course dates and location once confirmed, which helps search results.
- If you add **analytics**, choose a cookie-free option (e.g. Plausible or Fathom) so no consent banner is needed, and update `cookies.html` and the privacy policy.

**Technical (optional)**
- Serve photos as WebP or AVIF alongside JPEG for smaller downloads (extend `src/images.py` and `photo()` in `src/build.py` to output a `<picture>`).
- Replace the remaining page-specific inline `style=` attributes with CSS utility classes.
- Consider a simple automated check (e.g. a GitHub Action running `python3 src/build.py` and checking for no diff) so the committed HTML always matches its sources.
