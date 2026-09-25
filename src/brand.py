"""Generate print-ready logo files in assets/brand/ (text converted to outlines).

    python3 src/brand.py path/to/Fraunces.ttf path/to/DMSans.ttf

Needs fonttools (pip install fonttools) and static TTFs of Fraunces (700, 144pt
optical size) and DM Sans (700) from Google Fonts. The website itself does not need
this script; it only rebuilds the logo files.
"""
import pathlib, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/brand"
NAVY, CORAL, WHITE = "#14213d", "#f2603d", "#ffffff"

MARK_BODY = "M13 4h22a9 9 0 0 1 9 9v13a9 9 0 0 1-9 9H22l-9 8.5V35a9 9 0 0 1-9-9V13a9 9 0 0 1 9-9z"
MARK_WAVE = "M11 24c4.3-3.6 8.7-3.6 13 0s8.7 3.6 13 0"


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


def mark(x, y, s, body, accent, knockout=False, mid="m"):
    """Speech-bubble mark at (x, y), scaled from its 48-unit box by s."""
    t = f'transform="translate({x} {y}) scale({s})"'
    if knockout:  # one colour: wave and sun cut out of the bubble
        return (f'<mask id="{mid}"><g {t}><path d="{MARK_BODY}" fill="#fff"/>'
                f'<path d="{MARK_WAVE}" fill="none" stroke="#000" stroke-width="4.2" stroke-linecap="round"/>'
                f'<circle cx="31.5" cy="13.5" r="3.6" fill="#000"/></g></mask>'
                f'<rect x="{x}" y="{y}" width="{48*s}" height="{48*s}" fill="{body}" mask="url(#{mid})"/>')
    return (f'<g {t}><path d="{MARK_BODY}" fill="{body}"/>'
            f'<path d="{MARK_WAVE}" fill="none" stroke="{accent}" stroke-width="4.2" stroke-linecap="round"/>'
            f'<circle cx="31.5" cy="13.5" r="3.6" fill="{accent}"/></g>')


def svg(w, h, inner, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">{rect}{inner}</svg>\n'


def horizontal(fr, dm, word, sub, accent, knock):
    m = mark(0, 0, 2.5, word, accent, knock, "mh")
    d1, w1 = text_path(fr, "Sandbox", 78, 140, 74)
    d2, w2 = text_path(dm, "ENGLISH SUMMER SCHOOL", 19.5, 143, 108, tracking=0.16)
    w = 140 + max(w1, w2) + 6
    return svg(w, 120, m + f'<path d="{d1}" fill="{word}"/><path d="{d2}" fill="{sub}"/>')


def stacked(fr, dm, word, sub, accent, knock):
    d1, w1 = text_path(fr, "Sandbox", 96, 0, 250)
    d2, w2 = text_path(dm, "ENGLISH SUMMER SCHOOL", 22, 0, 292, tracking=0.16)
    w = max(w1, w2)
    d1, _ = text_path(fr, "Sandbox", 96, (w - w1) / 2, 250)
    d2, _ = text_path(dm, "ENGLISH SUMMER SCHOOL", 22, (w - w2) / 2, 292, tracking=0.16)
    return svg(w, 305, mark((w - 144) / 2, 0, 3, word, accent, knock, "ms") + f'<path d="{d1}" fill="{word}"/><path d="{d2}" fill="{sub}"/>')


def lanyard(dm, bg, fg, accent):
    # 20mm-high strip at 2px/mm; one repeat of mark + name, tile it along the lanyard.
    d, tw = text_path(dm, "SANDBOX ENGLISH SUMMER SCHOOL", 15, 46, 25.5, tracking=0.14)
    unit = 46 + tw + 34
    body = mark(12, 5, 0.62, fg, accent, knockout=(accent == bg), mid="ml")
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
        "lanyard-navy.svg": lanyard(dm, NAVY, WHITE, CORAL),
        "lanyard-coral.svg": lanyard(dm, CORAL, WHITE, CORAL),
    }
    for name, content in files.items():
        (OUT / name).write_text(content)
        print("wrote", name)


if __name__ == "__main__":
    main(*sys.argv[1:3])
