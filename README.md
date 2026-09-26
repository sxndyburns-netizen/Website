# Sandbox English Summer School — website

Marketing website for **Sandbox English** (trading as **Sandbox English Summer School**), a residential English summer school for young people aged 8–17 in London or the area around London, whichever the family or agent chooses. **The first summer is 2028.** The site will live at **sandboxenglish.co.uk**.

The site is for **parents, agents and group leaders**. Its job is to get them to **book a free consultation**. No prices are published: every quote is tailored after the consultation.

It's a fast, dependency-free static site (HTML + CSS + vanilla JS) that can be hosted anywhere (GitHub Pages, Netlify, Cloudflare Pages…).

## Editing and building

The pages in the repo root are **generated**. Edit the sources in `src/pages/`, then rebuild:

```bash
python3 src/build.py            # regenerates the root *.html files, credits.html, sitemap.xml and robots.txt
python3 -m http.server 8000     # preview at http://localhost:8000
```

The build needs only Python 3.11+, with no packages. It adds the shared `<head>`, header, navigation and footer to every page and expands a few shortcodes. The site URL, email address, social links and company details are set once at the top of `src/build.py` (`SITE_URL`, `EMAIL`, `SOCIAL`, `COMPANY`).

The build stops with an error if a shortcode is mistyped, a photo file is missing, or a photo has no entry in `credits.json`. It prints a warning while any company detail is still a `[placeholder]`. Running it twice gives identical output.

| Shortcode | Output |
| --- | --- |
| `{{photo:slug\|alt\|variant\|caption}}` | A photo for `assets/img/photos/<slug>.jpg` with a smaller version for phones (`variant` is empty, `wide`, or `tall` for the hero, which loads first) |
| `{{trips}}` | The excursion option cards (defined in `TRIPS`) |
| `{{icon:name}}` | An inline SVG icon (defined in `ICON`) |
| `{{founder}}` | Alexander's portrait from `assets/img/photos/founder.jpg`, or an "AB" monogram until that file exists |
| `{{company:key}}` | A company detail from `COMPANY` (`name`, `number`, `office`, `ico`) |

Page front matter is `title:`, `description:` and optionally `robots: noindex`.

Commit both the sources and the regenerated HTML, because the host serves the HTML as-is.

## Pages

The site is deliberately small: three main pages, plus legal and utility pages linked from the footer.

| File | Purpose |
| --- | --- |
| `index.html` | Everything families need, in sections the nav links to: who we work with, the programme (`#programme`), about us and the founder (`#about`, "About us" in the nav), safety and welfare (`#safety`), a typical day (`#day`), summer life (`#summer-life`), excursions (`#excursions`), food (`#food`), locations (`#locations`), FAQs (`#faq`) |
| `agents.html` | For agents (`#agents`) and group leaders (`#groups`), plus an FAQ for partners (`#agent-faq`) |
| `consultation.html` | Consultation form. It shows extra questions for agents and group leaders, and needs a phone number when phone or WhatsApp is chosen. Pre-fills from `?type=parent\|agent\|group` and `?area=london\|around-london` |
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
- **Logo:** a speech bubble (English) holding a sandcastle with a flag (Sandbox), with a sun and a wave (summer), next to the "Sandbox" wordmark. The simple mark is used in the website header and as the browser-tab icon. On shirts and printed materials, the stacked version (mark above the name) acts as the badge. It uses two colours only, so it prints cleanly on shirts and lanyards, and every version also works in a single colour. The mark is drawn once in `src/brand.py` (print files) and `MARK` in `src/build.py` (website header and footer); keep the two in sync.
- **Colours:** navy `#14213d` and coral `#f2603d` are the core brand pair. On the website, buttons and banners use a deeper coral `#c2412d` so white text is readable, and small coral text uses `#b83a22`. Sand `#fdf9f1`/`#f8efdc` is the web background. Sea `#2a9d8f`, sun `#f7b733` and sky `#4a7fd6` are web accents only. Ask your printer to match navy and coral to the nearest Pantone.
- **Type:** Fraunces (bold display serif) for "Sandbox", and DM Sans (bold, spaced capitals) for "ENGLISH SUMMER SCHOOL". Both are free Google Fonts. The website serves its own copies from `assets/fonts/`, so no request goes to Google.

**Logo files** (`assets/brand/`, text already converted to outlines for print):

| File | Use |
| --- | --- |
| `logo-full-colour.svg` | Website, documents, white or light shirts |
| `logo-navy.svg` | One-colour print on light fabric or paper |
| `logo-white.svg` | Navy or coral shirts, dark backgrounds |
| `logo-stacked-*.svg` | The badge for shirt chest or back prints and square spaces (full colour, navy, white) |
| `logo-on-navy.svg`, `logo-stacked-on-navy.svg` | Two colours on navy shirts or dark backgrounds (white bubble and name, coral details) |
| `mark-*.svg` | The bubble on its own: sleeves, social avatars, favicons (`assets/img/favicon.svg` is a copy of `mark-full-colour.svg`) |

**Browser-tab icons.** Safari ignores SVG tab icons, so every page also links `favicon.ico` (16, 32 and 48px, in the site root) and `assets/img/apple-touch-icon.png` (180px, on the sand background, for Safari and iPhone home screens). `assets/img/favicon-32.png` is a spare 32px PNG. All are rendered from `mark-full-colour.svg`: regenerate them whenever the mark changes. The build adds a content hash to each icon link (e.g. `favicon.ico?v=a4a4537e`), so when an icon changes its address changes too and Safari fetches it again instead of keeping its cached copy. If Safari still shows an old icon or a letter tile, its saved icons are stale (Manage Website Data doesn't clear them, and Private windows still use them). Quit Safari, open `~/Library/Safari/Favicon Cache` in Finder (Go → Go to Folder…), move its contents to the Bin, and reopen Safari. If that folder isn't there, use History → Clear History… → all history.
| `lanyard-navy.svg`, `lanyard-coral.svg` | One repeat of the lanyard design (20mm high). The printer tiles it along the strap |

## Photos

Every photo has a fixed slot: `assets/img/photos/<slug>.jpg`, plus a smaller `<slug>-800.jpg` that phones download instead. To add or replace a photo:

1. Save it pre-cropped to the slot's shape: 16:10 for `wide` slots, 4:5 for the hero, and 4:3 for everything else. Save around 1600px wide, or 1200px for the hero.
2. Add or update its entry in `assets/img/photos/credits.json`.
3. Run `python3 src/images.py`, then `python3 src/build.py`.

Sandbox English has no photos of its own yet. The current photos are free stock photos from [Pexels](https://www.pexels.com/license/) (no credit required), apart from two from [Wikimedia Commons](https://commons.wikimedia.org) (CC BY-SA, which requires credit). Every photo's photographer, licence and source is recorded in `credits.json`, and the build turns that into `credits.html`.

**Alexander's photo.** The About us portrait is `assets/img/photos/founder.jpg` (4:5, 1200×1500). If the file is missing, the section shows an "AB" monogram instead.

> **Temporary portrait.** The current `founder.jpg` is a fun photo of Alexander at a bin bag fashion show, used for now. When a professional headshot is uploaded:
> 1. Rename the current photo to `activities-fashion-show.jpg` (and its `-800` file), and rename its `credits.json` key to match.
> 2. Add it to the Summer life photo grid (`#summer-life` in `src/pages/index.html`) with the caption **"Bin bag fashion show"**, e.g. `{{photo:activities-fashion-show|Alexander Burns in a costume of black bin bags and a tall blue paper hat, with face paint, at a bin bag fashion show||Bin bag fashion show}}`. The grid shows 4:3 tiles cropped from the centre, so first crop the photo to 4:3 **from the top** to keep his head and hat in frame. A fifth tile leaves an uneven row, so check the grid at desktop width and at 390px.
> 3. Save the headshot as `founder.jpg` (4:5, about 1200px wide) with a `founder` entry in `credits.json`, and update the alt text in `FOUNDER` in `src/build.py`.
> 4. Run `python3 src/images.py` and `python3 src/build.py`. In the photo table below, rename the row to `activities-fashion-show.jpg` with "Used on" set to "index.html (Summer life)", keep the table in alphabetical order, and add a row for the new `founder.jpg`.

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
| `founder.jpg` | Alexander Burns at a bin bag fashion show (temporary portrait, see above) | Sandbox English | index.html (About us) |
| `hero-students.jpg` | Students of different ages walking into school, seen from behind | Pexels | index.html |
| `lessons.jpg` | Students seated at desks in a classroom | Pexels | index.html (a typical day) |
| `location-campus.jpg` | A modern glass building among trees | Pexels | index.html |
| `location-countryside.jpg` | A riverside meadow under a summer sky | Pexels | index.html |
| `location-grounds.jpg` | A large tree on a sunny green lawn | Pexels | index.html |
| `location-london.jpg` | London and the River Thames from above, at dawn | Pexels | index.html |
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
- **At least one member of staff for every 10 students** (a staff-to-student ratio of at least 1:10).
- **Alexander Burns is the Designated Safeguarding Lead.**
- Students of every English level are welcome, **including complete beginners**.
- Three meals a day and a packed lunch on excursion days, with dietary needs catered for. Rooms separated by age and gender. Daily time to call home and phone-free lessons. Airport meet-and-greet and transfers available.
- Locations: **London** or **the area around London**. Both are available, and it's the parent's or agent's choice, so copy should present them side by side as equal options ("choose London or the area around London"), never as the school's decision or with one only "on request". No venues are named. Only one site will operate in 2028, but the site doesn't say so.
- Founder: **Alexander Burns**, a student with several years' experience delivering enjoyable summer programmes, who founded Sandbox English to offer a better experience at a reasonable price. The school is founder-led and teaches English only.
- **Not accredited yet.** Never claim or imply accreditation or membership (British Council, English UK or others) until it is granted. See [Accreditation and visas](#accreditation-and-visas).
- Contact: `hello@sandboxenglish.co.uk`, @sandboxenglish on Instagram, Facebook and YouTube.

## ⚠️ Launch checklist

Work through these in order. Tick items off by editing this file, so the next session knows where things stand.

### 1. Must be done before the site goes live

These are blocking. Launching without them would lose enquiries or break UK law.

- [x] **Connect the consultation form** to a form service. Done with Formspree. See [Forms](#forms-formspree).
- [ ] **Move newsletter sign-ups to an email provider** (e.g. Buttondown or Brevo) before sending any newsletter. For now they arrive through Formspree as "Newsletter sign-up" emails.
- [ ] **Send a test submission** of both forms from a phone and a computer, and check they arrive.
- [ ] **Set up the mailbox** `hello@sandboxenglish.co.uk` and check it receives mail. It isn't set up yet, and it's the fallback the consultation form suggests when sending fails, as well as the contact address across the site.
- [ ] **Fill in the company details** in `COMPANY` at the top of `src/build.py`: registered company name, company number, registered office address and ICO registration number. They currently show as `[placeholders]` in the footer, the privacy policy and the terms, and the build warns until they're all replaced. If the business won't be a limited company, reword the footer in `footer()` and the "Who we are" and "About us" sections of the privacy policy and terms.
- [ ] **Name the email provider in the privacy policy** ("Who we share it with") once the mailbox is set up. Formspree and GitHub Pages are already named. Check Formspree's data processing terms match the transfer safeguard the policy describes.
- [ ] **Have the legal pages reviewed** by a solicitor or a reputable template service. `privacy.html`, `terms.html` and `cookies.html` are careful first drafts, not legal advice.
- [ ] **Register with the ICO and pay the data protection fee**, unless exempt. Most organisations that handle personal data must do this. Check at [ico.org.uk/fee](https://ico.org.uk/for-organisations/data-protection-fee/).
- [x] **Check the cookie policy is still true** once the forms are connected. The background (JavaScript) submission sets no cookies. Without JavaScript, visitors see Formspree's own confirmation page. `cookies.html` explains both.
- [ ] **Create the social accounts** @sandboxenglish on Instagram, Facebook and YouTube (the footer links to them), or remove any you won't use from `SOCIAL` in `src/build.py`.
- [x] **Point the domain at the site.** Live at `https://sandboxenglish.co.uk` since 26 September 2026: GoDaddy DNS points at GitHub Pages, the domain is verified on GitHub, and HTTPS is enforced. Setup details are in [Going live](#going-live-on-sandboxenglishcouk).
- [x] **Make `main` the default branch** on GitHub (Settings → General). GitHub Pages should publish from `main`.

### 2. Strongly recommended before promoting the site

These build trust with parents and agents.

- [ ] **Plan accreditation.** Visitors can only study an English course in the UK at an accredited institution, so this decides who can legally enrol. See [Accreditation and visas](#accreditation-and-visas).
- [ ] **Replace the temporary portrait of Alexander with a professional headshot**, and move the current bin bag fashion show photo to Summer life. See "Alexander's photo" under [Photos](#photos).
- [x] **Name the Designated Safeguarding Lead** in the Safety section (Alexander Burns, also named in About, the FAQs and on the agents page).
- [ ] **Get Alexander's DSL training** (a designated safeguarding lead course, often called Level 3).
- [ ] **Write the safeguarding, anti-bullying, online safety and code-of-conduct policies** and have them ready to send, since the site promises them on request.
- [ ] **Add a contact phone or WhatsApp number**, at least for agents and group leaders. Add it to the footer in `src/build.py` and the consultation page's sidebar.
- [ ] **Have booking terms and conditions ready.** The terms of use say every booking has separate booking terms, sent with the quote.
- [ ] **Write the agent terms** (commission, booking deadlines, payment schedule) so they can be confirmed in writing after a consultation, as the agents page promises.
- [ ] **Arrange insurance** (public liability and any other cover a residential course for children needs) before quoting.
- [ ] **State accreditation or membership honestly** once you have it (e.g. British Council, English UK). Don't add logos until they're granted.
- [x] **Set up Google Search Console** and submit `https://sandboxenglish.co.uk/sitemap.xml`. Done on 26 September 2026: domain property verified through GoDaddy, sitemap submitted.
- [x] **Set up Bing Webmaster Tools** and submit the sitemap. Done on 26 September 2026. Steps are in [Search engines](#search-engines-google-search-console-and-bing).
- [x] **Check the share preview** by pasting the site link into WhatsApp and a social network. Checked in WhatsApp on 26 September 2026. The 1200×630 image is `assets/img/share.jpg`; if it changes, add something like `?v2` to the link when testing, because WhatsApp caches previews.

### 3. When venues and dates are confirmed

- [ ] **Name the venues** on the home page (`#locations`) and in the FAQs, and replace the regional location photos with real photos of the venues (with permission).
- [ ] **Add course dates** and update the "When does it start?" and "Where will the course take place?" FAQs.
- [ ] **Update `CLAUDE.md` and the "Confirmed facts" section** of this README, so the no-venue rule is lifted and new facts can be used.
- [ ] **Add location pre-fill links** for the confirmed venues, and update the consultation form's "Preferred area" options if needed.

### 4. After the first summer

- [ ] **Replace stock photos with real ones** from the first summer. Get written parental consent, and keep to the rule that no child's face is visible.
- [ ] **Add testimonials** from parents, agents and group leaders, with their permission.
- [ ] **Remove "new school" wording** such as the "Why choose a new summer school?" FAQ.

## Accreditation and visas

This is advice to check with an immigration adviser (OISC-registered or a solicitor) and with the accrediting body. It is not legal advice.

- **Why it matters.** Under the UK Immigration Rules (Appendix Visitor: Permitted Activities), a visitor may study for up to six months only at an **accredited institution**. Visitors may also take "recreational" courses of up to 30 days at any provider, but the rules specifically exclude English language training from that. This applies to students who come visa-free with an ETA as well as those who need a Standard Visitor visa. Nearly all Sandbox English students will be visitors, so without accreditation they may be unable to enrol lawfully, and agents are unlikely to book.
- **Accreditation UK** (British Council with English UK) is the scheme agents and families recognise. Full accreditation normally needs a year of teaching English in the UK. New providers can apply for **provisional accreditation** after an inspection that shows they're ready to run courses to the scheme's standards. Summer centres are normally inspected while their courses are running.
- **Timing.** Contact Accreditation UK now to confirm the route for a brand-new, summer-only provider: what must be in place before inspection (company, venues, staff, policies, insurance), the fees, and whether provisional accreditation can be granted before the first students arrive in 2028. If it can't, ask whether a first summer is possible at all, for example only for UK-resident students, or in partnership with an already accredited provider.
- **Other accepted bodies.** The rules also accept some other inspection bodies (for example ISI or BAC). Ask the adviser which one suits a residential summer school for under-18s.
- **On the website.** Never claim or imply accreditation until it's granted. The visa FAQ on the home page doesn't mention accreditation. Update it once you have it.

## Forms (Formspree)

Both forms send to one Formspree form, set once as `FORM_ENDPOINT` at the top of `src/build.py` (currently `https://formspree.io/f/moevnyyl`). Formspree emails each submission to the address on the Formspree account and keeps a copy in its dashboard.

- **Consultation form** (`src/pages/consultation.html`): after validation, `assets/js/main.js` sends the answers in the background as JSON, then shows the on-page thank-you message. Values arrive readable (e.g. "Agent", "WhatsApp", "In London"). Fields hidden for the chosen enquirer type and empty fields are left out. The email subject is "Consultation request: <type> – <name>", and replying goes straight to the enquirer's email address.
- **Newsletter sign-up** (footer, in `src/build.py`): sends the email address to the same Formspree form with the subject "Newsletter sign-up". Add these people to a mailing list by hand until a newsletter service is chosen.
- **Spam:** both forms have a hidden `_gotcha` field. Formspree ignores any submission that fills it in.
- **If sending fails,** the consultation form shows an error and suggests emailing `hello@sandboxenglish.co.uk` instead, and the newsletter says to try again. Nothing pretends to have worked.
- **⚠️ The email fallback isn't set up yet.** `hello@sandboxenglish.co.uk` doesn't receive mail, so anyone who follows the error message's advice to email would get a bounce. The same address appears in the footer, on the consultation page and in the legal pages. Set up the mailbox (see the launch checklist) and send it a test message.
- **Without JavaScript,** the forms post normally and Formspree shows its own thank-you page.
- **The claude.ai preview can't send forms** (it blocks other sites), so test on the GitHub Pages site.
- **If a test shows an error,** check the form's settings on formspree.io: reCAPTCHA must be off for background (AJAX) submissions, and the free plan allows 50 submissions a month.

To change provider, update `FORM_ENDPOINT`, the privacy policy ("Who we share it with") and, if the provider sets cookies or loads scripts, `cookies.html`. Apart from form submissions, the site makes no third-party requests, and the cookie policy says so.

## Going live on sandboxenglish.co.uk

**Status: done.** The site is live at `https://sandboxenglish.co.uk` with HTTPS enforced, and `www` and the old `sxndyburns-netizen.github.io/Website/` address redirect there. The steps below are kept for reference, for example if the DNS ever needs redoing.

The domain is registered with **GoDaddy**. GitHub Pages publishes `main` from the root folder. The `CNAME` file in the repo root tells GitHub the site's domain; don't delete it.

**1. Verify the domain with GitHub** (recommended, stops anyone else claiming it on GitHub). On GitHub, click your profile picture → Settings → Pages → **Add a domain**, enter `sandboxenglish.co.uk`, and copy the TXT record it shows. Add it in GoDaddy (step 2), then press **Verify**.

**2. DNS records in GoDaddy** (My Products → sandboxenglish.co.uk → DNS):

| Type | Name | Value | Notes |
| --- | --- | --- | --- |
| A | `@` | `185.199.108.153` | Delete GoDaddy's existing `@` A records first (the parked page, e.g. `3.33.130.190`, `15.197.148.33`) |
| A | `@` | `185.199.109.153` | |
| A | `@` | `185.199.110.153` | |
| A | `@` | `185.199.111.153` | |
| AAAA | `@` | `2606:50c0:8000::153` (and `8001`, `8002`, `8003`) | Optional, for IPv6 |
| CNAME | `www` | `sxndyburns-netizen.github.io` | Replace GoDaddy's default `www` record |
| TXT | `_github-pages-challenge-sxndyburns-netizen` | (the code GitHub gives you) | From step 1 |

Also turn off any GoDaddy **domain forwarding** or Website Builder site for this domain. Leave MX records alone (they're for email, set up separately).

**3. Tell GitHub Pages.** In the repo, Settings → Pages → Custom domain should show `sandboxenglish.co.uk` (from the `CNAME` file). Wait for the DNS check to pass (minutes to a few hours).

**4. Tick "Enforce HTTPS"** once GitHub has issued the certificate. This can take up to 24 hours after DNS works. Then check `https://sandboxenglish.co.uk` and `https://www.sandboxenglish.co.uk` both load with the padlock (www redirects to the bare domain).

**Order matters:** change the DNS before the `CNAME` file reaches `main`. As soon as GitHub knows the domain, it redirects the old `sxndyburns-netizen.github.io/Website/` address there, so pointing the domain at GitHub first avoids a gap.

After the move:
- If Formspree restricts which sites can submit, add `sandboxenglish.co.uk`.
- Search engines should use the new address. Canonical links, the sitemap, `robots.txt` and the share image already use `https://sandboxenglish.co.uk`.
- The site now sits at the domain root, so the `/favicon.ico` fallback and `404.html` work for every mistyped address.

## Search engines (Google Search Console and Bing)

**Status:** Google Search Console is set up (domain property verified on 26 September 2026 with GoDaddy's automatic option, sitemap submitted). Bing Webmaster Tools is set up too, with the sitemap submitted.

1. Go to [search.google.com/search-console](https://search.google.com/search-console), choose **Add property → Domain**, and enter `sandboxenglish.co.uk` (no `https://` or `www`). A Domain property covers every version of the address.
2. Google shows a TXT record starting `google-site-verification=`. In GoDaddy's DNS, add a TXT record with Name `@` and that whole value, then press **Verify**. Leave the GitHub TXT record in place; both can exist.
3. In Search Console, open **Sitemaps** and submit `https://sandboxenglish.co.uk/sitemap.xml`.
4. For Bing, sign in at [bing.com/webmasters](https://www.bing.com/webmasters) and choose **Import from Google Search Console**. This copies the site and sitemap across.

The sitemap lists the public pages (home first). The photo credits and 404 pages are kept out of search with `noindex` and have no canonical link. Keep the verification TXT records in DNS, or the properties become unverified.

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
