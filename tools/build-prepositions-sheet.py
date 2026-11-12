#!/usr/bin/env python3
"""Build a one-page review sheet for the Voorzetselpaden frames.

Reads the game data and writes a standalone HTML page next to the site assets.
The page needs no server and no JavaScript: the drawings are composited to
cobalt, downscaled and embedded as data URIs, and every card is rendered here
rather than in the browser. Double-clicking the file is enough.

Usage:
    python3 tools/build-prepositions-sheet.py
"""

import base64
import html
import io
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "server/Oefenpad.Resources/Games/Data/prepositions.json"
ART = ROOT / "assets/voorzetselpaden"
OUT = ROOT / "assets/site/prepositions-sheet.html"

COBALT = (43, 80, 200)  # #2B50C8, the only ink
IMAGE_SIZE = (320, 477)  # 2:3 portrait, 1.7× the 190 px display width
PALETTE = 16

PAGE = """<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Voorzetselpaden — A0–A2 beeldblad</title>
<style>
  :root{
    --kobalt:#2B50C8;
    --papier:#fff;
    --inkt:#111;
    --grijs:#666;
    --lijn:#d9deea;
    --letter:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--papier);color:var(--inkt);font-family:var(--letter);line-height:1.4}
  header{padding:28px 24px 18px;border-bottom:2px solid var(--kobalt)}
  h1{margin:0 0 4px;font-size:clamp(24px,4vw,38px);letter-spacing:-.02em}
  .lead{margin:0;color:var(--grijs);max-width:75ch}
  .sum{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
  .sum span{border:1px solid var(--lijn);border-radius:999px;padding:4px 10px;font-size:13px}
  main{padding:20px 24px 48px}
  .blad{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;align-items:start}
  .niveau{border-top:1px solid var(--lijn);padding-top:8px;break-inside:avoid}
  .niveau-kop{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline;padding-bottom:6px}
  .niveau-kop h2{margin:0;font-size:18px}
  .niveau-kop code{color:var(--grijs);font-size:12px}
  .badge{border:1px solid var(--lijn);border-radius:999px;padding:2px 9px;font-size:11px;color:var(--grijs)}
  .kaarten{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:4px}
  .kaart{border:1px solid var(--lijn);border-radius:12px;padding:14px;background:var(--papier);break-inside:avoid}
  .beeld{display:block;width:100%;max-width:190px;height:auto;margin:0 auto 12px}
  .kaart h3{margin:0;font-size:18px;letter-spacing:-.01em}
  .betekenis{margin:2px 0 8px;color:var(--grijs);font-size:14px}
  .vlaggen{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 8px}
  .vlaggen span{border:1px solid var(--kobalt);border-radius:999px;padding:1px 8px;font-size:11px;color:var(--kobalt)}
  .vlaggen span.neutraal{border-color:var(--lijn);color:var(--grijs)}
  dl{margin:0;font-size:14px}
  dt{margin-top:9px;color:var(--grijs);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
  dd{margin:2px 0 0}
  .chunk{color:var(--kobalt);font-weight:700}
  .bouw{display:flex;flex-direction:column;gap:2px}
  .klein{color:var(--grijs);font-size:12px;margin-top:10px}
  @media print{
    header{padding:0 0 12px}
    main{padding:0}
    .blad{grid-template-columns:repeat(3,1fr);gap:10px}
    .niveau{grid-column:span 1 !important}
    .kaart{page-break-inside:avoid;padding:10px}
    .beeld{max-width:120px}
    body{font-size:12px}
  }
</style>
</head>
<body>
<header>
  <h1>Voorzetselpaden — A0–A2 beeldblad</h1>
  <p class="lead">Alle frames uit <code>prepositions.json</code> met hun tekening, chunk,
  betekenis, voorbeeldzin (NL/EN), bouwzin, controlevraag en contrastpartner.
  De afbeeldingen zijn dezelfde kobalt masks als in het spel, hier ingebed zodat
  deze pagina zonder server opent. Frames met <em>alleen ontdekken</em> komen
  alleen in de ontdekstap voor en worden niet gescoord.</p>
  <div class="sum">__SUM__</div>
</header>
<main>
  <div class="blad">__CARDS__</div>
</main>
</body>
</html>
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def data_uri(path: Path, cache: dict) -> str:
    """Composite the alpha mask onto white in cobalt, then inline it."""
    if path in cache:
        return cache[path]
    alpha = Image.open(path).getchannel("A").resize(IMAGE_SIZE, Image.LANCZOS)
    ink = Image.new("RGB", IMAGE_SIZE, COBALT)
    paper = Image.new("RGB", IMAGE_SIZE, (255, 255, 255))
    flat = Image.composite(ink, paper, alpha).quantize(colors=PALETTE, method=Image.MEDIANCUT)
    buffer = io.BytesIO()
    flat.save(buffer, format="PNG", optimize=True)
    uri = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")
    cache[path] = uri
    return uri


def mark_focus(nl: str, focus: list[str]) -> str:
    wanted = {word.lower() for word in focus}
    parts = []
    for word in nl.split(" "):
        bare = re.sub(r"[.,!?]+$", "", word).lower()
        parts.append(
            f'<span class="chunk">{esc(word)}</span>' if bare in wanted else esc(word)
        )
    return " ".join(parts)


def card(frame: dict, scenes: dict, by_id: dict, cache: dict) -> str:
    scene = scenes.get(frame["scene"]) or {"file": "", "alt": ""}
    name = Path(scene["file"]).name
    image = data_uri(ART / name, cache)

    contrast = "— (single)"
    partner = frame.get("contrast")
    if partner and partner in by_id:
        contrast = by_id[partner]["frame"]

    flags = []
    if frame.get("discoverOnly"):
        flags.append('<span class="neutraal">alleen ontdekken</span>')
    if frame.get("separable"):
        prefix = f" · {esc(frame['prefix'])}" if frame.get("prefix") else ""
        flags.append(f"<span>scheidbaar{prefix}</span>")
    if not partner:
        flags.append('<span class="neutraal">geen contrastpaar</span>')
    flag_html = f'<p class="vlaggen">{"".join(flags)}</p>' if flags else ""

    extra = []
    if frame.get("prefix"):
        extra.append(f'<dt>Los voorzetsel</dt><dd>{esc(frame["prefix"])}</dd>')
    if frame.get("pronominal"):
        extra.append(
            "<dt>Voornaamwoordelijk bijwoord</dt>"
            f'<dd>{esc(frame["pronominal"]["nl"])}<br>'
            f'<span class="klein">{esc(frame["pronominal"]["en"])}</span></dd>'
        )
    extra_html = "".join(extra)

    builds = "<br>".join(esc(" ".join(tokens)) + "." for tokens in frame["build"])
    concept = frame["concept"][0]
    yes_no = "Ja" if concept["answer"] else "Nee"

    return f"""
      <article class="kaart">
        <img class="beeld" src="{image}" width="{IMAGE_SIZE[0]}" height="{IMAGE_SIZE[1]}" alt="{esc(scene['alt'])}">
        <h3>{esc(frame['frame'])}</h3>
        <p class="betekenis">{esc(frame['en'])}</p>
        {flag_html}
        <dl>
          <dt>Voorbeeld</dt>
          <dd>{mark_focus(frame['example']['nl'], frame['focus'])}<br>
            <span class="klein">{esc(frame['example']['en'])}</span></dd>
          <dt>Bouwen</dt>
          <dd class="bouw">{builds}</dd>
          <dt>Controlevraag</dt>
          <dd>{esc(concept['question'])} <strong>{yes_no}</strong></dd>
          <dt>Contrast</dt>
          <dd>{esc(contrast)}</dd>
          {extra_html}
        </dl>
        <p class="klein">{esc(frame['scene'])} · {esc(scene['alt'])}</p>
      </article>"""


def section(level: dict, frames: list[dict], by_id: dict, scenes: dict, cache: dict,
            kind: str | None = None) -> str:
    cards = "".join(card(frame, scenes, by_id, cache) for frame in frames)
    span = min(len(frames), 2)
    body = len(level["frames"])
    if kind is not None:
        label = kind
    else:
        kind = "single" if body == 1 else "contrastpaar" if body == 2 else f"set van {body}"
        extra = len(frames) - body
        label = kind + (f" + {extra} ontdek" if extra else "")
    return f"""
      <section class="niveau" style="grid-column:span {span}">
        <div class="niveau-kop">
          <h2>{esc(level['name'])}</h2>
          <code>{esc(level['id'])}</code>
          <span class="badge">{esc(label)}</span>
        </div>
        <div class="kaarten">{cards}</div>
      </section>"""


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    scenes = data["scenes"]
    by_id = {frame["id"]: frame for frame in data["frames"]}
    cache: dict = {}

    blocks = []
    placed = set()
    for level in data["levels"]:
        placed.update(level["frames"])
        placed.update(level.get("extra") or [])
        frames = [by_id[frame_id] for frame_id in level["frames"] if frame_id in by_id]
        seen = {frame["id"] for frame in frames}
        for extra_id in level.get("extra") or []:
            if extra_id in by_id and extra_id not in seen:
                frames.append(by_id[extra_id])
        blocks.append(section(level, frames, by_id, scenes, cache))

    loose = [frame for frame in data["frames"] if frame["id"] not in placed]
    if loose:
        blocks.append(
            section({"id": "—", "name": "Niet ingedeeld", "frames": []}, loose, by_id, scenes, cache,
                    kind="losse frames")
        )

    pairs = len({tuple(sorted((f["id"], f["contrast"]))) for f in data["frames"] if f.get("contrast")})
    chips = [
        f"{len(data['frames'])} frames",
        f"{len(data['levels'])} niveaus",
        f"{len(scenes)} tekeningen",
        f"{pairs} met contrastpaar",
        f"{sum(1 for f in data['frames'] if f.get('discoverOnly'))} alleen ontdekken",
    ]
    summary = "".join(f"<span>{esc(chip)}</span>" for chip in chips)

    page = PAGE.replace("__SUM__", summary).replace("__CARDS__", "".join(blocks))
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
