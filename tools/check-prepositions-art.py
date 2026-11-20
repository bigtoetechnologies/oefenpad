#!/usr/bin/env python3
"""Reject Voorzetselpaden scene images that break the house rules.

Two passes over every image in a folder:

  1. measure  - deterministic pixel checks (PIL): one cobalt ink, white paper,
                no grey, no second colour, 2:3, big enough.
  2. vision   - optional. Asks a local vision model (LM Studio or anything
                OpenAI-compatible) whether the drawing shows what the card's
                "Must read" says and none of what its "Avoid" says.

The cards come from the band pages, which are the source of truth, so the
brief a picture is judged against is never a copy that can go stale.

    python3 tools/check-prepositions-art.py                     # incoming/
    python3 tools/check-prepositions-art.py DIR [DIR ...]
    python3 tools/check-prepositions-art.py --no-vision         # pixel pass only
    python3 tools/check-prepositions-art.py --html report.html --json report.json

Vision needs an OpenAI-compatible server with a vision model. In LM Studio:
load a VLM (e.g. Qwen2.5-VL-7B-Instruct), start the local server, then run
this tool; the model name is discovered from /v1/models. Nothing is sent to
the internet.

Exit code is 1 if any image failed, so it can gate a batch.
"""
import argparse
import base64
import html as H
import importlib.util
import io
import json
import sys
import urllib.error
import urllib.request
from colorsys import rgb_to_hsv
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = ROOT / "assets/verb-propositions/incoming"

# House rules, from Docs/game-art.html and base-prompt.txt: one flat cobalt on
# pure white. Ink is delivered at hue 214-216 in practice, so the window is
# deliberately wider than the nominal #2B50C8 (hue 216) to allow for encoder
# drift, and narrower than "any blue".
INK_HUE = (200.0, 235.0)
MIN_SAT = 0.45
WHITE_V, WHITE_S = 0.95, 0.06
GREY_S, GREY_V = 0.25, 0.90

# Thresholds. The accepted art measures ink 20-30%, white 65-78%, grey 0.0%.
# Grey, a second colour, tone and wrong framing are hard failures: they mean the
# picture is not in the house style at all. Ink outside its usual band is only a
# warning, because a legitimately sparse scene (one small figure) sits near 9%.
LIMITS = dict(ink=(12.0, 40.0), white=(55.0, 100.0), grey=(0.0, 3.0),
              other=(0.0, 3.0), mid=(0.0, 12.0))
ASPECT = 2 / 3
ASPECT_TOL = 0.03
MIN_SIDE = 512


def load_card_reader():
    """Import tools/prepositions-pages.py (hyphenated, so by path)."""
    path = Path(__file__).resolve().parent / "prepositions-pages.py"
    spec = importlib.util.spec_from_file_location("prepositions_pages", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def all_cards():
    pp = load_card_reader()
    cards = {}
    for page in pp.pages():
        cards.update(pp.read_cards(page))
    return cards


def flatten(im, bg=(255, 255, 255)):
    """Composite onto a background. Paper art goes on white; in-game masks are
    shown on a cobalt block, which is what a reviewer should see."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        paper = Image.new("RGBA", im.size, tuple(bg) + (255,))
        im = Image.alpha_composite(paper, im)
    return im.convert("RGB")


def measure(path, sample=320):
    with Image.open(path) as raw:
        im = flatten(raw)
        width, height = im.size
        # Downscale for the colour census: the checks are about proportions,
        # not detail, and this keeps 1000-image runs quick.
        scale = sample / max(width, height)
        small = im.resize((max(1, round(width * scale)), max(1, round(height * scale))))
    # tobytes() rather than getdata(): the latter is deprecated in Pillow 14.
    data = small.tobytes()
    total = len(data) // 3
    ink = white = grey = other = mid = 0
    hue_sum = 0.0
    for i in range(0, len(data), 3):
        r, g, b = data[i], data[i + 1], data[i + 2]
        h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
        hue = h * 360
        if s > MIN_SAT and INK_HUE[0] <= hue <= INK_HUE[1] and v > 0.15:
            ink += 1
            hue_sum += hue
        elif s < WHITE_S and v > WHITE_V:
            white += 1
        elif s < GREY_S and v < GREY_V:
            grey += 1
        elif s > 0.30 and v > 0.15:
            other += 1          # a chromatic colour that is not the ink
        else:
            mid += 1            # soft edges, gradients, tonal shading
    return dict(
        mode="paper",
        size=f"{width}x{height}", width=width, height=height,
        ink=100.0 * ink / total, white=100.0 * white / total,
        grey=100.0 * grey / total, other=100.0 * other / total,
        mid=100.0 * mid / total,
        hue=(hue_sum / ink) if ink else 0.0,
    )


def measure_mask(path, sample=320):
    """In-game art is an alpha mask drawn on a cobalt block by CSS: the colour
    lives in the stylesheet, not the file, so only coverage can be judged."""
    with Image.open(path) as raw:
        im = raw.convert("RGBA")
        width, height = im.size
        scale = sample / max(width, height)
        small = im.resize((max(1, round(width * scale)), max(1, round(height * scale))))
    alpha = bytearray(small.getchannel("A").tobytes())
    total = max(1, len(alpha))
    solid = sum(1 for a in alpha if a >= 128)
    soft = sum(1 for a in alpha if 8 < a < 248)
    return dict(
        mode="mask",
        size=f"{width}x{height}", width=width, height=height,
        ink=100.0 * solid / total, white=100.0 * (total - solid) / total,
        grey=0.0, other=0.0, mid=100.0 * soft / total, hue=0.0,
    )


def is_mask(path):
    """True when the file is an alpha mask on near-white, not a paper drawing."""
    with Image.open(path) as raw:
        if raw.mode not in ("RGBA", "LA", "P"):
            return False
        im = raw.convert("RGBA")
    alpha = im.getchannel("A")
    hist = alpha.histogram()
    clear = sum(hist[:16]) / max(1, im.size[0] * im.size[1])
    if clear < 0.05:            # barely any transparency: a paper drawing
        return False
    # Judge only the pixels that are actually drawn: transparent pixels can hold
    # any leftover RGB, and resampling would smear it into the visible ones.
    data = im.resize((64, 64)).tobytes()
    opaque = [(data[i], data[i + 1], data[i + 2])
              for i in range(0, len(data), 4) if data[i + 3] > 128]
    if not opaque:
        return False
    return all(min(c) > 230 for c in opaque)


def pixel_verdict(m):
    """Return (failures, warnings); no failures means the pixel pass is clean."""
    bad, warn = [], []
    if not LIMITS["ink"][0] <= m["ink"] <= LIMITS["ink"][1]:
        warn.append("ink %.1f%% outside %d-%d" % ((m["ink"],) + LIMITS["ink"]))
    if m.get("mode") == "mask":
        # colour is applied by CSS to a mask: nothing here can be judged on it
        ratio = m["height"] / m["width"] if m["width"] else 0
        if abs(ratio - 1 / ASPECT) / (1 / ASPECT) > ASPECT_TOL:
            bad.append("aspect %s" % m["size"])
        if min(m["width"], m["height"]) < MIN_SIDE:
            bad.append("too small %s" % m["size"])
        return bad, warn
    if m["white"] < LIMITS["white"][0]:
        bad.append("white %.1f%%" % m["white"])
    if m["grey"] > LIMITS["grey"][1]:
        bad.append("grey %.1f%%" % m["grey"])
    if m["other"] > LIMITS["other"][1]:
        bad.append("second colour %.1f%%" % m["other"])
    if m["mid"] > LIMITS["mid"][1]:
        bad.append("tone/soft edges %.1f%%" % m["mid"])
    ratio = m["height"] / m["width"] if m["width"] else 0
    if abs(ratio - 1 / ASPECT) / (1 / ASPECT) > ASPECT_TOL:
        bad.append("aspect %s" % m["size"])
    if min(m["width"], m["height"]) < MIN_SIDE:
        bad.append("too small %s" % m["size"])
    return bad, warn


VISION_PROMPT = """You are checking one illustration for a Dutch language
exercise. Each card has a "must" (what the picture has to show) and an "avoid"
(what would make it teach the wrong thing).

MUST: {must}
AVOID: {avoid}
INTENDED: {alt}

Answer only with JSON, no prose and no code fences:
{{"shows_must": true|false, "violations": ["..."], "text_in_image": true|false,
  "reason": "one short sentence"}}

shows_must is true only if every part of MUST is visible.
violations lists any AVOID item that is present.
text_in_image is true if there are letters, numbers or words anywhere."""


def discover_vlm(base_url):
    try:
        with urllib.request.urlopen(base_url.rstrip("/") + "/models", timeout=5) as r:
            data = json.load(r)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        sys.exit("no vision server at %s (%s).\nStart LM Studio's local server "
                 "and load a vision model, or pass --no-vision." % (base_url, exc))
    ids = [m.get("id", "") for m in data.get("data", [])]
    if not ids:
        sys.exit("the server at %s lists no models" % base_url)
    return ids[0]


def ask_vision(base_url, model, path, card, max_side=768):
    with Image.open(path) as raw:
        im = flatten(raw, (43, 80, 200) if is_mask(path) else (255, 255, 255))
        im.thumbnail((max_side, max_side))
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=88)
    payload = {
        "model": model,
        "temperature": 0,
        "max_tokens": 200,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": VISION_PROMPT.format(
                    must=card.get("must") or "(not given)",
                    avoid=card.get("avoid") or "(not given)",
                    alt=card.get("alt") or "(not given)")},
                {"type": "image_url", "image_url": {
                    "url": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()}},
            ],
        }],
    }
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            body = json.load(r)
        text = body["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, OSError, KeyError, ValueError) as exc:
        return None, "vision request failed: %s" % exc
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        out = json.loads(text)
    except ValueError:
        return None, "unreadable vision reply"
    if out.get("shows_must") is not True:
        return False, out.get("reason") or "does not show the must"
    if out.get("violations"):
        return False, "avoid: " + ", ".join(map(str, out["violations"]))[:80]
    if out.get("text_in_image"):
        return False, "text in image"
    return True, ""


THUMB_W = 150


def thumb_uri(path):
    with Image.open(path) as raw:
        im = flatten(raw, (43, 80, 200) if is_mask(path) else (255, 255, 255))
        im.thumbnail((THUMB_W, THUMB_W * 2))
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=72)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def write_html(path, rows, folders):
    esc = H.escape
    bad = [r for r in rows if r["status"] != "pass"]
    out = ["<!doctype html><meta charset='utf-8'>",
           "<title>Voorzetselpaden art check</title>",
           "<style>body{font-family:system-ui,sans-serif;margin:24px;background:#fff;color:#111}",
           "h1{font-size:20px}h2{font-size:16px;margin-top:28px}",
           "table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;",
           "padding:6px 8px;text-align:left;vertical-align:top;font-size:13px}",
           "th{background:#f4f4f4}img{display:block;width:", str(THUMB_W), "px}",
           "code{font-size:12px;color:#555}.why{color:#b00}</style>",
           "<h1>Voorzetselpaden art check</h1>",
           "<p>%d images checked in %s &middot; %d failed &middot; %d passed</p>"
           % (len(rows), esc(", ".join(folders)), len(bad), len(rows) - len(bad)),
           "<h2>Failures</h2>",
           "<table><tr><th>image</th><th>id</th><th>chunk</th><th>why</th></tr>"]
    for r in bad:
        out.append(
            "<tr><td><img src='%s' alt=''></td><td><code>%s</code></td><td>%s</td>"
            "<td class='why'>%s</td></tr>"
            % (thumb_uri(r["path"]), esc(r["id"]), esc(r.get("chunk") or ""),
               esc("; ".join(r["why"]))))
    out.append("</table>")
    if len(bad) != len(rows):
        out.append("<h2>Passed</h2><table><tr><th>image</th><th>id</th><th>chunk</th>"
                   "<th>ink</th><th>hue</th></tr>")
        for r in rows:
            if r["status"] == "pass":
                out.append("<tr><td><img src='%s' alt=''></td><td><code>%s</code></td>"
                           "<td>%s</td><td>%.1f%%</td><td>%.0f</td></tr>"
                           % (thumb_uri(r["path"]), esc(r["id"]), esc(r.get("chunk") or ""),
                              r["measure"]["ink"], r["measure"]["hue"]))
        out.append("</table>")
    path.write_text("\n".join(out), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folders", nargs="*", default=[str(DEFAULT_DIR)],
                    help="folders of PNGs to check (default: the incoming batch)")
    ap.add_argument("--no-vision", action="store_true", help="pixel checks only")
    ap.add_argument("--vlm-url", default="http://127.0.0.1:1234/v1")
    ap.add_argument("--vlm-model", default=None)
    ap.add_argument("--limit", type=int, default=0, help="check at most N images")
    ap.add_argument("--html", help="write a contact sheet of the failures")
    ap.add_argument("--json", dest="json_out", help="write the full report as JSON")
    args = ap.parse_args()

    cards = all_cards()
    files = []
    for folder in args.folders:
        files += sorted(Path(folder).glob("*.png"))
    if args.limit:
        files = files[:args.limit]
    if not files:
        sys.exit("no PNGs found in: " + ", ".join(args.folders))

    model = None
    if not args.no_vision:
        model = args.vlm_model or discover_vlm(args.vlm_url)
        print("vision: %s at %s" % (model, args.vlm_url), file=sys.stderr)

    rows = []
    for path in files:
        card_id = path.stem
        card = cards.get(card_id)
        row = {"path": str(path), "id": card_id,
               "chunk": (card or {}).get("chunk", ""), "why": [], "note": []}
        try:
            row["measure"] = measure_mask(path) if is_mask(path) else measure(path)
        except Exception as exc:                       # unreadable file
            row["measure"] = {}
            row["why"].append("unreadable: %s" % exc)
            row["status"] = "fail"
            rows.append(row)
            continue
        hard, warn = pixel_verdict(row["measure"])
        row["why"] += hard
        row["note"] += warn
        if model:
            if card is None:
                row["why"].append("no card with this id")
            else:
                ok, why = ask_vision(args.vlm_url, model, path, card)
                if ok is None:
                    row["why"].append(why)
                elif not ok:
                    row["why"].append(why)
            print("%-46s %s" % (card_id, "pass" if not row["why"] else "; ".join(row["why"])),
                  file=sys.stderr)
        row["status"] = "pass" if not row["why"] else "fail"
        rows.append(row)

    failed = [r for r in rows if r["status"] == "fail"]
    warned = [r for r in rows if r["status"] == "pass" and r["note"]]
    print("\n%d checked, %d passed, %d failed" % (len(rows), len(rows) - len(failed), len(failed)))
    for r in failed:
        print("  %-46s %s" % (r["id"], "; ".join(r["why"])))
    if warned:
        print("%d passed with a note:" % len(warned))
        for r in warned:
            print("  %-46s %s" % (r["id"], "; ".join(r["note"])))

    if args.html:
        write_html(Path(args.html), rows, args.folders)
        print("wrote", args.html)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(rows, indent=1), encoding="utf-8")
        print("wrote", args.json_out)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
