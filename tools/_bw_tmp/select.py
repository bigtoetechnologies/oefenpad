#!/usr/bin/env python3
"""Band the adverb contrast sets by frequency rank -> selection.json.
A set sits in the band of its most frequent member. Lexicon entries may carry a
part-of-speech suffix ("morgen (adv)", "meer num"); the lookup strips it and takes
the best rank among the variants. OVERRIDE places the sets whose rank misleads;
the reason for each is in REASON and is printed on the overview page."""
import csv, json, pathlib, re
from collections import defaultdict
H = pathlib.Path(__file__).parent
fr = {}
for r in csv.DictReader(open(H/'../lexicon/woorden-frequentie.tsv', encoding='utf-8'), delimiter='\t'):
    key = re.sub(r'\s+(\([^)]*\)|[a-z]+)$', '', r['nl']) if re.search(r'\s(\([^)]*\)|num|adv|adj|noun|prep|pron|conj|verb)$', r['nl']) else r['nl']
    fr[key] = min(fr.get(key, 10**6), int(r['rang']))
OVERRIDE = {'ingang': 'a1', 'vergelijking': 'a1', 'richting': 'a2', 'opzet': 'a2',
            'op-over': 'a1', 'doel': 'a2', 'dagdeel': 'a1',
            'bovenin-onderin': 'b1'}
REASON = {
    'ingang': 'naar binnen and naar buiten are two-word phrases with no rank; they build on binnen and buiten (A0), so A1.',
    'vergelijking': 'minder ranks 201 (A0), but comparing against a reference (meer dan, minder dan, evenveel) builds on the A0 amount words veel and weinig, so A1.',
    'richting': 'rechtdoor, linksaf and rechtsaf rank past 7000 or not at all, but a newcomer needs route words for directions early, so A2.',
    'opzet': 'expres and per ongeluk have no rank; A2.',
    'op-over': 'op (rank 6) and over (26) are ranked as prepositions; the senses "used up" and "left over" come later, so A1.',
    'doel': 'mis ranks 468 on other senses (the coursebook list gives B1) and raak is open, so A2.',
    'dagdeel': 'overdag ranks 2453 (A2), but the coursebook list gives A1, so A1.',
    'bovenin-onderin': 'neither bovenin nor onderin is in the 10,000-lemma lexicon, but a gap is not rarity; same pattern as bovenaan/onderaan and voorin/achterin (B1), so B1.',
}
# Everyday promotions (owner rule, decisions.html "Settled"): an everyday item sits at the lowest
# sensible level, A2 at the highest, even where corpus rank would put it in B1. cluster id ->
# (band, note). The reason printed on the overview is rendered from the lexicon by everyday_reason(),
# so every fact it states is read, not typed, and the checker re-reads each one:
#   Lexicon: each member's niveau, top2000 and herkomst (woorden.tsv) and rank (woorden-frequentie.tsv),
#            or "not in woorden.tsv" for a member the lexicon lacks.
#   Basis:   'judgment, not lexicon data' (no member is taught at or below the target band), else
#            'coursebook (members)'. Note: the judgment itself; it may not state lexicon facts.
EVERYDAY = {
    'vooraan-achteraan': ('a2', 'queuing at the shop till, the bus stop and the doctor is daily life, and joining a queue at the back is something a newcomer does every day'),
    'verderop-hiernaast': ('a2', 'the neighbours next door and the shop a little further on are how a newcomer hears directions in the street every day'),
    'dwars-schuin': ('a2', 'a car parked across the road, a picture hanging on a slant and a line drawn diagonally are things a newcomer sees and has to name in daily life (owner ruling, November)'),
    'boord': ('a0', 'getting on and off a ferry or a water bus is part of daily travel in the Netherlands, so the owner places the pair in the first band (owner ruling, November)'),
}
COURSEBOOK_FOR = {'a0': {'A1', 'les:nig'}, 'a1': {'A1', 'les:nig'}, 'a2': {'A1', 'les:nig'},
                  'b1': {'A1', 'les:nig', 'B1', 'les:register', 'les:taalcompleet'}}
LEX = {}
for r in csv.DictReader(open(H/'../lexicon/woorden.tsv', encoding='utf-8'), delimiter='\t'):
    LEX.setdefault(r['nl'], r)


def everyday_reason(cid, members):
    target, note = EVERYDAY[cid]
    facts, support = [], []
    for m in members:
        row = LEX.get(m['lemma'])
        if row is None:
            facts.append(f"{m['lemma']} not in woorden.tsv")
            continue
        f = f"{m['lemma']} niveau {row['niveau'] or 'none'}"
        if row['top2000']:
            f += f", top2000 {row['top2000']}"
        f += f", herkomst {row['herkomst']}"
        f += f", rank {m['rank']}" if m['rank'] else ', no usable rank'
        facts.append(f)
        if ({row['niveau']} | set(row['herkomst'].split(';'))) & COURSEBOOK_FOR[target]:
            support.append(m['lemma'])
    basis = f"coursebook ({', '.join(support)})" if support else 'judgment, not lexicon data'
    return f"Lexicon: {'; '.join(facts)}. Basis: {basis}. Note: {note}."


assert not set(EVERYDAY) & set(OVERRIDE)
OVERRIDE.update({k: v[0] for k, v in EVERYDAY.items()})
# This family has no B2 band: too few honest spatial adverbs rank past 5000 (owner ruling 20 Nov 2026),
# so B1 takes every set whose best member ranks 2501-10000.
def band(r): return 'a0' if r <= 250 else 'a1' if r <= 1000 else 'a2' if r <= 2500 else 'b1'
bands = defaultdict(list)
for l in open(H/'clusters.txt', encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    cid, axis, mem = [x.strip() for x in l.split(';')]
    ms = []
    for m in mem.split('|'):
        i, rest = m.split('='); lem, g = rest.split(':')
        ms.append(dict(id=i, lemma=lem, gloss=g, rank=fr.get(lem)))
    rs = [m['rank'] for m in ms if m['rank']]
    if cid not in OVERRIDE and not rs:
        raise SystemExit(f'{cid}: no member has a rank and the set has no OVERRIDE')
    b = OVERRIDE.get(cid) or band(min(rs))
    if cid in EVERYDAY:
        REASON[cid] = everyday_reason(cid, ms)
    bands[b].append(dict(id=cid, axis=axis, band=b, members=ms))
missing = set(EVERYDAY) - set(REASON)
if missing:
    raise SystemExit(f'EVERYDAY sets not in clusters.txt: {sorted(missing)}')
assert set(REASON) == set(OVERRIDE)
if __name__ == '__main__':
    for b in sorted(bands):
        print(b, len(bands[b]), 'clusters', sum(len(c['members']) for c in bands[b]), 'cards')
        print('  ', [c['id'] for c in bands[b]])
    json.dump(bands, open(H/'selection.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
