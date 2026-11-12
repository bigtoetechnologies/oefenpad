#!/usr/bin/env python3
"""Build the review sheet including art that is drawn but not yet in the game.

The stock builder reads prepositions.json and the shipped masks in
assets/voorzetselpaden, so it cannot show a frame that has only been delivered
as a full-size PNG. This script renders the same page, but appends the batches
from the art plans that are drawn and not integrated yet.

It imports the stock builder for the page shell, the CSS and the shipped cards,
so the two sheets cannot drift apart.

Usage:
    python3 tools/build-prepositions-preview.py
"""

import base64
import importlib.util
import io
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
STOCK = ROOT / "tools/build-prepositions-sheet.py"
DATA = ROOT / "server/Oefenpad.Resources/Games/Data/prepositions.json"
PENDING_PLANS = [
    # (plan file, full-size art folder, section title, note)
    (
        ROOT / "Docs/voorzetselpaden/a2-pairs.html",
        ROOT / "assets/verb-propositions/archived/04b-a2-pairs",
        "Batch 4b — A2 pair enhancement",
        "Getekend op 10 november 2026; twee scènes zijn op 12 november 2026 "
        "vervangen en moeten opnieuw getekend worden. Voorbeeldzin, bouwzin en "
        "controlevraag worden bij de integratie geschreven; die staan hier dus "
        "nog niet.",
    ),
]

SET = re.compile(r"\bSet ([AB])\b")
SMALL = (64, 96)

EXTRA_CSS = """
  .fase{grid-column:1/-1;margin-top:30px;padding-top:14px;border-top:2px solid var(--kobalt)}
  .fase h2{margin:0;font-size:22px;letter-spacing:-.01em}
  .fase p{margin:4px 0 0;color:var(--grijs);max-width:85ch;font-size:14px}
  .vlaggen span.nieuw{border-color:var(--kobalt);color:var(--kobalt)}
  .px64{display:flex;gap:12px;align-items:flex-start;margin-top:12px;padding-top:10px;border-top:1px dashed var(--lijn)}
  .px64 figure{margin:0;text-align:center}
  .px64 img{width:64px;height:96px;display:block;border:1px solid var(--lijn);border-radius:4px}
  .px64 figcaption{font-size:10px;color:var(--grijs);max-width:78px;line-height:1.2;margin:3px auto 0}
  .px64 .px64-kop{font-size:10px;text-transform:uppercase;letter-spacing:.04em;color:var(--grijs);margin:0 0 4px}
  .px64-kolom{margin:0}
"""


def load_stock():
    spec = importlib.util.spec_from_file_location("prepositions_sheet", STOCK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sheet = load_stock()
esc = sheet.esc


def ink_alpha(path: Path) -> Image.Image:
    """White paper to alpha for an incoming RGB PNG.

    The generator returns cobalt on near-white with no alpha channel, and the
    ink darkness varies per delivery. Normalise per image: take the darkest 1%
    as full ink, treat anything at or above paper level as empty.
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
    lut = [0 if value >= paper else max(0, min(255, round((paper - value) * 255 / span)))
           for value in range(256)]
    return grey.point(lut).resize(sheet.IMAGE_SIZE, Image.LANCZOS)


def uri(alpha: Image.Image, size: tuple) -> str:
    alpha = alpha.resize(size, Image.LANCZOS)
    ink = Image.new("RGB", size, sheet.COBALT)
    paper = Image.new("RGB", size, (255, 255, 255))
    flat = Image.composite(ink, paper, alpha).quantize(
        colors=sheet.PALETTE, method=Image.MEDIANCUT
    )
    buffer = io.BytesIO()
    flat.save(buffer, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def mono(text: str) -> str:
    """Escape, then turn the plan's `backticked ids` into code spans."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", esc(text))


def read_plan(path: Path) -> list[dict]:
    """Parse the band page, keeping the Set A / Set B grouping.

    The plans moved from Markdown trackers to one card per frame in
    Docs/voorzetselpaden/ on 12 November 2026. A card carries its fields as
    data-* attributes and class names, so this reads those rather than a table.
    """
    from html.parser import HTMLParser

    class Cards(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.rows = []
            self.cur = None
            self.set = None
            self.field = None
            self.buf = []

        def _flush(self):
            if self.cur is not None and self.field:
                self.cur[self.field] = " ".join("".join(self.buf).split())
            self.field, self.buf = None, []

        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            cls = a.get("class", "")
            if tag == "article" and "kaart" in cls.split():
                self._flush()
                m = SET.search(a.get("data-batch", ""))
                self.set = m.group(1) if m else None
                self.cur = {
                    "set": self.set,
                    "number": int(a.get("data-row") or 0),
                    "file": f'{a.get("data-id", "")}.png',
                    "status": (a.get("data-status") or "").strip(),
                    "frame": "", "en": "", "scene": "", "pair": "",
                }
            elif tag == "code" and self.field:
                self.buf.append("`")
            elif self.cur is not None:
                for name, key in (("chunk", "frame"), ("gloss", "en"),
                                  ("scene", "scene"), ("note", "pair")):
                    if name in cls.split():
                        self._flush()
                        self.field, self.buf = key, []
                        break

        def handle_endtag(self, tag):
            if tag == "code" and self.field:
                self.buf.append("`")
            elif tag in ("h3", "p", "dd"):
                self._flush()
            elif tag == "article" and self.cur is not None:
                self._flush()
                if self.cur["file"] != ".png":
                    self.rows.append(self.cur)
                self.cur = None

        def handle_data(self, data):
            if self.field:
                self.buf.append(data)

    text = path.read_text(encoding="utf-8")
    parser = Cards()
    parser.feed(text)
    parser.close()

    # Set membership comes from the page's batch index, which lists each
    # batch and its files in order. The cards themselves sit in contrast
    # clusters, not batch order.
    sets = {}
    for blk in re.finditer(r'<div class="batchrij" data-batch="(?P<b>[^"]*)">'
                           r'(?P<body>.*?)</div>', text, re.S):
        m = SET.search(blk.group("b"))
        if not m:
            continue
        for f in re.findall(r"<code>([^<]+\.png)</code>", blk.group("body")):
            sets[f] = m.group(1)

    rows = []
    for r in parser.rows:
        r["set"] = sets.get(r["file"]) or r.get("set")
        if r["set"]:
            rows.append(r)
    rows.sort(key=lambda r: (r["set"], r["number"]))
    return rows


def pending_card(row: dict, art: Path, cache: dict, shipped: dict, by_scene: dict,
                 by_id: dict, pending_by_file: dict, table: list) -> str:
    path = art / row["file"]
    image = cache.setdefault(("full", str(path)), uri(ink_alpha(path), sheet.IMAGE_SIZE))
    small = cache.setdefault((str(path)), uri(ink_alpha(path), SMALL))

    partners = []
    match = re.search(r"Pair with (\d+)", row["pair"])
    if match:
        number = int(match.group(1))
        if 1 <= number <= len(table) and number != row["number"]:
            partners.append(("pending", table[number - 1]["file"]))
    for ident in re.findall(r"`([^`]+)`", row["pair"]):
        # The plans cite either a scene id (stappen-uit-bus) or a frame id
        # (geinteresseerd-in); both have to resolve to a shipped scene.
        if ident in shipped:
            partners.append(("shipped", ident))
        elif ident in by_id:
            partners.append(("shipped", by_id[ident]["scene"]))
        elif ident in pending_by_file:
            partners.append(("pending", ident))

    thumbs = [
        f'<figure><img src="{small}" width="{SMALL[0]}" height="{SMALL[1]}" alt="">'
        f'<figcaption>{esc(row["frame"])}</figcaption></figure>'
    ]
    seen = set()
    for kind, ident in partners[:2]:
        if ident in seen:
            continue
        seen.add(ident)
        if kind == "shipped":
            scene = shipped[ident]
            frame = by_scene.get(ident, {}).get("frame", ident)
            partner_small = cache.setdefault(
                ("mask", scene["file"]),
                uri(Image.open(sheet.ART / Path(scene["file"]).name).getchannel("A"),
                    SMALL),
            )
            label = f'In het spel: {frame}'
        else:
            other = pending_by_file[ident]
            if other["file"] == row["file"] or other["status"] != "drawn":
                continue
            other_path = art / other["file"]
            partner_small = cache.setdefault((str(other_path)),
                                             uri(ink_alpha(other_path), SMALL))
            label = f'In 4b: {other["frame"]}'
        thumbs.append(
            f'<figure><img src="{partner_small}" width="{SMALL[0]}" height="{SMALL[1]}" alt="">'
            f'<figcaption>{esc(label)}</figcaption></figure>'
        )

    return f"""
      <article class="kaart">
        <img class="beeld" src="{image}" width="{sheet.IMAGE_SIZE[0]}" height="{sheet.IMAGE_SIZE[1]}" alt="">
        <h3>{esc(row['frame'])}</h3>
        <p class="betekenis">{esc(row['en'])}</p>
        <p class="vlaggen"><span class="nieuw">getekend, niet in het spel</span>
          <span class="neutraal">set {esc(row['set'])} #{row['number']}</span></p>
        <dl>
          <dt>Scenario</dt>
          <dd>{esc(row['scene'])}</dd>
          <dt>Paar</dt>
          <dd>{mono(row['pair'])}</dd>
          <dt>Voorbeeld</dt>
          <dd class="klein">nog niet geschreven</dd>
        </dl>
        <div class="px64-kolom"><p class="px64-kop">Op 64 px</p>
          <div class="px64">{''.join(thumbs)}</div></div>
        <p class="klein">{esc(row['file'])}</p>
      </article>"""


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    scenes = data["scenes"]
    by_id = {frame["id"]: frame for frame in data["frames"]}
    by_scene = {frame["scene"]: frame for frame in data["frames"]}
    cache: dict = {}

    blocks = []
    placed = set()
    for level in data["levels"]:
        placed.update(level["frames"])
        placed.update(level.get("extra") or [])
        frames = [by_id[f] for f in level["frames"] if f in by_id]
        seen = {frame["id"] for frame in frames}
        for extra_id in level.get("extra") or []:
            if extra_id in by_id and extra_id not in seen:
                frames.append(by_id[extra_id])
        blocks.append(sheet.section(level, frames, by_id, scenes, cache))
    loose = [frame for frame in data["frames"] if frame["id"] not in placed]
    if loose:
        blocks.append(sheet.section({"id": "—", "name": "Niet ingedeeld", "frames": []},
                                    loose, by_id, scenes, cache, kind="losse frames"))

    pending_total = 0
    needed_total = 0
    for plan, art, title, note in PENDING_PLANS:
        rows = read_plan(plan)
        if not rows:
            raise SystemExit(f"no frame cards parsed from {plan}")
        drawn = [row for row in rows if row["status"] == "drawn"]
        needed = [row for row in rows if row["status"] != "drawn"]
        pending_by_file = {row["file"]: row for row in rows}
        pending_total += len(drawn)
        needed_total += len(needed)
        needed_note = ""
        if needed:
            names = ", ".join(f"<code>{esc(row['file'])}</code>" for row in needed)
            needed_note = f" Still to draw: {names}."
        blocks.append(
            f'<section class="fase"><h2>{esc(title)}</h2>'
            f'<p>{len(rows)} frames: {len(drawn)} drawn, {len(needed)} still to '
            f'draw. {esc(note)}{needed_note}</p></section>'
        )
        for group in ("A", "B"):
            table = [row for row in rows if row["set"] == group]
            if not table:
                continue
            drawn_table = [row for row in table if row["status"] == "drawn"]
            blocks.append(
                f'<section class="fase"><h2>Set {group}</h2>'
                f'<p>{len(table)} frames, {len(drawn_table)} drawn, in the '
                f'numbering of {esc(Path(plan).name)}.</p></section>'
            )
            cards = "".join(
                pending_card(row, art, cache, scenes, by_scene, by_id,
                             pending_by_file, table)
                for row in drawn_table
            )
            blocks.append(
                f'<section class="niveau" style="grid-column:1/-1">'
                f'<div class="kaarten">{cards}</div></section>'
            )

    chips = [
        f"{len(data['frames'])} in het spel",
        f"{pending_total} getekend, nog niet in het spel",
    ]
    if needed_total:
        chips.append(f"{needed_total} te tekenen")
    chips += [
        f"{len(data['frames']) + pending_total} frames op dit blad",
        f"{len(data['levels'])} niveaus",
        f"{len(scenes)} tekeningen in het spel",
    ]
    summary = "".join(f"<span>{esc(chip)}</span>" for chip in chips)

    page = sheet.PAGE
    page = page.replace(
        "<title>Voorzetselpaden — A0–A2 beeldblad</title>",
        "<title>Voorzetselpaden — beeldblad</title>",
    )
    page = page.replace(
        "<h1>Voorzetselpaden — A0–A2 beeldblad</h1>",
        "<h1>Voorzetselpaden — beeldblad</h1>",
    )
    page = re.sub(
        r'<p class="lead">.*?</p>',
        '<p class="lead">Alles wat in het spel zit, plus de frames die al getekend '
        'zijn maar nog niet in <code>prepositions.json</code> staan. De afbeeldingen '
        'zijn ingebed, dus deze pagina opent zonder server en zonder JavaScript. '
        'Frames met <em>alleen ontdekken</em> komen alleen in de ontdekstap voor en '
        'worden niet gescoord.</p>',
        page,
        count=1,
        flags=re.S,
    )
    page = page.replace("</style>", EXTRA_CSS + "</style>")
    page = page.replace("__SUM__", summary).replace("__CARDS__", "".join(blocks))

    out = sheet.OUT
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size:,} bytes, "
          f"{len(data['frames'])} shipped + {pending_total} pending)")


if __name__ == "__main__":
    main()
