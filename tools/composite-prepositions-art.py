#!/usr/bin/env python3
"""Turn a delivered drawing into the file the site ships.

    python3 tools/composite-prepositions-art.py <delivered.png> <scene-id>

Delivered art arrives with the white paper baked in and is drawn 2:3 portrait.
There is no dark mode, so the shipped file carries the cobalt itself: the paper
is turned into an alpha mask, the mask is filled with the cobalt, and the result
is written to assets/voorzetselpaden/<scene-id>.png at 512 x 763.

One file per scene. The mask is not kept: rerun this from the delivered drawing
if the ink or the paper colour ever changes.

Do not point this at an already-shipped file — it would treat the cobalt as ink
and fill the whole frame.
"""
import os
import sys

from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "voorzetselpaden")
SIZE = (512, 763)
COLORS = 32
COBALT = (43, 80, 200)      # #2B50C8; the retired #1B3A6B must not creep in
PAPER = (255, 255, 255)
FLOOR = 10                  # keeps near-white noise out of the mask


def mask_from_paper(image):
    """paper -> 0, ink -> 255, on the darkest channel."""
    rgb = image.convert("RGB")
    darkest = ImageChops.darker(ImageChops.darker(rgb.getchannel("R"), rgb.getchannel("G")),
                                rgb.getchannel("B"))
    return darkest.point(lambda v: 0 if 255 - v <= FLOOR
                         else round((255 - v - FLOOR) * 255 / (255 - FLOOR)))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    source, scene_id = sys.argv[1], sys.argv[2]
    if not os.path.isfile(source):
        sys.exit(f"no such file: {source}")

    with Image.open(source) as delivered:
        alpha = mask_from_paper(delivered).resize(SIZE, Image.LANCZOS)

    ink = Image.new("RGB", SIZE, COBALT)
    paper = Image.new("RGB", SIZE, PAPER)
    flat = Image.composite(ink, paper, alpha).quantize(colors=COLORS, method=Image.MEDIANCUT)

    os.makedirs(OUT, exist_ok=True)
    target = os.path.join(OUT, f"{scene_id}.png")
    flat.save(target, format="PNG", optimize=True)
    print(f"{target}  ({os.path.getsize(target) // 1024} KB)")


if __name__ == "__main__":
    main()
