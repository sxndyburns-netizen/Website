"""Build the site's HTML pages from src/pages/ with a shared header and footer.

    python3 src/build.py

Each file in src/pages/ starts with `title:` and `description:` lines, then `---`,
then the page body. The body may use these shortcodes:

    {{icon:name}}                         inline SVG icon from ICON
    {{photo:slug|alt|variant|caption}}    photo slot for assets/img/photos/<slug>.jpg
                                          (variant: "", "wide" or "tall")
    {{trips}}                             the excursion cards from TRIPS
    {{campus:park}} / {{campus:uni}}      campus illustrations

It also writes credits.html from assets/img/photos/credits.json.
The generated .html files in the repo root are committed; never edit them directly.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(__file__).parent / "pages"

NAV = [
    ("index.html", "Home"),
    ("programmes.html", "Programmes"),
    ("campuses.html", "Campuses"),
    ("summer-life.html", "Summer life"),
    ("about.html", "Our story"),
]

LOGO = """<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="13" fill="#14213d"/><path d="M8 34.5c5-2.2 10.5-2.2 16 0s11 2.2 16 0V40H8z" fill="#e6c98f"/><path d="M13 9h22a5 5 0 0 1 5 5v9a5 5 0 0 1-5 5H22l-6 5v-5h-3a5 5 0 0 1-5-5v-9a5 5 0 0 1 5-5z" fill="#f2603d"/><circle cx="17" cy="18.5" r="2.3" fill="#fff"/><circle cx="24" cy="18.5" r="2.3" fill="#fff"/><circle cx="31" cy="18.5" r="2.3" fill="#fff"/></svg>"""

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

CAMPUS = {
    # Leighton Park: Victorian school house in private parkland with old oaks
    "park": """<svg viewBox="0 0 600 340" preserveAspectRatio="xMidYMid slice">
  <rect width="600" height="340" fill="#d6f0ec"/>
  <circle cx="500" cy="70" r="38" fill="#f7b733"/>
  <path d="M0 220c120-40 250-46 380-20s160 16 220 4v136H0z" fill="#7cc7b8"/>
  <path d="M0 250c140-24 300-22 420 0s140 10 180 4v86H0z" fill="#3fb3a4"/>
  <g transform="translate(210 118)">
    <rect x="0" y="40" width="180" height="92" fill="#fdf9f1"/>
    <path d="M-10 42 90 -6l100 48z" fill="#d94a28"/>
    <rect x="72" y="-40" width="36" height="60" fill="#fdf9f1"/>
    <path d="M66 -40l24-22 24 22z" fill="#d94a28"/>
    <g fill="#14213d"><rect x="18" y="62" width="18" height="26" rx="9"/><rect x="50" y="62" width="18" height="26" rx="9"/><rect x="112" y="62" width="18" height="26" rx="9"/><rect x="144" y="62" width="18" height="26" rx="9"/><rect x="82" y="-24" width="16" height="20" rx="8"/></g>
    <path d="M78 132v-30a12 12 0 0 1 24 0v30z" fill="#14213d"/>
  </g>
  <g fill="#1d7268"><circle cx="90" cy="178" r="56"/><circle cx="130" cy="150" r="40"/><circle cx="520" cy="185" r="50"/><circle cx="480" cy="160" r="36"/></g>
  <g fill="#14213d"><rect x="100" y="210" width="14" height="60"/><rect x="505" y="215" width="12" height="54"/></g>
  <path d="M0 300h600" stroke="#14213d" stroke-width="3"/>
  <g stroke="#14213d" stroke-width="3">
    <path d="M20 286v28M60 286v28M100 286v28M140 286v28M180 286v28M220 286v28M260 286v28M300 286v28M340 286v28M380 286v28M420 286v28M460 286v28M500 286v28M540 286v28M580 286v28"/>
  </g>
  <path d="M0 322c150-10 300-10 600 0v18H0z" fill="#e6c98f"/>
</svg>""",
    # Brunel: modern campus blocks with running track
    "uni": """<svg viewBox="0 0 600 340" preserveAspectRatio="xMidYMid slice">
  <rect width="600" height="340" fill="#e0eafa"/>
  <circle cx="90" cy="70" r="34" fill="#f7b733"/>
  <g transform="translate(150 80)">
    <rect x="0" y="40" width="120" height="150" fill="#1d2d52"/>
    <rect x="130" y="0" width="90" height="190" fill="#14213d"/>
    <rect x="230" y="60" width="130" height="130" fill="#3a4a6e"/>
    <g fill="#f7b733" opacity=".9">
      <rect x="14" y="58" width="92" height="10"/><rect x="14" y="84" width="92" height="10"/><rect x="14" y="110" width="92" height="10"/><rect x="14" y="136" width="92" height="10"/>
      <rect x="144" y="18" width="12" height="150"/><rect x="170" y="18" width="12" height="150"/><rect x="196" y="18" width="12" height="150"/>
      <rect x="246" y="78" width="98" height="12"/><rect x="246" y="104" width="98" height="12"/><rect x="246" y="130" width="98" height="12"/>
    </g>
    <rect x="-150" y="190" width="600" height="10" fill="#14213d"/>
  </g>
  <ellipse cx="300" cy="320" rx="330" ry="60" fill="#f2603d"/>
  <ellipse cx="300" cy="324" rx="290" ry="44" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="10 8"/>
  <ellipse cx="300" cy="328" rx="250" ry="30" fill="#3fb3a4"/>
  <g fill="#2a9d8f"><circle cx="530" cy="230" r="34"/><circle cx="60" cy="240" r="28"/></g>
</svg>""",
}


def icon(name):
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[name] + "</svg>"
    )


# ---------------------------------------------------------------------------
# Photos. Every real photo lives in assets/img/photos/<slug>.jpg.
# Until a file exists, a tinted placeholder (or illustration) shows instead.
# ---------------------------------------------------------------------------
HERO_ART = """<svg viewBox="0 0 560 520">
        <defs>
          <clipPath id="heroClip"><circle cx="290" cy="270" r="230"/></clipPath>
        </defs>
        <circle cx="290" cy="270" r="230" fill="#f1e0bb"/>
        <g clip-path="url(#heroClip)">
          <rect x="40" y="40" width="500" height="300" fill="#e0eafa"/>
          <circle cx="400" cy="140" r="52" fill="#f7b733"/>
          <path d="M40 330c80-50 170-60 260-30s170 20 240-10v230H40z" fill="#2a9d8f"/>
          <path d="M40 360c90-30 200-20 290 10s150 10 210-10v200H40z" fill="#3fb3a4"/>
          <!-- College building -->
          <g transform="translate(150 210)">
            <rect x="0" y="40" width="200" height="110" fill="#1d2d52"/>
            <rect x="70" y="0" width="60" height="150" fill="#14213d"/>
            <path d="M70 0l30-28 30 28z" fill="#f2603d"/>
            <path d="M0 40l20-18h160l20 18z" fill="#14213d"/>
            <g fill="#f7b733">
              <rect x="18" y="62" width="16" height="24" rx="8"/>
              <rect x="44" y="62" width="16" height="24" rx="8"/>
              <rect x="140" y="62" width="16" height="24" rx="8"/>
              <rect x="166" y="62" width="16" height="24" rx="8"/>
              <rect x="18" y="100" width="16" height="24" rx="8"/>
              <rect x="44" y="100" width="16" height="24" rx="8"/>
              <rect x="140" y="100" width="16" height="24" rx="8"/>
              <rect x="166" y="100" width="16" height="24" rx="8"/>
              <circle cx="100" cy="36" r="12"/>
            </g>
            <path d="M88 150v-34a12 12 0 0 1 24 0v34z" fill="#fdf9f1"/>
          </g>
          <!-- Trees -->
          <circle cx="110" cy="330" r="30" fill="#1d7268"/>
          <rect x="106" y="340" width="8" height="30" fill="#14213d"/>
          <circle cx="440" cy="325" r="36" fill="#1d7268"/>
          <rect x="436" y="340" width="8" height="34" fill="#14213d"/>
          <!-- Sand -->
          <path d="M40 440c70-24 160-26 250-6s170 18 250-4v90H40z" fill="#e6c98f"/>
          <!-- Bucket -->
          <g transform="translate(330 400)">
            <path d="M0 0h44l-6 42H6z" fill="#f2603d"/>
            <rect x="-3" y="-6" width="50" height="9" rx="4" fill="#d94a28"/>
            <path d="M2 -2c0-22 40-22 40 0" fill="none" stroke="#14213d" stroke-width="3"/>
          </g>
          <!-- Spade -->
          <g transform="translate(395 380) rotate(18)">
            <rect x="0" y="0" width="6" height="46" rx="3" fill="#14213d"/>
            <path d="M-8 44h22l-3 22a8 8 0 0 1-16 0z" fill="#4a7fd6"/>
          </g>
        </g>

        <!-- Speech bubbles -->
        <g class="bubble-float">
          <rect x="18" y="96" width="132" height="54" rx="27" fill="#f2603d"/>
          <path d="M112 146l18 20 2-22z" fill="#f2603d"/>
          <text x="84" y="131" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="24" font-weight="600" fill="#fff">Hello!</text>
        </g>
        <g class="bubble-float">
          <rect x="400" y="24" width="140" height="50" rx="25" fill="#14213d"/>
          <path d="M430 70l-10 20 26-16z" fill="#14213d"/>
          <text x="470" y="57" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="22" font-weight="600" fill="#fff">Bonjour</text>
        </g>
        <g class="bubble-float">
          <rect x="436" y="250" width="112" height="48" rx="24" fill="#f7b733"/>
          <path d="M452 294l-6 20 22-18z" fill="#f7b733"/>
          <text x="492" y="282" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="22" font-weight="600" fill="#14213d">¡Hola!</text>
        </g>
        <g class="bubble-float">
          <rect x="6" y="300" width="104" height="48" rx="24" fill="#ffffff" stroke="#14213d" stroke-width="2"/>
          <path d="M84 346l14 18 2-20z" fill="#ffffff" stroke="#14213d" stroke-width="2" stroke-linejoin="round"/>
          <rect x="80" y="340" width="22" height="6" fill="#fff"/>
          <text x="58" y="331" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="22" font-weight="600" fill="#14213d">Ciao</text>
        </g>
        <g class="bubble-float">
          <rect x="190" y="0" width="100" height="46" rx="23" fill="#4a7fd6"/>
          <path d="M230 42l4 18 12-18z" fill="#4a7fd6"/>
          <text x="240" y="31" text-anchor="middle" font-family="system-ui, sans-serif" font-size="20" font-weight="700" fill="#fff">你好</text>
        </g>
        <g class="bubble-float">
          <rect x="360" y="470" width="140" height="46" rx="23" fill="#2a9d8f"/>
          <text x="430" y="500" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="21" font-weight="600" fill="#fff">Merhaba</text>
        </g>
      </svg>"""

PROGRAMME_ART = {
    "programme-juniors": """<div style="background:#e0eafa;width:100%;height:100%"><svg viewBox="0 0 400 250" preserveAspectRatio="xMidYMid slice">
            <circle cx="330" cy="60" r="36" fill="#f7b733"/>
            <path d="M0 200c80-30 160-30 240-5s120 20 160 5v50H0z" fill="#2a9d8f"/>
            <path d="M120 50l40 40-40 40-40-40z" fill="#f2603d"/>
            <path d="M120 130c10 30-20 40-5 70" fill="none" stroke="#14213d" stroke-width="2.5"/>
            <text x="250" y="170" font-family="Fraunces, Georgia, serif" font-size="64" font-weight="700" fill="#14213d">8–12</text>
          </svg></div>""",
    "programme-teens": """<div style="background:#d6f0ec;width:100%;height:100%"><svg viewBox="0 0 400 250" preserveAspectRatio="xMidYMid slice">
            <circle cx="70" cy="70" r="44" fill="#fff" opacity=".7"/>
            <circle cx="120" cy="120" r="24" fill="#f7b733"/>
            <rect x="40" y="160" width="120" height="40" rx="20" fill="#f2603d"/>
            <path d="M0 225h400v25H0z" fill="#e6c98f"/>
            <text x="200" y="170" font-family="Fraunces, Georgia, serif" font-size="64" font-weight="700" fill="#14213d">13–15</text>
          </svg></div>""",
    "programme-leaders": """<div style="background:#fde3da;width:100%;height:100%"><svg viewBox="0 0 400 250" preserveAspectRatio="xMidYMid slice">
            <path d="M40 90l60-26 60 26-60 26z" fill="#14213d"/>
            <path d="M64 100v30c0 12 72 12 72 0v-30l-36 16z" fill="#1d2d52"/>
            <path d="M160 90v40" stroke="#f7b733" stroke-width="4"/>
            <circle cx="160" cy="134" r="6" fill="#f7b733"/>
            <rect x="0" y="210" width="400" height="40" fill="#f2603d" opacity=".25"/>
            <text x="200" y="170" font-family="Fraunces, Georgia, serif" font-size="64" font-weight="700" fill="#14213d">16–17</text>
          </svg></div>""",
}

PHOTO_FALLBACK = {
    "hero-students": "HERO_ART",
    "leighton-park-grounds": "campus:park",
    "brunel-campus": "campus:uni",
}


def photo(slug, alt, variant="", caption=""):
    fb = PHOTO_FALLBACK.get(slug)
    if fb == "HERO_ART":
        inner = HERO_ART
        cls = " photo--art"
    elif slug in PROGRAMME_ART:
        inner = PROGRAMME_ART[slug]
        cls = " photo--art"
    elif fb and fb.startswith("campus:"):
        inner = CAMPUS[fb.split(":")[1]]
        cls = " photo--art"
    else:
        inner = icon("image")
        cls = ""
    variant_cls = "".join(f" photo--{v}" for v in variant.split() if v)
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (
        f'<figure class="photo{variant_cls}{cls}">'
        f'<div class="photo__placeholder" aria-hidden="true">{inner}</div>'
        f'<img src="assets/img/photos/{slug}.jpg" alt="{alt}" loading="lazy" decoding="async" onerror="this.remove()">'
        f"{cap}</figure>"
    )


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
    <a class="brand" href="index.html" aria-label="Sandbox Languages home">
      {LOGO}
      <span class="brand-name">Sandbox<small>Languages</small></span>
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


FOOTER = f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html" aria-label="Sandbox Languages home">
          {LOGO}
          <span class="brand-name">Sandbox<small>Languages</small></span>
        </a>
        <p class="footer-note">A family-run English language summer school in the UK for young people aged 8–17, started by summer-school staff who wanted to make it more fun, more engaging and more affordable.</p>
        <div class="socials">
          <a href="#" aria-label="Sandbox Languages on Instagram">{icon("instagram")}</a>
          <a href="#" aria-label="Sandbox Languages on Facebook">{icon("facebook")}</a>
          <a href="#" aria-label="Sandbox Languages on YouTube">{icon("youtube")}</a>
        </div>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="programmes.html">Programmes</a></li>
          <li><a href="summer-life.html">Summer life</a></li>
          <li><a href="campuses.html">Campuses</a></li>
          <li><a href="about.html">Our story</a></li>
          <li><a href="about.html#faq">FAQs</a></li>
        </ul>
      </div>
      <div>
        <h4>Families</h4>
        <ul>
          <li><a href="consultation.html">Book a free consultation</a></li>
          <li><a href="campuses.html#compare">Choosing a campus</a></li>
          <li><a href="about.html#safeguarding">Safeguarding</a></li>
          <li><a href="consultation.html?type=group">Group leaders &amp; agents</a></li>
        </ul>
      </div>
      <div>
        <h4>Summer 2027 news</h4>
        <p>Be first to hear when summer 2027 places open, plus news from both campuses.</p>
        <form class="newsletter" novalidate>
          <label class="visually-hidden" for="newsletter-email">Email address</label>
          <input id="newsletter-email" type="email" placeholder="Your email" autocomplete="email" required>
          <button class="btn btn--primary btn--sm" type="submit">Sign up</button>
        </form>
        <p class="newsletter-msg" role="status" aria-live="polite"></p>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="mb-0">© <span data-year>2026</span> Sandbox Languages. All rights reserved.</p>
      <ul>
        <li><a href="#">Privacy policy</a></li>
        <li><a href="#">Terms &amp; conditions</a></li>
        <li><a href="#">Cookies</a></li>
        <li><a href="credits.html">Photo credits</a></li>
      </ul>
    </div>
  </div>
</footer>"""


# ---------------------------------------------------------------------------
# Photo credits, generated from assets/img/photos/credits.json
# ---------------------------------------------------------------------------
import json, html as _html


def credits_page():
    path = ROOT / "assets/img/photos/credits.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    rows = []
    for slug, c in sorted(data.items()):
        rows.append(
            f'<tr><th scope="row"><img src="assets/img/photos/{slug}.jpg" alt="" loading="lazy" '
            f'style="width:120px;height:80px;object-fit:cover;border-radius:8px"></th>'
            f'<td>{_html.escape(c["description"])}</td>'
            f'<td>{_html.escape(c["artist"])}</td>'
            f'<td><a href="{c["license_url"]}" rel="noopener">{_html.escape(c["license"])}</a></td>'
            f'<td><a href="{c["source"]}" rel="noopener">Source</a></td></tr>'
        )
    row_html = "\n          ".join(rows)
    body = f"""<section class="page-hero">
  <div class="container">
    <p class="breadcrumb"><a href="index.html">Home</a> / Photo credits</p>
    <h1>Photo credits</h1>
    <p class="lead">We are grateful to the photographers who share their work under open licences. Images may have been cropped or resized.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="table-wrap">
      <table>
        <thead><tr><th scope="col">Photo</th><th scope="col">Description</th><th scope="col">Photographer</th><th scope="col">Licence</th><th scope="col">Link</th></tr></thead>
        <tbody>
          {row_html}
        </tbody>
      </table>
    </div>
  </div>
</section>"""
    return body


def page(filename, title, description, body):
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#14213d">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400..700;1,9..40,400&amp;family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,500..700,0..100,0..1;1,9..144,500..700,0..100,0..1&amp;display=swap">
  <link rel="stylesheet" href="assets/css/styles.css">
  <script src="assets/js/main.js" defer></script>
</head>
<body>
{header(filename)}

<main id="main">
{body.strip()}
</main>

{FOOTER}
</body>
</html>
"""


def render(text):
    # {{icon:name}} shortcodes
    text = text.replace("{{trips}}", trips())
    text = re.sub(r"\{\{photo:([^}]*)\}\}", lambda m: photo(*m.group(1).split("|")), text)
    text = re.sub(r"\{\{campus:(\w+)\}\}", lambda m: CAMPUS[m.group(1)], text)
    return re.sub(r"\{\{icon:(\w+)\}\}", lambda m: icon(m.group(1)), text)


for src in sorted(SRC.glob("*.html")):
    raw = src.read_text()
    meta, body = raw.split("\n---\n", 1)
    fields = dict(line.split(": ", 1) for line in meta.strip().splitlines())
    out = page(src.name, fields["title"], fields["description"], render(body))
    (ROOT / src.name).write_text(out)
    print("wrote", src.name)

(ROOT / "credits.html").write_text(page("credits.html", "Photo Credits | Sandbox Languages", "Credits and licences for photographs used on the Sandbox Languages website.", credits_page()))
print("wrote credits.html")
