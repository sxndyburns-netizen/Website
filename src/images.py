"""Make the smaller 800px versions of every photo, used in srcset on phones.

    python3 src/images.py

Needs Pillow (pip install pillow). Run it after adding or replacing a photo in
assets/img/photos/, then run src/build.py. Existing 800px files are regenerated.
"""
import pathlib
from PIL import Image

PHOTOS = pathlib.Path(__file__).resolve().parent.parent / "assets/img/photos"
SMALL = 800

for path in sorted(PHOTOS.glob("*.jpg")):
    if path.stem.endswith(f"-{SMALL}"):
        continue
    im = Image.open(path).convert("RGB")
    if im.width > SMALL:
        im = im.resize((SMALL, round(im.height * SMALL / im.width)), Image.LANCZOS)
    out = path.with_name(f"{path.stem}-{SMALL}.jpg")
    im.save(out, "JPEG", quality=76, optimize=True, progressive=True)
    print(f"{out.name}: {out.stat().st_size // 1024} KB")
