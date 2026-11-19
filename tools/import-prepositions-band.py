#!/usr/bin/env python3
"""Rebuild Voorzetselpaden from the A0, A1, A2 and A2-pairs band pages.

`Docs/voorzetselpaden/a0.html`, `a1.html`, `a2.html` and `a2-pairs.html` are the master for the content:
one card per example scene, with the sentence, the build lines, the control
question and the alt text. This script reads them (read-only) and writes:

  server/Oefenpad.Resources/Games/Data/prepositions.json
  server/Oefenpad.Resources/Games/Data/meta.json
  assets/voorzetselpaden/<scene-id>.png   (only where the mask is missing)

Only cards that carry an image are used. A chunk with no image at all is not a
level, and a card without an image is not an example.

The game practices one chunk per level (`wachten op`, not `wachten`). A level
therefore holds every ready example of that chunk, and the contrast partner is
used for the Klopt stop.

The source art lives in `assets/verb-propositions/incoming/`, one folder per
band (`A0/`, `A1/`, ...). The conversion is the one in
`assets/verb-propositions/README.md`: white paper to alpha, 512 x 763, keeping
only alpha so the CSS mask paints the cobalt.

Usage:
    python3 tools/import-prepositions-band.py            # write everything
    python3 tools/import-prepositions-band.py --check    # report, write nothing
    python3 tools/import-prepositions-band.py --no-art   # JSON only
"""

import argparse
import html
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "Docs/voorzetselpaden"
INCOMING = ROOT / "assets/verb-propositions/incoming"
ART = ROOT / "assets/voorzetselpaden"
DATA = ROOT / "server/Oefenpad.Resources/Games/Data/prepositions.json"
META = ROOT / "server/Oefenpad.Resources/Games/Data/meta.json"

BANDS = ("a0", "a1", "a2", "a2-pairs")
MASK_SIZE = (512, 763)


def incoming_art(band: str, scene_id: str) -> Path | None:
    """The delivered drawing for a scene, filed under its band's folder.

    A file left loose in the pool root is still accepted, so an un-filed
    delivery keeps working while `incoming/` is being reorganised.
    """
    for path in (INCOMING / band.upper() / f"{scene_id}.png",
                 INCOMING / f"{scene_id}.png"):
        if path.exists():
            return path
    return None

ARTICLE = re.compile(r'<article class="kaart"([^>]*)>(.*?)</article>', re.S)
CHUNK_GROUP = re.compile(
    r'<div class="chunkgroep" data-chunk="([^"]+)" data-examples="\d+">')
CLUSTER = re.compile(r'<section class="cluster" data-stem="([^"]+)">')


def text(value: str) -> str:
    """Strip tags and entities, collapse whitespace."""
    value = re.sub(r"<br\s*/?>", "\n", value)
    value = re.sub(r"<[^>]+>", "", value)
    return " ".join(html.unescape(value).split())


def attribute(attrs: str, name: str) -> str:
    match = re.search(rf'{name}="([^"]*)"', attrs)
    return html.unescape(match.group(1)) if match else ""


def field(body: str, cls: str) -> str | None:
    match = re.search(rf'<dd class="{re.escape(cls)}">(.*?)</dd>', body, re.S)
    return match.group(1) if match else None


def read_card(attrs: str, body: str) -> dict:
    """One example card, as far as the game needs it."""
    example = field(body, "voorbeeld-nl") or ""
    sentence = text(example.split("<br")[0])

    english = re.search(r'<span class="voorbeeld-en">(.*?)</span>', example, re.S)
    question_html = field(body, "controlevraag") or ""
    answer = re.search(r'<strong class="antwoord">\s*(Ja|Nee)\s*</strong>', question_html)
    question = text(re.sub(r'<strong.*?</strong>', "", question_html, flags=re.S))

    builds = [text(value) for value in re.findall(
        r'<dd class="bouw">(.*?)</dd>', body, re.S)]

    return {
        "id": attribute(attrs, "data-id"),
        "band": attribute(attrs, "data-band"),
        "image": 'class="beeld"' in body,
        "scene": text(field(body, "scene") or ""),
        "alt": text(field(body, "alt") or ""),
        "nl": sentence,
        "en": text(english.group(1)) if english else "",
        "build": [value for value in builds if value],
        "question": question,
        "answer": answer.group(1) == "Ja" if answer else None,
        "contrast": text(field(body, "contrast") or ""),
        "prefix": text(field(body, "scheidbaar") or "") or None,
        "status": attribute(attrs, "data-status"),
    }


def read_band(band: str) -> list[dict]:
    """The band's chunk groups, in page order, with their example cards."""
    page = (DOCS / f"{band}.html").read_text(encoding="utf-8")
    clusters = [(match.start(), match.group(1)) for match in CLUSTER.finditer(page)]
    groups = list(CHUNK_GROUP.finditer(page))

    chunks = []
    for index, group in enumerate(groups):
        stop = groups[index + 1].start() if index + 1 < len(groups) else len(page)
        body = page[group.end():stop]
        cluster = ""
        for position, stem in clusters:
            if position < group.start():
                cluster = stem
            else:
                break

        cards = [read_card(match.group(1), match.group(2))
                 for match in ARTICLE.finditer(body)]
        if not cards:
            continue

        # The gloss sits on the first card of the chunk; later examples leave
        # it empty. Take the first one that is actually filled in.
        gloss = next((value for value in
                      (text(match.group(1)) for match in
                       re.finditer(r'<p class="gloss">(.*?)</p>', body, re.S))
                      if value), "")

        chunks.append({
            "band": band,
            "cluster": cluster,
            "chunk": html.unescape(group.group(1)),
            "gloss": gloss,
            "cards": cards,
        })
    return chunks


def slug(chunk: str) -> str:
    return chunk.replace(" ", "-")


def build_content() -> tuple[dict, list[str]]:
    """Turn the cards into the game's scenes, frames and levels."""
    chunks = [chunk for band in BANDS for chunk in read_band(band)]
    ready = [chunk for chunk in chunks
             if any(card["image"] and card["nl"] and card["build"] and card["question"]
                    for card in chunk["cards"])]
    ready_slugs = {slug(chunk["chunk"]): chunk for chunk in ready}

    # The page names an intended contrast partner on the chunk's first card.
    # Fall back to a sibling in the same cluster, then make the pairs mutual so
    # a chunk that the page left blank still gets the stop when its partner
    # names it.
    partners: dict[str, str | None] = {}
    for chunk in ready:
        intended = next((card["contrast"] for card in chunk["cards"]
                         if card["contrast"]), "")
        target = intended if intended in ready_slugs else None
        if target is None:
            target = next((slug(other["chunk"]) for other in ready
                           if other is not chunk
                           and other["cluster"] == chunk["cluster"]), None)
        partners[chunk["chunk"]] = target

    for chunk in list(partners):
        target = partners[chunk]
        if target and partners.get(target) is None:
            partners[target] = slug(chunk)

    scenes: dict[str, dict] = {}
    scene_bands: dict[str, str] = {}
    frames: list[dict] = []
    levels: list[dict] = []
    missing_art: list[str] = []

    for chunk in ready:
        name = chunk["chunk"]
        examples = [card for card in chunk["cards"]
                    if card["image"] and card["nl"] and card["build"] and card["question"]]
        if not examples:
            continue

        prefix = next((card["prefix"] for card in examples if card["prefix"]), None)
        focus = ([prefix] if prefix else []) + [name.split()[-1]]

        level_frames = []
        for card in examples:
            scenes[card["id"]] = {
                "file": f"art/{card['id']}.png",
                "alt": card["alt"] or card["nl"],
            }
            level_frames.append(card["id"])
            scene_bands[card["id"]] = chunk["band"]
            frames.append({
                "id": card["id"],
                "frame": name,
                "en": chunk["gloss"],
                "scene": card["id"],
                "contrast": None,
                "focus": focus,
                **({"separable": True, "prefix": prefix} if prefix else {}),
                "example": {"nl": card["nl"], "en": card["en"]},
                "build": [card["build"][0].split()],
                "concept": [{"question": card["question"], "answer": card["answer"]}],
            })

        target = partners.get(name)
        if target and target in {slug(other["chunk"]) for other in ready}:
            partner_chunk = next(other for other in ready
                                 if slug(other["chunk"]) == target)
            partner_ids = [card["id"] for card in partner_chunk["cards"]
                           if card["image"] and card["nl"] and card["build"]
                           and card["question"]]
            by_id = {frame["id"]: frame for frame in frames}
            for index, frame_id in enumerate(level_frames):
                by_id[frame_id]["contrast"] = partner_ids[index % len(partner_ids)]

        levels.append({
            "id": slug(name),
            "name": name,
            "band": chunk["band"],
            "frames": level_frames,
        })

    for scene_id in scenes:
        if not (ART / f"{scene_id}.png").exists():
            if incoming_art(scene_bands[scene_id], scene_id) is None:
                missing_art.append(scene_id)

    return ({"scenes": scenes, "frames": frames, "levels": levels}, missing_art,
            scene_bands)


def ink_alpha(path: Path) -> Image.Image:
    """White paper to alpha, normalising the delivered cobalt's darkness.

    Kept identical to `tools/build-prepositions-preview.py`: the darkest 1% is
    full ink, paper is 250. RGB is flattened because only alpha is shipped.
    """
    grey = Image.open(path).convert("L")
    hist = grey.histogram()
    total = sum(hist)
    seen = 0
    ink = 0
    for value, count in enumerate(hist):
        seen += count
        if seen >= total * 0.01:
            ink = value
            break
    ink = min(ink, 120)
    paper = 250
    span = max(1, paper - ink)
    lut = [0 if value >= paper
           else max(0, min(255, round((paper - value) * 255 / span)))
           for value in range(256)]
    return grey.point(lut).resize(MASK_SIZE, Image.LANCZOS)


def promote(scene_id: str, band: str, force: bool = False) -> bool:
    out = ART / f"{scene_id}.png"
    if out.exists() and not force:
        return False
    alpha = ink_alpha(incoming_art(band, scene_id))
    flat = Image.new("RGB", MASK_SIZE, (255, 255, 255))
    flat.putalpha(alpha)
    flat.save(out, optimize=True)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="write nothing")
    parser.add_argument("--no-art", action="store_true", help="JSON only")
    parser.add_argument("--force-art", action="store_true",
                        help="re-convert masks that already exist")
    args = parser.parse_args()

    content, missing, scene_bands = build_content()
    frames = len(content["frames"])
    levels = content["levels"]
    scenes = len(content["scenes"])
    pending = [scene for scene in content["scenes"]
               if not (ART / f"{scene}.png").exists()]

    print(f"{scenes} scenes, {frames} examples, {len(levels)} levels")
    for level in levels:
        print(f"  {level['band']}  {level['name']:<20} {len(level['frames'])} examples")

    if missing:
        raise SystemExit(f"no source art for: {', '.join(sorted(missing))}")

    if args.check:
        print(f"{len(pending)} masks still to promote")
        return

    if not args.no_art:
        written = sum(promote(scene, scene_bands[scene], args.force_art)
                      for scene in content["scenes"])
        print(f"promoted {written} masks into {ART.relative_to(ROOT)}")

    DATA.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")

    meta = json.loads(META.read_text(encoding="utf-8"))
    meta["generatedFrom"] = (
        "Docs/voorzetselpaden/a0.html, a1.html, a2.html and a2-pairs.html (cards with an image), "
        "via tools/import-prepositions-band.py")
    meta["scenes"] = scenes
    meta["frames"] = frames
    meta["levels"] = len(levels)
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    print(f"wrote {DATA.relative_to(ROOT)} and {META.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
