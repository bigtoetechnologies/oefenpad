#!/usr/bin/env python3
"""Regroup the master words that have no card yet by theme (domein).

Reads:  tools/lexicon/woorden.tsv, woorden-domein.tsv, woorden-woordsoort.tsv,
        woorden-frequentie.tsv, Docs/<family>/*.html (not voorzetselpaden),
        Docs/lexicon/bronnen.html (shell: head, sidebar, script)
Writes: tools/lexicon/themes-to-card.tsv and Docs/lexicon/themes-to-card.html
Usage:  python3 tools/build-themes-page.py
"""
import csv, collections, glob, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEX = os.path.join(ROOT, "tools", "lexicon")
OUT_TSV = os.path.join(LEX, "themes-to-card.tsv")
OUT_HTML = os.path.join(ROOT, "Docs", "lexicon", "themes-to-card.html")
SHELL = os.path.join(ROOT, "Docs", "lexicon", "bronnen.html")

FAMILIES = {  # folder -> (pos of its cards or None, label)
    "werkwoorden": ("verb", "Werkwoorden"),
    "scheidbare-werkwoorden": ("verb", "Scheidbare werkwoorden"),
    "bijvoeglijke-naamwoorden": ("adj", "Bijvoeglijke naamwoorden"),
    "zelfstandige-naamwoorden": ("noun", "Zelfstandige naamwoorden"),
    "bijwoorden": ("adv", "Bijwoorden"),
    "vaste-uitdrukkingen": (None, "Vaste uitdrukkingen"),
}
NOT_IMAGEABLE_THEMES = {"Abstract & general", "Function words", "Names"}
NOT_IMAGEABLE_POS = {"function", "name", "interjection"}
MAIN_POS = ["noun", "verb", "adj", "adv"]
TOP_N = 30

OPPOSITES = [
    ("groot", "klein"), ("hoog", "laag"), ("lang", "kort"), ("dik", "dun"),
    ("warm", "koud"), ("heet", "koud"), ("open", "dicht"), ("vol", "leeg"),
    ("zwaar", "licht"), ("hard", "zacht"), ("nat", "droog"), ("schoon", "vuil"),
    ("oud", "jong"), ("nieuw", "oud"), ("snel", "langzaam"), ("binnen", "buiten"),
    ("boven", "onder"), ("voor", "achter"), ("links", "rechts"), ("dag", "nacht"),
    ("zomer", "winter"), ("lente", "herfst"), ("man", "vrouw"), ("jongen", "meisje"),
    ("vader", "moeder"), ("zoon", "dochter"), ("broer", "zus"), ("opa", "oma"),
    ("koning", "koningin"), ("rijk", "arm"), ("blij", "verdrietig"),
    ("vriend", "vijand"), ("oorlog", "vrede"), ("begin", "einde"),
    ("ochtend", "avond"), ("noord", "zuid"), ("oost", "west"), ("stijgen", "dalen"),
    ("kopen", "verkopen"), ("geven", "nemen"), ("winnen", "verliezen"),
    ("vragen", "antwoorden"), ("leven", "dood"), ("sterk", "zwak"),
    ("breed", "smal"), ("diep", "ondiep"), ("vroeg", "laat"), ("goed", "slecht"),
    ("mooi", "lelijk"), ("gezond", "ziek"), ("veilig", "gevaarlijk"),
    ("hond", "kat"), ("berg", "dal"), ("land", "zee"), ("zon", "maan"),
    ("aankomen", "vertrekken"), ("slapen", "wakker"), ("trekken", "duwen"),
    ("inademen", "uitademen"), ("opstaan", "gaan zitten"), ("lachen", "huilen"),
]


def tsv(name):
    with open(os.path.join(LEX, name), encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE))
    return rows[1:]


def card_lemmas():
    art = re.compile(r'<article id="[^"]*" class="kaart" data-id="([^"]*)"[^>]*>(.*?)</article>', re.S)
    h3 = re.compile(r'<h3 class="chunk">(.*?)</h3>', re.S)
    cards = []
    for fam, (pos, _) in FAMILIES.items():
        for p in sorted(glob.glob(os.path.join(ROOT, "Docs", fam, "*.html"))):
            with open(p, encoding="utf-8") as f:
                text = f.read()
            for cid, body in art.findall(text):
                m = h3.search(body)
                lem = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else cid
                if fam == "zelfstandige-naamwoorden":
                    lem = re.sub(r"^(de|het) ", "", lem)
                    if cid.endswith("-meer"):
                        lem = cid[:-5]
                cards.append((fam, pos, lem))
    return cards


def main():
    master = {r[0]: r[1] for r in tsv("woorden.tsv")}
    domein = {r[0]: r[1] for r in tsv("woorden-domein.tsv")}
    pos_of = {r[0]: r[1] for r in tsv("woorden-woordsoort.tsv")}
    rang = {r[0]: int(r[2]) for r in tsv("woorden-frequentie.tsv") if r[2].isdigit()}

    by_base = collections.defaultdict(list)
    for k in master:
        m = re.match(r"^(.*) \([^)]*\)$", k)
        if m:
            by_base[m.group(1)].append(k)

    credit = collections.defaultdict(set)  # master key -> families
    for fam, pos, lem in card_lemmas():
        if lem in master:
            keys = [lem]
        else:
            keys = []
        keys += [k for k in by_base.get(lem, []) if pos is None or pos_of.get(k) == pos]
        for k in keys:
            credit[k].add(fam)

    themes = sorted(set(domein.values()))
    stat = {t: collections.Counter() for t in themes}
    fams = {t: collections.Counter() for t in themes}
    unc = {t: [] for t in themes}
    for k in master:
        t = domein[k]
        stat[t]["master"] += 1
        if credit[k]:
            stat[t]["carded"] += 1
            for f in credit[k]:
                fams[t][f] += 1
            continue
        p = pos_of.get(k, "")
        stat[t]["unc"] += 1
        stat[t][p if p in MAIN_POS else "other"] += 1
        img = t not in NOT_IMAGEABLE_THEMES and p not in NOT_IMAGEABLE_POS
        if img:
            stat[t]["img"] += 1
        unc[t].append((rang.get(k, 99999), k, p, master[k]))
    for t in themes:
        unc[t].sort()

    # TSV
    with open(OUT_TSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\", lineterminator="\n")
        w.writerow(["nl", "pos", "domein", "rang", "en"])
        for t in themes:
            for r, k, p, en in unc[t]:
                w.writerow([k, p, t, r, en])

    tot = collections.Counter()
    for t in themes:
        tot.update(stat[t])
    write_html(themes, stat, fams, unc, tot, len(master))
    print("master", tot["master"], "carded", tot["carded"], "uncarded", tot["unc"], "imageable", tot["img"])
    for t in sorted(themes, key=lambda t: -stat[t]["img"])[:5]:
        print(t, stat[t]["img"])


def e(s):
    return html.escape(s, quote=True)


def slug(t):
    return "theme-" + re.sub(r"[^a-z]+", "-", t.lower()).strip("-")


def n(x):
    return f"{x:,}"


def contrast_note(rows):
    have = {k: k for _, k, _, _ in rows}
    found = [f"{a} / {b}" for a, b in OPPOSITES if a in have and b in have]
    if not found:
        return "Contrast pairs: none obvious."
    return "Contrast pairs visible in this list: " + "; ".join(found) + "."


def write_html(themes, stat, fams, unc, tot, master_n):
    with open(SHELL, encoding="utf-8") as f:
        shell = f.read()
    head, rest = shell.split("<title>", 1)
    rest = rest.split("</title>", 1)[1]
    pre_main, rest2 = rest.split('<header class="doc-head">', 1)
    pre_main = pre_main.replace(' aria-current="page"', "")
    script = rest2[rest2.index("<script>"):]
    order = sorted(themes, key=lambda t: (-stat[t]["img"], t))
    top5 = order[:5]
    toc = [("the-answer-in-one-paragraph", "The answer in one paragraph"),
           ("definitions", "Definitions and caveats"),
           ("themes", "The themes in numbers"),
           ("by-theme", "The most frequent words per theme"),
           ("how-to-teach-these", "How to teach these")]
    toc_html = "".join(f'<li class="toc-h2"><a href="#{a}">{b}</a></li>' for a, b in toc)

    o = []
    o.append(head + "<title>Words still to teach, grouped by theme — Oefenpad documentation</title>" + pre_main)
    o.append('<header class="doc-head">\n      <h1>Words still to teach, grouped by theme</h1>\n'
             '      <p class="lede">The master words that have no card yet, regrouped by semantic domain instead of by CEFR level.</p>\n'
             '      <p class="doc-meta">Docs/lexicon/themes-to-card.html</p>\n    </header>\n')
    o.append(f'    <details class="page-toc" open><summary>On this page</summary><ul>{toc_html}</ul></details>\n')
    o.append('    <article class="prose">\n')
    o.append(f'<h2 id="the-answer-in-one-paragraph">The answer in one paragraph</h2>\n'
             f'<p><strong>{n(tot["unc"])} of the {n(master_n)} master words have no card</strong>, and about '
             f'<strong>{n(tot["img"])}</strong> of those are plausible candidates for picture cards. '
             f'The themes are the 29 semantic domains already tagged in <code>tools/lexicon/woorden-domein.tsv</code>; nothing was re-tagged by hand. '
             f'The five themes with the most imageable uncarded words are {", ".join(top5[:-1])} and {top5[-1]}. '
             f'The full list is <code>tools/lexicon/themes-to-card.tsv</code>, rebuilt by <code>tools/build-themes-page.py</code>.</p>\n')
    o.append('<h2 id="definitions">Definitions and caveats</h2>\n'
             '<p><strong>Carded</strong> means the headword appears as a card in Werkwoorden, Bijvoeglijke naamwoorden, Zelfstandige naamwoorden, '
             'Bijwoorden, Scheidbare werkwoorden or Vaste uitdrukkingen. Sense ids and plural cards map to their lemma; a sense key such as '
             '<code>bank (zitplaats)</code> counts when its base word is carded in a family of the same part of speech. '
             'Voorzetselpaden is not counted, and prepositions are function words, so they fall outside picture cards anyway.</p>\n'
             '<p><strong>The domain tags are noisy.</strong> A lemma is filed under its most common nominal sense, so a verb or adjective can sit in a theme that fits only its noun. '
             'The part-of-speech tags are noisy too, and a few lemmas are tagged <code>phrase</code> or fall under the wrong class. '
             'Treat every count as a starting point for the owner, not a measurement.</p>\n'
             '<p><strong>Imageable estimate.</strong> The themes Abstract &amp; general, Function words and Names, and the parts of speech function, name and interjection, count as not imageable. '
             'Everything else counts as an imageable candidate. This is a rough rule: many words in the remaining themes are still abstract or specialist.</p>\n')
    o.append('<h2 id="themes">The themes in numbers</h2>\n'
             '<p>Sorted by imageable estimate, largest first. The last column lists the existing card families that already hold at least one word of the theme.</p>\n'
             '<div class="table-wrap"><table>\n<thead><tr><th>Theme</th><th>Master words</th><th>Carded</th><th>Uncarded</th>'
             '<th>Noun</th><th>Verb</th><th>Adj</th><th>Adv</th><th>Other</th><th>Imageable estimate</th><th>Families already touching it</th></tr></thead>\n<tbody>\n')
    for t in order:
        s = stat[t]
        fl = ", ".join(f"{FAMILIES[f][1]} ({fams[t][f]})" for f in FAMILIES if fams[t][f]) or "none"
        o.append(f'<tr><td><a href="#{slug(t)}">{e(t)}</a></td><td>{n(s["master"])}</td><td>{n(s["carded"])}</td><td>{n(s["unc"])}</td>'
                 f'<td>{n(s["noun"])}</td><td>{n(s["verb"])}</td><td>{n(s["adj"])}</td><td>{n(s["adv"])}</td><td>{n(s["other"])}</td>'
                 f'<td>{n(s["img"])}</td><td>{e(fl)}</td></tr>\n')
    o.append(f'<tr><td><strong>Total</strong></td><td><strong>{n(tot["master"])}</strong></td><td><strong>{n(tot["carded"])}</strong></td>'
             f'<td><strong>{n(tot["unc"])}</strong></td><td><strong>{n(tot["noun"])}</strong></td><td><strong>{n(tot["verb"])}</strong></td>'
             f'<td><strong>{n(tot["adj"])}</strong></td><td><strong>{n(tot["adv"])}</strong></td><td><strong>{n(tot["other"])}</strong></td>'
             f'<td><strong>{n(tot["img"])}</strong></td><td></td></tr>\n</tbody></table></div>\n')
    o.append('<h2 id="by-theme">The most frequent words per theme</h2>\n'
             f'<p>Each block lists the {TOP_N} most frequent uncarded words of the theme, whatever their part of speech, by frequency rank (1 is the most frequent). '
             'The contrast note names opposites only where both words appear in the list shown.</p>\n')
    for t in order:
        rows = unc[t][:TOP_N]
        s = stat[t]
        o.append(f'<details id="{slug(t)}"><summary>{e(t)} — {n(s["unc"])} uncarded, {n(s["img"])} imageable</summary>\n')
        o.append(f'<p>{e(contrast_note(rows))}</p>\n')
        o.append('<div class="table-wrap"><table>\n<thead><tr><th>Lemma</th><th>Pos</th><th>Gloss</th><th>Rank</th></tr></thead>\n<tbody>\n')
        for r, k, p, en in rows:
            o.append(f'<tr><td>{e(k)}</td><td>{e(p)}</td><td>{e(en)}</td><td>{r if r != 99999 else ""}</td></tr>\n')
        if not rows:
            o.append('<tr><td colspan="4">No uncarded words.</td></tr>\n')
        o.append('</tbody></table></div>\n</details>\n')
    o.append('<h2 id="how-to-teach-these">How to teach these</h2>\n'
             '<p>The owner has decided four things for this group.</p>\n'
             '<div class="table-wrap"><table>\n<thead><tr><th>Decision</th><th>Meaning</th></tr></thead>\n<tbody>\n'
             '<tr><td>Image-based cards</td><td>The picture carries the meaning.</td></tr>\n'
             '<tr><td>No example sentences</td><td>A card shows the word and the picture only.</td></tr>\n'
             '<tr><td>Contrast pairs only where obvious</td><td>Opposites are paired when the list itself shows them; no pair is forced.</td></tr>\n'
             '<tr><td>No language-level bands</td><td>This group is organised by theme, not by A0 to B2.</td></tr>\n'
             '</tbody></table></div>\n'
             '<p>Three questions are still open and are not answered here.</p>\n'
             '<ol>\n<li>Card format: what a card for this group contains and how it is laid out.</li>\n'
             '<li>Who draws: who produces the artwork for the chosen words.</li>\n'
             '<li>Order of themes: which theme comes first and which words within it.</li>\n</ol>\n')
    o.append('    </article>\n'
             '    <nav class="pager" aria-label="Previous and next document"><a class="prev" href="index.html"><span>Prev</span>Lexicon overview</a></nav>\n'
             '    <footer class="footer">\n'
             '      <code>Docs/lexicon/themes-to-card.html</code> · Oefenpad documentation. This page is the document.\n'
             '    </footer>\n  </main>\n</div>\n')
    o.append(script)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write("".join(o))


if __name__ == "__main__":
    main()
