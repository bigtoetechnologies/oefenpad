#!/usr/bin/env python3
"""Write scenes/{a0,a1,a2,b1}.clusters.tsv and .cards.tsv from the author_*.py data."""
import importlib, json, pathlib
H = pathlib.Path(__file__).parent
sel = json.load(open(H/'selection.json'))
band_of = {c['id']: b for b, cs in sel.items() for c in cs}
mods = [importlib.import_module(n) for n in ('author_a0', 'author_a1', 'author_a2', 'author_b1', 'author_b1b', 'author_b1c', 'author_skip')]
CL = {b: [] for b in sel}; CA = {b: [] for b in sel}
cl_all = [r for m in mods for r in m.CL]
ca_all = {r[0]: r for m in mods for r in m.CARDS}
for i, where in mods[-1].DUP.items():
    r = ca_all[i]
    ca_all[i] = (i, f'SKIP: duplicate of {where}',) + tuple(r[2:])
for r in cl_all: CL[band_of[r[0]]].append(r)
for b, cs in sel.items():
    for c in cs:
        for m in c['members']:
            CA[b].append(ca_all.pop(m['id']))
assert not ca_all, ca_all.keys()
def clean(x):
    assert '\t' not in x and '\n' not in x, x
    return x.strip()
(H/'scenes').mkdir(exist_ok=True)
for b in sel:
    # order clusters like selection.json
    order = [c['id'] for c in sel[b]]
    rows = sorted(CL[b], key=lambda r: order.index(r[0]))
    with open(H/'scenes'/f'{b}.clusters.tsv', 'w', encoding='utf-8') as f:
        f.write('cluster\tframe\tsentence_nl\tsentence_en\n')
        for r in rows: f.write('\t'.join(clean(x) for x in r) + '\n')
    with open(H/'scenes'/f'{b}.cards.tsv', 'w', encoding='utf-8') as f:
        f.write('id\tscene\tmust\tavoid\tcontrast\texample_nl\texample_en\talt\n')
        for r in CA[b]: f.write('\t'.join(clean(x) for x in r) + '\n')
    print(b, len(rows), 'clusters', len(CA[b]), 'cards')
