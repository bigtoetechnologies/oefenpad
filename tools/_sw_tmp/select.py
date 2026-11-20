#!/usr/bin/env python3
"""Band the separable-verb contrast sets by frequency rank -> selection.json.

One rule for every set, whatever its authoring date:
  A set sits in the band of its most frequent member (A0 up to 250, A1 251-1000,
  A2 1001-2500, B1 2501-5000, B2 5001-10000). A set with no member ranked within
  10000 sits in B2, the last band.
  A promotion moves a set to any earlier band and needs a stated daily-life reason.
  A homograph entry moves a set later, because the member that ranks it counts mostly
  another sense than the one drawn (a rank correction, not a promotion).
Nothing else moves a set. An entry that does not move the set is an error.
Every member is separable: vertrekken and landen are Werkwoorden cards.

Sets after the '# expansion 2026-11-20' line in clusters.txt are batch 2 (the batch only
sets the example length; it never changes the band)."""
import csv, json, pathlib, sys
from collections import defaultdict
H = pathlib.Path(__file__).parent
fr = {r['nl']: int(r['rang']) for r in csv.DictReader(open(H/'../lexicon/woorden-frequentie.tsv'), delimiter='\t')}
LEX = {}
for r in csv.DictReader(open(H/'../lexicon/woorden.tsv', encoding='utf-8'), delimiter='\t'):
    LEX.setdefault(r['nl'], r)


def lexicon_facts(members):
    """Each member's niveau, top2000, herkomst (woorden.tsv) and rank (woorden-frequentie.tsv),
    printed on the overview beside every OVERRIDE; the checker re-derives each fact."""
    out = []
    for m in members:
        lem, row = m['lemma'], LEX.get(m['lemma'])
        if row is None:
            f = f'{lem} not in woorden.tsv'
        else:
            f = f"{lem} niveau {row['niveau'] or 'none'}"
            if row['top2000']:
                f += f", top2000 {row['top2000']}"
            f += f", herkomst {row['herkomst'] or 'none'}"
        out.append(f + (f", rank {fr[lem]}" if lem in fr else ', no rank'))
    return '; '.join(out)
OVERRIDE = {
    # promoted: earlier than rank, each with its daily-life reason
    'lamp':      ('a2', 'promoted', 'B1 by aandoen 3318; switching lights on and off is daily routine'),
    'radio':     ('a2', 'promoted', 'B1 by aanzetten 3557; switching a device on and off is daily routine, like the lamp set'),
    'koffer':    ('a2', 'promoted', 'B1 by inpakken 3927; packing for a trip is an early everyday task'),
    'telefoon':  ('a2', 'promoted', 'B1 by ophangen 4409; phoning a GP or school is needed early'),
    'voordeur':  ('a2', 'promoted', 'B1 by weggaan 4300; coming home and leaving are daily routine'),
    'jas':       ('a2', 'promoted', 'B1 by aantrekken 3367; dressing is daily routine'),
    'kamer':     ('a2', 'promoted', 'B1 by opruimen 2716; tidying and cleaning are daily household tasks'),
    'uitje':     ('a2', 'promoted', 'B1 by meegaan 4932; going along or staying at home (when ill, for a delivery) is said every week'),
    'bus':       ('a2', 'promoted', 'B2 by uitstappen 5363; getting on and off public transport is everyday from the first weeks'),
    'afwas':     ('a2', 'promoted', 'B2, no member ranked; washing and drying up is daily household language'),
    'bord':      ('a2', 'promoted', 'B2 by opeten 5213; eating up and leaving food is language of every meal'),
    'afval':     ('a2', 'promoted', 'B2 by weggooien 5837; throwing rubbish away is a daily household action'),
    'kraan':     ('a2', 'promoted', 'B2, no member ranked; turning a tap on and off is a daily household action'),
    'poortje':   ('a2', 'promoted', 'B2 by inchecken 6911; checking in and out with a transport card comes with every train or bus ride, like the bus set'),
    'gordel':    ('a2', 'promoted', 'B2 by losmaken 8066; putting on and undoing a seat belt is part of every car ride'),
    'rits':      ('a2', 'promoted', 'B2, no member ranked; zipping a coat up and down is daily dressing, like the jas set'),
    'tafel':     ('a2', 'promoted', 'B2 by afruimen 9345; laying and clearing the table happen at every meal'),
    'vaatwasser': ('a2', 'promoted', 'B2, no member ranked; loading and unloading the dishwasher is a daily household task, like the afwas set'),
    'woordenboek': ('a2', 'promoted', 'B1 by opzoeken 2524; looking a word up and writing it down are what a learner does from the first lessons (owner ruling 20 November: everyday sets sit at A2 at the highest)'),
    'brood':     ('a2', 'promoted', 'B1 by vasthouden 2770; passing bread along the table and holding it are language of every meal, like the bord and tafel sets (owner ruling 20 November)'),
    'doos':      ('b1', 'promoted', 'B2 by neerzetten 5342; lifting and putting down is work and moving language'),
    'pakket':    ('b1', 'promoted', 'B2 by afhalen 5645; posting and collecting parcels is a weekly task'),
    'blik':      ('b1', 'promoted', 'B2 by aankijken 5839; looking at someone and looking away is common in speech'),
    # homograph: later than rank because the ranking member counts mostly another sense
    'adem':      ('b2', 'homograph', 'inhouden 4511 ranks B1 through to contain and to deduct; the drawn sense rides on inademen 6680'),
}
ORDER = ['a0', 'a1', 'a2', 'b1', 'b2']
def band(r): return 'a0' if r <= 250 else 'a1' if r <= 1000 else 'a2' if r <= 2500 else 'b1' if r <= 5000 else 'b2'
bands, problems = defaultdict(list), []
batch = 1
for l in open(H/'clusters.txt', encoding='utf-8'):
    if l.startswith('# expansion 2026-11-20'): batch = 2
    if l.startswith('#') or not l.strip(): continue
    cid, axis, mem = [x.strip() for x in l.split(';')]
    ms = []
    for m in mem.split('|'):
        i, rest = m.split('='); lem, g = rest.split(':', 1)
        ms.append(dict(id=i, lemma=lem, gloss=g, rank=fr.get(lem), separable=True))
    rs = [m['rank'] for m in ms if m['rank']]
    by_rank = band(min(rs)) if rs else 'b2'   # no member within 10000: the last band
    b = by_rank
    if cid in OVERRIDE:
        ob, kind, why = OVERRIDE[cid]
        if kind not in ('promoted', 'homograph'):
            problems.append(f'{cid}: unknown OVERRIDE kind {kind}')
        if kind == 'promoted' and ORDER.index(ob) >= ORDER.index(by_rank):
            problems.append(f'{cid}: promoted to {ob} but rank band is {by_rank}')
        if kind == 'homograph' and ORDER.index(ob) <= ORDER.index(by_rank):
            problems.append(f'{cid}: homograph entry must move the set later than its rank band {by_rank}')
        if len(why.split(';')) < 2 or not why.split(';')[-1].strip():
            problems.append(f'{cid}: OVERRIDE reason must state the rank and then the reason after a semicolon')
        import re as _re
        mr = _re.match(r'(A0|A1|A2|B1|B2)(?: by (\S+) (\d+)|, no member ranked);', why)
        if kind == 'promoted':
            if not mr:
                problems.append(f'{cid}: promotion reason must open with the rank band, e.g. "B2 by opeten 5213;"')
            elif mr.group(1).lower() != by_rank or (mr.group(2) and (fr.get(mr.group(2)) != int(mr.group(3)) or int(mr.group(3)) != min(rs))) or (not mr.group(2) and rs):
                problems.append(f'{cid}: promotion reason states the wrong rank or band (rank band {by_rank}, best {min(rs) if rs else None})')
        b = ob
    entry = dict(id=cid, axis=axis, band=b, batch=batch, by_rank=by_rank, members=ms)
    if cid in OVERRIDE:
        entry['override'] = dict(kind=OVERRIDE[cid][1], reason=OVERRIDE[cid][2], lexicon=lexicon_facts(ms),
                                 basis='judgment' if OVERRIDE[cid][1] == 'promoted' else 'rank correction')
    bands[b].append(entry)
unknown = set(OVERRIDE) - {c['id'] for v in bands.values() for c in v}
if unknown:
    problems.append(f'OVERRIDE names unknown sets: {sorted(unknown)}')
if __name__ == '__main__':
    if problems:
        sys.exit('\n'.join(problems))
    for b in sorted(bands):
        print(b, len(bands[b]), 'sets', sum(len(c['members']) for c in bands[b]), 'cards')
        print('  ', [c['id'] for c in bands[b]])
    json.dump(bands, open(H/'selection.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
