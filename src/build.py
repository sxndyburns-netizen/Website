"""Build the site's HTML pages from src/pages/ with a shared head, header and footer.

    python3 src/build.py

Each file in src/pages/ starts with front matter (`title:`, `description:` and
optionally `robots: noindex`), then a line containing only `---`, then the page body.
The body may use these shortcodes:

    {{icon:name}}                         inline SVG icon from ICON
    {{photo:slug|alt|variant|caption}}    photo for assets/img/photos/<slug>.jpg
                                          (variant: "", "wide", "portrait" (4:5) or "tall";
                                          "tall" is the hero and loads first)
    {{trips}}                             the excursion cards from TRIPS
    {{founder}}                           Alexander's portrait (assets/img/photos/founder.jpg),
                                          or a monogram placeholder until that file exists
    {{company:key}}                       a company detail from COMPANY (name, number, office, ico)

It also writes credits.html (from assets/img/photos/credits.json), sitemap.xml and
robots.txt. The generated files in the repo root are committed; never edit them directly.
The build stops with an error if a shortcode is unknown, a photo file is missing, or a
photo has no entry in credits.json. It warns while any COMPANY detail is still a placeholder.
"""
import html
import json
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(__file__).parent / "pages"
PHOTOS = ROOT / "assets/img/photos"

SITE_NAME = "Sandbox English Summer School"
SITE_URL = "https://sandboxenglish.co.uk"
EMAIL = "hello@sandboxenglish.co.uk"
SOCIAL = [
    ("instagram", "Instagram", "https://www.instagram.com/sandboxenglish"),
    ("facebook", "Facebook", "https://www.facebook.com/sandboxenglish"),
    ("youtube", "YouTube", "https://www.youtube.com/@sandboxenglish"),
]

# Legal details, shown in the footer, privacy policy and terms. Values in [brackets] are
# placeholders: replace them once the company is registered (the build warns until then).
COMPANY = {
    "name": "[Company name] Ltd",
    "number": "[00000000]",
    "office": "[Registered office address]",
    "ico": "[ZA000000]",
}


def is_placeholder(value):
    return value.startswith("[")


NAV = [
    ("index.html#programme", "Programme"),
    ("index.html#about", "About us"),
    ("index.html#safety", "Safety"),
    ("index.html#summer-life", "Summer life"),
    ("index.html#locations", "Locations"),
    ("index.html#faq", "FAQs"),
    ("agents.html", "Agents &amp; groups"),
]

# Brand mark: a speech bubble (English) holding a sandcastle with a flag (Sandbox), with a
# sun and a wave (summer). Navy and coral only, so it prints cleanly on shirts and lanyards;
# print and one-colour versions live in assets/brand/ (made by src/brand.py, which uses the
# same paths). The header uses it on light backgrounds, the footer on navy.
MARK = {
    "body": "M13 4h22a9 9 0 0 1 9 9v13a9 9 0 0 1-9 9H22l-9 8.5V35a9 9 0 0 1-9-9V13a9 9 0 0 1 9-9z",
    "castle": "M10 26.5V16h1.8v1.8h1.9V16h1.8v10.5zM26.5 26.5V16h1.8v1.8h1.9V16h1.8v10.5z"
              "M15 26.5v-6h12v6zM17 26.5v-14h2v1.8h1.3v-1.8h1.4v1.8h1.3v-1.8h2v14z",
    "door": "M19.6 26.5v-2.9a1.4 1.4 0 0 1 2.8 0v2.9z",
    "flag": "M21.4 6.6l4.4 1.7-4.4 1.7z",
    "wave": "M9.5 30.8c2.5-2 5-2 7.5 0s5 2 7.5 0 5-2 7.5 0 5-2 7.5 0",
}


def logo(body="#14213d", castle="#ffffff", accent="#f2603d"):
    return (
        '<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true">'
        f'<path fill="{body}" d="{MARK["body"]}"/>'
        f'<path fill="{castle}" d="{MARK["castle"]}"/>'
        f'<path fill="none" stroke="{castle}" stroke-width=".9" stroke-linecap="round" d="M21 12.5V7"/>'
        f'<path fill="{body}" d="{MARK["door"]}"/>'
        f'<path fill="{accent}" d="{MARK["flag"]}"/>'
        f'<circle cx="36" cy="12.2" r="3.3" fill="{accent}"/>'
        f'<path fill="none" stroke="{accent}" stroke-width="2.3" stroke-linecap="round" d="{MARK["wave"]}"/>'
        "</svg>"
    )


USED_PHOTOS = set()


def attr(text):
    """Escape text for an HTML attribute (source text may already contain entities)."""
    return html.escape(html.unescape(text), quote=True)


def fail(message):
    sys.exit(f"build error: {message}")


def read_text(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def write_text(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")


ICON = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/>',
    "book": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.48 12.89 17 22l-5-3-5 3 1.52-9.11"/>',
    "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "food": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2M7 2v20M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
    "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>',
    "ball": '<circle cx="12" cy="12" r="10"/><path d="m12 7 4.5 3.3-1.7 5.2H9.2l-1.7-5.2z"/><path d="M12 2v5M21.5 9l-5 1.3M17.8 20l-3-4.5M6.2 20l3-4.5M2.5 9l5 1.3"/>',
    "palette": '<circle cx="13.5" cy="6.5" r="1.5"/><circle cx="17.5" cy="10.5" r="1.5"/><circle cx="8.5" cy="7.5" r="1.5"/><circle cx="6.5" cy="12.5" r="1.5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.93 0 1.65-.75 1.65-1.69 0-.44-.18-.84-.44-1.13-.29-.29-.44-.65-.44-1.13a1.64 1.64 0 0 1 1.67-1.67h2C19.2 16.38 22 13.58 22 10c0-4.42-4.48-8-10-8z"/>',
    "star": '<path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/>',
    "wifi": '<path d="M5 12.55a11 11 0 0 1 14.08 0M1.42 9a16 16 0 0 1 21.16 0M8.53 16.11a6 6 0 0 1 6.95 0M12 20h.01"/>',
    "bed": '<path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "train": '<rect x="4" y="3" width="16" height="14" rx="3"/><path d="M4 11h16M8 21l2-4M16 21l-2-4"/><circle cx="8.5" cy="14" r=".5"/><circle cx="15.5" cy="14" r=".5"/>',
    "tree": '<path d="M12 22v-6"/><path d="M12 16c-4.4 0-8-2.7-8-6.5C4 6 7.6 2 12 2s8 4 8 7.5c0 3.8-3.6 6.5-8 6.5z"/>',
    "video": '<path d="m22 8-6 4 6 4V8z"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "youtube": '<path d="M2.5 17a24 24 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.6 49.6 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24 24 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.6 49.6 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
}


TRIPS = [
    ("trip-london", "London walking tour",
     "A guided walk past Big Ben, Westminster Abbey, Buckingham Palace and the South Bank.",
     "Visitors walking across Westminster Bridge towards Big Ben"),
    ("trip-oxford", "Oxford tour",
     "Historic colleges, the Radcliffe Camera and the city's famous dreaming spires.",
     "The Radcliffe Camera in Oxford"),
    ("trip-cambridge", "Cambridge tour",
     "King's College, the Backs and the riverside of one of the world's great university cities.",
     "A historic college building in Cambridge"),
    ("trip-harry-potter", "Harry Potter Studio Tour",
     "Warner Bros. Studio Tour London: the real sets, costumes and props from the films.",
     "The Great Hall set at the Warner Bros. Studio Tour London"),
    ("trip-madame-tussauds", "Madame Tussauds London",
     "The world-famous wax museum, with film stars, sporting heroes and royalty.",
     "The green-domed exterior of Madame Tussauds London"),
]


def icon(name):
    if name not in ICON:
        fail(f"unknown icon '{name}'")
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[name] + "</svg>"
    )


# ---------------------------------------------------------------------------
# Photos. Every photo lives in assets/img/photos/<slug>.jpg, with a smaller
# <slug>-800.jpg made by src/images.py for phones.
# ---------------------------------------------------------------------------
def jpeg_size(path):
    """Return (width, height) of a JPEG using only the standard library."""
    data = path.read_bytes()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    fail(f"could not read the size of {path.name}")


SIZES = {
    "tall": "(min-width: 960px) 45vw, 100vw",
    "portrait": "(min-width: 900px) 25vw, 100vw",
    "wide": "(min-width: 900px) 50vw, 100vw",
    "": "(min-width: 900px) 25vw, (min-width: 600px) 50vw, 100vw",
}


def photo(slug, alt, variant="", caption=""):
    path = PHOTOS / f"{slug}.jpg"
    if not path.exists():
        fail(f"missing photo assets/img/photos/{slug}.jpg")
    USED_PHOTOS.add(slug)
    w, h = jpeg_size(path)
    src = f"assets/img/photos/{slug}.jpg"
    small = PHOTOS / f"{slug}-800.jpg"
    srcset = ""
    if small.exists():
        srcset = f' srcset="assets/img/photos/{slug}-800.jpg 800w, {src} {w}w" sizes="{SIZES[variant]}"'
    loading = 'fetchpriority="high"' if variant == "tall" else 'loading="lazy"'
    cls = f" photo--{variant}" if variant else ""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (
        f'<figure class="photo{cls}">'
        f'<img src="{src}"{srcset} width="{w}" height="{h}" alt="{attr(alt)}" {loading} decoding="async">'
        f"{cap}</figure>"
    )


FOUNDER = ("founder", "Alexander Burns in a costume of black bin bags and a tall blue paper hat, with face paint, at a bin bag fashion show")


def founder():
    """Alexander's portrait, or a monogram placeholder until founder.jpg is added."""
    slug, alt = FOUNDER
    caption = "<strong>Alexander Burns</strong> Founder and Designated Safeguarding Lead"
    if (PHOTOS / f"{slug}.jpg").exists():
        return photo(slug, alt, "portrait", caption)
    return (
        '<figure class="photo photo--portrait photo--monogram">'
        '<span class="monogram" aria-hidden="true">AB</span>'
        f"<figcaption>{caption}</figcaption></figure>"
    )


def trips():
    cards = []
    for slug, name, text, alt in TRIPS:
        cards.append(f"""      <article class="trip reveal">
        {photo(slug, alt, "wide")}
        <div class="trip__body">
          <h3>{name}</h3>
          <p>{text}</p>
          <ul class="trip__tags" aria-label="Included">
            <li>Free time</li><li>Packed lunch</li><li>Staff-led</li>
          </ul>
        </div>
      </article>""")
    return '<div class="trip-grid">\n' + "\n".join(cards) + "\n    </div>"


# ---------------------------------------------------------------------------
# Shared header and footer
# ---------------------------------------------------------------------------
def brand(on_navy=False):
    mark = logo(body="#ffffff", castle="#14213d") if on_navy else logo()
    return f"""{mark}
      <span class="brand-name">Sandbox<small>English Summer School</small></span>"""


def header(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    cta_cur = ' aria-current="page"' if current == "consultation.html" else ""
    items.append(f'<li class="nav-cta"><a class="btn btn--primary btn--sm" href="consultation.html"{cta_cur}>Book a consultation</a></li>')
    nav_items = "\n        ".join(items)
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="{SITE_NAME} home">
      {brand()}
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
        {nav_items}
      </ul>
    </nav>
  </div>
</header>"""


def footer():
    social = "".join(f'<a href="{url}" rel="noopener" aria-label="Sandbox English on {name}">{icon(ic)}</a>' for ic, name, url in SOCIAL)
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html" aria-label="{SITE_NAME} home">
          {brand(on_navy=True)}
        </a>
        <p class="footer-note">A residential English summer school for young people aged 8–17, in London or the area around it: you choose. Launching summer 2028.</p>
        <p class="footer-note"><a href="mailto:{EMAIL}">{EMAIL}</a><br>@sandboxenglish</p>
        <div class="socials">
          {social}
        </div>
      </div>
      <div>
        <h2 class="footer-title">Explore</h2>
        <ul>
          <li><a href="index.html#programme">The programme</a></li>
          <li><a href="index.html#about">About us</a></li>
          <li><a href="index.html#summer-life">Summer life &amp; excursions</a></li>
          <li><a href="index.html#locations">Locations</a></li>
          <li><a href="index.html#faq">FAQs</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer-title">Work with us</h2>
        <ul>
          <li><a href="consultation.html">Book a free consultation</a></li>
          <li><a href="agents.html">Agents</a></li>
          <li><a href="agents.html#groups">Group leaders</a></li>
          <li><a href="index.html#safety">Safety &amp; welfare</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer-title">Summer 2028</h2>
        <p>Be the first to hear when places for our first summer open.</p>
        <form class="newsletter" action="#" method="post" novalidate>
          <label class="visually-hidden" for="newsletter-email">Email address</label>
          <input id="newsletter-email" type="email" name="email" placeholder="Your email" autocomplete="email" required>
          <button class="btn btn--primary btn--sm" type="submit">Sign up</button>
        </form>
        <p class="newsletter-msg" role="status" aria-live="polite"></p>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="mb-0">© <span data-year>2026</span> {COMPANY["name"]}, trading as {SITE_NAME}. Registered in England and Wales, company number {COMPANY["number"]}. Registered office: {COMPANY["office"]}.</p>
      <ul>
        <li><a href="privacy.html">Privacy policy</a></li>
        <li><a href="terms.html">Terms of use</a></li>
        <li><a href="cookies.html">Cookies</a></li>
        <li><a href="credits.html">Photo credits</a></li>
      </ul>
    </div>
  </div>
</footer>"""


# ---------------------------------------------------------------------------
# Page wrapper
# ---------------------------------------------------------------------------
STRUCTURED_DATA = {
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    "name": "Sandbox English",
    "alternateName": SITE_NAME,
    "url": SITE_URL + "/",
    "email": EMAIL,
    "logo": SITE_URL + "/assets/img/favicon.svg",
    "image": SITE_URL + "/assets/img/share.jpg",
    "description": "Residential English summer school for ages 8–17, in London or the area around London, from summer 2028.",
    "founder": {"@type": "Person", "name": "Alexander Burns"},
    "sameAs": [url for _, _, url in SOCIAL],
}
if not is_placeholder(COMPANY["name"]):
    STRUCTURED_DATA["legalName"] = COMPANY["name"]


def page(filename, meta, body):
    title, description = attr(meta["title"]), attr(meta["description"])
    path = "" if filename == "index.html" else filename
    robots = '\n  <meta name="robots" content="noindex">' if meta.get("robots") == "noindex" else ""
    ld = ""
    if filename == "index.html":
        ld = '\n  <script type="application/ld+json">' + json.dumps(STRUCTURED_DATA, ensure_ascii=False) + "</script>"
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">{robots}
  <meta name="theme-color" content="#14213d">
  <link rel="canonical" href="{SITE_URL}/{path}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:locale" content="en_GB">
  <meta property="og:url" content="{SITE_URL}/{path}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{SITE_URL}/assets/img/share.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="assets/fonts/dm-sans-roman-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/fraunces-roman-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/styles.css">
  <script src="assets/js/main.js" defer></script>{ld}
</head>
<body>
{header(filename)}

<main id="main">
{body.strip()}
</main>

{footer()}
</body>
</html>
"""


def company(key):
    if key not in COMPANY:
        fail(f"unknown company detail '{key}'")
    return COMPANY[key]


def render(text, source):
    text = text.replace("{{trips}}", trips())
    text = text.replace("{{founder}}", founder())
    text = re.sub(r"\{\{company:(\w+)\}\}", lambda m: company(m.group(1)), text)
    text = re.sub(r"\{\{photo:([^}]*)\}\}", lambda m: photo(*m.group(1).split("|")), text)
    text = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: icon(m.group(1)), text)
    leftover = re.search(r"\{\{[^}]*\}\}", text)
    if leftover:
        fail(f"unknown shortcode {leftover.group(0)} in {source}")
    return text


def parse(source):
    raw = read_text(source)
    if "\n---\n" not in raw:
        fail(f"{source.name} has no '---' line after its front matter")
    head, body = raw.split("\n---\n", 1)
    meta = {}
    for line in head.strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    for key in ("title", "description"):
        if key not in meta:
            fail(f"{source.name} is missing '{key}:'")
    return meta, body


# ---------------------------------------------------------------------------
# Photo credits
# ---------------------------------------------------------------------------
def credits_page(credits):
    rows = []
    for slug, c in sorted(credits.items()):
        thumb = f"assets/img/photos/{slug}-800.jpg" if (PHOTOS / f"{slug}-800.jpg").exists() else f"assets/img/photos/{slug}.jpg"
        licence = html.escape(c["license"])
        if c.get("license_url"):
            licence = f'<a href="{attr(c["license_url"])}" rel="noopener">{licence}</a>'
        source = f'<a href="{attr(c["source"])}" rel="noopener">Source</a>' if c.get("source") else "—"
        rows.append(
            f'<tr><td><img class="credit-thumb" src="{thumb}" alt="" loading="lazy" width="120" height="80"></td>'
            f'<th scope="row">{html.escape(c["description"])}</th>'
            f'<td>{html.escape(c["artist"])}</td>'
            f'<td>{licence}</td>'
            f'<td>{source}</td></tr>'
        )
    row_html = "\n          ".join(rows)
    return f"""<section class="page-hero">
  <div class="container">
    <p class="breadcrumb"><a href="index.html">Home</a> / Photo credits</p>
    <h1>Photo credits</h1>
    <p class="lead">We are grateful to the photographers who share their work under open licences. Images may have been cropped or resized.</p>
  </div>
</section>
<section class="section section--tight-top">
  <div class="container">
    <div class="table-wrap">
      <table>
        <caption class="visually-hidden">Photographs used on this website, with photographer, licence and source</caption>
        <thead><tr><td></td><th scope="col">Photo</th><th scope="col">Photographer</th><th scope="col">Licence</th><th scope="col">Link</th></tr></thead>
        <tbody>
          {row_html}
        </tbody>
      </table>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def main():
    pages = []
    for source in sorted(SRC.glob("*.html")):
        meta, body = parse(source)
        write_text(ROOT / source.name, page(source.name, meta, render(body, source.name)))
        pages.append((source.name, meta))
        print("wrote", source.name)

    credits = json.loads(read_text(PHOTOS / "credits.json"))
    missing = sorted(USED_PHOTOS - set(credits))
    if missing:
        fail(f"no credits.json entry for: {', '.join(missing)}")
    for slug in sorted(set(credits) - USED_PHOTOS):
        print(f"warning: credits.json lists '{slug}', which no page uses")
    write_text(ROOT / "credits.html", page("credits.html", {
        "title": f"Photo Credits | {SITE_NAME}",
        "description": f"Credits and licences for photographs used on the {SITE_NAME} website.",
        "robots": "noindex",
    }, credits_page(credits)))
    print("wrote credits.html")

    urls = [f"{SITE_URL}/" if name == "index.html" else f"{SITE_URL}/{name}"
            for name, meta in pages if meta.get("robots") != "noindex"]
    sitemap = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    write_text(ROOT / "sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}\n</urlset>\n')
    write_text(ROOT / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")

    placeholders = [key for key, value in COMPANY.items() if is_placeholder(value)]
    if placeholders:
        print(f"warning: company details still placeholders: {', '.join(placeholders)} (COMPANY in src/build.py)")


if __name__ == "__main__":
    main()
