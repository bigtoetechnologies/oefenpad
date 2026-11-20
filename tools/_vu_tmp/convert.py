#!/usr/bin/env python3
"""scenes/<band>.txt (authoring format, '||' separators) -> <band>.clusters.tsv and <band>.cards.tsv.
Lines: 'C||cluster||frame||sentence_nl||sentence_en' and
'K||id||scene||must||avoid||contrast||example_nl||example_en||alt||register||literal'."""
import glob, os, sys
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenes')
CH = 'cluster\tframe\tsentence_nl\tsentence_en'
KH = 'id\tscene\tmust\tavoid\tcontrast\texample_nl\texample_en\talt\tregister\tliteral'
for p in sorted(glob.glob(os.path.join(H, '*.txt'))):
    if p.endswith('BRIEF.txt'): continue
    c, k = [CH], [KH]
    for n, l in enumerate(open(p, encoding='utf-8'), 1):
        l = l.rstrip('\n')
        if not l.strip() or l.startswith('#'): continue
        f = [x.strip() for x in l.split('||')]
        if f[0] == 'C' and len(f) == 5: c.append('\t'.join(f[1:]))
        elif f[0] == 'K' and len(f) == 11: k.append('\t'.join(f[1:]))
        else: sys.exit(f'{p}:{n}: bad row ({f[0]}, {len(f)} fields)')
    base = p[:-4]
    open(base + '.clusters.tsv', 'w', encoding='utf-8').write('\n'.join(c) + '\n')
    open(base + '.cards.tsv', 'w', encoding='utf-8').write('\n'.join(k) + '\n')
    print(os.path.basename(p), len(c) - 1, 'clusters', len(k) - 1, 'cards')
