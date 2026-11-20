#!/usr/bin/env python3
"""Band the fixed-expression contrast sets by frequency rank -> selection.json.
The lexicon holds single words, not chunks, so frequency is only a first pass and
banding is editorial. A chunk is ranked by its most frequent CONTENT word (the keys
after the second colon in clusters.txt; prepositions and articles are left out on
purpose, they would put every chunk in A0). A set sits in the band of its most
frequent member: A0 up to rank 250, A1 to 1000, A2 to 2500, B1 to 5000, B2 to 10000.
A key may name a part of speech, 'pas(noun)', for the lexicon rows split by part of
speech ('pas (noun)', 'arm (noun)'); a bare key that only exists in such split rows is
an error, so the author picks the sense drawn. Keys missing from the lexicon (pitje,
wagenwijd, draf, galop, ganzenpas, kluitje, coulisse) carry no rank; a set whose keys
are all missing needs an OVERRIDE or an EVERYDAY entry.
OVERRIDE maps a set to (band, reason): abstract relations pushed up, homograph ranks
corrected, and sets whose chunk is harder than its commonest word. The builder prints
every reason on the overview, and the checker rejects an override that repeats the
band the ranks already give.
A cluster line may end with '; xref=family:card-id' for a partner drawn elsewhere."""
import csv, json, pathlib, re
from collections import defaultdict
H = pathlib.Path(__file__).parent
fr = {r['nl']: int(r['rang']) for r in csv.DictReader(open(H/'../lexicon/woorden-frequentie.tsv', encoding='utf-8'), delimiter='\t')}
split = defaultdict(list)                     # 'pas' -> ['pas (adv)', 'pas (noun)']
for w in fr:
    m = re.fullmatch(r'(.+?) \((\w+)\)', w)
    if m: split[m.group(1)].append(w)
OVERRIDE = {
    'plaats': ('a2', 'in plaats van is an abstract swap, though plaats is rank 116 (SKIP set)'),
    'volgorde': ('a2', 'elkaar (120) is a pronoun; the spatial relations are harder than the word'),
    'omgeving': ('a1', 'stad is rank 139, but op het platteland and in de bergen are not A0 chunks'),
    'stappen': ('a2', 'stap (447) and keer (99, a function-like noun) understate a finer contrast'),
    'gezelschap': ('a2', 'twee is rank 56, but met zijn tweeën is not a first-weeks chunk'),
    'opzet': ('b1', 'ongeluk (878) ranks the base word; met opzet and per ongeluk are B1 chunks'),
    'wegtocht': ('b1', 'plek (366) ranks the base word; ter plekke keeps an old case form and is a B1 chunk'),
    'klok-draai': ('b1', 'klok (1761) ranks the clock; the turning directions are a B1 pair (SKIP set)'),
    'op-zijn-kop': ('b1', 'kop (492) is ranked as head or cup, not as the chunk'),
    'wind': ('b1', 'wind (911) ranks the weather word; riding with or against it is a B1 pair'),
    'delen': ('b1', 'stuk (356) ranks the base word; in tweeën and in stukjes are B1 chunks'),
    'orde': ('b1', 'rij (710) and elkaar (120) are not the difficulty of op een rij and door elkaar'),
    'samen-lopen': ('a2', 'hand (261) would place it in A1; arm in arm (arm 9643) is the harder half'),
    'voeten': ('a2', 'voet (993) would place it in A1; op sokken (sok 6338) is the harder half'),
    'muur-plafond': ('a2', 'muur (837) would place it in A1; aan het plafond (plafond 3487) is the harder half'),
    'eerste': ('a1', 'eerste (59) is a numeral; voor het eerst and voor het laatst are A1 chunks (SKIP set)'),
    'bloem-knop': ('b1', 'knop (2118) is ranked mostly as button or switch; the bud sense is rarer, so bloei (3909) places the set'),
    'dier-wild': ('b1', 'wild (1638) is ranked as the adjective; the noun in in het wild is rarer, so gevangenschap (4215) places the set'),
    'paardengang': ('b2', 'draf and galop are not in the 10,000-lemma list, so no rank places the set'),
    'kleding': ('a2', 'pak (984) would place it in A1, but in plus a bare garment is a productive pattern and pyjama (5871) is everyday vocabulary, so the set sits in A2, not B2'),
    'toneel': ('b2', 'plank (3303) ranks the shelf or board; coulisse is not in the 10,000-lemma list and both chunks are literary'),
    'groep-lopen': ('b2', 'ganzenpas and kluitje are not in the 10,000-lemma list, so no rank places the set'),
}
# Everyday rule (decisions.html, 20 November 2026): everyday items sit at the lowest sensible
# level, A2 at the highest; a promotion is stated as judgment. EVERYDAY maps a set to
# (band, note). The overview reason is rendered from the lexicon by everyday_reason(), so
# every fact it prints is read, not typed: for each member, each rank key's niveau, top2000
# and herkomst (woorden.tsv) and rank (woorden-frequentie.tsv), or that the key is not a
# woorden.tsv row. The note is free text and must not state lexicon facts (no digits,
# 'rank', 'niveau' and the like); the checker re-reads every cited fact.
# Considered on 20 November 2026 and kept in B1/B2 (not daily life, or not a thing a learner
# meets daily): opzet, wegtocht, klok-draai, op-zijn-kop, wind, orde, delen, paard-stal, wal,
# bloem-knop, bocht, dier-wild, meubel-onder, schip, toneel, paardengang, pas, groep-lopen.
EVERYDAY = {
    'pan-vuur': ('a2', 'water on the boil and a pan on a low flame are daily kitchen talk; the old upward move for the rarer pitje is withdrawn'),
    'raam-kier': ('a2', 'a window left ajar or thrown wide open is daily household talk'),
}
LEX = {}
for r in csv.DictReader(open(H/'../lexicon/woorden.tsv', encoding='utf-8'), delimiter='\t'):
    LEX.setdefault(r['nl'], r)
def lex_key(k):
    m = re.fullmatch(r'(.+?)\((\w+)\)', k)
    return f'{m.group(1)} ({m.group(2)})' if m else k
def everyday_reason(cid, members):
    target, note = EVERYDAY[cid]
    if target not in ('a0', 'a1', 'a2'): raise SystemExit(f'{cid}: EVERYDAY band {target} is above A2')
    if cid in OVERRIDE: raise SystemExit(f'{cid}: in both OVERRIDE and EVERYDAY')
    facts = []
    for m in members:
        for k in m['keys']:
            w = lex_key(k)
            row = LEX.get(w)
            if not row:
                facts.append(f"{m['lemma']}: {w} not in woorden.tsv")
                continue
            f = f"{m['lemma']}: {w} niveau {row['niveau'] or 'none'}"
            if row['top2000']: f += f", top2000 {row['top2000']}"
            f += f", herkomst {row['herkomst']}"
            f += f", rank {fr[w]}" if w in fr else ', no rank'
            facts.append(f)
    if not facts: raise SystemExit(f'{cid}: EVERYDAY set has no rank keys to cite')
    return f"Lexicon: {'; '.join(facts)}. Basis: judgment, not lexicon data. Note: {note}."
def rank_of(k):
    m = re.fullmatch(r'(.+?)\((\w+)\)', k)
    if m:
        w = f'{m.group(1)} ({m.group(2)})'
        if w not in fr: raise SystemExit(f'key {k}: no lexicon row "{w}"')
        return fr[w]
    if k in fr: return fr[k]
    if split.get(k): raise SystemExit(f'key {k}: the lexicon splits it by part of speech {split[k]}; write e.g. {k}(noun)')
    return None
def band(r): return 'a0' if r <= 250 else 'a1' if r <= 1000 else 'a2' if r <= 2500 else 'b1' if r <= 5000 else 'b2' if r <= 10000 else None
bands = defaultdict(list)
seen = set()
for l in open(H/'clusters.txt', encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    parts = [x.strip() for x in l.split(';')]
    cid, axis, mem = parts[:3]
    seen.add(cid)
    xref = ''
    for extra in parts[3:]:
        if extra.startswith('xref='): xref = extra[5:]
        else: raise SystemExit(f'{cid}: unknown field {extra}')
    ms = []
    for m in mem.split('|'):
        i, rest = m.split('=', 1)
        chunk, gloss, keys = rest.split(':')
        keys = keys.split()
        ranks = [r for r in (rank_of(k) for k in keys) if r is not None]
        ms.append(dict(id=i, lemma=chunk, gloss=gloss, keys=keys, rank=min(ranks) if ranks else None))
    rs = [m['rank'] for m in ms if m['rank']]
    rank_band = band(min(rs)) if rs else None
    b = OVERRIDE[cid][0] if cid in OVERRIDE else EVERYDAY[cid][0] if cid in EVERYDAY else rank_band
    if b is None: raise SystemExit(f'{cid}: no rank and no OVERRIDE')
    c = dict(id=cid, axis=axis, band=b, rank_band=rank_band, members=ms)
    if cid in OVERRIDE: c['override'] = OVERRIDE[cid][1]
    if cid in EVERYDAY: c['everyday'] = everyday_reason(cid, ms)
    if xref: c['xref'] = xref
    bands[b].append(c)
for cid in set(EVERYDAY) - seen: raise SystemExit(f'EVERYDAY {cid}: no such set in clusters.txt')
if __name__ == '__main__':
    for b in sorted(bands):
        print(b, len(bands[b]), 'clusters', sum(len(c['members']) for c in bands[b]), 'cards')
        print('  ', [c['id'] for c in bands[b]])
    json.dump(bands, open(H/'selection.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
