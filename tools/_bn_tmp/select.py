#!/usr/bin/env python3
"""Band the adjective contrast clusters by frequency rank -> selection.json.

A cluster sits in the band of its most frequent member (the learner already
knows one half; the card teaches the partner). Bands: A0 <= 250, A1 <= 1000,
A2 <= 2500, B1 <= 5000, B2 <= 10000 (tools/lexicon/woorden-frequentie.tsv).

Lookup is by exact lemma. Homograph split entries such as "hol (adj)" are
recorded as split_rank but never used for banding: the lexicon ranks them after
the real list (about 8700-9710), so the number is not a frequency.
A cluster with no usable rank, or whose rank band is wrong for the sense drawn,
takes an OVERRIDE with a reason; the reason is printed on the overview page.
An override that repeats the rank band is an error.
"""
import csv, json, pathlib, sys
from collections import defaultdict
H = pathlib.Path(__file__).parent
fr = {r['nl']: int(r['rang']) for r in csv.DictReader(open(H/'../lexicon/woorden-frequentie.tsv'), delimiter='\t')}

# A participle or derived adjective with no lexicon row is NOT thereby rarer than rank 10000:
# the lexicon files it under its base lemma. Such sets are banded by the base lemma, and the
# reason cites that lemma and its rank (check-adjective-cards.py verifies every cited rank).
OVERRIDE = {
    # cluster: (band, reason)
    'vermogen': ('a1', 'arm and rijk have no plain lexicon row (only split homograph entries); money words are first-year inburgering topics'),
    'energie': ('a1', 'moe has no plain lexicon row; fit (2665) alone would put the core word moe in B1'),
    'prijs': ('a1', 'duur has no plain lexicon row; goedkoop (1758) alone gives A2, but price is a first-year shopping topic'),
    'vorm-lijn': ('b1', 'recht has no plain lexicon row; krom (6544) alone gives B2, one band too late for a basic shape word'),
    'staat': ('a2', 'heel ranks 64 as the adverb "very"; banded by kapot (1066) plus one band for the whole/broken sense'),
    'weer': ('a1', 'weather is a first-year inburgering topic; bewolkt has no lexicon row and zonnig (5517) gives B2'),
    'netheid': ('a1', 'clean/dirty is a first-year inburgering topic (review M14)'),
    'nattigheid': ('a1', 'wet/dry is a first-year inburgering topic (review M14)'),
    'smaak': ('a2', 'taste is an everyday topic; zoet (2622) gives B1 (review M14)'),
    'diepte': ('a2', 'ondiep ranks 7084; the rare partner moves the set up one band (review M15)'),
    'moed': ('a2', 'dapper ranks 3975; the rare partner moves the set up one band (review M15)'),
    'aanwezigheid': ('a2', 'afwezig ranks 4074; the rare partner moves the set up one band (review M15)'),
    'geluid': ('a2', 'luid (3203) is written register; the rare partner moves the set up one band (review M1)'),
    'pasvorm': ('a2', 'wijd (4370) and strak (2687) give B1, but clothing fit is an A2 shopping topic (review H2)'),
    # B1/B2 expansion, 20 Nov 2026; base-lemma banding per owner ruling, fix pass 2
    'vorm-stof': ('b2', 'vast ranks 235 for the senses "fixed, steady, certainly"; the solid-matter sense drawn here is rare, so the set follows vloeibaar (6055)'),
    'temperament': ('b2', 'mak has no lexicon row and is rare; the rare partner moves the set up one band from agressief (3368)'),
    'wind': ('a2', 'winderig and windstil have no lexicon row; banded by the base noun wind (911), one band up for the derived forms, after the A1 weather set'),
    'patroon': ('b1', 'gestreept, geruit and gestippeld have no lexicon row; banded by the base noun streep (3217)'),
    'strijkgoed': ('b2', 'gekreukt and gestreken have no lexicon row; banded by the base verb strijken (5428)'),
    'vijver': ('b2', 'bevroren and ontdooid have no lexicon row; banded by the base verb bevriezen (7440)'),
    'bal': ('b2', 'opgepompt and leeggelopen have no lexicon row; banded by the base verb oppompen (8788)'),
    'schil': ('b2', 'geschild and ongeschild have no lexicon row; banded by the base verb schillen (7584)'),
    'tapijt': ('b2', 'opgerold and uitgerold have no lexicon row and nor do oprollen or uitrollen; plain rollen (1895) is a different verb, so the set stays in B2'),
}

# Everyday promotions (owner rule, decisions.html, 20 Nov 2026): everyday items sit at
# the lowest sensible level, A2 at the highest, even where corpus frequency puts them in
# B1/B2. cluster -> (band, note). The overview reason is rendered from the lexicon by
# everyday_reason(), so every fact it states is read, not typed:
#   Lexicon: each member's niveau, top2000 and herkomst (woorden.tsv) and rank
#            (woorden-frequentie.tsv), or "no woorden.tsv row".
#   Basis:   always judgment; "with coursebook support (x)" names the members the
#            lexicon says are taught at or below the target band (COURSEBOOK_FOR).
#   Note:    the judgment; it must not state lexicon facts (no digits, niveau, rank ...).
# rijpheid (rijp/onrijp) would qualify but is not promoted: both cards are SKIP (ripeness reads by colour).
EVERYDAY = {
    'lucht':      ('a2', 'airing a stuffy room is daily home life'),
    'kruiding':   ('a2', 'bland or spicy food is daily kitchen and table talk'),
    'bereiding':  ('a2', 'a raw or a boiled egg is daily cooking'),
    'orde':       ('a2', 'a tidy or a messy room or desk is daily home life'),
    'stevigheid': ('a2', 'a sturdy or a wobbly chair, table or ladder is daily home life'),
}
# A member is taught at or below a band when its woorden.tsv niveau or herkomst says so.
COURSEBOOK_FOR = {'a0': {'A1', 'les:nig'}, 'a1': {'A1', 'les:nig'}, 'a2': {'A1', 'les:nig'}}
LEX = {}
for r in csv.DictReader(open(H/'../lexicon/woorden.tsv'), delimiter='\t'):
    LEX.setdefault(r['nl'], r)


def everyday_reason(cid, members):
    target, note = EVERYDAY[cid]
    facts, support = [], []
    for m in members:
        row = LEX.get(m['lemma'])
        if row is None:
            f = f"{m['lemma']} no woorden.tsv row"
        else:
            f = f"{m['lemma']} niveau {row['niveau'] or 'none'}"
            if row['top2000']:
                f += f", top2000 {row['top2000']}"
            f += f", herkomst {row['herkomst']}"
            if ({row['niveau']} | set(row['herkomst'].split(';'))) & COURSEBOOK_FOR[target]:
                support.append(m['lemma'])
        f += f", rank {m['rank']}" if m['rank'] else ', no usable rank'
        facts.append(f)
    basis = 'judgment, not lexicon data' if not support else f"judgment, with coursebook support ({', '.join(support)})"
    return f"Everyday promotion. Lexicon: {'; '.join(facts)}. Basis: {basis}. Note: {note}."


def band(r): return 'a0' if r <= 250 else 'a1' if r <= 1000 else 'a2' if r <= 2500 else 'b1' if r <= 5000 else 'b2'


bands = defaultdict(list)
problems = []
for l in open(H/'clusters.txt'):
    if l.startswith('#') or not l.strip(): continue
    cid, axis, mem = [x.strip() for x in l.split(';')]
    ms = []
    for m in mem.split('|'):
        i, rest = m.split('='); lem, g = rest.split(':', 1)
        split = next((fr[k] for k in (f'{lem} (adj)', f'{lem} (adv)', f'{lem} (noun)') if k in fr), None)
        ms.append(dict(id=i, lemma=lem, gloss=g, rank=fr.get(lem), split_rank=split))
    rs = [m['rank'] for m in ms if m['rank']]
    rank_band = band(min(rs)) if rs else None
    c = dict(id=cid, axis=axis, members=ms, rank_band=rank_band)
    if cid in OVERRIDE and cid in EVERYDAY:
        problems.append(f'{cid}: in both OVERRIDE and EVERYDAY')
    if cid in EVERYDAY:
        b = EVERYDAY[cid][0]
        if b not in ('a0', 'a1', 'a2'):
            problems.append(f'{cid}: EVERYDAY band {b} is above A2')
        if rank_band in ('a0', 'a1', 'a2') and b >= rank_band:
            problems.append(f'{cid}: EVERYDAY {b} does not move the set below its rank band {rank_band}')
        c.update(override=b, override_reason=everyday_reason(cid, ms), everyday=True)
    elif cid in OVERRIDE:
        b, why = OVERRIDE[cid]
        if b == rank_band:
            problems.append(f'{cid}: OVERRIDE {b} repeats the rank band')
        c.update(override=b, override_reason=why)
    elif rank_band is None:
        problems.append(f'{cid}: no member has a lexicon rank and there is no OVERRIDE')
        continue
    else:
        b = rank_band
    c['band'] = b
    bands[b].append(c)
seen_ids = {l.split(';')[0].strip() for l in open(H/'clusters.txt') if l.strip() and not l.startswith('#')}
for k in set(EVERYDAY) | set(OVERRIDE):
    if k not in seen_ids:
        problems.append(f'{k}: EVERYDAY/OVERRIDE names an unknown cluster')
if __name__ == '__main__':
    for b in sorted(bands):
        print(b, len(bands[b]), 'clusters', sum(len(c['members']) for c in bands[b]), 'cards')
        print('  ', [c['id'] for c in bands[b]])
    for p in problems:
        print('ERROR', p)
    if problems:
        sys.exit(1)
    json.dump(bands, open(H/'selection.json', 'w'), ensure_ascii=False, indent=1)
