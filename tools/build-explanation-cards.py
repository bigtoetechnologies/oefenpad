#!/usr/bin/env python3
"""Build the explanation-card pages and check their Dutch.

Sources (the master copy): tools/_ex_tmp/*.json, each a list of cards.
Output: Docs/explanation-cards/index.html, a0.html, a1.html, a2.html.

Usage:
  python3 tools/build-explanation-cards.py              build all pages, fail on any error
  python3 tools/build-explanation-cards.py --check F... check only the given JSON files, write nothing

Card fields (see tools/_ex_tmp/BRIEF.md for the rules):
  verb, sense, gloss, forms[], picture, mark, alt, note, examples[4]
  optional: key (lexicon key when it carries a suffix), band + band_why (hand-set band), tier
Example fields: text[2..4 sentences], question, answer (ja|nee), scene (all but example 1)
"""
import glob, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from explanation_lib import (ROOT, band_of, CEIL, OVERRIDES, check_ex, load_ranks)

SRC_DIR = os.path.join(ROOT, "tools", "_ex_tmp")
OUT_DIR = os.path.join(ROOT, "Docs", "explanation-cards")
TEMPLATE = os.path.join(ROOT, "Docs", "lexicon", "themes-to-card.html")
BANDS_BUILT = ["a0", "a1", "a2", "b1", "b2"]
BANNED_ART = ["windmill", "clog", "tulip", "canal", "cheese", "herring", "chips", "fries"]
SOURCE_NOTE = "Dutch Wiktionary (nl.wiktionary.org)"

def e(s): return html.escape(s, quote=False)

def load_cards(files=None):
    cards = []
    for f in files or sorted(glob.glob(os.path.join(SRC_DIR, "*.json"))):
        for c in json.load(open(f, encoding="utf-8")):
            c["_file"] = os.path.basename(f)
            cards.append(c)
    return cards

def validate(c, ranks):
    errs = []
    label = f'{c.get("verb","?")} / {c.get("sense","?")[:30]}'
    for f in ("verb", "sense", "gloss", "forms", "picture", "mark", "alt", "note", "examples"):
        if not c.get(f): errs.append(f"missing {f}")
    if errs: return label, errs, None
    key = c.get("key", c["verb"])
    if key not in ranks:
        errs.append(f"lexicon key not found: {key}")
        return label, errs, None
    band = c.get("band") or band_of(ranks[key])
    if c.get("band") and not c.get("band_why"): errs.append("band set by hand needs band_why")
    if band not in CEIL: errs.append(f"band {band} outside A0-B2")
    if len(c["examples"]) != 4: errs.append(f'{len(c["examples"])} examples, need 4')
    forms = {x.lower() for x in c["forms"]} | {c["verb"].lower()}
    stem = c["verb"][:-2] if c["verb"].endswith("en") else c["verb"]
    if len(stem) >= 6 and stem.lower() in c["alt"].lower():
        errs.append("alt text contains the verb stem")
    for fm in forms:
        if re.search(r"\b" + re.escape(fm) + r"\b", c["alt"].lower()): errs.append(f"alt text contains form {fm}")
    blob = (c["picture"] + " " + c["mark"] + " " + " ".join(x.get("scene") or "" for x in c["examples"])).lower()
    for w in BANNED_ART:
        if w in blob: errs.append(f"banned imagery in scene: {w}")
    worst_all = (0, "")
    for n, x in enumerate(c["examples"], 1):
        t = x.get("text") or []
        if not 2 <= len(t) <= 4: errs.append(f"ex{n}: {len(t)} sentences, need 2-4")
        if not str(x.get("question", "")).endswith("?"): errs.append(f"ex{n}: question must end with ?")
        if x.get("answer") not in ("ja", "nee"): errs.append(f"ex{n}: answer must be ja or nee")
        if n > 1 and not x.get("scene"): errs.append(f"ex{n}: scene missing")
        if any(re.search(r"\d", s) for s in t + [x.get("question", "")]): errs.append(f"ex{n}: digit in text")
        w, bad, unk = check_ex(forms, x, band, ranks)
        if w[0] > worst_all[0]: worst_all = w
        errs += [f"ex{n}: above {band}: {b}" for b in bad] + [f"ex{n}: unresolved word {u}" for u in unk]
    return label, errs, (band, worst_all, ranks[key])

CSS = """
.kaart{margin:2.2em 0;padding-top:.4em;border-top:1px solid var(--lijn)}
.mock{margin:0;border:2px solid var(--kobalt);border-radius:14px;padding:14px;background:var(--papier)}
.mock .pic{border:1.5px dashed var(--lijn);border-radius:10px;padding:18px 10px;text-align:center;font-size:12.5px;color:var(--grijs)}
.mock .tekst{margin:12px 0 4px;font-size:17px;font-weight:600;line-height:1.45}
.mock .tekst p{margin:2px 0}
.mock .vraag{margin:10px 0 8px;font-size:17px;font-weight:800;color:var(--kobalt)}
.mock .knoppen{display:flex;gap:10px}
.mock .knoppen span{flex:1;text-align:center;padding:8px;border:2px solid var(--kobalt);border-radius:10px;font-weight:800;font-size:16px}
.mock .uitkomst{margin-top:8px;font-size:12px;color:var(--grijs)}
.mocks{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin:1em 0}
"""

def mock(x, pic, gloss):
    t = "".join(f"<p>{e(s)}</p>" for s in x["text"])
    return (f'<div class="mock"><div class="pic">{e(pic)}</div><div class="tekst">{t}</div>'
            f'<div class="vraag">{e(x["question"])}</div><div class="knoppen"><span>ja</span><span>nee</span></div>'
            f'<div class="uitkomst">Right answer: <b>{e(x["answer"])}</b>. Then the gloss: {e(gloss)}.</div></div>')

def slug(c):
    return re.sub(r"[^a-z]+", "-", (c["verb"] + "-" + c["sense"].split("(")[0]).lower()).strip("-")[:40]

def card_html(c, info):
    band, worst, rank = info
    mocks = "".join(mock(x, x.get("scene") or ("picture: " + c["mark"]), c["gloss"]) for x in c["examples"])
    band_note = f' Band set by hand: {e(c["band_why"])}.' if c.get("band") else ""
    return (f'<section class="kaart" id="{slug(c)}"><h3>{e(c["verb"])} — {e(c["sense"])}</h3>'
            f'<p><strong>Band {band}</strong> (lemma rank {rank}).{band_note}</p>'
            f'<div class="table-wrap"><table><tbody>'
            f'<tr><th>Scene (example 1)</th><td>{e(c["picture"])}</td></tr>'
            f'<tr><th>Must read</th><td>{e(c["mark"])}</td></tr>'
            f'<tr><th>Alt text (Dutch)</th><td>{e(c["alt"])}</td></tr>'
            f'<tr><th>Note</th><td>{e(c["note"])}</td></tr></tbody></table></div>'
            f'<div class="mocks">{mocks}</div></section>')

def page(title, lede, body, name):
    tpl = open(TEMPLATE, encoding="utf-8").read()
    head, rest = tpl.split('<main id="main">', 1)
    _, tail = rest.split("</main>", 1)
    head = re.sub(r"<title>.*?</title>", f"<title>{e(title)} — Oefenpad documentation</title>", head, 1, re.S)
    head = head.replace("</style>", CSS + "</style>", 1)
    art = (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Docs</a><span>/</span><span>Explanation cards</span></nav>'
           f'<header class="doc-head"><h1>{e(title)}</h1><p class="lede">{lede}</p>'
           f'<p class="doc-meta">Docs/explanation-cards/{name}</p></header><article class="prose">{body}</article>'
           f'<footer class="footer"><code>Docs/explanation-cards/{name}</code> · Oefenpad documentation. This page is the document.</footer>')
    return head + '<main id="main">' + art + "</main>" + tail

def build(cards, ranks):
    fail, results = False, []
    for c in cards:
        label, errs, info = validate(c, ranks)
        if errs:
            fail = True
            print(f'ERR {c["_file"]}: {label}')
            for x in errs: print("   -", x)
        else:
            results.append((c, info))
    return fail, results

def split_hold(res):
    live = [(c, i) for c, i in res if not c.get("hold")]
    held = [c for c, _ in res if c.get("hold")]
    return live, held

def main():
    args = sys.argv[1:]
    if args and args[0].startswith("-") and args[0] != "--check":
        print(__doc__); sys.exit(2)
    ranks = load_ranks()
    if args and args[0] == "--check":
        fail, res = build(load_cards(args[1:]), ranks)
        print(f"{len(res)} cards OK" + ("; ERRORS ABOVE" if fail else ""))
        sys.exit(1 if fail else 0)
    cards = load_cards()
    fail, res = build(cards, ranks)
    if fail:
        print("BUILD FAILED"); sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    res, held = split_hold(res)
    res.sort(key=lambda ci: (ci[1][2] if not ci[0].get("band") else CEIL[ci[0]["band"]] - 1, ci[0]["verb"], ci[0]["sense"]))
    counts, idx_rows = {}, []
    built = []
    for b in BANDS_BUILT:
        sel = [(c, i) for c, i in res if i[0].lower() == b]
        if not sel: continue
        built.append(b)
        counts[b] = (len(sel), len({c["verb"] for c, _ in sel}), sum(len(c["examples"]) for c, _ in sel))
        toc = "".join(f'<li><a href="#{slug(c)}">{e(c["verb"])}</a> — {e(c["sense"])}</li>' for c, _ in sel)
        body = (f"<p>{counts[b][0]} cards for {counts[b][1]} verbs, four examples each. Every Dutch word is at or below the {b.upper()} band by lemma rank.</p>"
                f'<details><summary>Cards on this page</summary><ul>{toc}</ul></details>' + "".join(card_html(c, i) for c, i in sel))
        open(os.path.join(OUT_DIR, b + ".html"), "w", encoding="utf-8").write(
            page(f"Explanation cards — {b.upper()}", f"Picture, short Dutch scene and one question for the {b.upper()} verbs that have no single honest drawing.", body, b + ".html"))
        for c, (band, worst, rank) in sel:
            idx_rows.append(f'<tr><td><a href="{b}.html#{slug(c)}">{e(c["verb"])}</a></td><td>{e(c["sense"])}</td><td>{band}</td><td>{e(worst[1]) or "—"} (rank {worst[0]})</td></tr>')
    ovr = "".join(f"<tr><td>{e(w)}</td><td>{r}</td><td>{band_of(r)}</td><td>{e(why)}</td></tr>" for w, (r, why) in OVERRIDES.items())
    hold_html = ("<div class=\"table-wrap\"><table><thead><tr><th>Verb</th><th>Sense</th><th>Why held</th></tr></thead><tbody>"
                 + "".join(f"<tr><td>{e(c['verb'])}</td><td>{e(c['sense'])}</td><td>{e(c['hold'])}</td></tr>" for c in held)
                 + "</tbody></table></div>") if held else "<p>None.</p>"
    tot = [sum(counts[b][i] for b in built) for i in range(3)]
    rows = "".join(f'<tr><td><a href="{b}.html">{b.upper()}</a></td><td>{counts[b][0]}</td><td>{counts[b][1]}</td><td>{counts[b][2]}</td></tr>' for b in built)
    body = f"""<h2 id="state">State</h2>
<p>{tot[0]} cards for {tot[1]} verbs, {tot[2]} examples, as briefs and static mocks. No drawings exist.</p>
<div class="table-wrap"><table><thead><tr><th>Page</th><th>Cards</th><th>Verbs</th><th>Examples</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2 id="rules">Rules</h2>
<p>The rules are in <a href="../decisions.html">Docs/decisions.html</a> and the format is shown in <a href="../explanation-cards-pilot.html">the pilot</a>. In short: a picture, two to four short Dutch sentences, one ja/nee question, four examples per sense, every word at or below the card's band, senses from {e(SOURCE_NOTE)}.</p>
<h2 id="rebuild">Rebuild</h2>
<p>Edit the JSON files in <code>tools/_ex_tmp/</code>, then run <code>python3 tools/build-explanation-cards.py</code>. The build fails on any card that breaks a rule. Rerunning overwrites these pages.</p>
<h2 id="hand">Ranks set by hand</h2>
<div class="table-wrap"><table><thead><tr><th>Word</th><th>Rank used</th><th>Band</th><th>Why</th></tr></thead><tbody>{ovr}</tbody></table></div>
<h2 id="limits">Limits</h2>
<ul><li>The Dutch and alt text are AI-written; no native speaker has read them.</li><li>Examples 2 to 4 carry a scene line only; alt text is written when they are drawn.</li><li>Where a surface form has several homograph keys, the best rank is used, so the check is generous there.</li></ul>
<h2 id="hold">On hold</h2>
{hold_html}
<h2 id="all">Every card</h2>
<div class="table-wrap"><table><thead><tr><th>Verb</th><th>Sense</th><th>Band</th><th>Highest word</th></tr></thead><tbody>{''.join(idx_rows)}</tbody></table></div>"""
    open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(
        page("Explanation cards", "Verbs with no single honest drawing, taught with a picture, a short Dutch scene and one yes/no question, one card per sense.", body, "index.html"))
    print(f"wrote {len(res)} cards: " + ", ".join(f"{b}={counts[b][0]}" for b in built))

if __name__ == "__main__":
    main()
