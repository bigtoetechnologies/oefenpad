#!/usr/bin/env python3
"""Band the noun contrast sets -> selection.json.
Default: a set sits in the band of its most frequent member (rank in
tools/lexicon/woorden-frequentie.tsv). Plural forms (kinderen ...) are not in
the lexicon, so only singulars count. B1 is rank 2501-5000, B2 is 5001-10000;
a set whose best rank is above 10000 has no band and stops the run.
Frequency rank misplaces concrete nouns: corpus text rarely mentions shoes or
cows, but a beginner needs them. OVERRIDE places a set by theme instead; every
override carries its reason, and the builder lists each one on the overview."""
import csv, json, pathlib
from collections import defaultdict
H = pathlib.Path(__file__).parent

# cluster id -> (band, basis, note). The overview reason is rendered from the
# lexicon by reason() below, so every fact it states is read, not typed:
#   Lexicon: each member's niveau, top2000 and herkomst (woorden.tsv) and rank
#            (woorden-frequentie.tsv).
#   Basis:   'coursebook' only when a member is taught at or below the target
#            band (see COURSEBOOK_FOR); otherwise 'judgment', which says plainly
#            that the lexicon does not support the move.
#   Note:    free text; it must not state lexicon facts (the checker rejects
#            'coursebook', 'bijlage', 'niveau', 'rank', digits and the like there).
# What the columns mean (tools/lexicon/extraheer-woorden.py, Docs/lexicon/index.html):
#   niveau A1 = taught in Nederlands in gang; B1 = taught in Nederlands in actie;
#   open = in Bijlage 8 but taught in neither coursebook. herkomst bijlage8 = in
#   Bijlage 8, the 5,000 most frequent lemmas (Tiberius & Schoonheim 2014): a
#   frequency list, not a teaching list. les:nig / les:register / les:taalcompleet
#   = curated vocabulary of Nederlands in gang / Nederlands in actie / TaalCompleet B1.
OVERRIDE = {
    'ledemaat':      ('a1', 'coursebook', 'body parts sit with hand/voet'),
    'been-getal':    ('a1', 'coursebook', 'kept beside arm/been, so the leg is taught once'),
    'schoeisel':     ('a1', 'judgment', 'schoen is basic clothing a beginner needs'),
    'boerderijdier': ('a1', 'judgment', 'koe, schaap and varken are basic animal words a beginner needs'),
    'fruit':         ('a1', 'judgment', 'appel and peer are basic food words a beginner needs'),
    'lichtbron':     ('a2', 'judgment', 'lamp is an everyday household word'),
    'muis-getal':    ('a2', 'judgment', 'muis is a common animal word and sits with the other plural sets'),
    'hoofddeksel':   ('a2', 'judgment', 'hoed and pet sit with the other clothing'),
    'pad':           ('b1', 'judgment', 'de pad (toad) is a rare word; the single lexicon row for pad is taken to be the path sense (inference)'),
    # Promotions from the 2026-11-20 B1/B2 review, re-checked against the lexicon the same day.
    'beengewricht':  ('a2', 'coursebook', 'a learner needs the joints at the doctor'),
    'armgewricht':   ('a2', 'coursebook', ''),
    'mand-emmer':    ('a2', 'coursebook', ''),
    'terras-balkon': ('a2', 'coursebook', ''),
    'schuur-kas':    ('a2', 'coursebook', ''),
    'tomaat-paprika': ('a2', 'coursebook', ''),
    'sok-kous':      ('a2', 'judgment', 'sok is a daily clothing word'),
    'handdoek-laken': ('a2', 'judgment', 'handdoek and laken are daily household words'),
    'citroen-sinaasappel': ('a2', 'judgment', 'citroen and sinaasappel are everyday shopping words'),
    'koekje-wafel':  ('a2', 'judgment', 'koekje is an everyday food word'),
    'wond-pleister': ('b1', 'coursebook', 'first-aid words a learner needs at the doctor'),
    # Everyday-item promotions (owner rule, decisions.html, 2026-11-20): a very common
    # daily-life object goes to A2 or lower whatever its corpus frequency. All judgment.
    'bes':           ('a2', 'judgment', 'strawberries and cherries are everyday shopping fruit'),
    'stofzuiger-bezem': ('a2', 'judgment', 'the vacuum cleaner and the broom are daily cleaning tools'),
    'deken-dekbed':  ('a2', 'judgment', 'a blanket or a duvet is on every bed'),
    'mond':          ('a2', 'judgment', 'tand and tong are daily words, from brushing teeth to the dentist'),
    'kam-tandenborstel': ('a2', 'judgment', 'comb and toothbrush are daily washing things'),
    'kruispunt-rotonde': ('a2', 'judgment', 'every route description and cycle trip uses them'),
    'winterkleding': ('a2', 'judgment', 'scarf, hat and gloves are daily winter clothing'),
    'kraan':         ('a2', 'judgment', 'the tap is in every kitchen; the crane moves with it as its partner'),
    'oven-magnetron': ('a2', 'judgment', 'oven and microwave are in nearly every kitchen'),
    'pompoen-meloen': ('a2', 'judgment', 'pumpkin and melon are everyday shopping produce'),
    'noot':          ('a2', 'judgment', 'the peanut is an everyday food; walnut and almond move with it'),
    'pan':           ('a2', 'judgment', 'saucepan and frying pan are used daily'),
    'stopcontact-schakelaar': ('a2', 'judgment', 'every room has a socket and a light switch'),
    'sandaal-slipper': ('a2', 'judgment', 'sandals and flip-flops are everyday summer footwear'),
}

# Highest band a 'judgment' promotion may reach: everyday items sit at A2 at the highest.
# A judgment override that moves a set DOWN in level (pad) is not a promotion.
JUDGMENT_CEILING = 'a2'

# The everyday-item review of 2026-11-20: every set that sat in B1 or B2 that day, and
# the decision. 'promoted' sets carry their reason in OVERRIDE; 'kept' sets carry one
# clause here. The checker fails any B1/B2 set missing from this table, so a set added
# to B1/B2 later must be reviewed for everyday items too.
EVERYDAY_REVIEW = {
    # B1
    'pad': ('b1', 'kept', 'de pad (toad) is not an everyday word'),
    'konijn-haas': ('b1', 'kept', 'pet and wild animal, not a daily-life item'),
    'haai-dolfijn': ('b1', 'kept', 'sea animals'),
    'vlinder-mot': ('b1', 'kept', 'insects'),
    'ezel-pony': ('b1', 'kept', 'animals rarely met in daily life'),
    'nest-kooi': ('b1', 'kept', 'animal homes'),
    'vogeldeel': ('b1', 'kept', 'parts of an animal'),
    'beek-vijver': ('b1', 'kept', 'landscape words'),
    'woestijn-moeras': ('b1', 'kept', 'landscape words'),
    'bootdeel': ('b1', 'kept', 'sailing terms'),
    'hek-schutting': ('b1', 'kept', 'the open or closed fence is a fine distinction, not a daily need'),
    'deken-dekbed': ('b1', 'promoted', None),
    'kelder-zolder': ('b1', 'kept', 'house spaces many newcomers in flats do not have'),
    'mond': ('b1', 'promoted', None),
    'gezichtsdeel': ('b1', 'kept', 'face detail beyond the A1 face set'),
    'vinger': ('b1', 'kept', 'finger names beyond hand and finger'),
    'rolstoel-kinderwagen': ('b1', 'kept', 'mobility aids, not a daily item for most learners'),
    'kam-tandenborstel': ('b1', 'promoted', None),
    'boomdeel': ('b1', 'kept', 'parts of a tree'),
    'vrachtwagen-bestelwagen': ('b1', 'kept', 'goods vehicles a learner sees but rarely names'),
    'helikopter-drone': ('b1', 'kept', 'rare in daily life'),
    'kruispunt-rotonde': ('b1', 'promoted', None),
    'lijn': ('b1', 'kept', 'material distinctions'),
    'gereedschap': ('b1', 'kept', 'DIY tools'),
    'sluiting': ('b1', 'kept', 'parts of clothing, not the clothing itself'),
    'sieraad': ('b1', 'kept', 'jewellery, not a daily need'),
    'gezichtshaar': ('b1', 'kept', 'describing appearance, not a daily item'),
    'naald-speld': ('b1', 'kept', 'sewing'),
    'winterkleding': ('b1', 'promoted', None),
    'piano-orgel': ('b1', 'kept', 'instruments'),
    'eend-zwaan': ('b1', 'kept', 'birds'),
    'olifant-neushoorn': ('b1', 'kept', 'zoo animals'),
    'tijger-jaguar': ('b1', 'kept', 'zoo animals'),
    'kraan': ('b1', 'promoted', None),
    'slang': ('b1', 'kept', 'snake and hose, neither a daily item'),
    'vlieg-mug': ('b1', 'kept', 'insects'),
    'oven-magnetron': ('b1', 'promoted', None),
    'kikker-schildpad': ('b1', 'kept', 'animals'),
    'bes': ('b1', 'promoted', None),
    'stofzuiger-bezem': ('b1', 'promoted', None),
    'wond-pleister': ('b1', 'kept', 'injury words: the wound is not a daily item, and the plaster moves with it'),
    # B2
    'hert-geit': ('b2', 'kept', 'animals'),
    'ooievaar-reiger': ('b2', 'kept', 'birds'),
    'uil-papegaai': ('b2', 'kept', 'birds'),
    'slak-rups': ('b2', 'kept', 'garden animals'),
    'krokodil-hagedis': ('b2', 'kept', 'reptiles'),
    'krab-kreeft': ('b2', 'kept', 'sea animals'),
    'otter-bever': ('b2', 'kept', 'wild animals'),
    'mossel-oester': ('b2', 'kept', 'shellfish, not everyday shopping'),
    'kwal-inktvis': ('b2', 'kept', 'sea animals'),
    'sprinkhaan-krekel': ('b2', 'kept', 'insects'),
    'eekhoorn-egel': ('b2', 'kept', 'wild animals'),
    'telescoop-verrekijker': ('b2', 'kept', 'optical instruments'),
    'pompoen-meloen': ('b2', 'promoted', None),
    'noot': ('b2', 'promoted', None),
    'pan': ('b2', 'promoted', None),
    'zeef-vergiet': ('b2', 'kept', 'kitchen tools beyond the daily pan'),
    'haard-kachel': ('b2', 'kept', 'most homes heat with radiators'),
    'schep-hark': ('b2', 'kept', 'garden tools'),
    'kwast-penseel': ('b2', 'kept', 'painting tools'),
    'kruk-fauteuil': ('b2', 'kept', 'seat distinctions beyond the A1 chair and sofa'),
    'stopcontact-schakelaar': ('b2', 'promoted', None),
    'spijker-schroef': ('b2', 'kept', 'DIY'),
    'schroevendraaier-moersleutel': ('b2', 'kept', 'DIY tools'),
    'mouw-kraag': ('b2', 'kept', 'parts of clothing, not the clothing itself'),
    'sandaal-slipper': ('b2', 'promoted', None),
    'oorbel-broche': ('b2', 'kept', 'jewellery, not a daily need'),
    'racket-peddel': ('b2', 'kept', 'sports gear'),
    'snorkel-zwembril': ('b2', 'kept', 'holiday gear'),
    'kano-kajak': ('b2', 'kept', 'boats'),
    'viool-cello': ('b2', 'kept', 'instruments'),
    'trompet-trombone': ('b2', 'kept', 'instruments'),
    'rund-getal': ('b2', 'kept', 'a farming word; the everyday animal is the A1 cow'),
}

# A member supports a 'coursebook' basis for a target band when the lexicon says
# it is taught at or below that band. Keys: niveau values and herkomst tags.
COURSEBOOK_FOR = {
    'a0': {'A1', 'les:nig'}, 'a1': {'A1', 'les:nig'}, 'a2': {'A1', 'les:nig'},
    'b1': {'A1', 'les:nig', 'B1', 'les:register', 'les:taalcompleet'},
}

# Members whose lexicon row carries a part-of-speech suffix (the bare form is not a row).
LEX_ROW = {'arm': 'arm (noun)', 'enkel': 'enkel (noun)'}

# Coursebook words (woorden.tsv niveau A0/A1 or top2000) that may stay in B1/B2,
# because the card draws another sense than the coursebook one. The checker reads this.
COURSEBOOK_SENSE = {
    'wortel': 'the coursebook A1 sense is carrot; the boomdeel card draws the root',
}


# Lemmas with no usable rank. The lexicon's suffixed rows ("enkel (noun)") carry a
# frequency from a failed lookup (zipf about 1.5, rank 9600+), so they are never
# used. A member listed here is banded by its partners alone; the reason is printed
# on the overview.
NO_RANK = {
    'enkel': 'the bare form enkel is not in the frequency list and the row "enkel (noun)" has a placeholder rank; the set is banded by knie (2671)',
}


def band(r):
    if r > 10000:
        raise SystemExit(f'rank {r} is beyond B2 (10000)')
    return 'a0' if r <= 250 else 'a1' if r <= 1000 else 'a2' if r <= 2500 else 'b1' if r <= 5000 else 'b2'


fr = {r['nl']: int(r['rang']) for r in csv.DictReader(open(H/'../lexicon/woorden-frequentie.tsv'), delimiter='\t')}
LEX = {}
for r in csv.DictReader(open(H/'../lexicon/woorden.tsv'), delimiter='\t'):
    LEX.setdefault(r['nl'], r)


def qualifies(row, target):
    tags = {row['niveau']} | set(row['herkomst'].split(';'))
    return bool(tags & COURSEBOOK_FOR.get(target, set()))


def reason(cid, members):
    target, basis, note = OVERRIDE[cid]
    facts, support, done = [], [], set()
    for m in members:
        lem = m['lemma']
        if lem in done:
            continue
        done.add(lem)
        row_id = LEX_ROW.get(lem, lem)
        if row_id not in LEX:
            if m['id'].endswith('-meer'):
                continue          # plural card: not a lemma
            raise SystemExit(f'{cid}: {row_id} is not in woorden.tsv')
        row = LEX[row_id]
        f = f"{row_id} niveau {row['niveau'] or 'none'}"
        if row['top2000']:
            f += f", top2000 {row['top2000']}"
        f += f", herkomst {row['herkomst']}"
        f += f", rank {m['rank']}" if m['rank'] else ', no usable rank'
        facts.append(f)
        if qualifies(row, target):
            support.append(row_id)
    if basis == 'coursebook':
        if not support:
            raise SystemExit(f'{cid}: basis coursebook, but no member is taught at or below {target}')
        b = f"coursebook ({', '.join(support)})"
    elif basis == 'judgment':
        if not note:
            raise SystemExit(f'{cid}: basis judgment needs a note that states the judgment')
        if support:
            raise SystemExit(f'{cid}: basis judgment, but {support} is taught at or below {target}; say coursebook')
        b = 'judgment, not lexicon data'
    else:
        raise SystemExit(f'{cid}: unknown basis {basis}')
    out = f"Lexicon: {'; '.join(facts)}. Basis: {b}."
    return out + (f" Note: {note}." if note else '')


bands = defaultdict(list)
seen = set()
for l in open(H/'clusters.txt'):
    if l.startswith('#') or not l.strip(): continue
    parts = [x.strip() for x in l.split(';')]
    cid, axis, mem = parts[:3]
    seen.add(cid)
    ms = []
    for m in mem.split('|'):
        i, rest = m.split('=')
        f = rest.split(':')
        lem, g, art, pl, dim = f[:5]
        base = f[5] if len(f) > 5 else ''
        ms.append(dict(id=i, lemma=lem, gloss=g, article=art, plural=pl, dim=dim, base=base, rank=None if lem in NO_RANK else fr.get(lem)))
    rs = [m['rank'] for m in ms if m['rank']]
    rank_band = band(min(rs)) if rs else None
    entry = dict(id=cid, axis=axis, members=ms, rank_band=rank_band)
    if cid in OVERRIDE:
        entry['override'] = reason(cid, ms)
        b = OVERRIDE[cid][0]
        if b == rank_band:
            raise SystemExit(f'OVERRIDE for {cid} repeats the rank band {b}')
    else:
        b = rank_band
    entry['band'] = b
    bands[b].append(entry)
BAND_ORDER = ['a0', 'a1', 'a2', 'b1', 'b2']
for cid, (tgt, basis, _n) in OVERRIDE.items():
    for b_, cs in bands.items():
        for c in cs:
            if c['id'] == cid and basis == 'judgment' and c['rank_band'] and \
                    BAND_ORDER.index(tgt) < BAND_ORDER.index(c['rank_band']) and \
                    BAND_ORDER.index(tgt) > BAND_ORDER.index(JUDGMENT_CEILING):
                raise SystemExit(f'{cid}: judgment promotion to {tgt}; everyday items go to {JUDGMENT_CEILING} or lower')
for cid, (was, dec, why) in EVERYDAY_REVIEW.items():
    if cid not in seen:
        raise SystemExit(f'EVERYDAY_REVIEW names unknown cluster {cid}')
    if dec == 'promoted' and (cid not in OVERRIDE or not OVERRIDE[cid][2]):
        raise SystemExit(f'{cid}: promoted without an OVERRIDE note')
    if dec == 'kept' and not why:
        raise SystemExit(f'{cid}: kept without a reason')
unknown = set(OVERRIDE) - seen
if unknown:
    raise SystemExit(f'OVERRIDE names unknown clusters: {sorted(unknown)}')
if __name__ == '__main__':
    for b in sorted(bands):
        print(b, len(bands[b]), 'sets', sum(len(c['members']) for c in bands[b]), 'cards')
        for c in bands[b]: print('  ', c['id'], [(m['id'], m['rank']) for m in c['members']], '(override)' if 'override' in c else '')
    out = dict(bands)
    out['_no_rank'] = NO_RANK
    out['_coursebook_sense'] = COURSEBOOK_SENSE
    out['_coursebook_for'] = {k: sorted(v) for k, v in COURSEBOOK_FOR.items()}
    out['_lex_row'] = LEX_ROW
    out['_judgment_ceiling'] = JUDGMENT_CEILING
    out['_everyday_review'] = {k: list(v) for k, v in EVERYDAY_REVIEW.items()}
    json.dump(out, open(H/'selection.json', 'w'), ensure_ascii=False, indent=1)
