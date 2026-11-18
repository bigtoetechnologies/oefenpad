#!/usr/bin/env python3
"""Embed delivered drawings into their band page and file the source PNG.

    python3 tools/_vp_tmp/apply-vp-batch.py a1 tools/_vp_tmp/batches/a1-kijken

For every PNG in the folder whose name is a card id on that page it replaces
the "not drawn yet" placeholder, or an older embedded drawing, with the new one
at the page's 260 x 390 size; sets data-status="drawn"; adds the getekend badge;
copies the full-size PNG into incoming/<BAND>/; and, for the bands the game
reads, promotes the mask. Idempotent: running it twice changes nothing the
second time.
"""

import base64
import importlib.util
import io
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PAGES = ROOT / "Docs/voorzetselpaden"
INCOMING = ROOT / "assets/verb-propositions/incoming"
ART = ROOT / "assets/voorzetselpaden"
GAME_BANDS = ("a0", "a1")

SIZE = (260, 390)
COLORS = 32
ARTICLE = re.compile(r'(?s)<article class="kaart[^"]*"[^>]*>.*?</article>')


def data_uri(path: Path) -> str:
    with Image.open(path) as source:
        small = source.convert("RGB").resize(SIZE, Image.LANCZOS)
    flat = small.quantize(colors=COLORS, method=Image.MEDIANCUT)
    buffer = io.BytesIO()
    flat.save(buffer, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def image_tag(path: Path, alt: str) -> str:
    return (f'<img class="beeld" src="{data_uri(path)}" '
            f'width="{SIZE[0]}" height="{SIZE[1]}" alt="{alt}">')


def add_badge(body: str) -> str:
    if 'class="getekend"' in body:
        return body
    banner = re.search(r'<p class="vlaggen">', body)
    if banner:
        return (body[:banner.end()] + '<span class="getekend">drawn</span>'
                + body[banner.end():])
    gloss = re.search(r'<p class="gloss">.*?</p>', body, re.S)
    if not gloss:
        raise SystemExit("no gloss to anchor the getekend badge")
    return (body[:gloss.end()] + '<p class="vlaggen"><span class="getekend">drawn</span></p>'
            + body[gloss.end():])


def apply(band: str, folder: Path) -> None:
    page_path = PAGES / f"{band}.html"
    page = page_path.read_text(encoding="utf-8")
    sources = {p.stem: p for p in folder.glob("*.png")}
    if not sources:
        raise SystemExit(f"no PNG in {folder}")

    pieces, last = [], 0
    embedded, replaced, skipped = [], [], []
    for match in ARTICLE.finditer(page):
        card = match.group(0)
        head, body, tail = re.match(r"(<article\b[^>]*>)(.*)(</article>)", card,
                                    re.S).groups()
        scene_id = re.search(r'data-id="([^"]+)"', head).group(1)
        source = sources.get(scene_id)
        if source is None:
            continue

        alt = re.search(r'<dd class="alt">(.*?)</dd>', body, re.S)
        tag = image_tag(source, alt.group(1) if alt else scene_id)
        if 'class="beeld"' in body:
            existing = re.search(r'<img class="beeld" src="([^"]*)"', body)
            if existing and existing.group(1) == re.search(r'src="([^"]*)"', tag).group(1):
                skipped.append(scene_id)
                continue
            body = re.sub(r'<img class="beeld"[^>]*>', tag, body, count=1)
            replaced.append(scene_id)
        elif '<p class="geenbeeld">not drawn yet</p>' in body:
            body = body.replace('<p class="geenbeeld">not drawn yet</p>', tag, 1)
            embedded.append(scene_id)
        else:
            raise SystemExit(f"{scene_id}: no placeholder and no drawing to replace")

        head = re.sub(r'data-status="[^"]*"', 'data-status="drawn"', head, count=1)
        body = add_badge(body)
        pieces.append(page[last:match.start()])
        pieces.append(head + body + tail)
        last = match.end()

    if not (embedded or replaced):
        print(f"{band}: nothing to change ({len(skipped)} already current)")
        return
    pieces.append(page[last:])
    page = "".join(pieces)

    total = len(ARTICLE.findall(page))
    drawn = sum(1 for m in ARTICLE.finditer(page) if 'class="beeld"' in m.group(0))
    summary = re.search(r'<div class="sum">(.*?)</div>', page, re.S)
    if not summary:
        raise SystemExit("no header summary")
    spans = [s for s in re.findall(r'<span>.*?</span>', summary.group(1), re.S)
             if "drawn" not in s]
    spans.append(f"<span>{drawn} of {total} drawn</span>")
    page = (page[:summary.start()] + '<div class="sum">' + "".join(spans) + '</div>'
            + page[summary.end():])

    page_path.write_text(page, encoding="utf-8")

    target = INCOMING / band.upper()
    target.mkdir(parents=True, exist_ok=True)
    for scene_id in embedded + replaced:
        shutil.copy2(sources[scene_id], target / f"{scene_id}.png")

    promoted = []
    if band in GAME_BANDS:
        spec = importlib.util.spec_from_file_location(
            "import_prepositions_band", ROOT / "tools/import-prepositions-band.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        promoted = [i for i in embedded + replaced if module.promote(i, band)]

    print(f"{band}: embedded {len(embedded)}, replaced {len(replaced)}, "
          f"unchanged {len(skipped)}")
    print(f"  embedded: {', '.join(embedded) or '-'}")
    print(f"  replaced: {', '.join(replaced) or '-'}")
    print(f"  header:   {drawn} of {total} drawn")
    print(f"  masks:    {', '.join(promoted) or 'none promoted'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    apply(sys.argv[1], Path(sys.argv[2]).resolve())
