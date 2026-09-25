"""Generate print-ready logo files in assets/brand/ (text converted to outlines).

    python3 src/brand.py path/to/Fraunces.ttf path/to/DMSans.ttf

Needs fonttools (pip install fonttools brotli) and TTFs of Fraunces (700, 144pt
optical size) and DM Sans (700). Static instances can be made from the site's own
variable fonts in assets/fonts/ with fontTools.varLib.instancer. The website itself
does not need this script; it only rebuilds the logo files.

The mark is a speech bubble (English) holding a sandcastle with a flag (Sandbox),
with a sun and a wave (summer). src/build.py draws the same mark inline for the
website header and footer, and assets/img/favicon.svg is mark-full-colour.svg.
"""
import pathlib, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/brand"
NAVY, CORAL, WHITE = "#14213d", "#f2603d", "#ffffff"

# The mark, on a 48-unit grid. Keep in sync with MARK in src/build.py.
MARK_BODY = "M13 4h22a9 9 0 0 1 9 9v13a9 9 0 0 1-9 9H22l-9 8.5V35a9 9 0 0 1-9-9V13a9 9 0 0 1 9-9z"
MARK_CASTLE = ("M10 26.5V16h1.8v1.8h1.9V16h1.8v10.5zM26.5 26.5V16h1.8v1.8h1.9V16h1.8v10.5z"
               "M15 26.5v-6h12v6zM17 26.5v-14h2v1.8h1.3v-1.8h1.4v1.8h1.3v-1.8h2v14z")
MARK_DOOR = "M19.6 26.5v-2.9a1.4 1.4 0 0 1 2.8 0v2.9z"
MARK_POLE = "M21 12.5V7"
MARK_FLAG = "M21.4 6.6l4.4 1.7-4.4 1.7z"
MARK_SUN = (36, 12.2, 3.3)
MARK_WAVE = "M9.5 30.8c2.5-2 5-2 7.5 0s5 2 7.5 0 5-2 7.5 0 5-2 7.5 0"


def text_path(font, text, size, x, y, tracking=0.0):
    """Return (svg path d, advance width) for text with baseline at y."""
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    pen = SVGPathPen(gs)
    cx = x
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        gs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, cx, y)))
        cx += font["hmtx"][g][0] * scale + tracking * size
    return pen.getCommands(), cx - x - tracking * size


def mark_parts(castle, accent):
    """The castle, flag, sun and wave on top of the bubble."""
    cx, cy, r = MARK_SUN
    return (f'<path d="{MARK_CASTLE}" fill="{castle}"/>'
            f'<path d="{MARK_POLE}" fill="none" stroke="{castle}" stroke-width=".9" stroke-linecap="round"/>'
            f'<path d="{MARK_FLAG}" fill="{accent}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{accent}"/>'
            f'<path d="{MARK_WAVE}" fill="none" stroke="{accent}" stroke-width="2.3" stroke-linecap="round"/>')


def mark(x, y, s, body, accent, knockout=False, mid="m", castle=WHITE):
    """Speech-bubble mark at (x, y), scaled from its 48-unit box by s.

    Full colour: `body` bubble, `castle` sandcastle, `accent` flag, sun and wave.
    knockout=True (one colour): everything inside the bubble is cut out, so the
    background shows through.
    """
    t = f'transform="translate({x} {y}) scale({s})"'
    if knockout:
        return (f'<mask id="{mid}"><g {t}><path d="{MARK_BODY}" fill="#fff"/>{mark_parts("#000", "#000")}'
                f'<path d="{MARK_DOOR}" fill="#fff"/></g></mask>'
                f'<rect x="{x}" y="{y}" width="{48*s}" height="{48*s}" fill="{body}" mask="url(#{mid})"/>')
    return (f'<g {t}><path d="{MARK_BODY}" fill="{body}"/>{mark_parts(castle, accent)}'
            f'<path d="{MARK_DOOR}" fill="{body}"/></g>')


def svg(w, h, inner, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">{rect}{inner}</svg>\n'


def horizontal(fr, dm, word, sub, accent, knock, body=None, castle=WHITE):
    m = mark(0, 0, 2.5, body or word, accent, knock, "mh", castle)
    d1, w1 = text_path(fr, "Sandbox", 78, 140, 74)
    d2, w2 = text_path(dm, "ENGLISH SUMMER SCHOOL", 19.5, 143, 108, tracking=0.16)
    w = 140 + max(w1, w2) + 6
    return svg(w, 120, m + f'<path d="{d1}" fill="{word}"/><path d="{d2}" fill="{sub}"/>')


def stacked(fr, dm, word, sub, accent, knock, body=None, castle=WHITE):
    d1, w1 = text_path(fr, "Sandbox", 96, 0, 250)
    d2, w2 = text_path(dm, "ENGLISH SUMMER SCHOOL", 22, 0, 292, tracking=0.16)
    w = max(w1, w2)
    d1, _ = text_path(fr, "Sandbox", 96, (w - w1) / 2, 250)
    d2, _ = text_path(dm, "ENGLISH SUMMER SCHOOL", 22, (w - w2) / 2, 292, tracking=0.16)
    return svg(w, 305, mark((w - 144) / 2, 0, 3, body or word, accent, knock, "ms", castle) + f'<path d="{d1}" fill="{word}"/><path d="{d2}" fill="{sub}"/>')


def lanyard(dm, bg, fg, accent):
    # 20mm-high strip at 2px/mm; one repeat of mark + name, tile it along the lanyard.
    d, tw = text_path(dm, "SANDBOX ENGLISH SUMMER SCHOOL", 15, 46, 25.5, tracking=0.14)
    unit = 46 + tw + 34
    body = mark(12, 5, 0.62, fg, accent, knockout=(accent == bg), mid="ml", castle=bg)
    return svg(unit, 40, body + f'<path d="{d}" fill="{fg}"/>', bg=bg)


def main(fraunces, dmsans):
    fr, dm = TTFont(fraunces), TTFont(dmsans)
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "logo-full-colour.svg": horizontal(fr, dm, NAVY, CORAL, CORAL, False),
        "logo-navy.svg": horizontal(fr, dm, NAVY, NAVY, NAVY, True),
        "logo-white.svg": horizontal(fr, dm, WHITE, WHITE, WHITE, True),
        "logo-stacked-full-colour.svg": stacked(fr, dm, NAVY, CORAL, CORAL, False),
        "logo-stacked-navy.svg": stacked(fr, dm, NAVY, NAVY, NAVY, True),
        "logo-stacked-white.svg": stacked(fr, dm, WHITE, WHITE, WHITE, True),
        "mark-full-colour.svg": svg(48, 48, mark(0, 0, 1, NAVY, CORAL)),
        "mark-navy.svg": svg(48, 48, mark(0, 0, 1, NAVY, NAVY, True)),
        "mark-white.svg": svg(48, 48, mark(0, 0, 1, WHITE, WHITE, True)),
        "logo-on-navy.svg": horizontal(fr, dm, WHITE, CORAL, CORAL, False, castle=NAVY),
        "logo-stacked-on-navy.svg": stacked(fr, dm, WHITE, CORAL, CORAL, False, castle=NAVY),
        "mark-on-navy.svg": svg(48, 48, mark(0, 0, 1, WHITE, CORAL, castle=NAVY)),
        "lanyard-navy.svg": lanyard(dm, NAVY, WHITE, CORAL),
        "lanyard-coral.svg": lanyard(dm, CORAL, WHITE, CORAL),
    }
    for name, content in files.items():
        (OUT / name).write_text(content)
        print("wrote", name)


if __name__ == "__main__":
    main(*sys.argv[1:3])
