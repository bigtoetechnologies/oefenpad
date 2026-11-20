#!/usr/bin/env python3
"""Copy a delivered drawing into the file the site ships.

    python3 tools/composite-prepositions-art.py <delivered.png> <scene-id>
    python3 tools/composite-prepositions-art.py --all

Delivered art arrives with the white paper baked in and is drawn 2:3 portrait.
The drawing already carries the ink, so the shipped file is the drawing: it is
shrunk to 512 x 763 and palette-compressed to keep the repo small. Nothing is
masked, nothing is recoloured, no second file exists per scene.

Do not point this at an already-shipped file: it would reshrink a 512 x 763
copy instead of starting from the drawing.
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "voorzetselpaden")
INCOMING = os.path.join(ROOT, "assets", "verb-propositions", "incoming")
SIZE = (512, 763)
COLORS = 96         # the drawing is ink on paper; 96 keeps its own cobalt and the brush edge


def ship(source, scene_id):
    with Image.open(source) as delivered:
        flat = delivered.convert("RGB").resize(SIZE, Image.LANCZOS)
    flat = flat.quantize(colors=COLORS, method=Image.MEDIANCUT)

    os.makedirs(OUT, exist_ok=True)
    target = os.path.join(OUT, f"{scene_id}.png")
    flat.save(target, format="PNG", optimize=True)
    return target, os.path.getsize(target)


def all_ids():
    for base, _dirs, files in os.walk(INCOMING):
        for name in sorted(files):
            if name.lower().endswith(".png"):
                yield os.path.join(base, name), os.path.splitext(name)[0]


def main():
    args = sys.argv[1:]
    if args == ["--all"]:
        total = 0
        pairs = list(all_ids())
        for source, scene_id in pairs:
            _target, size = ship(source, scene_id)
            total += size
        print(f"{len(pairs)} files, {total / (1024 * 1024):.1f} MB")
        return
    if len(args) != 2:
        sys.exit(__doc__)
    source, scene_id = args
    if not os.path.isfile(source):
        sys.exit(f"no such file: {source}")
    target, size = ship(source, scene_id)
    print(f"{target}  ({size // 1024} KB)")


if __name__ == "__main__":
    main()
