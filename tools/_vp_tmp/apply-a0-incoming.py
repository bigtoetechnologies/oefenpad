#!/usr/bin/env python3
"""One-off: embed the missing A0 drawings and tag every A0 card as drawn.

The band page is the source and holds base64 art inline, so this edits it with
a regex pass rather than by hand. Idempotent: cards that already carry an image
keep it, and a `getekend` badge is only added once.
"""

import base64
import importlib.util
import io
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
PAGE = ROOT / "Docs/voorzetselpaden/a0.html"
INCOMING = ROOT / "assets/verb-propositions/incoming"
ART = ROOT / "assets/voorzetselpaden"

SIZE = (260, 390)  # matches the cards already on the page
COLORS = 32
ARTICLE = re.compile(r'<article class="kaart[^"]*"[^>]*>.*?</article>', re.S)


def data_uri(scene_id: str) -> str:
    """Incoming full-size RGB -> 260x390 palette PNG, exactly as on the page."""
    with Image.open(INCOMING / f"{scene_id}.png") as source:
        small = source.convert("RGB").resize(SIZE, Image.LANCZOS)
    flat = small.quantize(colors=COLORS, method=Image.MEDIANCUT)
    buffer = io.BytesIO()
    flat.save(buffer, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def main() -> None:
    page = PAGE.read_text(encoding="utf-8")
    pieces: list[str] = []
    last = 0
    embedded: list[str] = []
    tagged: list[str] = []

    for match in ARTICLE.finditer(page):
        card = match.group(0)
        opening = re.match(r"(<article\b[^>]*>)(.*)(</article>)", card, re.S)
        head, body, tail = opening.groups()
        scene_id = re.search(r'data-id="([^"]+)"', head).group(1)

        if 'class="beeld"' not in body:
            if not (INCOMING / f"{scene_id}.png").exists():
                raise SystemExit(f"no source art for {scene_id}")
            alt = re.search(r'<dd class="alt">(.*?)</dd>', body, re.S).group(1)
            img = (f'<img class="beeld" src="{data_uri(scene_id)}" '
                   f'width="{SIZE[0]}" height="{SIZE[1]}" alt="{alt}">')
            if '<p class="geenbeeld">not drawn yet</p>' not in body:
                raise SystemExit(f"{scene_id}: no placeholder to replace")
            body = body.replace('<p class="geenbeeld">not drawn yet</p>', img, 1)
            embedded.append(scene_id)

        # Art is present on every card from here on.
        if not re.search(r'data-status="[^"]*"', head):
            raise SystemExit(f"{scene_id}: no data-status attribute")
        head = re.sub(r'data-status="[^"]*"', 'data-status="drawn"', head, count=1)

        if 'class="getekend"' not in body:
            banner = re.search(r'<p class="vlaggen">', body)
            if banner:
                body = (body[:banner.end()]
                        + '<span class="getekend">drawn</span>'
                        + body[banner.end():])
            else:
                gloss = re.search(r'<p class="gloss">.*?</p>', body, re.S)
                if not gloss:
                    raise SystemExit(f"{scene_id}: no gloss to anchor the banner")
                body = (body[:gloss.end()]
                        + '<p class="vlaggen"><span class="getekend">drawn</span></p>'
                        + body[gloss.end():])
            tagged.append(scene_id)

        pieces.append(page[last:match.start()])
        pieces.append(head + body + tail)
        last = match.end()

    pieces.append(page[last:])
    page = "".join(pieces)

    before = '<div class="sum"><span>10 verb-prepositions</span><span>40 cards</span></div>'
    after = ('<div class="sum"><span>10 verb-prepositions</span><span>40 cards</span>'
             '<span>40 of 40 drawn</span></div>')
    if before in page:
        page = page.replace(before, after, 1)
    elif after not in page:
        raise SystemExit("header summary not found")

    PAGE.write_text(page, encoding="utf-8")

    # Promote a game mask for the newly embedded scenes. The colour pipeline is
    # the reviewed one, imported rather than copied. Cards that already had art
    # (such as the weak-picture letten-op-kind) are left alone: promoting one
    # would accept a drawing the page itself flags for redraw.
    spec = importlib.util.spec_from_file_location(
        "import_prepositions_band", ROOT / "tools/import-prepositions-band.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    promoted = [scene_id for scene_id in embedded if module.promote(scene_id)]

    print(f"embedded {len(embedded)} images: {', '.join(embedded)}")
    print(f"added getekend badge to {len(tagged)} cards")
    print(f"promoted {len(promoted)} masks: {', '.join(promoted)}")


if __name__ == "__main__":
    main()
